require python3.5

pip3 install numpy

pip3 install urllib

pip3 install pillow

pip3 install scipy

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
