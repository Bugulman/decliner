#!/bin/sh
$PAN = pwd
echo $PAN
python -m setup sdist
echo '------PACKAGE COMPILED-------'
cd dist
echo '-------DIR CHANGED----------'
pip install oily_report-1.2.1.tar.gz
pip install oily_report-1.2.1.tar.gz
sleep 3
