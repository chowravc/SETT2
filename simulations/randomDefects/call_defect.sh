#!/bin/bash

mkdir dataFolder
cd dataFolder
runName=$(echo $(date +%Y%m%d_%H%M%S))
mkdir run"$runName"
cd run"$runName"
decross=25
mkdir data
mkdir im
cp ../../randomD.py ./
for value in {1..10}
do
    python randomD.py $decross
    name1=`echo "out$value.dat"`
    name2=`echo "defect$value.dat"`
    name3=`echo "image$value.bmp"`
    echo $name1
    mv out.dat data/$name1
    mv defect.dat data/$name2
    mv training.bmp im/$name3
done


