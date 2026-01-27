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
    keys = ["free-form_annotation", "templated_annotation", "scenario_text", "question"]
    text = ""

    for key in keys:
        text_key = example[key]
        if text_key != "":
            text += f"<{key}>" + text_key + f"</{key}>\n"

    answers_texts = f"<a_answer>{example['optionA']}</a_answer>\n<b_answer>{example['optionB']}</b_answer>\n<c_answer>{example['optionC']}</c_answer>\n<d_answer>{example['optionD']}</d_answer>"

    text += answers_texts

    return text

def chech_empty_annotation(json_data):
    for d in json_data:
        if d["free-form_annotation"] == "" and  d["templated_annotation"] == "":
            print(d["question_id"])

def create_csv(data):
    questions_ids = []
    scenario_ids = []
    texts = []
    answers = []
    categories = []

    for entry in data:
        questions_ids.append(entry["question_id"])
        scenario_ids.append(entry["scenario_id"])
        texts.append(concatenate_example(entry))
        answers.append(entry["answer"])
        categories.append(entry["category"])

    d = {"question_id":questions_ids, "scenario_id": scenario_ids, "answer":answers, "categories":categories, "text":texts}

    return pd.DataFrame(d)

if __name__ == '__main__':
    args = parse_args()
    
    data = load_json(args.input_path) 

    print(concatenate_example(data[0]))

    d = create_csv(data)

    d.to_csv(args.output_path, index=False)

