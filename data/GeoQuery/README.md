# Geoquery

Geoquery was originally intended to translate sentences to their corresponding logical queries using a semantic parser. It used data from the database Geobase gathered in 1996.

We use the version of the database made available by Finegan-Dollak et al. who used it evaluate their system in text-to-sql tasks.
Their repository can be found [here](https://github.com/jkkummerfeld/text2sql-data). 

## Download Data

We will use the database available to retrieve the answers. You'll need for that the [database](https://github.com/jkkummerfeld/text2sql-data/blob/master/data/geography-db.added-in-2020.sqlite), and the [data](https://github.com/jkkummerfeld/text2sql-data/blob/master/data/geography.json), [test](https://github.com/jkkummerfeld/text2sql-data/blob/master/data/original/geography.uw.test.txt) and [dev](https://github.com/jkkummerfeld/text2sql-data/blob/master/data/original/geography.uw.dev.txt) files containing the questions and their translation in sql.

Please note that while running the code, two syntax errors happened. It affected the requests lines 129 and 223 of the train file.

We were able to easily solve them by replacing the sql resquest of these lines. We give here the new requests (please put them in a single line or the code will not work).

For line 129 :
```sql
SELECT COUNT(river.river_name) FROM river WHERE river.traverse = 'texas' AND river.length > (SELECT MAX(river.length) FROM river WHERE river.river_name = 'red');
```

For line 223 (you just need to delete the external paranthesis) :
```sql
SELECT city.state_name FROM city WHERE city.population = (SELECT min(tmp.population) FROM (SELECT city.population FROM city, state WHERE state.capital = city.city_name) tmp);
```

## Query the Database

The next step is to query the database to get the answers to the questions. For that, run the script **code/query_db.py**.

```bash
python3 query_db.py --db_path 'PATH_TO_DB' --train_file 'PATH_TO_TRAIN.txt' --dev_file 'PATH_TO_DEV.txt' --test_file 'PATH_TO_TEST.txt' --output_path 'PATH_TO_OUTPUT.csv'
```

## Converting to HF dataset format

Run the notebook **code/to_HF.ipynb**, to have the Hugging Faces dataset.

## Citation

Thanks to the authors for their work. If you use this dataset, please cite their paper :

```Tex
@inproceedings{finegan-dollak-etal-2018-improving,
    title = "Improving Text-to-{SQL} Evaluation Methodology",
    author = "Finegan-Dollak, Catherine  and
      Kummerfeld, Jonathan K.  and
      Zhang, Li  and
      Ramanathan, Karthik  and
      Sadasivam, Sesh  and
      Zhang, Rui  and
      Radev, Dragomir",
    editor = "Gurevych, Iryna  and
      Miyao, Yusuke",
    booktitle = "Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2018",
    address = "Melbourne, Australia",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P18-1033/",
    doi = "10.18653/v1/P18-1033",
    pages = "351--360",
}

@inproceedings{data-geography-original
  dataset   = {Geography, original},
  author    = {John M. Zelle and Raymond J. Mooney},
  title     = {Learning to Parse Database Queries Using Inductive Logic Programming},
  booktitle = {Proceedings of the Thirteenth National Conference on Artificial Intelligence - Volume 2},
  year      = {1996},
  pages     = {1050--1055},
  location  = {Portland, Oregon},
  url       = {http://dl.acm.org/citation.cfm?id=1864519.1864543},
}
```