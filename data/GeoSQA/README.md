# GeoSQA

GeoSQA is a dataset compiling 4,110 geographical scenario-based questions in the GaoKao style. The dataset also contains an image for each question that was annotated making it suitable for LM. The dataset is only available in chinese, so our main work was to translate it.

## Download Data

You can download the data [here](http://ws.nju.edu.cn/gaokao/geosqa/1.0/). 

Download the file named **dataset_release_no_image.zip**.

By command line :

```bash
wget http://ws.nju.edu.cn/gaokao/geosqa/1.0/dataset_release_no_image.zip
```

Then **unzip** it.

## Extract the data

We extract the data from the .json original file and put it in a .csv file as this format makes the translation easier. 

```bash
python extract.py --input_path PATH_TO_ORIGINAL_FILE.json --ouput_path PATH_TO_OUTPUT_FILE.csv
```

## Translate the data

We used **google drive** to translate the entire dataset as we can directly translate an entire column using google's model.

## Construct the data

We then re-construct the translated data.

```bash
python extract.py --input_path PATH_TO_TRANSLATED_FILE.csv --ouput_path PATH_TO_OUTPUT_FILE.csv
```

## Sanity Check and conversion to Hugging Faces Dataset

We then look for missing information lost in translation. For these cases, we manually handle them. 
We also split the original dataset in three making sure there is no leaking scenario between the splits.

For that run the notebook **check_sanity.ipynb**.

## Citation

Thanks to the authors for their work. If you use this dataset, please cite their paper :

@misc{huang2019geosqabenchmarkscenariobasedquestion,
      title={GeoSQA: A Benchmark for Scenario-based Question Answering in the Geography Domain at High School Level}, 
      author={Zixian Huang and Yulin Shen and Xiao Li and Yuang Wei and Gong Cheng and Lin Zhou and Xinyu Dai and Yuzhong Qu},
      year={2019},
      eprint={1908.07855},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/1908.07855}, 
}

