# Event Based, Near Eye Gaze Tracking Beyond 10,000Hz
### arXiv preprint: [https://arxiv.org/abs/2004.03577](https://arxiv.org/abs/2004.03577) 
#### Angelopoulos*, Martel*, Kohli, Conradt, and Wetzstein
<p align="center">
  <a style="text-decoration:none !important;" href="https://twitter.com/ml_angelopoulos?ref_src=twsrc%5Etfw" alt="package management"> <img src="https://img.shields.io/twitter/follow/ml_angelopoulos?style=social" /> </a>
</p>

<div align="center">
  <img width="100%" alt="Eye-Tracker Illustration" src="misc/github_event_based_eye_tracking_teaser.gif">
</div>
<div align="center">
  Our gaze tracker in action (from <a href="https://www.youtube.com/watch?v=-7EneYIfinM&feature=youtu.be">our video here</a>).
</div>

<br/><br/>

This repository includes instructions for downloading and using our 27-person, near-eye, event- and frame-based gaze-tracking dataset.

## Enviroment setup

```
conda env create -f ebv-eye.yml 
```

## Data 

Download the 27-person dataset using the setup script (you might have to change user permissions with ```chmod u+x setup.sh``` before). 
Note that in the paper we only use subjects 4-27 because subjects 1-3 were recorded with a slightly different, suboptimal setup.
```
bash setup.sh 
```

## Sample visualization 
We have provided a simple python script which reads and visualizes our data. Run it with:

```
python visualize.py --data_dir ./eye_data --subject 3 --eye left --buffer 1000 
```

`buffer` controls how many events are rendered as a group. Increasing it will make the rendering faster, but blockier. 

This visualization is not real-time; the speed is limited by the rendering rate of matplotlib. The primary use of this
visualizer is to provide a minimal example of proper data parsing and alignment.

## Dataset organization
This dataset contains synchronized left and right, IR illuminated eye data from 27 subjects. The data was collected
using DAVIS 364b sensors from iniVation. For additional details regarding setup and data collection, please refer to
Section 4 of [the associated paper](https://arxiv.org/abs/2004.03577).

The data is stored in the `./eye_data/` directory. This directory contains 27 subdirectories, one for each subject. Within
each of these subject directories is two folders titled, 0 and 1. 0 corresponds to the left eye and 1 corresponds to the
right eye. Within each of these eye directories is a frames directory for video data and an events.aerdat file for event
data. Each of these formats will be explained below

<bf>Example</bf>: the video data for left eye for subject 3 is located at "eye_data/user3/0/frames/"

Event Data:
The events.aerdat file contains all the event based information in a sequential, raw binary format.
Every time an event was registered by the sensor, the following information was written directly to the binary file:
* Polarity (unsigned char, 1 byte) Whether the event was positive or negative.
* Timestamp (uint16, 4 bytes) The time, in us, at which the event was captured.
* Row (uint8, 2 bytes) The row-location of the activated pixel.
* Col (uint8, 2 bytes) The column-location of the activated pixel.
Thus, to read events.aerdat, the file must be loaded into memory and parsed byte-by-byte, in the order (uint8, uint8, uint16, unsigned char), 
where each 4-tuple indexes the information about a single event. We include an example of this parsing in `parser.py`.

<bf>Example</bf>: the event data for the right eye of subject 11 is located at "eye_data/user11/1/events.aerdat"

Frame Data:
The frames directory contains regular video data stored as a set of image frames. The video was taken at
~25 FPS and each frame is a 8-bit 346 × 260 px greyscale png file. The filename of the frame contains
the following information: in what order the frames were captured, where the subject was looking, and when the frame was captured in us.
The filename has the format "Index_Row_Column_Stimulus_Timestamp.png", where:

* Index: (int) indexes the images according to what order they were captured in. Can be used to align the left
  and right eyes.

* Row: (int) the row of the display on which the stimulus point was shown to the subject at the time the frame was captured.
  This is measured in pixels, starting from the top of the screen, and ending at the bottom 
  (higher values corresponds to lower on the screen). Vertical center is 540px.

* Column: (int) the column of the display on which the stimulus point was shown to the subject at the time the frame was captured.
  This is measured in pixels, starting from the left side of the screen, and ending at the right side 
  (higher values corresponds to further right on the screen from the subject's perspective). Horizontal center is 960px.

* Stimulus: (string, {'s','p','st'}) 's' stands for "saccade." In this mode, the stimulus shown to the subject was a small dot
  which randomly jumped to a different point on the screen after five seconds. 'p' stands for "smooth pursuit." In this mode,
  the stimulus, again a small dot, smoothly moved across the screen at a fixed rate. 'st' stands for "stop." A large pause symbol
  was shown to users in-between 's' and 'p' stimuli, and before the experiment began.

* Timestamp: (int) the time, in us, at which the frame was captured, as reported by the internal clock of the DAVIS sensor.
  Time starts when the sensor is turned on, and [clocks are synchronized between sensors using a sync connector](https://inivation.com/wp-content/uploads/2019/08/DAVIS346.pdf).
  Thus timestams are synchronized between both eyes, and with the corresponding .aerdat files.

* <bf>Example</bf>: "94_540_1122_s_237060314.png" is the 94th captured image in the video. It was captured 237060314 
  microseconds from the time the sensor was powered on, and the stimulus was a saccadic stimulus
  located 540 pixels down and 1122 pixels right, from the top left corner of the screen as seen by the subject.

The monitor on which the stimulus was displayed was a Sceptre 1080p X415BV_FSR. This model has a 40 inch diagonal, 1920x1080 pixel resolution, and was placed 40 cm away from the user, with the user's eyes roughly centered on the screen.
      
## Cite

[Event Based, Near Eye Gaze Tracking Beyond 10,000Hz](https://arxiv.org/abs/2004.03577):

```
@article{angelopoulos2020event,
  title={Event Based, Near Eye Gaze Tracking Beyond 10,000 Hz},
  author={Angelopoulos, Anastasios N and Martel, Julien NP and Kohli, Amit PS and Conradt, Jorg and Wetzstein, Gordon},
  journal={arXiv preprint arXiv:2004.03577},
  year={2020}
}
```
