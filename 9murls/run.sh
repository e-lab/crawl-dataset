#/usr/bin/python3
python3 getImages.py dict.csv 41classes.csv download/images_2016_08/validation/images.csv download/machine_ann_2016_08/validation/labels.csv 2 testTrain  &&\
python3 getImages.py dict.csv 41classes.csv download/images_2016_08/train/images.csv download/machine_ann_2016_08/train/labels.csv 2 testTrain
