#!/usr/bin/env python3
"""
Amit Kohli, Julien Martel, and Anastasios Angelopoulos
August 10, 2020
This script provides a visualization of the ebv-eye data.
"""

import argparse
import struct
import glob
import os
import matplotlib.pyplot as plt
from PIL import Image
from collections import namedtuple

parser = argparse.ArgumentParser(description='Arguments for using the eye visualizer')
parser.add_argument('--subject', type=int, default=22, help='which subject to evaluate')
parser.add_argument('--eye', default='left', choices=['left', 'right'],
                    help='Which eye to visualize, left or right')
parser.add_argument('--data_dir', default=os.path.join(os.getcwd(), 'eye_data'),
                    help='absolute path to eye_data/, by default assumes same parent dir as this script')
parser.add_argument('--buffer', type=int, default=1000, help='How many events to store before displaying.')
opt = parser.parse_args()

'Types of data'
Event = namedtuple('Event', 'polarity row col timestamp')
Frame = namedtuple('Frame', 'row col img timestamp')

'Color scheme for event polarity'
color = ['r', 'g']


def glob_imgs(path):
    imgs = []
    for ext in ['*.png', '*.jpg', '*.JPEG', '*.JPG']:
        imgs.extend(glob.glob(os.path.join(path,'**', ext), recursive=True))
    return imgs


'Reads an event file'
def read_aerdat(filepath):
    with open(filepath, mode='rb') as file:
        file_content = file.read()

    ''' Packet format'''
    packet_format = 'BHHI'                              # pol = uchar, (x,y) = ushort, t = uint32
    packet_size = struct.calcsize('='+packet_format)    # 16 + 16 + 8 + 32 bits => 2 + 2 + 1 + 4 bytes => 9 bytes
    num_events = len(file_content)//packet_size
    extra_bits = len(file_content)%packet_size

    '''Remove Extra Bits'''
    if extra_bits:
        file_content = file_content[0:-extra_bits]

    ''' Unpacking'''
    event_list = list(struct.unpack('=' + packet_format * num_events, file_content))
    event_list.reverse()

    return event_list


'Parses the filename of the frames'
def get_path_info(path):
    path = path.split('/')[-1]
    filename = path.split('.')[0]
    path_parts = filename.split('_')
    index = int(path_parts[0])
    stimulus_type = path_parts[3]
    timestamp = int(path_parts[4])
    return {'index': index, 'row': int(path_parts[1]), 'col': int(path_parts[2]), 'stimulus_type': stimulus_type,
            'timestamp': timestamp}


'Manages both events and frames as a general data object'
class EyeDataset:

    'Initialize by creating a time ordered stack of frames and events'
    def __init__(self, data_dir, user):
        self.data_dir = data_dir
        self.user = user

        self.frame_stack = []
        self.event_stack = []

    def __len__(self):
        return len(self.frame_stack) + len(self.event_stack)

    def __getitem__(self, index):
        'Determine if event or frame is next in time by peeking into both stacks'
        frame_timestamp = self.frame_stack[-1].timestamp
        event_timestamp = self.event_stack[-4]

        'Returns selected data type'
        if event_timestamp < frame_timestamp:
            polarity = self.event_stack.pop()
            row = self.event_stack.pop()
            col = self.event_stack.pop()
            timestamp = self.event_stack.pop()
            event = Event(polarity, row, col, timestamp)
            return event
        else:
            frame = self.frame_stack.pop()
            img = Image.open(frame.img).convert("L")
            frame = frame._replace(img=img)
            return frame

    'Loads in data from the data_dir as filenames'
    def collect_data(self, eye=0):
        print('Loading Frames....')
        self.frame_stack = self.load_frame_data(eye)
        print('There are ' + str(len(self.frame_stack)) + ' frames \n')
        print('Loading Events....')
        self.event_stack = self.load_event_data(eye)
        print('There are ' + str(len(self.event_stack)) + ' events \n')

    def load_frame_data(self, eye):
        filepath_list = []
        user_name = "user" + str(self.user)
        img_dir = os.path.join(self.data_dir, user_name, str(eye), 'frames')
        img_filepaths = list(glob_imgs(img_dir))
        img_filepaths.sort(key=lambda name: get_path_info(name)['index'])
        img_filepaths.reverse()
        for fpath in img_filepaths:
            path_info = get_path_info(fpath)
            frame = Frame(path_info['row'], path_info['col'], fpath, path_info['timestamp'])
            filepath_list.append(frame)
        return filepath_list

    def load_event_data(self, eye):
        user_name = "user" + str(self.user)
        event_file = os.path.join(self.data_dir, user_name, str(eye), 'events.aerdat')
        filepath_list = read_aerdat(event_file)
        return filepath_list


'Displays the data as fast as GUI can render'
def display_data(eye_dataset):
    col_buffer = []
    row_buffer = []
    polarity_buffer = []
    s = plt.plot([],[])[0]
    
    init_img_axis = False
    for i, data in enumerate(eye_dataset):
        if type(data) is Frame:
            if not init_img_axis:
            	img_axis = plt.imshow(data.img)
            	init = True
            else:
            	img_axis.set_data(data.img)
            plt.draw()
            plt.pause(0.0001)
        else:
            col_buffer += [data.col]
            row_buffer += [data.row]
            polarity_buffer += [color[data.polarity]]
            if not len(col_buffer) % opt.buffer:
                s.remove()
                s = plt.scatter(col_buffer, row_buffer, color=polarity_buffer, s=1)
                col_buffer.clear()
                row_buffer.clear()
                polarity_buffer.clear()
                plt.pause(0.0001)

    plt.show()


def main():
    eye_dataset = EyeDataset(opt.data_dir, opt.subject)
    if opt.eye == 'left':
        print('Showing the left eye of subject ' + str(opt.subject) + '\n')
        print('Loading Data from ' + opt.data_dir + '..... \n')
        eye_dataset.collect_data(0)
    else:
        print('Showing the right eye of subject ' + str(opt.subject)+ '\n')
        print('Loading Data from ' + opt.data_dir + '..... \n')
        eye_dataset.collect_data(1)

    print('Displaying Data using a ' + str(opt.buffer)+ ' event buffer...')
    display_data(eye_dataset)



if __name__ == '__main__':
    main()







