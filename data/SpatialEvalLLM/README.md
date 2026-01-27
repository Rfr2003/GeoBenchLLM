# SpatialEvalLLM

The SpatialEvallLLM dataset aims to assess the ability of language models to understand and navigate differents spatial configurations. The authors offered two levels of descriptions : 
- **global** : the structure is entirely described
- **local** : only partial information of the structure is given.

The data is synthetic and can be generated at this [repo](https://github.com/runopti/SpatialEvalLLM). We used the same data as the authors for their paper and available [here](https://huggingface.co/datasets/yyamada/SpatialEvalLLM).

## Download Data

Go to the Hugging Faces [repo](https://huggingface.co/datasets/yyamada/SpatialEvalLLM) and download the repositories **map_global** and **map_local**. 

## Conversion to Hugging Faces Dataset

Run the notebook **codes/extract.ipynb**, to have the Hugging Faces dataset.

## Citation

Thanks to the authors for their work. If you use this dataset, please cite their paper :

@article{yamada2023evaluating,
    title={Evaluating Spatial Understanding of Large Language Models},
    author={Yamada, Yutaro and Bao, Yihan and Lampinen, Andrew K and Kasai, Jungo and Yildirim, Ilker},
    journal={Transactions on Machine Learning Research},
    year={2024}
}

