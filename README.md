Authors: 
Shashank Chavali
Naman Singh
Vishal Mulimani

The folder contains the following codes, 
1) Training.py: This is the code that is run for the first time to train the device. It records the gaze points and produces 'training_show.tsv' file which has the data of gaze points. 
2) Testing.py: After running 'Training.py', this execute this code. Datasets are stored in 'test_show.tsv'. 
3) Security.py: This is the heart of the program, where the actual security is implemented. This codes takes the datasets produced by the training phase and testing phase. Little math is involved in it and it says that weather the access has to be given to the user or not. If the datasets match 50% of each other, then access is given. We have given 50% because we are using web-cam. If the user is recommended to use Eye-Tracker device then the threshold has to be given more than 80%. 

The folder also contains pygazetracker directory, which has the header file which we directly cloned from github. 
Link for the github is : https://github.com/esdalmaijer/webcam-eyetracker

Our project has been updated in github for further development. 
