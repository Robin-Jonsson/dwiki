#!/bin/sh
scss_files=`find dwiki/static/dwiki -name "*.scss"`
for file in $scss_files; do
    filename="${file%.*}"
    if [[ `basename $file` != _* ]]; then
        sassc $file $filename.css
    fi
done
