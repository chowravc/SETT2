#!/bin/bash
cp * dataFolder/
cd dataFolder
gfortran -O3 -o defect.o defect.f90
gfortran -O3 -o defectT.o aveDefect.f90

#mkdir data
#arguments g, beta, N, endT 
python param.py
file="./params.txt"
runName=$(echo $(date +%Y%m%d_%H%M%S))
mkdir run"$runName"
cd run"$runName"
mkdir movies
cp ../params.txt ./
while read -r params
do
    g=`echo $params| awk '{print $1}'`
    beta=`echo $params| awk '{print $2}'`
    mu=`echo $params| awk '{print $3}'`
    N=`echo $params| awk '{print $4}'`
   # mkdir ./g-"$g"
   # cd ./g-"$g"
   # mkdir ./beta-"$beta"
   # cd beta-"$beta"
   # mkdir ./mu-"$mu"
   # cd ./mu-"$mu"
    echo $params > param.txt
    dName=`echo "./data-g-$g-beta-$beta-mu-$mu"` 
    mkdir $dName
    #mkdir ./g-"$g"-beta-"$beta"-mu-"$mu"-data 
    cd $dName

    cp ../../defect.o ./
    cp ../../ePlot.gnu ./
    ./defect.o $params | tee -a meanE.dat
    echo 'start video encoding program'
    cp ../../dtrack.sh ./ 
    cp ../../defectT.o ./
    ./dtrack.sh $N >> output.txt
    mv ./output.txt ../g-"$g"_b-"$beta"_mu-"$mu"-defectTracks.txt
    cd ../
    pwd
    cp ../defectMovie.py ./
    echo $dName
    python defectMovie.py $dName
    cp defect.mp4 ./movies/g-"$g"_b-"$beta"_mu-"$mu"-defect.mp4
    cp dT.mp4 ./movies/g-"$g"_b-"$beta"_mu-"$mu"-tracking.mp4
    mv defect.mp4 g-"$g"_b-"$beta"_mu-"$mu"-defect.mp4
    cd ../
done <$file
#./defect.o 10, .4, 64, 1001
#mv *.dat data/

