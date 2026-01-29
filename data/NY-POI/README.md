# NY-POI

This dataset, also called FourSquare dataset, was introduced by Yang et al. in the paper __'Modeling User Activity Preference by Leveraging User Spatial Temporal Characteristics in LBSNs'__ and can be found in its original version [here](https://sites.google.com/site/yangdingqi/home/foursquare-dataset).

However, we will focus on the task definition introduced by Feng et al. in their paper __'Where to Move Next: Zero-shot Generalization of LLMs for Next POI Recommendation'__ [(github)](https://github.com/LLMMove/LLMMove). 

They used a version of the dataset already preprocessed by prior works : 
1. By Yang et al. in __'GETNext: Trajectory Flow Map Enhanced Transformer for Next POI Recommendation'__ [(github)](https://github.com/songyangco/GETNext)
2. Then by Yan et al. in __'Spatio-Temporal Hypergraph Learning for Next POI Recommendation'__ [(github)](https://github.com/alipay/Spatio-Temporal-Hypergraph-Model).

## Download Data

First, you will need to download the version of the dataset preprocessed by **1.** [here](https://github.com/alipay/Spatio-Temporal-Hypergraph-Model/blob/main/data/nyc/raw.zip).

Then unzip it. We are interested in the files **NYC_train.csv**, **NYC_test.csv** and **NYC_val.csv**. Put them under the same repository.

## Applying preprocessing from 2.

In order to simplify things, we took only the files involved in the preprocessing stage of the data from the [github repository](https://github.com/alipay/Spatio-Temporal-Hypergraph-Model) and put them in the directory **codes/Spatio-Temporal-Hypergraph-Model**. You'll need to run the file **codes/Spatio-Temporal-Hypergraph-Model/preprocess_main.py**

```bash
python3 preprocess_main.py --preprocessed_dir 'PATH_TO_DIR_WITH_NYC.ZIP_CONTENT' --output_dir 'PATH_TO_THE_OUTPUT_DIR'
```

## Conversion to Hugging Faces Dataset

Run the notebook **codes/create_dataset.ipynb**, to have the Hugging Faces dataset.

In this notebook, we took the code from [LLMMove ](https://github.com/LLMMove/LLMMove) for the cells 11 and 12.

## Citation

Thanks to the authors for their work. If you use this dataset, please cite their paper :

```Tex

@inproceedings{Yang_2022, series={SIGIR ’22},
   title={GETNext: Trajectory Flow Map Enhanced Transformer for Next POI Recommendation},
   url={http://dx.doi.org/10.1145/3477495.3531983},
   DOI={10.1145/3477495.3531983},
   booktitle={Proceedings of the 45th International ACM SIGIR Conference on Research and Development in Information Retrieval},
   publisher={ACM},
   author={Yang, Song and Liu, Jiamou and Zhao, Kaiqi},
   year={2022},
   month=jul, pages={1144–1153},
   collection={SIGIR ’22} 
}
   
@ARTICLE{6844862,
  author={Yang, Dingqi and Zhang, Daqing and Zheng, Vincent W. and Yu, Zhiyong},
  journal={IEEE Transactions on Systems, Man, and Cybernetics: Systems}, 
  title={Modeling User Activity Preference by Leveraging User Spatial Temporal Characteristics in LBSNs}, 
  year={2015},
  volume={45},
  number={1},
  pages={129-142},
  keywords={Tensile stress;Data models;Context modeling;Correlation;Hidden Markov models;Location based social networks;spatial;temporal;tensor factorization;user activity preference;Location based social networks;spatial;temporal;tensor factorization;user activity preference},
  doi={10.1109/TSMC.2014.2327053}
}

@inproceedings{10.1145/3539618.3591770,
    author = {Yan, Xiaodong and Song, Tengwei and Jiao, Yifeng and He, Jianshan and Wang, Jiaotuan and Li, Ruopeng and Chu, Wei},
    title = {Spatio-Temporal Hypergraph Learning for Next POI Recommendation},
    year = {2023},
    isbn = {9781450394086},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3539618.3591770},
    doi = {10.1145/3539618.3591770},
    booktitle = {Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval},
    pages = {403–412},
    numpages = {10},
    keywords = {graph transformer, hypergraph, next poi recommendation},
    location = {Taipei, Taiwan},
    series = {SIGIR '23}
}

@INPROCEEDINGS{10605522,
  author={Feng, Shanshan and Lyu, Haoming and Li, Fan and Sun, Zhu and Chen, Caishun},
  booktitle={2024 IEEE Conference on Artificial Intelligence (CAI)}, 
  title={Where to Move Next: Zero-shot Generalization of LLMs for Next POI Recommendation}, 
  year={2024},
  volume={},
  number={},
  pages={1530-1535},
  keywords={Accuracy;Large language models;Computational modeling;Buildings;Chatbots;Cognition;Data models;LLMs;Next POI Recommendation;Zero-shot;Spatial-Temporal Data},
  doi={10.1109/CAI59869.2024.00277}
}

```
