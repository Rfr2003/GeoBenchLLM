# GKMC

GKMC is a dataset compiling 1,600 geographical scenario-based questions in the GaoKao style. Contrary to the GeoSQA dataset, GKMC does not contain images, making a clear separation between them two. The dataset is only available in chinese, so our main work was to translate it.

## Download Data

You can download the data [here](https://github.com/nju-websoft/Jeeves-GKMC/blob/main/GKMC/dataset.json). 

By command line :

```bash
wget https://github.com/nju-websoft/Jeeves-GKMC/blob/main/GKMC/dataset.json
```

## Extract the data

We extract the data from the .json original file and put it in a .csv file as this format makes the translation easier. 

```bash
python extract.py --input_path PATH_TO_ORIGINAL_FILE.json --ouput_path PATH_TO_OUTPUT_FILE.csv
```

## Translate the data

We used **google drive** to translate the entire dataset as we can directly translate an entire column using google's model.

## Construct the data

We then re-construct the translated data. For some questions, the re-constuction will fail because of the translation. You will have to manually translate these questions.

```bash
python construct_dataset.py --input_path PATH_TO_TRANSLATED_FILE.csv --ouput_path PATH_TO_OUTPUT_FILE.csv
```

## Sanity Check and conversion to Hugging Faces Dataset

We then look for missing information lost in translation.

For that run the notebook **check_sanity.ipynb**.

## Citation

Thanks to the authors for their work. If you use this dataset, please cite their paper :

@misc{huang2021retrieverreadermeetsscenariobasedmultiplechoice,
      title={When Retriever-Reader Meets Scenario-Based Multiple-Choice Questions}, 
      author={Zixian Huang and Ao Wu and Yulin Shen and Gong Cheng and Yuzhong Qu},
      year={2021},
      eprint={2108.13875},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2108.13875}, 
}

