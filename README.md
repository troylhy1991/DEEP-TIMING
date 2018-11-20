# DEEP-TIMING
Deep Learning Solution to TIMING (Time-lapse Microscopy in Nanowell Grids) Project created and maintained by [Single-Cell Lab](http://singlecell.chee.uh.edu/), [FARSight Group](http://www.farsight-toolkit.org/wiki/Main_Page), [STIM Laboratory](http://stim.ee.uh.edu/) and [HULA Lab](https://www.hvnguyen.com/hula-lab) at University of Houston, Houston, Texas.

## Introduction

Deep learning algorithms show top performance on image classification and object detection tasks over general-purpose image domains (IMAGENET, MSCOCO). This repository explores the performance of state-of-art image classifier and object detector on a different domain consisting of time-lapse microscopy images collected in TIMING project. Extended from the initial exploration, we created annotated TIMING datasets efficiently using man-in-the-loop fashion and our customized annotation tool, to support the fine-tuning of the deep learning models. And an end-to-end TIMING pipeline is developed to detect, track and quantify cells with robustness and flexibility.

## Highlights

* High-quality annotated TIMING Data
  Leveraging unsupervised algorithm and man-in-the-loop fashion, we generated more than 5,000 nanowell images with cell bounding box annotations, 180 sequences of time-lapse nanowell frames with bounding box as well as track ID annotations and 72,000 cropped cell patches with apoptosis status (positive/negative) annotations.

* Cell detection leveraging phase-contrast channel and Faster R-CNN algorithm


* Label-free apoptosis classification using CNN and LSTM Models


* Customized visualization tool from TIMING2-board



## Installation


## Usage


## Contact
Email: hlu9@uh.edu
