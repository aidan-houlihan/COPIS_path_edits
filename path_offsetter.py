# -*- coding: utf-8 -*-

from inspect import getfile
from re import T
import numpy as np
import json
import tkinter
from tkinter import * #Entry, BOTTOM, LEFT, RIGHT, TOP, Label, StringVar, Tk, Button, mainloop, ttk, Frame
from tkinter.filedialog import askopenfilename


edit_or_combine_test = 1
cam_to_edit = "" 
consecutive = ""
x_offset = ""
y_offset = ""
z_offset = ""
edit_pan_tilt = ""
pan = ""
tilt = ""
name = ""
series_num =""
start = ""
end = ""
number_of_paths = ""


def set_value(value):
  global edit_or_combine_test
  edit_or_combine_test = value
  root.destroy()
  
def set_value_cams():
  global cam_to_edit
  cam_to_edit = cam.get()
  root.destroy()

def set_consecutive(value):
  global consecutive
  consecutive = value
  root.destroy()

def getXYZ():
  global x_offset ,y_offset, z_offset
  x_offset = float(x.get())
  y_offset = float(y.get())
  z_offset = float(z.get())
  root.destroy()

def pan_tilt_ask(value):
  global edit_pan_tilt
  edit_pan_tilt = value
  root.destroy()

def getPT():
  global pan, tilt
  pan = float(p.get())
  tilt = float(t.get())
  root.destroy()
  
def getFilename():
  global name
  name = file.get()
  root.destroy()

def getSections():
  global series_num
  series_num = int(sections.get())
  root.destroy()

def getStartEnd():
  global start, end
  start = int(st.get())
  end = int(en.get())
  root.destroy()

def getPaths():
  global number_of_paths
  number_of_paths = int(path_num.get())
  root.destroy()


root = Tk()
root.eval('tk::PlaceWindow . center')
f = Frame(root)
Button(f, text='Edit a path',command=lambda *args: set_value("a")).pack(side = LEFT, padx = 20, pady = 5)
Button(f, text='Add paths',command=lambda *args: set_value("b")).pack(side = RIGHT, padx= 10, pady = 5)
label = Label(root, text = "Choose what you would like to do!")
label.pack()
f.pack()
root.mainloop()

  
#EDITING PATHS
if edit_or_combine_test == "a":

  root = Tk()
  root.withdraw()
  filename = askopenfilename()
  root.destroy()


  #Check valid .cproj file
  while True:
    if filename.endswith('.cproj'):
      break
    else:
      print("Sorry, that file is not a COPIS path, please choose another file\n")
      root = Tk()
      root.withdraw()
      filename = askopenfilename()
      root.destroy()

  

  # reading the data from the file
  with open(filename) as f:
    path_file = f.read()

  # reconstructing the data as a dictionary
  path = json.loads(path_file)

  #get the length of the imaging path (in pose sets)
  poses = (len(path['imaging_path']))


  root = Tk()
  root.eval('tk::PlaceWindow . center')
  root.attributes('-topmost',True)
  f=Frame(root)
  label = Label(root, text = "If you would like to edit only a single camera enter its index, if not enter 'n'.").pack(side = TOP, pady = 5)
  cam = Entry(root)
  cam.pack(pady = 5)
  Button(root, text = "Continue", command=lambda *args: set_value_cams()).pack(side = BOTTOM, pady = 5)
  root.mainloop()

  #cam_to_edit = input("If you would like to edit only a single camera enter its index, if not enter 'n'.\n")
  
  #check the camera index or n value from input
  while True:
    if cam_to_edit == "0" or cam_to_edit == "1" or cam_to_edit == "2" or cam_to_edit == "3" or cam_to_edit == "4" or cam_to_edit == "5" or cam_to_edit == "n":
      break
    else:
      root = Tk()
      root.eval('tk::PlaceWindow . center')
      f=Frame(root)
      label = Label(root, text = "Sorry, your input was not valid, enter a camera index (0-5) or n").pack(side = TOP, pady = 20)
      cam = Entry(root)
      cam.pack(pady = 20)
      Button(root, text = "Continue", command=lambda *args: set_value_cams()).pack(side = BOTTOM, pady = 20)
      root.mainloop()

  if cam_to_edit != "n":

    root = Tk()
    root.eval('tk::PlaceWindow . center')
    f= Frame(root)
    label = Label(root, text = "Do you wish to edit...")
    Button(f, text = "All poses for this camera?", command=lambda *args: set_consecutive("a")).pack(side = LEFT, padx = 10, pady =10)
    Button(f, text = "Certain sections of poses?", command=lambda *args: set_consecutive("b")).pack(side = RIGHT, padx = 10, pady = 10)
    label.pack(pady = 10)
    f.pack()
    root.mainloop()

    #editing all for this cam
    if consecutive == "a":
      cam_to_edit = int(cam_to_edit)

      root = Tk()
      root.eval('tk::PlaceWindow . center')
      Label(root, text = "Enter your X, Y, and Z Offsets and press Submit").grid(row = 0, sticky= N)
      Label(root, text = "X Offset").grid(row = 1, sticky = W)
      Label(root, text = "Y Offset").grid(row = 2, sticky = W)
      Label(root, text = "Z Offset").grid(row = 3, sticky = W)
      x=Entry(root)
      y=Entry(root)
      z=Entry(root)
      x.grid(row = 1, column = 0)
      y.grid(row = 2, column = 0)
      z.grid(row = 3, column = 0)
      Button(root, text = "Submit", command=lambda *args: getXYZ()).grid(row = 5, column = 0)
      root.mainloop()

      root = Tk()
      root.eval('tk::PlaceWindow . center')
      f= Frame(root)
      label = Label(root, text = "Do you wish to fix pan and tilt?")
      Button(f, text = "Yes", command=lambda *args: pan_tilt_ask("y")).pack(side = LEFT, padx = 10, pady =10)
      Button(f, text = "No", command=lambda *args: pan_tilt_ask("n")).pack(side = RIGHT, padx = 10, pady = 10)
      label.pack(pady = 10)
      f.pack()
      root.mainloop()

      #edit_pan_tilt = input("Would you like to fix pan and tilt? y/n\n")

      if edit_pan_tilt == "y":
        root = Tk()
        root.eval('tk::PlaceWindow . center')
        Label(root, text = "Enter your pan and tilt values and press Submit").grid(row = 0, sticky= N)
        Label(root, text = "Pan").grid(row = 1, sticky = W)
        Label(root, text = "Tilt").grid(row = 2, sticky = W)
        p=Entry(root)
        t=Entry(root)
        p.grid(row = 1, column = 0)
        t.grid(row = 2, column = 0)
        Button(root, text = "Submit", command=lambda *args: getPT()).grid(row = 5, column = 0)
        root.mainloop()

      for i in range(0,poses):

        cams = len(path['imaging_path'][i])

        for j in range(0, cams):

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

    #editing sections
    else: 

      root = Tk()
      root.eval('tk::PlaceWindow . center')
      Label(root, text = "How many sections would you like to adjust?").grid(row = 0, sticky= N)
      Label(root, text = "Number of Sections").grid(row = 1, sticky = W)
      sections=Entry(root)
      sections.grid(row = 1, column = 0)
      Button(root, text = "Submit", command=lambda *args: getSections()).grid(row = 2, column = 0)
      root.mainloop()

      series_dct = {}

      for i in range(0,series_num):

            series_dct[i] = []

            root = Tk()
            root.eval('tk::PlaceWindow . center')
            Label(root, text = ("Enter the starting and ending poses for Section %s" % str(i+1))).grid(row = 0, sticky= N)
            Label(root, text = "Start").grid(row = 1, sticky = W)
            Label(root, text = "End").grid(row = 2, sticky = W)
            st=Entry(root)
            en=Entry(root)
            st.grid(row = 1, column = 0)
            en.grid(row = 2, column = 0)
            Button(root, text = "Submit", command=lambda *args: getStartEnd()).grid(row = 5, column = 0)
            root.mainloop()

            for p in range(start, end+1):
                series_dct[i].append(p)

      root = Tk()
      root.eval('tk::PlaceWindow . center')
      Label(root, text = "Enter your X, Y, and Z Offsets and press Submit").grid(row = 0, sticky= N)
      Label(root, text = "X Offset").grid(row = 1, sticky = W)
      Label(root, text = "Y Offset").grid(row = 2, sticky = W)
      Label(root, text = "Z Offset").grid(row = 3, sticky = W)
      x=Entry(root)
      y=Entry(root)
      z=Entry(root)
      x.grid(row = 1, column = 0)
      y.grid(row = 2, column = 0)
      z.grid(row = 3, column = 0)
      Button(root, text = "Submit", command=lambda *args: getXYZ()).grid(row = 5, column = 0)
      root.mainloop()

      root = Tk()
      root.eval('tk::PlaceWindow . center')
      f= Frame(root)
      label = Label(root, text = "Do you wish to fix pan and tilt?")
      Button(f, text = "Yes", command=lambda *args: pan_tilt_ask("y")).pack(side = LEFT, padx = 10, pady =10)
      Button(f, text = "No", command=lambda *args: pan_tilt_ask("n")).pack(side = RIGHT, padx = 10, pady = 10)
      label.pack(pady = 10)
      f.pack()
      root.mainloop()

      if edit_pan_tilt == "y":
        root = Tk()
        root.eval('tk::PlaceWindow . center')
        Label(root, text = "Enter your pan and tilt values and press Submit").grid(row = 0, sticky= N)
        Label(root, text = "Pan").grid(row = 1, sticky = W)
        Label(root, text = "Tilt").grid(row = 2, sticky = W)
        p=Entry(root)
        t=Entry(root)
        p.grid(row = 1, column = 0)
        t.grid(row = 2, column = 0)
        Button(root, text = "Submit", command=lambda *args: getPT()).grid(row = 5, column = 0)
        root.mainloop()

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

  #editing all cameras          
  else:
    root = Tk()
    root.eval('tk::PlaceWindow . center')
    Label(root, text = "Enter your X, Y, and Z Offsets and press Submit").grid(row = 0, sticky= N)
    Label(root, text = "X Offset").grid(row = 1, sticky = W)
    Label(root, text = "Y Offset").grid(row = 2, sticky = W)
    Label(root, text = "Z Offset").grid(row = 3, sticky = W)
    x=Entry(root)
    y=Entry(root)
    z=Entry(root)
    x.grid(row = 1, column = 0)
    y.grid(row = 2, column = 0)
    z.grid(row = 3, column = 0)
    Button(root, text = "Submit", command=lambda *args: getXYZ()).grid(row = 5, column = 0)
    root.mainloop()

    root = Tk()
    root.eval('tk::PlaceWindow . center')
    f= Frame(root)
    label = Label(root, text = "Do you wish to fix pan and tilt?")
    Button(f, text = "Yes", command=lambda *args: pan_tilt_ask("y")).pack(side = LEFT, padx = 10, pady =10)
    Button(f, text = "No", command=lambda *args: pan_tilt_ask("n")).pack(side = RIGHT, padx = 10, pady = 10)
    label.pack(pady = 10)
    f.pack()
    root.mainloop()

    if edit_pan_tilt == "y":
      root = Tk()
      root.eval('tk::PlaceWindow . center')
      Label(root, text = "Enter your pan and tilt values and press Submit").grid(row = 0, sticky= N)
      Label(root, text = "Pan").grid(row = 1, sticky = W)
      Label(root, text = "Tilt").grid(row = 2, sticky = W)
      p=Entry(root)
      t=Entry(root)
      p.grid(row = 1, column = 0)
      t.grid(row = 2, column = 0)
      Button(root, text = "Submit", command=lambda *args: getPT()).grid(row = 5, column = 0)
      root.mainloop()
    
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

  #getting filename settings
  root = Tk()
  root.eval('tk::PlaceWindow . center')
  Label(root, text = "Enter 'NewFilename.cproj' or type n to generate automatically").grid(row = 0, sticky= N)
  Label(root, text = "Filename").grid(row = 1, sticky = W)
  file=Entry(root)
  file.grid(row = 1, column = 0)
  Button(root, text = "Submit and Save", command=lambda *args: getFilename()).grid(row = 2, column = 0)
  root.mainloop()

  #automatic file naming  
  if name == "n":
      new_filename = filename[:len(filename)-6] + "_edited" + ".cproj"
      print(new_filename)

      with open(new_filename, 'w') as convert_file:
        convert_file.write(json.dumps(path))

  #setting user inputed filename
  else:
      with open(name, 'w') as convert_file:
        convert_file.write(json.dumps(path))


#COMBINING PATHS
elif edit_or_combine_test == "b":

  root = Tk()
  root.eval('tk::PlaceWindow . center')
  root.attributes('-topmost',True)
  f=Frame(root)
  label = Label(root, text = "How many paths would you like to combine? All settings besides \n poses (proxies, profiles  etc.) will be taken from the first path chosen").pack(side = TOP, pady = 5)
  path_num = Entry(root)
  path_num.pack(pady = 5)
  Button(root, text = "Submit", command=lambda *args: getPaths()).pack(side = BOTTOM, pady = 5)
  root.mainloop()

  # number_of_paths = int(input("How many paths would you like to combine? All settings besides camera poses (proxies, device profiles, etc.) will be taken from the first path chosen\n"))
  paths = {}
  combined_path = {"imaging_path" : [] , "profile": {}, "proxies":{}}

  for i in range(number_of_paths):
    paths[i] = {}
   
    root = Tk()
    root.withdraw()
    filename = askopenfilename()
    root.destroy()

    while True:
      if filename.endswith('.cproj'):
        break
      else:
        print("Sorry, that file is not a COPIS path, please choose another file\n")
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

  #getting filename settings
  root = Tk()
  root.eval('tk::PlaceWindow . center')
  root.attributes('-topmost',True)
  Label(root, text = "Enter 'NewFilename.cproj' or type n to generate automatically").grid(row = 0, sticky= N)
  Label(root, text = "Filename").grid(row = 1, sticky = W)
  file=Entry(root)
  file.grid(row = 1, column = 0)
  Button(root, text = "Submit and Save", command=lambda *args: getFilename()).grid(row = 2, column = 0)
  root.mainloop()

  for i in range(len(paths)):
    for j in range(len(paths[i]['imaging_path'])):

      combined_path['imaging_path'].append(paths[i]['imaging_path'][j])

  if name == "n":
    new_filename = path1name[:len(path1name)-6] + "_combined" + ".cproj"
    print(new_filename)

    with open(new_filename, 'w') as convert_file:
      convert_file.write(json.dumps(combined_path))

  else:
    with open(name, 'w') as convert_file:
      convert_file.write(json.dumps(combined_path))
      print(name)


else:
  print("hit a button you idiot")