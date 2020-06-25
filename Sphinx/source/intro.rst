Test Page for Stuff
*******************

How to Run a Model on Images

Brief Description of what is going on:

 You have a bunch of images (*.tif files). You also have a pre-trained model with files ForLL.meta and ForLL.pb.

(Rough Notes)
Program expects yolo_custom2.meta and .pb in ‘SETT\darkflow\built_graph’. The directory built_graph needs to be created and rename your pretrained model ForLL.meta and .pb to yolo_custom2.* and paste them into that directory.

In the config meta make everything false other than correct images, runModel and saveRun. Even validate should be false.
Now run it once . You will get an error message but the root directory containing SETT will have a new directory ‘data’.

In data, paste all your *.tif images into ‘data\collated\annotations’. These should be raw uncorrected images.
Run the model again. 

‘data\collated\annotations\corrected\outIMG’ will contain your output images with defect locations and .json files.
You can now use these .json files to validate data.

How to Validate Data

Brief Description of what is going on:
    You have already finished running the model on some images and get an output of .json files (named *.json). Now you want to determine how well the model performed in mAP so you also have labelled .xml files (named *.xml).
    
Let us start with the following things:
.json files from detection.
.xml files from hand labelling.

Files being used:
config.yml from ForLL folder
Put this in the SETT directory
ForLL.pb and ForLL.meta
Create directory “bin” in “darkflow”
Put both of these files in the directory.
“input” directory from mAP-master
Copy this directory directly into mAP
A lot of files from validationData

Stepwise setup:
Clone SETT from github
https://github.com/mlfilms/SETT
Download ForLL folder
Download validationData folder
Download mAP:
https://github.com/Cartucho/mAP
Create a new conda environment. I found it least painful when there are no existing packages in  anaconda or pip.
Run pip install -r requirements.txt
Run python setup.py build_ext --inplace
From ForLL folder, copy config.yml and paste it directly into SETT. Overwrite existing config.yml.
Go to “meta” in config.yml and edit as follows:
correctImages: false
enhanceImages: false
extractSmartNoise: false
runModel: false
runName: ForLL
runSimulation: false
saveModel: false
saveRun: true
trainModel: false
validate: true
Go to “darkflow” in config.yml and edit as follows:
meta_file: bin/ForLL.meta
pb_file: bin/ForLL.pb
Open the directory “darkflow” in SETT. Create a directory “bin”.
From ForLL folder, copy ForLL.pb and ForLL.meta into “darkflow/bin”.
Open the directory “mAP” in SETT. Copy directory “input” from the “mAP” download in STEP 4 into mAP in SETT.
Open validate.py in mAP and edit as follows:
Change:
wipeFolder(mAPTruthPath)
wipeFolder(mAPDetectionPath)
To:
flag = input("Enter 'yes' to wipe ground-truth and detection-results")
    if flag == "yes":
        wipeFolder(mAPTruthPath)
        wipeFolder(mAPDetectionPath)
From ‘validationData’ downloaded on STEP 3, open ‘validationData\images\corrected\outIMG’. Copy all .json files here. Paste them into SETT at ‘SETT\mAP\input\detection-results’ after making sure no other files exist.
From ‘validationData’ downloaded on STEP 3, open ‘validationData\annotations\out’. Copy all .xml files here. Paste them into SETT at ‘SETT\mAP\input\ground-truth’ after making sure no other files exist there.
Run python overlord.py config.yml
Python should start validating. Make sure to press enter and not input ‘yes’ when asked.
Results will be outputted to ‘SETT\runData\ForLL’.






