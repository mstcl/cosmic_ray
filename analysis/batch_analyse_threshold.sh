#! /bin/sh

for filename in $HOME/data/*.dat
  do
    [ -e "$filename" ] || continue
    echo "$filename"
    analysis.py -i "$filename"
done
