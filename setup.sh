#!/usr/bin/env bash

mkdir eye_data
cd eye_data

# Subject by subject
wget -v -O user3.tar.gz -L https://berkeley.box.com/shared/static/csdre0tcgg8yvqj3n1ps8cr67di79vxj
tar -xzf user3.tar.gz
rm user3.tar.gz

wget -v -O user9.tar.gz -L https://berkeley.box.com/shared/static/i34p1v1k0oq8it2orp9o8y41knse815x 
tar -xzf user9.tar.gz
rm user9.tar.gz

cd ..
