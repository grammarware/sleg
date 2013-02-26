#!/bin/sh

echo $@ > commit.msg
./genHome.py
cd wiki
git add -A
git commit -F ../commit.msg
cd ..
./md2html.py
cd up
git add -A
git commit -F ../commit.msg
cd ..
git add *.py *.sh up wiki
git commit -F commit.msg
rm commit.msg
