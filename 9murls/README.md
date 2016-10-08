
#Need python >= 3.5

#To install dependency
#Also see requirement.txt

```
sh install.sh
```

Have to upgrade pip3 when fail init pip3 in ubuntu

```
sudo -H python3 -m pip install --upgrade pip
```

# First Downloading url and lebel files
```
sh download.sh
```

# To download images from given csv file

Do python3 getImages.py with follow argument options
1st argument : dict.csv
2end argument: Your classes.csv
3rd argument : path to images.csv i.e. images_2016_08/validation/images.csv
4th argument : path to labels.csv i.e. machine_ann_2016_08/validation/labels.csv
5th argument : Number of Max images per class
6th argument : Target folder to download

i.e.
```
python3 getImages.py dict.csv 41classes.csv path_To_images.csv path_To_labels.csv numbe_of_img_per_class targetFolder
```

#To test

```
sh run.sh
```

note: labels.csv and images.csv must sync i.e. train/labels.csv train/images.csv
note: class: scissors is not in validation dataset it's only at trainSet
