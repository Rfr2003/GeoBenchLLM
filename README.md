# GeoBenchmark

## 🌍 What is it ?

**GeoBenchmark** is a very accessible and complete benchmark to assess LLMs abilities across **8 geo-related tasks**. We also provide an **easy framework** to evaluate models.

The datasets and metrics are available at our **Hugging Face** page : <https://huggingface.co/collections/rfr2003/geobenchmark>.

## 📁 Codes Structure

- data/            # codes for reproducing each dataset. Check the directories inside this folder for more information.
- src/             # codes for inference and evaluation.
- configs/         # LLM's configs used for the results shown in our paper.
- gens/            # the model generations that we obtained.
- example.ipynb    # a script to rapidly infer on a dataset and evaluate.

## 🔧 Installation

Install Python dependencies.

```bash
pip install -r requirements.txt
```

## 🦾 Inference

We provide a script for inference. Here is an example of how ot run it:

```bash
python -m src.infer \
    --model_name="Qwen/Qwen3-8B" \
    --dataset_name "GeoSQA" \ #Specify "all" to infer on all datasets
    --output_dir './gens' \
    --config_path './configs/qwen.yaml'
    --verbose \
    --batch_size 32
```

You can also specify these parameters:
- **think_mode**: Activates thinking mode.
- **evaluate**: Also evaluates at the end of inference.
- **sample**: Activates sampling.
- **n_samples**: Specify the number of samples.
- **max_model_len**: Specifies the max length used by VLLM (requires more VRAM).

## 🦿 Evaluating

We provide a script for evaluating the genrations obtained after the last step. Here is an example of how ot run it:

```bash
python -m src.eval_gens \
    --model_name="Qwen/Qwen3-8B" \
    --dataset_name "GeoSQA" \ #Specify "all" to infer on all datasets
    --output_dir './evals' \
    --gens_path './gens'
    --verbose 
```

You can also specify these parameters:
- **think_mode**: Activates thinking mode.
- **sample**: Activates sampling.
- **n_samples**: Specify the number of samples.
- **force_eval**: Re-run the evaluation even if a file containing the results for the right setting exists.

## 📄 Datasets Information

| Category        | Tasks                  | Datasets                                 | Train                 | Dev                 | Test                      |
| --------------- | ---------------------- | ---------------------------------------- | --------------------- | ------------------- | ------------------------- |
| **Knowledge**   | Coordinates Prediction | GeoQuestions1089_coord                        | –                     | –                   | 87                        |
|                 | Yes/No questions       | GeoQuestions1089_YN                         | –                     | –                   | 181                       |
|                 | Regression             | GeoQuestions1089_regression<br>GeoQuery_regression             | –<br>182              | –<br>17             | 231<br>89                 |
|                 | Place prediction       | GeoQuestions1089_place<br>GeoQuery_place<br>MS-Marco_place | –<br>346<br>23 513    | –<br>33<br>4 149    | 455<br>184<br>2 907       |
| **──────────**  | **──────────**         | **──────────**                           | **──────────**        | **──────────**      | **──────────**            |
| **Reasoning**   | Scenario Complex QA    | GeoSQA<br>GKMC                           | 2 644<br>–                | 628<br>–              | 838<br>1 600            |
|                 | Spatial Reasoning      | SpatialEvalLLM<br>SpartUN<br>StepGame    | –<br>37 095<br>50 000 | –<br>5 600<br>5 000 | 1 400<br>5 551<br>100 000 |
| **──────────**  | **──────────**         | **──────────**                           | **──────────**        | **──────────**      | **──────────**            |
| **Application** | POI Recommendation     | TourismQA<br>NY-QA                       | 19 762<br>–           | 2 109<br>–          | 2 153<br>1 347            |
|                 | Path Finding           | GridRoute<br>PPNL_single<br>PPNL_multi  | –<br>16 032<br>53 440  | –<br>2 004<br>6 680 | 300<br>19 044<br>55 440    |
| **──────────**  | **──────────**         | **──────────**                           | **──────────**        | **──────────**      | **──────────**            |
| **Total**       | –                      | –                                        | **203 014**           | **26 220**          | **191 807**               |

## 💬 Citation

If you use this benchmark, please cite our paper.

