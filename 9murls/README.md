# Open Image Dataset downloader

Downloads images from the Google Open Image Dataset: https://github.com/openimages/dataset


## To install dependency

Needs python >= 3.5

See requirement.txt for python pacakges

```
sh install.sh
```

Have to upgrade pip3 when fail init pip3 in ubuntu

```
sudo -H python3 -m pip install --upgrade pip
```

## First Downloading url and lebel files
```
sh download.sh
```

## To download images from given csv file

Do python3 getImages.py with follow option options

1st option : dict.csv

2end option: Your classes.csv

3rd option : path to images.csv i.e. images_2016_08/validation/images.csv

4th option : path to labels.csv i.e. machine_ann_2016_08/validation/labels.csv

5th option : Number of Max images per class

6th option   : Number of Threads

6th option : Target folder to download

#To test

```
sh run.sh
```

note: labels.csv and images.csv must sync i.e. train/labels.csv train/images.csv
note: class: scissors is not in validation dataset it's only at trainSet
