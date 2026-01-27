# SpartUN

SpartUN was created to test PLM abilities on spatial language processing tasks.

The data is synthetic and can be generated at this [repo](https://github.com/HLR/SpaRTUN/tree/main). We didn't generate new data but used the one made available by the authors.

## Download Data

Download [this](https://www.cse.msu.edu/~kordjams/data/SPARTUN.zip) and unzip it.

For each split a lot of files are available, we used the ones called **train.json**, **dev.json** and **test.json**.

## Conversion to Hugging Faces Dataset

Run the notebook **codes/join.ipynb**, to have the Hugging Faces dataset.

## Citation

Thanks to the authors for their work. If you use this dataset, please cite their paper :

@inproceedings{mirzaee-kordjamshidi-2022-transfer,
    title = "Transfer Learning with Synthetic Corpora for Spatial Role Labeling and Reasoning",
    author = "Mirzaee, Roshanak  and
      Kordjamshidi, Parisa",
    booktitle = "Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing",
    month = dec,
    year = "2022",
    address = "Abu Dhabi, United Arab Emirates",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.emnlp-main.413",
    pages = "6148--6165",
    abstract = "",
}

