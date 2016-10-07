require python3.5

run sh install.sh to install dependency

Have to upgrade pip3 when fail init pip3

```
sudo -H python3 -m pip install --upgrade pip
```

Downloading url and lebel files
```
sh download.sh
```

To do python3 getImages.py with follow argument options
1st argument : dict.csv
2end argument: Your classes.csv
3rd argument : path to images.csv i.e. images_2016_08/validation/images.csv
4th argument : path to labels.csv i.e. machine_ann_2016_08/validation/labels.csv
5th argument : Number of Max images per class
6th argument : Target folder to download

```
python3 getImages.py dict.csv 41classes.csv path_To_images.csv path_To_labels.csv numbe_of_img_per_class targetFolder
```
Shell script to run code after downloading files it will generate testTrain as root folder.

To check in easy way try run.sh
```
sh run.sh
```
note: labels.csv and images.csv must sync i.e. train/labels.csv train/images.csv
note: class: scissors is not in validation dataset it's only at trainSet
