from ast import main
import sqlite3
import pandas as pd
from tqdm import tqdm
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db_path", type=str, help="Path to the .sqlite containing the database")
    parser.add_argument("--train_file", type=str, help="Path to the .txt file containing the train data")
    parser.add_argument("--dev_file", type=str, help="Path to the .txt file containing the dev data")
    parser.add_argument("--test_file", type=str, help="Path to the .txt file containing the test data")
    parser.add_argument("--output_path", type=str, help="Path of the final .json file")
    
    args = parser.parse_args()
    return args


def init(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor

def get_answer(cursor, query):
    try:
        cursor.execute(query)
    except Exception as e:
        print("Erreur SQL :", e)
        print("Requête exécutée :", query)
        return []
    rows = cursor.fetchall()

    answers = []

    for row in rows:
        answers.append(row[0])

    return answers

def parse_docs(cursor, args):
    splits = ['train', 'dev', 'test']
    files = [args.train_file, args.dev_file, args.test_file]
    data = {'question':[], 'answer':[], 'split':[], 'type':[]}

    for split, file in zip(splits, files):
        with open(file, 'r') as f:
            lines = f.read().splitlines()
            for line in tqdm(lines):
                r = line.split("|||")
                answer = get_answer(cursor, r[1])
                if len(answer) > 0:
                    q = r[0].strip()
                    q = q[0].upper() + q[1:]
                    if '?' not in q:
                        q += ' ?'
                    data['question'].append(q)
                    try:
                        float(answer[0])
                        qtype = 'regression'
                    except:
                        qtype = 'place'

                    if qtype == 'regression':
                        for i in range(len(answer)):
                            answer[i] = float(answer[i])
                        if len(set(answer)) <= 1:
                            answer = list(set(answer))
                            
                    data['type'].append(qtype)
                    data['answer'].append(answer)
                    data['split'].append(split)
                

    
    df = pd.DataFrame(data)
    df.to_json(args.output_path, orient="records", force_ascii=False, indent=4)

if __name__ == '__main__':
    args = parse_args()
    conn, cursor = init(args.db_path)
    parse_docs(cursor, args)
    conn.close()
