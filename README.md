# DEEP-TIMING
Deep Learning Solution to TIMING (Time-lapse Microscopy in Nanowell Grids) Project created and maintained by [Single-Cell Lab](http://singlecell.chee.uh.edu/), [FARSight Group](http://www.farsight-toolkit.org/wiki/Main_Page), [STIM Laboratory](http://stim.ee.uh.edu/) and [HULA Lab](https://www.hvnguyen.com/hula-lab) at University of Houston, Houston, Texas.

## Introduction

Deep learning algorithms show top performance on image classification and object detection tasks over general-purpose image domains (IMAGENET, MSCOCO). This repository explores the performance of state-of-art image classifier and object detector on a different domain consisting of time-lapse microscopy images collected in TIMING project. Extended from the initial exploration, we created annotated TIMING datasets efficiently using man-in-the-loop fashion and our customized annotation tool, to support the fine-tuning of the deep learning models. And an end-to-end TIMING pipeline is developed to detect, track and quantify cells with robustness and flexibility.

## Highlights

* High-quality annotated TIMING Data. 
  Leveraging unsupervised algorithm and man-in-the-loop fashion, we generated more than 5,000 nanowell images with cell bounding box annotations, 180 sequences of time-lapse nanowell frames with bounding box as well as track ID annotations and 72,000 cropped cell patches with apoptosis status (positive/negative) annotations. Annotated data can be found in the [Deep TIMING Supplementary Materials]() folder.

* Cell detection leveraging phase-contrast channel and Faster R-CNN algorithm. 
  Trained state-of-art cell detector using [Faster R-CNN](https://github.com/rbgirshick/py-faster-rcnn) model. Tested cell detection performance using different combination of input channels.
  
<p align="center">
  <img src="https://github.com/troylhy1991/DEEP-TIMING/blob/master/imgs/detect_model.PNG" width="400">
  <img src="https://github.com/troylhy1991/DEEP-TIMING/blob/master/imgs/detect_result.PNG" width="400">
</p>

* Label-free apoptosis classification using CNN and LSTM Models
  Implemented state-of-art convolutional neural net classifier. Used reccurent model (LSTM) to improve sequence classification performance considering temporal dependency.

<p align="center">
  <img src="https://github.com/troylhy1991/DEEP-TIMING/blob/master/imgs/cnn-lstm2.PNG" width="400">
  <img src="https://github.com/troylhy1991/DEEP-TIMING/blob/master/imgs/apoptosis_classification.PNG" width="400">
</p>


* Customized visualization tool from TIMING2-board
<p align="center">
  <img src="https://github.com/troylhy1991/DEEP-TIMING/blob/master/imgs/labelTrack.PNG" width="600">
</p>
## Requirements:

* 64-bit computer with at least 2GHz processor running Windows, Linux or Mac
* CUDA-enabled GPU, memory >= 8 GB recommended
* Hard drive storage >= 2TB, solid-state hard drive strongly recommended

## Installation
(1) Download this repository and put the folder say /HOME_DIRECTORY/DEEP-TIMING/

(2) Download auxiliary modules and test data, and copy the folders to /HOME_DIRECTORY/DEEP-TIMING/ and to /HOME_DIRECTORY/DEEP-TIMING/DATA/raw/. (create folder DATA and subdirectory /raw/ and /results respectively.)

 * [DT2-detector](https://drive.google.com/drive/folders/1Wpe37aHK4fIPuJFnHtGkreXGMnQ1C881?usp=sharing)
 
 * [test data](https://drive.google.com/drive/folders/1gAyU5QkZNY29x9N8DENkYpeJ_B_6Aqq5?usp=sharing)
 
(3) Download and install [Anaconda](https://www.anaconda.com/download/?lang=en-us)

(4) Create the environments for TIMING2-pipeline and TIMING2-board, open Anaconda Prompt, change to DEEP-TIMING home directory /HOME_DIRECTORY/DEEP-TIMING/, and type python setup_env.py

(5) Set up DT-pipeline, in the prompt, type activate DT-pipeline, and then type python setup_DT_pipeline.py

(6) Open another Anaconda Prompt, change to DEEP-TIMING home directory, type activate DT-board, and then type python setup_DT_board.py (independent from step 5)

(7) Have a cup of coffee, will be ready in several minutes.

## Usage
1.DT-Pipeline wil do cell detection, tracking and feature calculation with phase contrast channels; follow the steps in [Deep-TIMING-Pipeline-Demo.ipynb](https://github.com/troylhy1991/DEEP-TIMING/blob/master/DEEP-TIMING-Pipeline-Demo.ipynb);

2.The evaluation data, scripts are included in the [Supplementary Materials](). And the evaluation steps can be fould [here](https://github.com/troylhy1991/DEEP-TIMING/tree/master/docs)

## Contact
Email: hlu9@uh.edu

## License
This code is free for non-commerical use only
