#TO get images from csv list files

Create list.csv Column name NAME list what you want under NAME

1. Collect urls

```bash
python scrape_urls_master.py test.csv
```

test.csv form

```csv
NAME
dog
cat
```

2. Download images from urls

```bash
pthon download_from_json_master.py json_files
```

It will download images under images folder

#This repo is for creating a large scale image data set from World Wide Web.

Requirements: look for details require.txt

```bash
pip3 install nltk

```
To use wordnet.py

Need to install nltk and nltk.download('all')

```bash
sudo apt-get install imagemagick graphicsmagick
```

