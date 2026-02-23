import multiprocessing
multiprocessing.set_start_method("spawn", force=True)

from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest
import json
import pandas as pd
import datasets
from transformers import AutoTokenizer
import os
from src.utils.utils import *
from src.utils.datasets_handler import *
from typing import List, Dict
from src.eval_gens import eval_gens
from tqdm import tqdm
import sys

def instanciate_model(args):
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    llm = LLM(model=args.model_name, max_model_len=args.max_model_len, enable_lora=args.is_ft, max_loras=1, max_lora_rank=args.max_lora_rank)

    return tokenizer, llm

def batched(iterable, batch_size):
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]
        
def run(args, DataSet, llm, tokenizer):
    
    DataSet.build_prompts(args, tokenizer)

    if args.sample:
        dataset = DataSet.get_sampled_split('test', args.n_samples)
    else:
        dataset = DataSet.get_split('test')
    

    if args.verbose:
        print(f"Begin of generation")
    
    sampling_params = SamplingParams(**getLLMConfig(args, DataSet.max_tokens))
    prompts = dataset["prompt"]
    if args.verbose:
        print(f"Promp example :\n {prompts[0]}")
        print(f"Size test : {len(prompts)}")

    if args.is_ft:
        if args.lora_path:
            lora_path = args.lora_path 
        else:
            lora_path = f"/projects/iris/rferreir/GeoBenchmark/models/{args.model_name}/{DataSet.name}"
        lora_request = LoRARequest("lora", 1, lora_path)
    else:
        lora_request = None

    outputs = []

    batch_size = args.batch_size

    for prompt_batch in tqdm(
            batched(prompts, batch_size),
            total=(len(prompts) + batch_size - 1) // batch_size,
            desc="Generation",
            file=sys.stdout
        ):
        o = llm.generate(
            prompt_batch,
            sampling_params,
            lora_request=lora_request
        )
        outputs.extend(o)

    if args.think_mode:
        thinkings = []
        for out in outputs:
            s = out.outputs[0].text.split('</think>')
            out.outputs[0].text = s[-1].strip()
            thinkings.append(s[0])

        results = DataSet.results_and_thinkings(outputs, thinkings, split='test', dataset=dataset)
    else:
        results = DataSet.results(outputs, split='test', dataset=dataset)

    to_save = {'dataset_name': DataSet.name, 'model_name': args.model_name, 'think_mode': args.think_mode, 'generations': results}

    if args.evaluate:
        metrics = eval_gens(args.model_name, DataSet, results, think_mode=args.think_mode)
        to_save['metrics'] = metrics['metrics']
        
    output_dir = args.output_dir

    t = ""
    if args.think_mode:
        t = "_think"
    
    file_name = f'{args.model_name.split('/')[-1]}{t}_{DataSet.name}.json'
        
    with open(os.path.join(output_dir, file_name), 'w') as f:
        json.dump(to_save, f)
        
def main():
    args = parse_args()
    if args.verbose:
        print_args(args)

    os.makedirs(args.output_dir, exist_ok=True)
        
    model_name = args.model_name

    tokenizer, llm = instanciate_model(args)

    if 'all' in args.dataset_name:
        args.dataset_name = list(DATASET_CLASSES.keys())

    for d_name in args.dataset_name:
        if args.verbose:
            print(f"Generating for : {d_name}")
        DataSet = DATASET_CLASSES[d_name](tokenizer=tokenizer)
        run(args, DataSet, llm, tokenizer)

if __name__ == "__main__":
    main()