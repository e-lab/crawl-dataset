#!/usr/bin/env bash

export DOWNLOAD_DIR='./source'
mkdir ${DOWNLOAD_DIR}
cd ${DOWNLOAD_DIR}


wget https://storage.googleapis.com/openimages/2016_08/images_2016_08_v3.tar.gz
wget https://storage.googleapis.com/openimages/2016_08/machine_ann_2016_08.tar.gz
wget https://storage.googleapis.com/openimages/2016_08/human_ann_2016_08.tar.gz

tar xf images_2016_08_v3.tar.gz && rm images_2016_08_v3.tar.gz
tar xf machine_ann_2016_08.tar.gz && rm machine_ann_2016_08.tar.gz
tar xf human_ann_2016_08.tar.gz && rm human_ann_2016_08.tar.gz


