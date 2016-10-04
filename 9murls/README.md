require python3.5

pip install pillow
pip install scipy

python getimages.py dict.csv 41classes.csv path_To_images.csv path_To_labels.csv numbe_of_img_per_class targetFolder

note: labels.csv and images.csv must sync i.e. train/labels.csv train/images.csv
