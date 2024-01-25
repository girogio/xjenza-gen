#!/bin/bash

compile(){
    echo "Compiling $1..."
    pdflatex -interaction=nonstopmode -halt-on-error -file-line-error $1.tex > /dev/null
}

clean(){
    echo "Cleaning..."
    for file in *.aux *.log *.out *.toc *.bbl *.blg *.bcf *.xml *.run.xml *.fls *.fdb_latexmk *.synctex.gz; do
        rm -f $file
    done
}

run(){
    compile $1
    echo "Running biber..."
    biber $1  > /dev/null 2>&1
    compile $1
    compile $1
    clean
    echo "Done."
}

