import json
import pandas as pd
import datasets
import os
from src.utils.utils import *
from src.utils.datasets_handler import *
from typing import List, Dict
from tqdm import tqdm

def eval_gens(model_name, DataSet, results=None, gen_path=None, think_mode=False):

    if results is None:    
        data = load_json(gen_path)
        if 'think_mode' in data:
            think_mode = data['think_mode']      
        results = data['generations']


    to_save = {'dataset_name': DataSet.name, 'model_name': model_name, 'think_mode': think_mode}


    metrics = DataSet.evaluate(results)
    to_save['metrics'] = metrics

    return to_save
    
        
def main():
    args = parse_args_eval()
    if args.verbose:
        print_args(args)

    output_dir = args.output_dir

    os.makedirs(output_dir, exist_ok=True)
        
    if 'all' in args.dataset_name:
        args.dataset_name = list(DATASET_CLASSES.keys())

    for d_name in tqdm(args.dataset_name):

        t = ""
        if args.think_mode:
            t = "_think"
        file_name = f"{args.model_name.split('/')[-1]}{t}_{d_name}.json"

        gen_path = args.gens_path
        
        if not gen_path.endswith(".json"):
            gen_path = os.path.join(gen_path, file_name)

        if not os.path.exists(gen_path):
            if args.verbose:
                print(f"Generations file for dataset {d_name} not found.")
            continue

        if not args.force_eval and os.path.exists(os.path.join(output_dir, file_name)):
            if args.verbose:
                print(f"Results file for dataset {d_name} already in directory : skipping.")
            continue
            
        if args.verbose:
            print(f"Evaluating for : {d_name}")
        DataSet = DATASET_CLASSES[d_name]()
        to_save = eval_gens(args.model_name, DataSet, gen_path=gen_path, think_mode=args.think_mode)
                
        with open(os.path.join(output_dir, file_name), 'w') as f:
            json.dump(to_save, f)

if __name__ == "__main__":
    main()