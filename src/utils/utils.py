import argparse
import os
import json
import yaml


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="Qwen/Qwen3-0.6B", choices=["meta-llama/Llama-3.1-8B-Instruct", "Qwen/Qwen3-0.6B", "Qwen/Qwen3-1.7B", "Qwen/Qwen3-4B-Instruct-2507", "Qwen/Qwen3-8B", "mistralai/Mistral-7B-Instruct-v0.2", "mistralai/Mistral-7B-Instruct-v0.3", "mistralai/Ministral-8B-Instruct-2410"])
    parser.add_argument("--dataset_name", type=str, nargs='+', default=["GeoSQA"], choices=["GeoQuery_place", "GeoQuery_regression", "GeoQuestions1089_regression", "GeoQuestions1089_coord", "GeoQuestions1089_place", "GeoQuestions1089_YN", "GeoSQA", "GKMC", "GridRoute", "MsMarco", "NY-POI", "PPNL_multi", "PPNL_single", "SpartUN", "SpatialEvalLLM", "StepGame", "TourismQA", "all"])

    parser.add_argument("--sample", action='store_true')
    parser.add_argument("--verbose", action='store_true')
    parser.add_argument("--n_samples", type=int, default=150)
    parser.add_argument("--batch_size", type=int, default=128)

    parser.add_argument("--max_model_len", type=int, default=16000)
    parser.add_argument("--max_lora_rank", type=int, default=16)

    parser.add_argument("--config_path", type=str, default=None, help='Path to the .yaml file specifying the LLM configuration')
    parser.add_argument("--is_ft", action='store_true', help='Specifies if the model was fine-tuned or not')
    parser.add_argument("--think_mode", action='store_true')
    parser.add_argument("--lora_path", type=str, default=None, help='Path to the lora adapter')

    parser.add_argument("--output_dir", type=str, required=True)

    parser.add_argument("--evaluate", action='store_true')
    
    args = parser.parse_args()
    return args

def parse_args_api():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name", type=str, nargs='+', default=["GeoSQA"], choices=["GeoQuery_place", "GeoQuery_regression", "GeoQuestions1089_regression", "GeoQuestions1089_coord", "GeoQuestions1089_place", "GeoQuestions1089_YN", "GeoSQA", "GKMC", "GridRoute", "MsMarco", "NY-POI", "PPNL_multi", "PPNL_single", "SpartUN", "SpatialEvalLLM", "StepGame", "TourismQA", "all"])

    parser.add_argument("--sample", action='store_true')
    parser.add_argument("--verbose", action='store_true')
    parser.add_argument("--n_samples", type=int, default=150)

    parser.add_argument("--thinking_level", type=str, choices=['low', 'high'], default='low')

    parser.add_argument("--output_dir", type=str, required=True)

    parser.add_argument("--evaluate", action='store_true')
    
    args = parser.parse_args()
    return args

def parse_args_eval():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="Qwen/Qwen3-0.6B", choices=["meta-llama/Llama-3.1-8B-Instruct", "Qwen/Qwen3-0.6B", "Qwen/Qwen3-1.7B", "Qwen/Qwen3-4B-Instruct-2507", "Qwen/Qwen3-8B", "mistralai/Mistral-7B-Instruct-v0.2", "mistralai/Mistral-7B-Instruct-v0.3", "mistralai/Ministral-8B-Instruct-2410", "openai/gpt-oss-120b"])
    parser.add_argument("--dataset_name", type=str, nargs='+', default=["GeoSQA"], choices=["GeoQuery_place", "GeoQuery_regression", "GeoQuestions1089_regression", "GeoQuestions1089_coord", "GeoQuestions1089_place", "GeoQuestions1089_YN", "GeoSQA", "GKMC", "GridRoute", "MsMarco", "NY-POI", "PPNL_multi", "PPNL_single", "SpartUN", "SpatialEvalLLM", "StepGame", "TourismQA", "all"])

    parser.add_argument("--verbose", action='store_true')
    parser.add_argument("--think_mode", action='store_true')
    parser.add_argument("--is_ft", action='store_true', help='Specifies if the model was fine-tuned or not')
    parser.add_argument("--force_eval", action='store_true', help="Evaluates even if the file for evaluation already exists")
    
    parser.add_argument("--gens_path", type=str, default=None, help='Path to the .json file containing the generations made by the model or to the directory containing a file named as ModelName_DatasetName.json')
    parser.add_argument("--output_dir", type=str, required=True)
    
    args = parser.parse_args()
    return args

def parse_args_train():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="Qwen/Qwen3-0.6B", choices=["meta-llama/Llama-3.1-8B-Instruct", "Qwen/Qwen3-0.6B", "Qwen/Qwen3-1.7B", "Qwen/Qwen3-4B-Instruct-2507", "Qwen/Qwen3-8B", "mistralai/Mistral-7B-Instruct-v0.2", "mistralai/Mistral-7B-Instruct-v0.3", "mistralai/Ministral-8B-Instruct-2410"])
    parser.add_argument("--dataset_name", type=str, default="GeoSQA", choices=["GeoQuery_place", "GeoQuery_regression", "GeoQuestions1089_regression", "GeoQuestions1089_coord", "GeoQuestions1089_place", "GeoQuestions1089_YN", "GeoSQA", "GKMC", "GridRoute", "MsMarco", "NY-POI", "PPNL_multi", "PPNL_single", "bAbI19", "SpartUN", "SpatialEvalLLM", "StepGame", "TourismQA"])
    
    parser.add_argument("--sample", action='store_true')
    parser.add_argument("--think_mode", action='store_true')
    parser.add_argument("--verbose", action='store_true')
    parser.add_argument("--n_samples", type=int, default=150)

    #training args
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--gradient_accumulation", type=int, default=8)
    parser.add_argument("--max_seq_length", type=int, default=2048)
    parser.add_argument("--lora_rank", type=int, default=16)

    #wandb args
    parser.add_argument("--wandb", action='store_true')
    parser.add_argument("--project", type=str, default="GeoBenchmark")

    parser.add_argument("--output_dir", type=str)
    parser.add_argument("--config_path", type=str, default=None, help='Path to the .yaml file specifying the LLM configuration')
    
    args = parser.parse_args()
    return args

def print_args(args):
    print("Arguments:")
    for arg, value in vars(args).items():
        print(f"  {arg:<15}: {value}")


def load_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def load_yaml(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    return config

def getLLMConfig(args, dataset_max_tokens):
    if args.think_mode:
        key = "thinking"
    else:
        key = "non_thinking"

    if args.config_path is None:
        params = {}
    else:
        llm_config = load_yaml(args.config_path)
        params = llm_config['modes'][key]

    if 'max_tokens' not in params:
        params['max_tokens'] = dataset_max_tokens

    if args.verbose:
        print(f"Sampling params : {params}")

    return params