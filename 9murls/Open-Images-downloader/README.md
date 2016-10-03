# Open Image Dataset Downloader

This is download script of [Open Dataset](https://github.com/openimages/dataset)

It needs large amount of disk space.

## Preparation

```
pip install -r requiments
```

## How to use it

Download csv file from

```
bash download.sh
```

Then start to download

```
python run.py ./download/images_2016_08/train/images.csv ./download/images_2016_08/validation/images.csv ./download/images --num_workers 30
```