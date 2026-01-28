# MsMarco

MS MARCO is a large-scale dataset created by Microsoft for information retrieval and question answering, based on real user queries from Bing. It pairs questions with relevant passages and human-written answers to train and evaluate search and QA models.

You can find their website [here](https://microsoft.github.io/msmarco/).

We will use the data from the Question and Answering task v2.1.

## Download Data

We use the v2.1 of the dataset to construct ours. You can find it on their website or directly on [Hugging Faces](https://huggingface.co/datasets/microsoft/ms_marco). You will need the train and the dev splits as the test one doesn't disclose the answers. 

Note that the following code uses the .json files downloaded from the Ms Marco website. Even if the data is the same it will need a little wor on your side to transform it from HF datasets format to a json one compatible with the code.

Ms Marco contains 56 721 LOCATIONS questions (geography related) through its train and dev splits. However some of these questions are not really relevant ('where was elvis stationed in Germany') or ambiguous. That's why we used the work of Hamzei et al. that already analyzed the questions. You can find their github repo [here](https://github.com/haonan-li/place-qa-AGILE19/tree/master). You'll need to download the following [file](https://github.com/haonan-li/place-qa-AGILE19/blob/master/data/result/result.json) containing their results.

## Filtering the questions and building the final dataset

For that you'll need to run the notebook **code/to_HF.ipynb**.

## Citation

Thanks to the authors for their work. If you use this dataset, please cite their paper :

@article{DBLP:journals/corr/NguyenRSGTMD16,
  author    = {Tri Nguyen and
               Mir Rosenberg and
               Xia Song and
               Jianfeng Gao and
               Saurabh Tiwary and
               Rangan Majumder and
               Li Deng},
  title     = {{MS} {MARCO:} {A} Human Generated MAchine Reading COmprehension Dataset},
  journal   = {CoRR},
  volume    = {abs/1611.09268},
  year      = {2016},
  url       = {http://arxiv.org/abs/1611.09268},
  archivePrefix = {arXiv},
  eprint    = {1611.09268},
  timestamp = {Mon, 13 Aug 2018 16:49:03 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/NguyenRSGTMD16.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}

@inbook{placequestions,
author = {Hamzei, Ehsan and Li, Haonan and Vasardani, Maria and Baldwin, Timothy and Winter, Stephan and Tomko, Martin},
year = {2020},
month = {01},
pages = {3-19},
title = {Place Questions and Human-Generated Answers: A Data Analysis Approach},
isbn = {978-3-030-14745-7},
doi = {10.1007/978-3-030-14745-7_1}
}

