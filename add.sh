#!/bin/bash 
DST="/Users/scampion/Photos"
SRC="$1"

mkdir -p $DST
import_size=`du -sh "$SRC"`
initial_size=`du -sh "$DST"`
python sortphotos.py --sort y  --sort m --sort d --keep-duplicates "$SRC" $DST
intermediate_size=`du -sh "$DST"`
python DuplicateFiles.py -root  $DST -remove
echo 
echo "Import size       : $import_size"
echo "Initial size      : $initial_size"
echo "Intermediate size : $intermediate_size"
echo "Final size        : `du -sh $DST`"

