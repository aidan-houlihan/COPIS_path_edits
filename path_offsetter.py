# -*- coding: utf-8 -*-

import numpy as np
import json
import tkinter
from tkinter import Tk 
from tkinter.filedialog import askopenfilename

Tk().withdraw()
filename = askopenfilename() 
print(filename)

# reading the data from the file
with open(filename) as f:
	path_file = f.read()

# reconstructing the data as a dictionary
path = json.loads(path_file)

# # importing easygui module
# from easygui import *

# #offset message box  
# text = "Enter Your Path Edits"
# title = "Path Edits"
# input_list = ["X-Offset", "Y-Offset", "Z-Offset"]
# output = multenterbox(text, title, input_list)

# x_offset,y_offset,z_offset = output

# print(x_offset)
# print(y_offset)
# print(z_offset)

cam_to_edit = input("If you would like to edit only a single camera enter its index, if not enter n.\n")
consecutive = input("Are the poses you wish to edit a)all for this cam, b)a consecutive section of poses, or c)non-consecutive sections of poses?\n")

if consecutive == "b":
    consec_poses = []
    start = int(input("Enter the starting pose: "))
    end = int(input("Enter the ending pose: "))

    for p in range(start, end+1):
        print(p)
        consec_poses.append(p)

if consecutive == "c":
    series_num = int(input("How many sections of cameras do you wish to adjust? "))

    series_dct = {}

    for i in range(0,series_num):

        series_dct['series_%s' %i] = []

        start = int(input("Enter the starting pose for section %s: " % str(i+1)))
        end = int(input("Enter the ending pose for section %s: " % str(i+1)))

        for p in range(start, end+1):
            series_dct['series_%s' %i].append(p)

x_offset = float(input("Enter x-offset or press enter to skip\n") or "0")
y_offset = float(input("Enter y-offset or press enter to skip\n") or "0")
z_offset = float(input('Enter z-offset or press enter to skip\n') or "0")

edit_pan_tilt = input("Would you like to fix pan and tilt? y/n\n")

if edit_pan_tilt == "y":
  pan = float(input("Enter pan fix or press enter to skip\n") or "0")
  tilt = float(input("Enter tilt fix or press enter to skip\n") or "0")

poses = (len(path['imaging_path']))

name = input("Enter 'New Filename.cproj' or use n to name automatically\n")

input("Press enter to continue...")

if cam_to_edit !=  "n":

  cam_to_edit = int(cam_to_edit)

  for i in range(0,poses):

    cams = len(path['imaging_path'][i])

    for j in range(0, cams):

      print(path['imaging_path'][i][j][0]['device'])

      if path['imaging_path'][i][j][0]['device'] == cam_to_edit:

        new_x = float(path['imaging_path'][i][j][0]['args'][0][1]) + x_offset
        new_y = float(path['imaging_path'][i][j][0]['args'][1][1]) + y_offset
        new_z = float(path['imaging_path'][i][j][0]['args'][2][1]) + z_offset

        path['imaging_path'][i][j][0]['args'][0][1] = str(new_x)
        path['imaging_path'][i][j][0]['args'][1][1] = str(new_y)
        path['imaging_path'][i][j][0]['args'][2][1] = str(new_z)

        if edit_pan_tilt == "y":
          path['imaging_path'][i][j][0]['args'][3][1] = str(pan)
          path['imaging_path'][i][j][0]['args'][4][1] = str(tilt)
         
else:
  for i in range(0,poses):

    cams = len(path['imaging_path'][i])

    for j in range(0, cams):
      new_x = float(path['imaging_path'][i][j][0]['args'][0][1]) + x_offset
      new_y = float(path['imaging_path'][i][j][0]['args'][1][1]) + y_offset
      new_z = float(path['imaging_path'][i][j][0]['args'][2][1]) + z_offset

      path['imaging_path'][i][j][0]['args'][0][1] = str(new_x)
      path['imaging_path'][i][j][0]['args'][1][1] = str(new_y)
      path['imaging_path'][i][j][0]['args'][2][1] = str(new_z)

      if edit_pan_tilt == "y":
        path['imaging_path'][i][j][0]['args'][3][1] = str(pan)
        path['imaging_path'][i][j][0]['args'][4][1] = str(tilt)
  
if name == "n":
  new_filename = filename[:len(filename)-6] + "_edited" + ".cproj"
  print(new_filename)

  with open(new_filename, 'w') as convert_file:
    convert_file.write(json.dumps(path))

else:

  with open(name, 'w') as convert_file:
    convert_file.write(json.dumps(path))

# Tk().withdraw()
# add1 = askopenfilename() 
# print(filename)

# # reading the data from the file
# with open(add1) as f:
# 	add_path1 = f.read()

# # reconstructing the data as a dictionary
# path1 = json.loads(add_path1)

# Tk().withdraw()
# add2 = askopenfilename() 
# print(filename)

# # reading the data from the file
# with open(add2) as f:
# 	add_path2 = f.read()

# # reconstructing the data as a dictionary
# path2 = json.loads(add_path2)

input("All done! Press Enter to close this window...")