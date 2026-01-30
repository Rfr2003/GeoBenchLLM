# GeoQuestions1089

GeoQuestions1089 is a geospatial question-answering dataset targeting the Knowledge Graph YAGO2geo. It contains 1089 triples of geospatial questions, their answers, and the respective SPARQL/GeoSPARQL queries.

Their repository can be found [here](https://github.com/AI-team-UoA/GeoQuestions1089). 

## Download the Data

The dataset is divided into two files : [GeoQuestions1089.json](https://github.com/AI-team-UoA/GeoQuestions1089/blob/main/GeoQuestions1089.json) and [GeoQuestions1089_answers.json](https://github.com/AI-team-UoA/GeoQuestions1089/blob/main/GeoQuestions1089_answers.json). Download them.

Then, we will also need the union of the Yago2 + Yago2Geo knowledge graph. The authors gave a link to download it, however the Yago2Geo files couldn't be imported into GraphDB (used to query the graph, download it [here](https://graphdb.ontotext.com/)). We then download it from the knowlegde graph [homepage](https://yago2geo.di.uoa.gr/).

Our advise is to :
- Download the graph from [here](https://yago2geo.di.uoa.gr/data/yago2_plus_geo.zip).
- Only keep the file **yago-2_ascii.nt**, discard the others.
- Download the content of Yago2geo for the 4 existing countries (Greece, Ireland, UK and USA) from [here](https://yago2geo.di.uoa.gr/).
- Put all the files in the same folder with **yago-2_ascii.nt**.

Then, you can run this command to import everything into GraphDB :

```bash
importrdf load --force -c PATH_TO_CONGIG_FILE.ttl -m parallel PATH_TO_THE_FOLDER_CONTAINING_THE_DATA
```

We also gave you an example for the configuration file for setting up GraphDB.

## Processing the data

First, run in parallel GraphDB.

Once it's running, you can run the script **code/extract.py** to obtain the dataset with cleaned answers in a .json format.

```bash
python3 code/extract.py --output_dir 'PATH_TO_THE_OUTPUT_DIR' --data_dir 'PATH_TO_THE_DIR_CONTAINING_THE_DATA' --db_url 'http://localhost:7200/repositories/NAME_OF_THE_GRAPHDB_REPO'
```

Note that the __data_dir__ must contain the files : **GeoQuestions1089.json** and **GeoQuestions1089_answers.json**.

## Converting to HF dataset format

Run the notebook **code/create_dataset.ipynb**, to have the Hugging Faces dataset. We also do some more processing in it as translating some places names from Greek to English and converting some values in square degrees to square kilometers.

## Citation

Thanks to the authors for their work. If you use this dataset, please cite their paper :

```Tex
@inproceedings{10.1007/978-3-031-47243-5_15,
  title = {Benchmarking Geospatial Question Answering Engines Using the Dataset GeoQuestions1089},
  author = {Sergios-Anestis Kefalidis, Dharmen Punjani, Eleni Tsalapati, 
         Konstantinos Plas, Mariangela Pollali, Michail Mitsios, 
         Myrto Tsokanaridou, Manolis Koubarakis and Pierre Maret},
  booktitle = {The Semantic Web - {ISWC} 2023 - 22nd International Semantic Web Conference,
            Athens, Greece, November 6-10, 2023, Proceedings, Part {II}},
  year = {2023}
}
```