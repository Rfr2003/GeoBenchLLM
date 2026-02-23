import evaluate

_evaluate_MQC = evaluate.load("rfr2003/mcq_eval")
_evaluate_coord = evaluate.load("rfr2003/coord_eval")
_evaluate_NY_POI = evaluate.load("rfr2003/ny_poi_evaluate")
_evaluate_KW = evaluate.load("rfr2003/keywords_evaluate")
_evaluate_regression = evaluate.load("rfr2003/regression_evaluate")
_evaluate_path_planning = evaluate.load("rfr2003/path_planning_evaluate")
_evaluate_place_gen = evaluate.load("rfr2003/place_gen_evaluate")

import numpy as np
bleu = evaluate.load('bleu')
bert_score = evaluate.load('bertscore')

def evaluate_MQC(generations, golds):
    return _evaluate_MQC.compute(generations=generations, golds=golds)

def evaluate_KW(generations, golds, keywords=['yes', 'no'], strict=True):
    for i in range(len(golds)):
        golds[i] = [str(g) for g in golds[i]]
    return _evaluate_KW.compute(generations=generations, golds=golds, keywords=keywords, strict=strict)

def evaluate_many_to_many(generations, golds):
    return _evaluate_place_gen.compute(generations=generations, golds=golds)
    
def evaluate_regression(generations, golds):
    return _evaluate_regression.compute(generations=generations, golds=golds)

def evaluate_coord(generations, golds, d_range=20):
    return _evaluate_coord.compute(generations=generations, golds=golds, d_range=d_range)

def evaluate_path_planning(generations, golds, obstacles, ends, n):
    return _evaluate_path_planning.compute(generations=generations, golds=golds, obstacles=obstacles, ends=ends, n=n)

def evaluate_POI(gens, golds, n_chances=10):
    return _evaluate_NY_POI.compute(generations=gens, golds=golds, n_chances=n_chances)

def evaluate_MSMarco(generations, golds):
    assert len(generations) == len(golds)
    assert isinstance(golds, list)

    metrics = {f"bert_score_{k}":np.mean(v).item() for k,v in bert_score.compute(predictions=generations, references=golds, lang="en").items() if k in ['recall', 'precision', 'f1']}
    metrics.update({
        'bleu-1': bleu.compute(predictions=generations, references=golds, max_order=1)['bleu']
    })
    
    return metrics