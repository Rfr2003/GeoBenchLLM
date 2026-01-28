# PPNL

PPNL was created to assess the spatial-temporal reasoning abilities of LLMs through path planning tasks.

The data is synthetic and can be generated at this [repo](https://github.com/MohamedAghzal/llms-as-path-planners/tree/main/ppnl-spatial-temporal-reasoning). We didn't generate new data but used the one made available by the authors.

## Download Data

You will need the directories **single_goal** and **multi_goal** in the [github repository](https://github.com/MohamedAghzal/llms-as-path-planners/tree/main/ppnl-spatial-temporal-reasoning).

## Conversion to Hugging Faces Dataset

Run the notebook **codes/create_dataset.ipynb**, to have the Hugging Faces dataset.

## Citation

Thanks to the authors for their work. If you use this dataset, please cite their paper :

```Tex
@inproceedings{aghzal2024can,
  title={Can Large Language Models be Good Path Planners? A Benchmark and Investigation on Spatial-temporal Reasoning},
  author={Aghzal, Mohamed and Plaku, Erion and Yao, Ziyu},
  booktitle={ICLR 2024 Workshop on Large Language Model (LLM) Agents},
  year={2024}
}
```
