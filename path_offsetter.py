# -*- coding: utf-8 -*-

import numpy as np
import json
import tkinter
from tkinter import Tk 
from tkinter.filedialog import askopenfilename


edit_or_combine = input("Would you like to a)edit a path, or b)combine two paths?\n")

if edit_or_combine == "a":
 
  #Tk().withdraw()
  filename = askopenfilename() 
  print(filename)

  # reading the data from the file
  with open(filename) as f:
    path_file = f.read()

  # reconstructing the data as a dictionary
  path = json.loads(path_file)

  poses = (len(path['imaging_path']))

  consecutive = 0

  cam_to_edit = input("If you would like to edit only a single camera enter its index, if not enter n.\n")

  if cam_to_edit != "n":
    consecutive = input("Are the poses you wish to edit a)all for this cam or b)a section(s) of poses?\n")

  if consecutive == "x":
      consec_poses = []
      start = int(input("Enter the starting pose: "))
      end = int(input("Enter the ending pose: "))

      for p in range(start, end+1):
          print(p)
          consec_poses.append(p)

  if consecutive == "b":
      series_num = int(input("How many sections of cameras do you wish to adjust? "))

      series_dct = {}

      for i in range(0,series_num):

          series_dct[i] = []

          start = int(input("Enter the starting pose for section %s: " % str(i+1)))
          end = int(input("Enter the ending pose for section %s: " % str(i+1)))

          for p in range(start, end+1):
              series_dct[i].append(p)

  x_offset = float(input("Enter x-offset or press enter to skip\n") or "0")
  y_offset = float(input("Enter y-offset or press enter to skip\n") or "0")
  z_offset = float(input('Enter z-offset or press enter to skip\n') or "0")

  edit_pan_tilt = input("Would you like to fix pan and tilt? y/n\n")

  if edit_pan_tilt == "y":
    pan = float(input("Enter pan fix or press enter to skip\n") or "0")
    tilt = float(input("Enter tilt fix or press enter to skip\n") or "0")

  name = input("Enter 'New Filename.cproj' or enter n to name automatically\n")

  input("Press enter to continue...")

  if cam_to_edit !=  "n":

    cam_to_edit = int(cam_to_edit)

    if consecutive == "a":

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
    
    # if consecutive == "x":

    #   for i in consec_poses:

    #     cams = len(path['imaging_path'][consec_poses[i]])

    #     for j in range(0,cams):

    #       if path['imaging_path'][consec_poses[i]][j][0]['device'] == cam_to_edit:

    #         new_x = float(path['imaging_path'][i][j][0]['args'][0][1]) + x_offset
    #         new_y = float(path['imaging_path'][i][j][0]['args'][1][1]) + y_offset
    #         new_z = float(path['imaging_path'][i][j][0]['args'][2][1]) + z_offset

    #         path['imaging_path'][i][j][0]['args'][0][1] = str(new_x)
    #         path['imaging_path'][i][j][0]['args'][1][1] = str(new_y)
    #         path['imaging_path'][i][j][0]['args'][2][1] = str(new_z)

    #         if edit_pan_tilt == "y":
    #           path['imaging_path'][i][j][0]['args'][3][1] = str(pan)
    #           path['imaging_path'][i][j][0]['args'][4][1] = str(tilt)

    if consecutive == "b":
      for i in range((len(series_dct))):
        for j in range(len(series_dct[i])): 
          cams = len(path['imaging_path'][series_dct[i][j]])

          for k in range(0, cams):
            if path['imaging_path'][series_dct[i][j]][k][0]['device'] == cam_to_edit:

              new_x = float(path['imaging_path'][series_dct[i][j]][k][0]['args'][0][1]) + x_offset
              new_y = float(path['imaging_path'][series_dct[i][j]][k][0]['args'][1][1]) + y_offset
              new_z = float(path['imaging_path'][series_dct[i][j]][k][0]['args'][2][1]) + z_offset

              path['imaging_path'][series_dct[i][j]][k][0]['args'][0][1] = str(new_x)
              path['imaging_path'][series_dct[i][j]][k][0]['args'][1][1] = str(new_y)
              path['imaging_path'][series_dct[i][j]][k][0]['args'][2][1] = str(new_z)

              if edit_pan_tilt == "y":
                path['imaging_path'][series_dct[i][j]][k][0]['args'][3][1] = str(pan)
                path['imaging_path'][series_dct[i][j]][k][0]['args'][4][1] = str(tilt)
            
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

  input("All done! Press Enter to close this window...")

else:
  
  number_of_paths = int(input("How many paths would you like to combine? All settings besides camera poses (proxies, device profiles, etc.) will be taken from the first path chosen\n"))
  paths = {}
  combined_path = {"imaging_path" : [] , "profile": {}, "proxies":{}}

  for i in range(number_of_paths):
    paths[i] = {}
    print("Select path %s" % str(i+1))
   
    #Tk().withdraw()
    filename = askopenfilename()

    if i == 0:
      path1name = filename

    # reading the data from the file
    with open(filename) as f:
      path = f.read()

    # reconstructing the data as a dictionary
    path_i= json.loads(path)

    paths[i] = path_i

   
  combined_path['profile'] = paths[0]['profile']
  combined_path['proxies'] = paths[0]['proxies']

  name = input("Enter 'New Filename.cproj' or enter n to name automatically\n")

  input("Press enter to continue...")


  for i in range(len(paths)):
    for j in range(len(paths[i]['imaging_path'])):

      combined_path['imaging_path'].append(paths[i]['imaging_path'][j])

  if name == "n":
    new_filename = path1name[:len(path1name)-6] + "_combined" + ".cproj"
    print(new_filename)

    with open(new_filename, 'w') as convert_file:
      convert_file.write(json.dumps(combined_path))

  with open(name, 'w') as convert_file:
    convert_file.write(json.dumps(combined_path))

  input("All done! Press Enter to close this window...")
