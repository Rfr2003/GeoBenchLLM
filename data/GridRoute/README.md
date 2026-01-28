# GridRoute

GridRoute is a dataset trying to assess LLM's abilities in path finding in Grid Environments.

The data is synthetic and can be generated at this [repo](https://github.com/LinChance/GridRoute). We used the same data as the authors available in their github reporsitory.

## Download Data

Go [here](https://github.com/LinChance/GridRoute/tree/main/data) and download the files **dataset.csv** and **reference.csv**. 

## Conversion to Hugging Faces Dataset

Run the notebook **codes/join.ipynb**, to have the Hugging Faces dataset.

## Citation

Thanks to the authors for their work. If you use this dataset, please cite their paper :

```Tex
@misc{li2025gridroutebenchmarkllmbasedroute,
      title={GridRoute: A Benchmark for LLM-Based Route Planning with Cardinal Movement in Grid Environments}, 
      author={Kechen Li and Yaotian Tao and Ximing Wen and Quanwei Sun and Zifei Gong and Chang Xu and Xizhe Zhang and Tianbo Ji},
      year={2025},
      eprint={2505.24306},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2505.24306}, 
}
```
