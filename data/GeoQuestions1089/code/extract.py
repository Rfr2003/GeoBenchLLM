from enum import Enum
import pandas as pd
import json
import re
from shapely import wkt
from shapely.ops import transform
from pyproj import Transformer
import numpy as np
from shapely.geometry import GeometryCollection
from enum import Enum
from collections import Counter
from tqdm import tqdm
from SPARQLWrapper import SPARQLWrapper, JSON
import argparse
import os

first_words = []

class AnswerType(Enum):
    NUMBER = 0
    URL = 1
    POLYGON = 2
    STR = 3
    OTHER = 4

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, required=True, help="Path to the directory containing GeoQuestions1089.json and GeoQuestions1089_answers.json")
    parser.add_argument("--output_dir", type=str, required=True, help="Path to the directory where to save the data")
    parser.add_argument("--db_url", type=str, required=True, help="URl where the database is listening")
    
    args = parser.parse_args()
    return args

def load_json(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return list(data.values())

def polygon_to_coordinates(text):

    text = text.strip()

    match = re.search(r'(POLYGON\s*\(\(.*?\)\)|MULTIPOLYGON\s*\(\(\(.*?\)\)\))', text, re.DOTALL)
    if not match:
        return []

    geom = match.group(0)
    geom = wkt.loads(geom)

    centroid = geom.centroid
    return [(centroid.y, centroid.x)] #(lat, long)

def detect_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def detect_type(text):
    
    url_pattern = re.compile(
        r'^(https?|ftp)://[^\s/$.?#].[^\s]*$',
        re.IGNORECASE
    )
    
    if detect_number(text.strip()):
        return AnswerType.NUMBER 
    elif url_pattern.match(text.strip()):
        return AnswerType.URL
    elif text.strip().isalnum():
        return AnswerType.STR
    elif re.search(r'POLYGON', text.strip(), re.IGNORECASE):
        return AnswerType.POLYGON
    else:
        return AnswerType.OTHER

def clean_url(url, db_url):
    stopwords = ["geoentity", "wikicategory", "osientity", "osentity", "wordnet"]
    entity = url.split('/')[-1]
    # Greek entities
    if "gagentity" in entity:
        sparql = SPARQLWrapper(db_url)
        sparql.setQuery(f"""
                PREFIX y2geoo: <http://kr.di.uoa.gr/yago2geo/ontology/>
                
                SELECT ?name
                WHERE {{
                    <{url}> y2geoo:hasGAG_Name ?name .
                }}
                """)
        sparql.setReturnFormat(JSON)
        
        results = sparql.query().convert()
        for r in results["results"]["bindings"]:
            entity = r["name"]["value"]
            
    #Ireland entities
    elif "osientity" in entity:
        sparql = SPARQLWrapper(db_url)
        sparql.setQuery(f"""
                PREFIX y2geoo: <http://kr.di.uoa.gr/yago2geo/ontology/>
                
                SELECT ?name
                WHERE {{
                    <{url}> y2geoo:hasOSI_Name ?name .
                }}
                """)
        sparql.setReturnFormat(JSON)
        
        results = sparql.query().convert()
        for r in results["results"]["bindings"]:
            entity = r["name"]["value"]
            
    #USA entities
    elif "osnientity" in entity:
        sparql = SPARQLWrapper(db_url)
        sparql.setQuery(f"""
                PREFIX y2geoo: <http://kr.di.uoa.gr/yago2geo/ontology/>
                
                SELECT ?name
                WHERE {{
                    <{url}> y2geoo:hasOSNI_Name ?name .
                }}
                """)
        sparql.setReturnFormat(JSON)
        
        results = sparql.query().convert()
        for r in results["results"]["bindings"]:
            entity = r["name"]["value"]

    #UK entities
    elif "osentity" in entity:
        sparql = SPARQLWrapper(db_url)
        sparql.setQuery(f"""
                PREFIX y2geoo: <http://kr.di.uoa.gr/yago2geo/ontology/>
                
                SELECT ?name
                WHERE {{
                    <{url}> y2geoo:hasOS_Name ?name .
                }}
                """)
        sparql.setReturnFormat(JSON)
        
        results = sparql.query().convert()
        for r in results["results"]["bindings"]:
            entity = r["name"]["value"]
    else:
        split = entity.split('_')
        first_words.append(split[0])
        if split[0] in stopwords or re.match(r".*entity$", split[0], re.IGNORECASE):
            split = split[1:]
        if split[-1].isnumeric():
            split = split[:-1]
        entity = " ".join(split).replace('%27', "'")
    return entity

def clean_answer(answer, db_url):
    replicate = False
    a_type = None
    if answer == None:
        return [], replicate, []
    if isinstance(answer, dict):
        final_answer = [answer['boolean']]
        a_type = ['bool']
    elif detect_type(answer) == AnswerType.POLYGON:
        final_answer = polygon_to_coordinates(answer)
        a_type = ['coord']
    else:
        # get rid of GeoQuestions_w (same triples than the others but with mistakes)
        pattern = re.compile(r"same-as:(\d+)")
        matches = pattern.findall(answer)
        if matches:
            final_answer = matches[0].split(":")[-1]
            replicate = True
        else:
            final_answer = []
            a_type = []
            lines = answer.splitlines()[1:]
            for line in lines:
                line = line.replace('"', "")
                for l in line.split(','):
                    detected_type = detect_type(l)
                    if detected_type == AnswerType.URL:
                        new_answer = clean_url(l, db_url)
                        a_type.append('str')
                    elif detected_type == AnswerType.NUMBER:
                        new_answer = float(l)
                        a_type.append('numeric')
                    elif detected_type == AnswerType.STR:
                        new_answer = l.replace('%27', "'")
                        a_type.append('str')
                    else:
                        new_answer = None
                    if new_answer:
                        final_answer.append(new_answer)
    return final_answer, replicate, a_type

def clean_answers(answers, db_url):
    clean = []
    replicates = []
    a_types = []
    for answer in tqdm(answers):
        a, replicate, a_type = clean_answer(answer, db_url)
        clean.append(a)
        replicates.append(replicate)
        a_types.append(a_type)
    return clean, replicates, a_types

def create_csv(questions, answers, output_dir, db_url):
    cleaned_answers, replicates, a_types = clean_answers(answers, db_url)
    data = {"question":[], 
            "cleaned_answer":[],
            "category":[] ,
            "original_answer":[], 
            'answer_type':[]}
    for question, cleaned_answer, answer, rep, ans_type in zip(questions, cleaned_answers, answers, replicates, a_types):
        if rep:
            continue
        data['question'].append(question['Question'])
        data['category'].append(question['Category'])
        if len(ans_type) > 0 and ans_type[0] != 'coord':
            data['original_answer'].append(answer)
        else:
            # to avoid having a file too fat from unreadable data
            data['original_answer'].append(None)
        a = cleaned_answer
        cat = question['Category']
        a_type = ans_type
        data['cleaned_answer'].append(a)
        data['answer_type'].append(a_type)

    df = pd.DataFrame(data)
    df.to_json(os.path.join(output_dir, "dataset.json"), orient="records", force_ascii=False, indent=4)

if __name__ == '__main__':
    args = parse_args()
    questions = load_json(os.path.join(args.data_dir, "GeoQuestions1089.json"))
    answers = load_json(os.path.join(args.data_dir, "GeoQuestions1089_answers.json"))
    
    create_csv(questions, answers, args.output_dir, args.db_url)



