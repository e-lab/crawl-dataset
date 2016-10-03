# -*- coding: utf-8 -*-
from __future__ import print_function

"""
    Date: 10/1/16
    &copy;2016 Takanori Ogata. All rights reserved.
"""
__author__ = 'ogata'

import os
import csv
from time import time
import requests
from tqdm import tqdm
from concurrent import futures
import click
from scipy.misc import imresize, imread, imsave
from time import sleep


def resize_image(img, new_w):
    h, w, _ = img.shape
    scale = float(new_w) / w
    new_h = int(h * scale)
    new_img = imresize(img, (new_h, new_w), interp='bilinear')
    return new_img


def download_image(image_id, url, save_dirname, resize_width):
    file_name = url.split("/")[-1]
    filepath = os.path.join(save_dirname,
                            '{}____{}'.format(image_id, file_name))

    if os.path.exists(filepath):
        return True

    res = requests.get(url, stream=True)

    if res.status_code != 200:
        print('warn: status code is {} - {}'.format(res.status_code, url))
        return False

    with open(filepath, 'wb') as file:
        for chunk in res.iter_content(chunk_size=1024):
            file.write(chunk)
    try:
        # resize and save image
        img = imread(filepath)
        if img.shape[1] > resize_width:
            resized = resize_image(img, resize_width)
            imsave(filepath, resized)
    except Exception as e:
        print('warn: failed to process {}, url: {}'.format(filepath, url))
        os.remove(filepath)
        print(e)
        return False
    return True


def load_csv(csv_filepath):
    with open(csv_filepath, 'rb') as fp:
        reader = csv.reader(fp)
        next(reader)  # skip header
        lists = list(reader)
    return lists


def download_images_from_csv(csv_filepath, save_dir, num_workers, resize_width):
    lists = load_csv(csv_filepath)
    print('csv:', csv_filepath, 'save dir:', save_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    def process(row):
        image_id, url = row[0], row[1]
        retry_count = 3
        while retry_count > 0:
            res = download_image(image_id, url, save_dir, resize_width)
            if res:
                break
            retry_count -= 1
            sleep(3.0)
        if retry_count == 0:
            print('warn: cannot download {}'.format(url))

    print('start to download...')
    t_start = time()
    with futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        mappings = [executor.submit(process, row) for row in lists]
        for dummy in tqdm(futures.as_completed(mappings), total=len(mappings)):
            pass

    t_end = time()
    print('total: {}[s]'.format(t_end - t_start))


@click.command()
@click.argument('train_csv')
@click.argument('validation_csv')
@click.argument('save_dir')
@click.option('--num_workers', default=1)
@click.option('--resize_width', default=1024)
def main(train_csv, validation_csv, save_dir, num_workers, resize_width):
    print('download train images')
    download_images_from_csv(train_csv,
                             os.path.join(save_dir, 'train'), num_workers, resize_width)

    print('download validation images')
    download_images_from_csv(validation_csv,
                             os.path.join(save_dir, 'validation'), num_workers, resize_width)


if __name__ == '__main__':
    main()
