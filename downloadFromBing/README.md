##This repo is for creating a large scale image data set from World Wide Web.
##To get images from csv list files

Create list.csv Column name NAME list what you want under NAME

test.csv form

```csv
NAME
dog
cat
```

1. Collect urls

```bash
python3 scrape_urls_master.py test.csv
```

2. Download images from urls

```bash
python3 download_from_json_master.py json_files
```

It will download images under images folder


Requirements: look for details require.txt

```bash
pip3 install nltk

```
To use wordnet.py

Need to install nltk and nltk.download('all')

```bash
sudo apt-get install imagemagick graphicsmagick
```

