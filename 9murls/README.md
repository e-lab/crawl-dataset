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

```
python3 getImages.py dict.csv 41classes.csv path_To_images.csv path_To_labels.csv numbe_of_img_per_class targetFolder
```
Shell script to run code after downloading files it will generate testTrain as root folder.

```
sh run.sh
```
note: labels.csv and images.csv must sync i.e. train/labels.csv train/images.csv
note: class: scissors is not in validation dataset it's only at trainSet
