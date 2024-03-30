#!/bin/sh -e

rm -rf -- *.po \
   polist.inc

wget --mirror --level=1 -nd -nv -A.po \
 https://translationproject.org/latest/make

source_counter=2
for file in *.po; do
    echo "Source$source_counter: $file" >> polist.inc
    source_counter=$((source_counter + 1))
done
