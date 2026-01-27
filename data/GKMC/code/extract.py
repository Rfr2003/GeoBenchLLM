import pandas as pd
import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, help="Path to the file dataset_release_no_image.json extracted")
    parser.add_argument("--output_path", type=str, help="Path of the .csv obtained")
    
    args = parser.parse_args()
    return args

def load_json(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data

def explore_example(data):
    example = data[0]

    for key, value in example.items():
        print(f"{key} : {value}")

def concatenate_example(example):
    keys = ["scenario", "question"]
    text = ""

    for key in keys:
        if key == "scenario":
            text += "Scenario :\n"
        else:
            text += "Question :\n"
        text_key = example[key]
        if text_key != "":
            text += text_key + "\n\n"

    answers_texts = f"Answers :\nA) {example['A']}\n\nB) {example['B']}\n\nC) {example['C']}\n\nD) {example['D']}"

    text += answers_texts

    return text

def create_csv(data):
    ids = []
    texts = []
    answers = []

    for entry in data:
        ids.append(entry["id"])
        texts.append(concatenate_example(entry))
        answers.append(entry["answer"])

    d = {"id":ids, "answer":answers, "text":texts}

    return pd.DataFrame(d)

if __name__ == '__main__':
    args = parse_args()
    
    data = load_json(args.input_path) 

    print(concatenate_example(data[0]))

    d = create_csv(data)

    d.to_csv(args.output_path, index=False)

