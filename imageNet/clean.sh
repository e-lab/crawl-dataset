#! /bin/bash

find ./person -maxdepth 1 -mindepth 1 -type d | while read d; do
    for file in $d; do
        echo file
        find $file -maxdepth 1 -mindepth 1 -type f | while read img; do
          if [[ ($img != *.png) ]]
          then
              echo %img delete
              rm -f $img
          fi
        done
    done
done
