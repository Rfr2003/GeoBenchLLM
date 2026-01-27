import pandas as pd
import json
import re
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, help="Path to the .csv containing the translations")
    parser.add_argument("--output_path", type=str, help="Path of the final .csv file")
    
    args = parser.parse_args()
    return args

def parse(row):
    text = row['translated_text']
    pattern = r"Scenario\s*:\s*(.*?)\s*Question\s*:\s*(.*?)\s*Answers?\s*:\s*(.*)"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        scenario, question, answers = match.groups()
        row['scenario'] = scenario.strip()
        row['question'] = question.strip()
        row['answers'] = answers.strip()
        text = row['answers']
        pattern = r"A\)\s*(.*?)\s*B\)\s*(.*?)\s*C\)\s*(.*?)\s*D\)\s*(.*)"
    
        match = re.search(pattern, text)
        if match:
            row["A"] = match.group(1).strip()
            row["B"] = match.group(2).strip()
            row["C"] =  match.group(3).strip()
            row["D"] = match.group(4).strip()
    else:
        print(row['id'])

    return row

if __name__ == '__main__':
    args = parse_args()
    data = pd.read_csv(args.input_path) 

    print(data.columns)

    df = data.apply(parse, axis=1)

    print(df.head())

    df.to_csv(args.output_path, index=False)

