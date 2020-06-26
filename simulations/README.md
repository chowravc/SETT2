# XYModel
Code to solve the XY model with both a Monte-Carlo method and a Landau Ginzburg method. I have a simple python implementation that I did to test the ideas out, and then I moved to Fortran.

## Running with Docker

The simulations can be run in a docker container. Simply pull the docker image from dockerhub with

```
docker pull jeffmm/mlfilms:latest
```
Alternatively, you can build the container locally by navigating to the root folder of the repo and running
```
bash build_docker.sh
```
Navigate to the simulation directory and run the simulation by running the bash script. The script will run the simulation in the container while mounting the current directory, so that output files will sync locally.
```
cd fortran/LandauGin/
bash run_docker.sh
```
## Random Defect Generation
The folder randomDefects contains the code necessary for generating perfectly annotated simulation data.
Run 
```
./call_defect.sh
```
to generate data files of simulated defects. You can modify the last number in the line
```
for value in {1..100}
```
to change how many data files are generated.
To transform those data files into images and annotations useful for machine learning, run 
```
python accumulate.py
```
This script will create a new folder called accumulated which contains all of the generated defect setups in image form, a folder containing images with the defects marked, a folder containing xml annotations for the defects, and a folder with noisy versions of the images (useful for training)


## Generating Movies

The code is a simple implementation of the Metropolis algorithm. I have it set up with a rat's nest of helper scripts, so I'll take a top down view
of a typical run.

1. Generating Parameter List

The user vi's into param.py (which is just a script to generate a text file of a list of parameters), and hardcodes in the parameters that they want.
I have it set up so that you can test out a multitude of temperatures and elastic constants for the simulation. Param.py spits out params.txt,
which is a simple textfile containing the simulation parameters.

2. Calling Main Script

The user then runs ./call_defect.sh, which is a simple shell script which:
i. compiles the fortran code
ii. reads in the parameters for the simulation runs
iii. generates a directory tree for each parameter combination, to keep the results organized
iv. runs the code defect.f90, which generates the .dat files
v. runs defectMovie.py which takes the .dat files and creates a movie of both the texture, and the movement of the defects
vi. organizes everything as nicely as I can manage.

At the end of the day, you should have a timestamped folder run-timestamp-- and in it will be a folder that says movies-- which will contain 
all the movies your simulation run generated. I have the python movie program also put the labels of the parameters in the movies directly, 
which I find helpful.

## Monte-Carlo
The high level view of this method is you are solving an **energy** minimization problem with the XY hamiltonian, with added thermal flucuations.
The monte-carlo's parameters are:
g -- the elastic constant
beta -- 1/Temperature
N -- the size of the grid
endT -- how long the simulation runs
I don't know enough about Monte-Carlo stuff, but because you aren't directly interacting with an equation of motion here, the time-step may
not be linearly proportional to real time.

## The Landau-Ginzburg 
The high level view of this method is that you are solving Newton's equations for a **torque** with added thermal flucuations. Because you have actually made contact with an equation of motion, I'm more comfortable interpreting each time-step of the simulation as real time.

## Dependencies
The python programs needs the usual suspects: pandas, numpy, matplotlib, as well as moviepy and PIL
The fortran program doesn't have any dependencies-- I'm not linking any externals to it.

```