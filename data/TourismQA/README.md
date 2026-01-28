# TourismQA

This dataset aims to challenge systems on the task of answering Points-of-Interest recommendation questions. The dataset harvest questions asked by users on multiples platforms (TripAdvisor, ...) as well as reviews left by other users. The original task was to use these reviews to recommend the most relevant POI to a certain question.

## Download Data

We weren't able to generate the dataset from the original github repository. However, thanks to Li et al. who gave the dataset, we were able to put our hands on it. 
You can download it [here](https://huggingface.co/lmlmcat/lamb-data/tree/main).

Then extract the files in it.

## Converting to HF dataset format

Run the notebook **code/transform_generative.ipynb**, to have the Hugging Faces dataset.

## Citation

Thanks to the authors for their work. If you use this dataset, please cite their paper :

```TeX
@inproceedings{10.1145/3459637.3482320,
author = {Contractor, Danish and Shah, Krunal and Partap, Aditi and Singla, Parag and Mausam, Mausam},
title = {Answering POI-recommendation Questions using Tourism Reviews},
year = {2021},
isbn = {9781450384469},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3459637.3482320},
doi = {10.1145/3459637.3482320},
booktitle = {Proceedings of the 30th ACM International Conference on Information \& Knowledge Management},
pages = {281–291},
numpages = {11},
keywords = {large scale qa, poi-recommendation, question answering, real world task, tourism qa},
location = {Virtual Event, Queensland, Australia},
series = {CIKM '21}
}


@misc{li2024locationawaremodularbiencoder,
      title={Location Aware Modular Biencoder for Tourism Question Answering}, 
      author={Haonan Li and Martin Tomko and Timothy Baldwin},
      year={2024},
      eprint={2401.02187},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2401.02187}, 
}
```