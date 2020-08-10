# event_based_gaze_tracking
Thanks for your interest in the ebv-eye dataset! Below is a brief description of the dataset and how to work with it.
Please direct any questions to ...

This dataset contains synchronized left and right, IR illuminated eye data from 24 subjects. The data was collected
using DAVIS 364b sensors from iniVation. For additional details regarding setup and data collection, please refer to
Section 4 of the paper.

The data is stored in the eye_data/ directory. This directory contains 24 subdirectories, one for each subject. Within
each of these subject directories is two folders titled, 0 and 1. 0 corresponds to the left eye and 1 corresponds to the
right eye. Within each of these eye directories is a frames directory for video data and an events.aerdat file for event
data. Each of these formats will be explained below

      Example: the video data for left eye for subject 3 is located at "eye_data/user3/0/frames/"
      Example: the event data for the right eye of subject 11 is located at "eye_data/user11/1/events.aerdat"

Frame Data:
The frames directory contains regular video data stored as a set of image frames. The video was taken at
~25 FPS and each frame is a 8-bit 346 × 260 px greyscale png file. Each frame is indexed via its filename in the
following format: "Index_Row_Column_Stimulus_Timestamp.png".

      Index: (int) indexes the images according to what order they were captured in. Can be used to align the left
      and right eyes. Can also be used to leave out frames capturing blinks using the csv files in the blinks directory.

      Row: (int) which row (how low) on the screen the stimulus point when the frame was captured. This is measured in
      pixels going from the top of the screen to the bottom (higher values corresponds to lower on the screen).
      Vertical center is 540px.

      Column: (int) which column (how right) on the screen the stimulus point when the frame was captured. This is
      measured in pixels going from the left of the screen to the right (higher values corresponds to more right on the
      screen). Horizontal center is 960px.

      Stimulus: (string) which type of stimulus was being displayed when the frame was captured. 'st' means stop and is
      when there was no stimulus and the subject was getting prepared to begin. 's' is for saccade and the stimulus was
      a stationary point on the screen which jumps in a to a random point on the screen after waiting a fixed period of
      time. 'p' is for smooth pursuit and the stimulus was a point on the screen that smoothly moves across the screen at
      a fixed rate.

      Timestamp: (int) what exact time the frame was captured relative to when the sensor was turned on 
      in microseconds. This timestamp is consistent between both eyes and with the corresponding event data. 
      The timestamp is also consistent with the Index, i.e as the Index increases so does the timestamp.

       Example: "94_540_1122_s_237060314.png" is the 94th captured image in the video 237060314 
       microseconds from sensor init, and the stimulus was for saccades located 540 pixels down and 1122 pixels right  
       from the top left corner of the screen.
      
      
Event Data:
The events.aerdat file contains all the event based information in a binary format.
