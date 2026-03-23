import datasets 
import ast
import re
import numpy as np
import os
from src.utils.evaluate_funcs import *
import operator

THINKING_MODELS={"Qwen/Qwen3-8B", "Qwen/Qwen3-0.6B", "Qwen/Qwen3-1.7B"}

class DataSet():
    def __init__(self, name, tokenizer=None):
        self.name = name
        self.max_tokens = 100
        self.dataset = datasets.load_dataset("rfr2003/GeoBenchLLM", self.name)
        self.tokenizer = tokenizer
        self.op = operator.gt
        self.metric = "accuracy"

    def get_split(self, split='test'):
        return self.dataset[split]

    def get_sampled_split(self, split='test', n_samples=150):
        dataset = self.get_split(split).shuffle(seed=42)
        if n_samples > len(dataset):
            n_samples = len(dataset)
        dataset = dataset.select(range(n_samples))
        return dataset
        
    def get_messages(self, row):
        pass

    def get_answer(self, row):
        pass

    def results(self, outputs, split='test'):
        pass
        
    def evaluate(self, results):
        pass

    def results_and_thinkings(self, outputs, thinkings, split='test', dataset=None):
        results = self.results(outputs, split, dataset)
        for r, t in zip(results, thinkings):
            r['thinking'] = t

        return results

    def get_messages_with_answer(self, row):
        m = self.get_messages(row)
        m.extend(self.get_answer(row))
        return m

    def tokenize(self, args, messages, tokenizer, add_generation_prompt=True):
        if args.model_name in THINKING_MODELS:
            t = False
            if args.think_mode:
                t = True
            return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=add_generation_prompt, enable_thinking=t)
        else:
            return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=add_generation_prompt)
        
    def build_prompts(self, args, tokenizer, column_name="prompt"):
        def _build_prompts(row):
        
            messages = self.get_messages(row)
            prompt = messages
            if tokenizer:
                prompt = self.tokenize(args, messages, tokenizer)
            return {column_name:prompt}
    
        self.dataset = self.dataset.map(_build_prompts)
    
    def build_messages(self, args, tokenizer):
        def _build_messages(row):
        
            m = self.get_messages_with_answer(row)
            m = self.tokenize(args, m, tokenizer, add_generation_prompt=False)
                
            return {'text':m}

        self.dataset = self.dataset.map(_build_messages)

    def compare_metric(self, v1, v2):
        return self.op(v1, v2)
       
class DataSet_GeoQuery_place(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("GeoQuery_place", tokenizer=tokenizer)
        self.max_tokens = 100
        self.op = operator.lt
        self.metric = "median macro-mean"

    def get_messages(self, row):
        messages = [
            {"role": "system", "content": """You are a concise and knowledgeable geography assistant. 
            You will have to answer questions involving spatial relationships between geographic entities.
            All data refers to the United States in the year 1996.
            You'll be asked a to give the names of ONE or SEVERAL places. Give your answer in the following format : [place1, place2...]. Do not elaborate and give only the answer."""},
            {"role": "user", "content": row['question']}
        ]
        return messages

    def get_answer(self, row):
        a = [
            {"role": "assistant", "content": str(row['answer'])}
        ]
        
        return a

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, q, a in zip(outputs, dataset['question'], dataset['answer']):
            dic = {"question":q,
                   "generated_answer":out.outputs[0].text,
                   "gold_answer":a
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds = [], []
        
        for el in results:
            gens.append(el['generated_answer'])
            golds.append(el['gold_answer'])
        return evaluate_many_to_many(gens, golds)


class DataSet_GeoQuery_regression(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("GeoQuery_regression", tokenizer=tokenizer)
        self.max_tokens = 100
        self.op = operator.lt
        self.metric = "median macro-mean"

    def get_messages(self, row):
        messages = [
            {"role": "system", "content": """You are a concise and knowledgeable geography assistant. 
            You will have to answer questions involving spatial relationships between 2 or more geographic entities. 
            All data refers to the United States in the year 1996.
            You'll be asked one or several numerical values. Give your answer in the following format : [value1, value2...]. 
             Write numbers using digits only, with NO thousand separators. Do NOT use commas to group digits (e.g., write 2000, not 2,000). Do not elaborate and give only the answer."""},
            {"role": "user", "content": row['question']}
        ]
        return messages

    def get_answer(self, row):
        a = [
            {"role": "assistant", "content": str(row['answer'])}
        ]
        
        return a

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, q, a in zip(outputs, dataset['question'], dataset['answer']):
            dic = {"question":q,
                   "generated_answer":out.outputs[0].text,
                   "gold_answer":a
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds = [], []
        
        for el in results:
            gens.append(el['generated_answer'])
            golds.append(el['gold_answer'])
        return evaluate_regression(gens, golds)
            


class DataSet_GeoQuestions1089_regression(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("GeoQuestions1089_regression", tokenizer=tokenizer)
        self.max_tokens = 100
        self.op = operator.lt
        self.metric = "median macro-mean"

    def get_messages(self, row):
        a_type = ""
        if 'sq km' in row['answer_type']:
            a_type = "You'll be asked the area of one or several entities, give your answer in SQUARE KILOMETERS."
        else:
            a_type = "You'll be asked one or several numerical values."
                
        messages = [
            {"role": "system", "content": f"You are a helpful geography assistant. You will have to answer questions involving spatial relationships between 2 or more geographic entities. Tha data is from 2019 and targets Greece, United-Kingdom, Ireland and United States of America. {a_type} Give your answer in the following format : [value1, value2...].  Write numbers using digits only, with NO thousand separators. Do NOT use commas to group digits (e.g., write 2000, not 2,000). Do not elaborate and give only the answer."},
            {"role": "user", "content": row['question']}
        ]
        return messages

    def get_answer(self, row):
        a = [
            {"role": "assistant", "content": str(row['answer'])}
        ]
        
        return a

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, q, a, t in zip(outputs, dataset['question'], dataset['answer'], dataset['answer_type']):
            dic = {"question":q,
                   "generated_answer":out.outputs[0].text,
                   "gold_answer":a,
                   "type":t
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds = [], []
        
        for el in results:
            gens.append(el['generated_answer'])
            golds.append(el['gold_answer'])
        return evaluate_regression(gens, golds)


class DataSet_GeoQuestions1089_coord(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("GeoQuestions1089_coord", tokenizer=tokenizer)
        self.max_tokens = 20
        self.metric = "coord_accuracy"

    def get_messages(self, row):
        messages = [
            {"role": "system", "content": f"You are a helpful geography assistant. You will have to answer questions about the features (population, area...) of a single geographic entity. Tha data is from 2019 and targets Greece, United-Kingdom, Ireland and United States of America. You'll be asked the coordinates of a geographic entity. Give your answer in the following format : (LATITUDE, LONGITUDE). Do not elaborate and give only the answer."},
            {"role": "user", "content": row['question']}
        ]
        return messages

    def get_answer(self, row):
        a = [
            {"role": "assistant", "content": f"({row['answer'][0]}, {row['answer'][1]})"}
        ]
        
        return a

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, q, a, t in zip(outputs, dataset['question'], dataset['answer'], dataset['answer_type']):
            dic = {"question":q,
                   "generated_answer":out.outputs[0].text,
                   "gold_answer":a,
                   "type":t
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds = [], []
        
        for el in results:
            gens.append(el['generated_answer'])
            golds.append(el['gold_answer'][0])
        return evaluate_coord(gens, golds)


class DataSet_GeoQuestions1089_place(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("GeoQuestions1089_place", tokenizer=tokenizer)
        self.max_tokens = 1000
        self.op = operator.lt
        self.metric = "median macro-mean"

    def get_messages(self, row):
        messages = [
            {"role": "system", "content": f"You are a helpful geography assistant. You will have to answer questions involving spatial relationships between 2 or more geographic entities. Tha data is from 2019 and targets Greece, United-Kingdom, Ireland and United States of America. You'll be asked a to give the names of ONE or SEVERAL places. Give your answer in the following format : [place1, place2...]. Do not elaborate and give only the answer."},
            {"role": "user", "content": row['question']}
        ]
        return messages

    def get_answer(self, row):
        a = [
            {"role": "assistant", "content": str(row['answer'])}
        ]
        
        return a

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, q, a, t in zip(outputs, dataset['question'], dataset['answer'], dataset['answer_type']):
            dic = {"question":q,
                   "generated_answer":out.outputs[0].text,
                   "gold_answer":a,
                   "type":t
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds = [], []
        
        for el in results:
            gens.append(el['generated_answer'])
            golds.append(el['gold_answer'])
        return evaluate_many_to_many(gens, golds)


class DataSet_GeoQuestions1089_YN(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("GeoQuestions1089_YN", tokenizer=tokenizer)
        self.max_tokens = 3

    def get_messages(self, row):
        messages = [
            {"role": "system", "content": f"You are a helpful geography assistant. You will have to answer questions involving one or more geographic entities. The data is from 2019 and targets Greece, United-Kingdom, Ireland and United States of America. You'll be asked a boolean question. Answer by TRUE or FALSE only. Do not elaborate and give only the answer."},
            {"role": "user", "content": row['question']}
        ]
        return messages

    def get_answer(self, row):
        a = [
            {"role": "assistant", "content": str(row['answer'][0]).upper()}
        ]
        
        return a

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, q, a, t in zip(outputs, dataset['question'], dataset['answer'], dataset['answer_type']):
            dic = {"question":q,
                   "generated_answer":out.outputs[0].text,
                   "gold_answer":a,
                   "type":t
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds = [], []
        
        for el in results:
            gens.append(el['generated_answer'])
            golds.append(el['gold_answer'])
        return evaluate_KW(gens, golds, keywords=['true', 'false'], strict=True)


class DataSet_GeoSQA(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("GeoSQA", tokenizer=tokenizer)
        self.max_tokens = 3

    def get_messages(self, row):
        question = f"""Image Annotation :
        {row['annotation']}
        
        Scenario :
        {row['scenario']}

        Question :
        {row['question']}

        Choices :
        A) {row['A']}
        B) {row['B']}
        C) {row['C']}
        D) {row['D']}
        """
        messages = [
            {"role": "system", "content": "You are a strict and precise geography assistant specialized in GaoKao-style multiple-choice questions. You will receive an IMAGE TEXT ANNOTATION and a linked SCENARIO followed by a QUESTION and several answer choices labeled A, B, C, D (or similar). Exactly one option is correct. Your task is to identify the correct answer using the IMAGE ANNOTATION and the SCENARIO and reply ONLY with the corresponding letter (e.g., A, B, C, or D). Do not include any explanation, reasoning, punctuation, or extra text. Respond with a single uppercase letter only."},
            {"role": "user", "content": question}
        ]
        return messages

    def get_answer(self, row):
        a = [
            {"role": "assistant", "content": row['answer']}
        ]
        
        return a

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, a in zip(outputs, dataset['answer']):
            dic = {"generated_answer":out.outputs[0].text,
                   "gold_answer":a
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds = [], []
        for el in results:
            gens.append(el['generated_answer'])
            golds.append(el['gold_answer'])
        return evaluate_MQC(gens, golds)

class DataSet_GKMC(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("GKMC", tokenizer=tokenizer)
        self.max_tokens = 3

    def get_messages(self, row):
        question = f"""Scenario :
        {row['scenario']}

        Question :
        {row['question']}

        Choices :
        A) {row['A']}
        B) {row['B']}
        C) {row['C']}
        D) {row['D']}
        """
        messages = [
            {"role": "system", "content": "You are a strict and precise geography assistant specialized in GaoKao-style multiple-choice questions. You will receive a SCENARIO followed by a QUESTION and several answer choices labeled A, B, C, D (or similar). Exactly one option is correct. Your task is to identify the correct answer and reply ONLY with the corresponding letter (e.g., A, B, C, or D). Do not include any explanation, reasoning, punctuation, or extra text. Respond with a single uppercase letter only."},
            {"role": "user", "content": question}
        ]
        return messages

    def get_answer(self, row):
        a = [
            {"role": "assistant", "content": row['answer']}
        ]
        
        return a

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, a, q_id in zip(outputs, dataset['answer'], dataset['question_id']):
            dic = {"generated_answer":out.outputs[0].text,
                   "gold_answer":a,
                   "q_id":q_id
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds = [], []
        for el in results:
            gens.append(el['generated_answer'])
            golds.append(el['gold_answer'])
        return evaluate_MQC(gens, golds)


class DataSet_GridRoute(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("GridRoute", tokenizer=tokenizer)
        self.max_tokens = 300
        self.metric = "optimal_ratio"

    def get_messages(self, row):
        obs = [(p[0], p[1]) for p in row['obstacles_coords']]
        messages = [
            {"role": "system", "content": f"""You are an expert in path planning. You're given a square matrix of size {row['matrix_size']} with these obstacles coordinates {obs}. You're goal is plan a continous path going from a starting point S of coordinates ({row['start'][0]}, {row['start'][1]}) to an end point E of coordinates ({row['end'][0][0]}, {row['end'][0][1]}) that avoid all the obstacles. There are some rules you must respect : 
            - You can only follow 4 directions : UP, DOWN, LEFT and RIGHT. 
            - The ouput has to be in the format : [(x1, y1), (x2,y2), (x3, y3)...]."""},
            {"role": "user", "content": f'Give a path going from the starting point S to the end point E in the expected format without any extra explanations.'}
        ]
        return messages

    def get_answer(self, row):
        path = [(p[0], p[1]) for p in row['path']]
        a = [
            {"role": "assistant", "content": str(path)}
        ]
        
        return a

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, p, obs, n, e in zip(outputs, dataset['path'], dataset['obstacles_coords'], dataset['matrix_size'], dataset['end']):
            dic = {"generated_answer":out.outputs[0].text,
                   "gold_path":p,
                   "obs":obs,
                   "n":n,
                   "end": e
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds, obs, ends, n = [], [], [], [], []
        
        for el in results:
            gens.append(el['generated_answer'])
            golds.append(el['gold_path'])
            obs.append(el['obs'])
            ends.append(el['end'])
            n.append(el['n'])
        return evaluate_path_planning(gens, golds, obs, ends, n)


class DataSet_MsMarco_place(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("MsMarco", tokenizer=tokenizer)
        self.max_tokens = 300
        self.metric = "bleu-1"

    def get_messages(self, row):
        messages = [
            {"role": "system", "content": """You are a geography expert."""},
            {"role": "user", "content": f"You will be asked location questions involving one or more geographic entities asked by users on Internet. Answer the following geographic question with the most precise answer possible. \nQuestion: {row['question']}"}
        ]
        return messages

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, q, a in zip(outputs, dataset['question'], dataset['answer']):
            dic = {"question":q,
                   "generated_answer":out.outputs[0].text,
                   "gold_answer":a
                  }
            results.append(dic)
        return results

    def get_answer(self, row):
        a = [
            {"role": "assistant", "content": row['answer']}
        ]
        
        return a

    def evaluate(self, results):
        gens, golds = [], []
        for el in results:
            gens.append(el['generated_answer'])
            golds.append([el['gold_answer']])
        return evaluate_MSMarco(gens, golds)

class DataSet_NY_POI(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("NY-POI", tokenizer=tokenizer)
        self.max_tokens = 100
        self.metric = "accuracy@1"

    def get_messages(self, row):
        messages = [
            {
                "role": "system",
                "content": f"""
        You are a recommendation system that predicts a user's next point of interest (POI).
        
        ### Input Data
        - **Long-term check-ins** (Format: POIID, Category, Time): {row['long-term_check-ins']}
        - **Recent check-ins** (Format: POIID, Category, Time): {row['recent_check-ins']}
        - **Candidate set** (Format: POIID, Distance, Category): {row['candidates']}
        
        Each POI is represented by:
        - **POIID**: unique identifier of the POI.
        - **Distance**: distance in kilometers between the user and the POI.
        - **Category**: semantic type of the POI (e.g., restaurant, park, shop).
        - **Time**: timestamp (UTC) of the user's visit.
        
        ### Task
        Recommend the next POI that the user is most likely to visit from the **candidate set**, based on their check-in history.
        
        ### Key Considerations
        1. **Long-term preferences** — users often revisit categories or locations they have frequented before.  
        2. **Recent preferences** — users’ latest visits indicate their short-term interests.  
        3. **Distance** — users are more likely to visit nearby POIs.  
        4. **Category transitions** — consider typical sequential transitions between categories (e.g., from café → park → restaurant).  
        
        Think carefully about the relationships between these factors before generating your answer.
        """
            },
            {
                "role": "user",
                "content": """
        Provide a list of the **10 most likely POIs** (by their POIID) from the <candidate set> that the user might visit next.  
        Return the answer ONLY in the format:  
        [POIID1, POIID2, ..., POIID10]  
        Do not include explanations or additional text.
        """
            }
        ]
        return messages

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, a in zip(outputs, dataset['answer']):
            dic = {"generated_answer":out.outputs[0].text,
                   "gold_answer":a
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds = [], []
        for el in results:
            gens.append(el['generated_answer'])
            golds.append(el['gold_answer'][0])
        return evaluate_POI(gens, golds, n_chances=10)


class DataSet_PPNL_multi(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("PPNL_multi", tokenizer=tokenizer)
        self.max_tokens = 300
        self.metric = "optimal_ratio"

    def get_messages(self, row):
        obs = [(p[0], p[1]) for p in row['obstacles_coords']]
        goal = [(p[0], p[1]) for p in row['end']]
        messages = [
            {"role": "system", "content": f"""You are an expert in path planning. You're given a square matrix of size {row['matrix_size']} with these obstacles coordinates {obs}. You're goal is plan a continous path going from a starting point S of coordinates ({row['start'][0]}, {row['start'][1]}) that pass through every objective points E of coordinates {goal} that avoid all the obstacles. There are some rules you must respect : 
            - You can only follow 4 directions : UP, DOWN, LEFT and RIGHT. 
            - The ouput has to be in the format : [(x1, y1), (x2,y2), (x3, y3)...].
            - If a valid path cannot be created without touching any obstacle, return an emtpy path []."""},
            {"role": "user", "content": f'Give a path going from the starting point S passing through every objective point E in the expected format without any extra explanations.'}
        ]
        return messages

    def get_answer(self, row):
        path = [(p[0], p[1]) for p in row['path']]
        a = [
            {"role": "assistant", "content": str(path)}
        ]
        
        return a

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, obs, p, s, g, n in zip(outputs, dataset['obstacles_coords'], dataset['path'], dataset['start'], dataset['end'], dataset['matrix_size']):
            dic = {"generated_answer":out.outputs[0].text,
                   "gold_path":p,
                   "obs":obs,
                   "start":s,
                   "end":g,
                   "n":n
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds, obs, ends, n = [], [], [], [], []
        
        for el in results:
            gens.append(el['generated_answer'])
            golds.append(el['gold_path'])
            obs.append(el['obs'])
            ends.append(el['end'])
            n.append(el['n'])
        return evaluate_path_planning(gens, golds, obs, ends, n)

class DataSet_PPNL_single(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("PPNL_single", tokenizer=tokenizer)
        self.max_tokens = 300
        self.metric = "optimal_ratio"

    def get_messages(self, row):
        obs = [(p[0], p[1]) for p in row['obstacles_coords']]
        messages = [
            {"role": "system", "content": f"""You are an expert in path planning. You're given a square matrix of size {row['matrix_size']} with these obstacles coordinates {obs}. You're goal is plan a continous path going from a starting point S of coordinates ({row['start'][0]}, {row['start'][1]}) to an end point E of coordinates ({row['end'][0][0]}, {row['end'][0][1]}) that avoid all the obstacles. There are some rules you must respect : 
            - You can only follow 4 directions : UP, DOWN, LEFT and RIGHT. 
            - The ouput has to be in the format : [(x1, y1), (x2,y2), (x3, y3)...].
            - If a valid path cannot be created without touching any obstacle, return an emtpy path []."""},
            {"role": "user", "content": f'Give a path going from the starting point S to the end point E in the expected format without any extra explanations.'}
        ]
        return messages

    def get_answer(self, row):
        path = [(p[0], p[1]) for p in row['path']]
        a = [
            {"role": "assistant", "content": str(path)}
        ]
        
        return a

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, obs, p, s, e, n in zip(outputs, dataset['obstacles_coords'], dataset['path'], dataset['start'], dataset['end'], dataset['matrix_size']):
            dic = {"generated_answer":out.outputs[0].text,
                   "gold_path":p,
                   "obs":obs,
                   "start":s,
                   "end":e,
                   "n":n
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds, obs, ends, n = [], [], [], [], []
        
        for el in results:
            gens.append(el['generated_answer'])
            golds.append(el['gold_path'])
            obs.append(el['obs'])
            ends.append(el['end'])
            n.append(el['n'])
        return evaluate_path_planning(gens, golds, obs, ends, n)
        
class DataSet_SpartUN(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("SpartUN", tokenizer=tokenizer)
        self.max_tokens = 100

    def get_messages(self, row):
        def prompt_YN(row):
            question = f"""### Scenario :
            {row['scenario']}
    
            ### Question :
            {row['question']}
            """
            messages = [
                {"role": "system", "content": "You are a strict and precise geography assistant with topological abilities. You will receive a SCENARIO followed by a YES / NO QUESTION. Your task is to reply to the question based on the scenario. Do not include any explanation, reasoning, punctuation, or extra text. Respond with YES or NO in uppercase letter only."},
                {"role": "user", "content": question}
            ]
    
            return messages
    
        def prompt_FR(row):
            candidates = ""
            for c in row['candidates_answers']:
                candidates += c.upper() + "\n"
            question = f"""### Scenario :
            {row['scenario']}
    
            ### Question :
            {row['question']}
    
            ### Possible topological relations :
            {candidates}
            """
            messages = [
                {"role": "system", "content": "You are a precise geography assistant specialized in topological reasoning. You will receive a SCENARIO, a QUESTION, and a list of POSSIBLE ANSWERS representing topological relations. Your task is to output the correct(s) topological relation(s) based solely on the information provided. Respond with exactly one or multiple of the possible answers that you think are correct, written in uppercase letters only, without explanation or punctuation."},
                {"role": "user", "content": question}
            ]
    
            return messages
    
        if row['type'] == 'YN':
            return prompt_YN(row)
        else:
            return prompt_FR(row)
            
    def get_answer(self, row):
        if row['type'] == 'YN':
            ans = row['answer'][0].upper()
        else:
            ans = str([r.upper() for r in row['answer']])
            
        a = [
            {"role": "assistant", "content": ans}
        ]
        
        return a

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, t, a, k, q_id, cand_ans in zip(outputs, dataset['type'], dataset['answer'], dataset['k_hop'], dataset['question_id'], dataset['candidates_answers']):
            dic = {"generated_answer":out.outputs[0].text,
                   "gold_answer":a,
                   "type":t,
                   'k_hop': k,
                   'q_id': q_id,
                   'candidates_answers': cand_ans
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds = {'YN': [], 'FR': []}, {'YN': [], 'FR': []}
        fr_candidates = None
        for el in results:
            t = el['type']
            gens[t].append(el['generated_answer'])
            golds[t].append(el['gold_answer'])
            if fr_candidates is None and t == 'FR':
                fr_candidates = el['candidates_answers']
                
        yn_metrics = evaluate_KW(gens['YN'], golds['YN'], ['yes', 'no'])
        fr_metrics = evaluate_KW(gens['FR'], golds['FR'], fr_candidates)

        yn_metrics = {f"yn_{k}": v for k, v in yn_metrics.items()}
        fr_metrics = {f"fr_{k}": v for k, v in fr_metrics.items()}

        metrics = yn_metrics
        metrics.update(fr_metrics)

        # Macro average
        metrics.update({'accuracy': (metrics['yn_accuracy'] + metrics['fr_accuracy'])/2})

        return metrics


class DataSet_SpatialEvalLLM(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("SpatialEvalLLM", tokenizer=tokenizer)
        self.max_tokens = 10

    def get_messages(self, row):
        q = f"""### Scenario :
        {row['scenario']}

        ### Question :
        {row['question']}
        """
        messages = [
            {
                "role": "system",
                "content": 
                    """You are a precise geography assistant specialized in topological reasoning. You will receive a SCENARIO describing a tile map of different shapes and sizes. In each tile, you'll find an object. One or multiple objects are the answer to the question. Output only the name(s) of the object(s) and do NOT include explanations, punctuation, or extra text."""

            },
            {"role": "user", "content": q}
        ]
        return messages

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, a, k, s in zip(outputs, dataset['answer'], dataset['k_hop'], dataset['struct_type']):
            dic = {"generated_answer":out.outputs[0].text,
                   "gold_answer":a,
                   "k":k,
                   "struct":s
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        '''
        gens, golds = {}, {}
        for el in results:
            struct = el['struct']
            k = el['k']
            if not struct in gens:
                gens[struct] = {}
                golds[struct] = {}

            if not k in gens[struct]:
                gens[struct][k] = []
                golds[struct][k] = []
                
            gens[struct][k].append(el['generated_answer'])
            golds[struct][k].append(el['gold_answer'])
        '''
        gens, golds = [], []
        for el in results:
            gens.append(el['generated_answer'])
            golds.append(el['gold_answer'])
        return evaluate_KW(gens, golds, keywords=None, strict=True)
        


class DataSet_StepGame(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("StepGame", tokenizer=tokenizer)
        self.max_tokens = 20

    def get_messages(self, row):
        candidates = ""
        for c in row['candidates_answers']:
            candidates += c.upper() + "\n"
        question = f"""### Scenario :
        {row['scenario']}

        ### Question :
        {row['question']}

        ### Possible topological relations :
        {candidates}
        """
        messages = [
            {
                "role": "system",
                "content": 
                    """You are a precise and rule-abiding geography assistant specialized in topological reasoning. You will receive a SCENARIO, a QUESTION, and a list of POSSIBLE TOPOLOGICAL RELATIONS. 
                    Your task:
                    - Determine which of the listed topological relations best describes the situation.
                    - Respond with EXACTLY one of the possible answers.
                    Formatting rules:
                    - Output only the answer word, in UPPERCASE letters (e.g., 'ABOVE').
                    - Do NOT include explanations, punctuation, or extra text."""

            },
            {"role": "user", "content": question}
        ]
        return messages

    def get_answer(self, row):
        a = [
            {"role": "assistant", "content": row['answer']}
        ]
        
        return a

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, a, k, cand_ans, sce, q in zip(outputs, dataset['answer'], dataset['k_hop'], dataset['candidates_answers'], dataset['scenario'], dataset['question']):
            dic = {"generated_answer":out.outputs[0].text,
                   "gold_answer":a,
                   "k":k,
                   'candidates_answers': cand_ans,
                   'sq': sce + " " + q
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds = [], []
        fr_candidates = results[0]['candidates_answers']
        for el in results:
            gens.append(el['generated_answer'])
            golds.append([el['gold_answer']])
                
        return evaluate_KW(gens, golds, fr_candidates)
        
class DataSet_TourismQA(DataSet):
    def __init__(self, tokenizer=None):
        super().__init__("TourismQA", tokenizer=tokenizer)
        self.max_tokens = 50
        self.metric = "bleu-1"

    def get_messages(self, row):
        messages = [
            {"role": "system", "content": "You are a strict and precise geography assistant specialized in POI recommendation. You will receive a QUESTION asked by a user asking for a POI recommendation. Do not include any explanation, reasoning, punctuation, or extra text. Respond with a single POI name that you think is a good fit for the user's request."},
            {"role": "user", "content": row['question']}
        ]
        return messages

    def get_answer(self, row):
        a = [
            {"role": "assistant", "content": row['answers_names'][0]}
        ]
        
        return a

    def results(self, outputs, split='test', dataset=None):
        if dataset is None:
            dataset = self.dataset[split]
        results = []
        for out, a in zip(outputs, dataset['answers_names']):
            dic = {"generated_answer":out.outputs[0].text,
                   "gold_answer":a
                  }
            results.append(dic)
        return results

    def evaluate(self, results):
        gens, golds = [], []
        for el in results:
            gens.append(el['generated_answer'])
            golds.append(el['gold_answer'])
        return evaluate_many_to_many(gens, golds)


DATASET_CLASSES = {
    "GeoQuery_place": DataSet_GeoQuery_place,
    "GeoQuery_regression": DataSet_GeoQuery_regression,
    "GeoQuestions1089_regression": DataSet_GeoQuestions1089_regression,
    "GeoQuestions1089_coord": DataSet_GeoQuestions1089_coord,
    "GeoQuestions1089_place": DataSet_GeoQuestions1089_place,
    "GeoQuestions1089_YN": DataSet_GeoQuestions1089_YN,
    "GeoSQA": DataSet_GeoSQA,
    "GKMC": DataSet_GKMC,
    "GridRoute": DataSet_GridRoute,
    "MsMarco": DataSet_MsMarco_place,
    "NY-POI": DataSet_NY_POI,
    "PPNL_multi": DataSet_PPNL_multi,
    "PPNL_single": DataSet_PPNL_single,
    "SpartUN": DataSet_SpartUN,
    "SpatialEvalLLM": DataSet_SpatialEvalLLM,
    "StepGame": DataSet_StepGame,
    "TourismQA": DataSet_TourismQA
}
