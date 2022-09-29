# -*- coding: utf-8 -*-

from ast import Return
from inspect import getfile
from re import T
import numpy as np
import json
import tkinter
from tkinter import * 
from tkinter.filedialog import askopenfilename

edit_or_combine_test = 1
cam_to_edit = None 
consecutive = None
x_offset = None
y_offset = None
z_offset = None
edit_pan_tilt = None
pan = None
tilt = None
name = None
series_num =None
start = None
end = None
number_of_paths = None
filename = None


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

# def getStartEnd():
#   global start, end
#   start = int(st.get())
#   end = int(en.get())
#   root.destroy()

def getPaths():
  global number_of_paths
  number_of_paths = int(path_num.get())
  root.destroy()

def Close():
  root.destroy()

def getAll():
  global x_offset, y_offset, z_offset, pan, tilt, edit_pan_tilt, name, cam_to_edit, consecutive
  cam_to_edit = index_entry.get()
  consecutive = check_sections.get()
  x_offset = float(x.get())
  y_offset = float(y.get())
  z_offset = float(z.get())
  edit_pan_tilt = pan_tilt_checkbox.get()
  pan = float(p.get())
  tilt = float(t.get())
  name = file.get()
  root.destroy()

def pan_tilt_enable():
  if pan_tilt_checkbox.get() == "y":
    p.config(state=NORMAL)
    t.config(state=NORMAL)
  elif pan_tilt_checkbox.get() == "n":
    p.config(state=DISABLED)
    t.config(state=DISABLED)

def sections_checkbox_enable():
  if index_entry.get() == "0" or index_entry.get() == "1" or index_entry.get() == "2" or index_entry.get() == "3" or index_entry.get() == "4" or index_entry.get() == "5":
    Sections_CheckBox.config(state=NORMAL)
  else:
    Sections_CheckBox.config(state=DISABLED)
    section_entry.config(state=DISABLED)


def sections_enable():
  if check_sections.get() == "a" or Sections_CheckBox['state'] ==DISABLED:
    section_entry.config(state=DISABLED)
  elif check_sections.get() == "b":
    section_entry.config(state = NORMAL)

def getStartEnd():
  global start, end
  start = int(st.get())
  end = int(en.get())
  for p in range(start, end+1):
    series_dct[i].append(p)
  root.destroy()

def make_sections():
  global start, end, series_dct

  number = section_num.get()
  print(number)
  series_dct = {}

  for i in range(number):

    print(i)

    series_dct[i] = []

    root = Tk()
    root.attributes('-topmost',True)
    root.title("COPIS Path Editor")
    Label(root, text = ("Enter the starting and ending poses for Section %s" % str(i+1))).grid(row = 0, sticky= N)
    Label(root, text = "Start").grid(row = 1, sticky = W)
    Label(root, text = "End").grid(row = 2, sticky = W)
    st=Entry(root)
    en=Entry(root)
    st.grid(row = 1, column = 0)
    en.grid(row = 2, column = 0)
    Button(root, text = "Submit", command=lambda *args: getStartEnd()).grid(row = 5, column = 0)
    root.eval('tk::PlaceWindow . center')

#INITIAL DIALOG BOX
root = Tk()
root.title("COPIS Path Editor")
root.eval('tk::PlaceWindow . center')
f = Frame(root)
Button(f, text='Edit a path',command=lambda *args: set_value("a")).pack(side = LEFT, padx = 10, pady = 5)
Button(f, text='Combine paths',command=lambda *args: set_value("b")).pack(side = LEFT, padx= 10, pady = 5)
Button(f, text='Invert a path',command=lambda *args: set_value("c")).pack(side = LEFT, padx= 10, pady = 5)
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
      print("Sorry, that file is not a COPIS path, please choose a .cproj file\n")
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

  #SETTINGS DIALOG BOX
  root = Tk()
  root.title("COPIS Path Editor")
  root.eval('tk::PlaceWindow . center')
  root.attributes('-topmost',True)
  root.columnconfigure(0,weight=1)
  root.columnconfigure(1, weight = 5)

  #Title
  Label(root, text = "Enter your Settings and press Submit").grid(row = 0, column= 0)

  #Camera Index Selection
  Label(root, text = "Type a camera index to edit\nand hit Enter (Leave blank for all)").grid(row =1, column=0)
  #index = StringVar()
  index_entry=Entry(root)
  index_entry.bind('<Return>', lambda *args: sections_checkbox_enable())
  index_entry.grid(row = 1, column = 1, pady = 5, padx = 5)

  #Camera Section Selection
  check_sections = StringVar()
  Sections_CheckBox = Checkbutton(root, text = "Check to edit multiple\nsections for this camera", variable= check_sections, onvalue = "b", offvalue = "a", command = lambda *args: sections_enable())
  Sections_CheckBox.grid(row = 2, column = 0)
  Sections_CheckBox.deselect()
  Sections_CheckBox.config(state=DISABLED)

  Label(root, text = "Enter the number of sections to edit\nand press Enter").grid(row = 3, column = 0, sticky =E)
  section_num = IntVar()
  section_entry = Entry(root, textvariable = section_num)
  section_entry.config(state=DISABLED)
  section_entry.bind('<Return>', lambda *args: make_sections())
  section_entry.grid(row=3, column = 1, padx = 5)


  #XYZ Offset Settings
  Label(root, text = "X Offset").grid(row = 4, column = 0,sticky = E)
  Label(root, text = "Y Offset").grid(row = 5, column = 0,sticky = E)
  Label(root, text = "Z Offset").grid(row = 6, column = 0,sticky = E)
  x=Entry(root)
  y=Entry(root)
  z=Entry(root)
  x.grid(row = 4, column = 1, padx = 5)
  y.grid(row = 5, column = 1, padx = 5)
  z.grid(row = 6, column = 1, padx = 5)

  #Pan and Tilt Settings

  pan_tilt_checkbox = StringVar()
  PanTilt_Checkbutton = Checkbutton(root, text = "Check to Fix Pan and Tilt", variable = pan_tilt_checkbox, onvalue = "y", offvalue= "n", command = lambda *args: pan_tilt_enable())
  PanTilt_Checkbutton.grid(row = 7, column = 0)
  PanTilt_Checkbutton.deselect()
  Label(root, text = "Pan").grid(row = 8, column = 0,sticky = E)
  Label(root, text = "Tilt").grid(row = 9, column = 0,sticky = E)
  p=Entry(root)
  t=Entry(root)
  p.grid(row = 8, column = 1, padx = 5)
  t.grid(row = 9, column = 1, padx = 5)

  #New Filename Settings
  Label(root, text = "Enter name or leave blank \nto generate automatically").grid(row = 10, column = 0)
  file=Entry(root)
  file.grid(row = 10, column = 1)
  #Button(root, text = "Submit and Save", command=lambda *args: getFilename()).grid(row = 2, column = 0)

  Button(root, text = "Submit and Save", command= lambda *args: getAll()).grid(row = 13, column = 0, pady = 5)
  root.eval('tk::PlaceWindow . center')
  root.mainloop()

  print(cam_to_edit)
  print(x_offset)
  print(y_offset)
  print(z_offset)
  print(edit_pan_tilt)
  print(pan)
  print(tilt)
  print(name)

  ##OLDER DIALOG BOXES
  root = Tk()
  root.withdraw()
  filename = askopenfilename()
  root.destroy()

  root = Tk()
  root.title("COPIS Path Editor")
  root.attributes('-topmost',True)
  f=Frame(root)
  label = Label(root, text = "If you would like to edit only a single camera \n enter its index, if not leave blank.").pack(side = TOP, pady = 5)
  cam = Entry(root)
  cam.pack(pady = 5)
  Button(root, text = "Continue", command=lambda *args: set_value_cams()).pack(side = BOTTOM, pady = 5)
  root.eval('tk::PlaceWindow . center')
  root.mainloop()
  
  #check the camera index or n value from input
  while True:
    if cam_to_edit == "0" or cam_to_edit == "1" or cam_to_edit == "2" or cam_to_edit == "3" or cam_to_edit == "4" or cam_to_edit == "5" or cam_to_edit == "":
      break
    else:
      root = Tk()
      root.title("COPIS Path Editor")
      f=Frame(root)
      label = Label(root, text = "Sorry, your camera input was not valid, enter a camera index (0-5) or leave blank").pack(side = TOP, pady = 20)
      cam = Entry(root)
      cam.pack(pady = 20)
      Button(root, text = "Continue", command=lambda *args: set_value_cams()).pack(side = BOTTOM, pady = 20)
      root.eval('tk::PlaceWindow . center')
      root.mainloop()

  if cam_to_edit != "":

    root = Tk()
    root.title("COPIS Path Editor")
    f= Frame(root)
    label = Label(root, text = "Do you wish to edit...")
    Button(f, text = "All poses for this camera?", command=lambda *args: set_consecutive("a")).pack(side = LEFT, padx = 10, pady =10)
    Button(f, text = "Certain sections of poses?", command=lambda *args: set_consecutive("b")).pack(side = RIGHT, padx = 10, pady = 10)
    label.pack(pady = 10)
    f.pack()
    root.eval('tk::PlaceWindow . center')
    root.mainloop()

    #editing all for this cam
    if consecutive == "a":
      cam_to_edit = int(cam_to_edit)

      root = Tk()
      root.title("COPIS Path Editor")
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
      root.eval('tk::PlaceWindow . center')
      root.mainloop()

      root = Tk()
      root.title("COPIS Path Editor")
      f= Frame(root)
      label = Label(root, text = "Do you wish to fix pan and tilt?")
      Button(f, text = "Yes", command=lambda *args: pan_tilt_ask("y")).pack(side = LEFT, padx = 10, pady =10)
      Button(f, text = "No", command=lambda *args: pan_tilt_ask("n")).pack(side = RIGHT, padx = 10, pady = 10)
      label.pack(pady = 10)
      f.pack()
      root.eval('tk::PlaceWindow . center')
      root.mainloop()

      if edit_pan_tilt == "y":
        root = Tk()
        root.title("COPIS Path Editor")
        Label(root, text = "Enter your pan and tilt values and press Submit").grid(row = 0, sticky= N)
        Label(root, text = "Pan").grid(row = 1, sticky = W)
        Label(root, text = "Tilt").grid(row = 2, sticky = W)
        p=Entry(root)
        t=Entry(root)
        p.grid(row = 1, column = 0)
        t.grid(row = 2, column = 0)
        Button(root, text = "Submit", command=lambda *args: getPT()).grid(row = 5, column = 0)
        root.eval('tk::PlaceWindow . center')
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
      root.title("COPIS Path Editor")
      Label(root, text = "How many sections would you like to adjust?").grid(row = 0, sticky= N)
      Label(root, text = "Number of Sections").grid(row = 1, sticky = W)
      sections=Entry(root)
      sections.grid(row = 1, column = 0)
      Button(root, text = "Submit", command=lambda *args: getSections()).grid(row = 2, column = 0)
      root.eval('tk::PlaceWindow . center')
      root.mainloop()

      series_dct = {}

      for i in range(0,series_num):

            series_dct[i] = []

            root = Tk()
            root.title("COPIS Path Editor")
            Label(root, text = ("Enter the starting and ending poses for Section %s" % str(i+1))).grid(row = 0, sticky= N)
            Label(root, text = "Start").grid(row = 1, sticky = W)
            Label(root, text = "End").grid(row = 2, sticky = W)
            st=Entry(root)
            en=Entry(root)
            st.grid(row = 1, column = 0)
            en.grid(row = 2, column = 0)
            Button(root, text = "Submit", command=lambda *args: getStartEnd()).grid(row = 5, column = 0)
            root.eval('tk::PlaceWindow . center')
            root.mainloop()

            for p in range(start, end+1):
                series_dct[i].append(p)

      root = Tk()
      root.title("COPIS Path Editor")
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
      root.eval('tk::PlaceWindow . center')
      root.mainloop()

      root = Tk()
      root.title("COPIS Path Editor")
      f= Frame(root)
      label = Label(root, text = "Do you wish to fix pan and tilt?")
      Button(f, text = "Yes", command=lambda *args: pan_tilt_ask("y")).pack(side = LEFT, padx = 10, pady =10)
      Button(f, text = "No", command=lambda *args: pan_tilt_ask("n")).pack(side = RIGHT, padx = 10, pady = 10)
      label.pack(pady = 10)
      f.pack()
      root.eval('tk::PlaceWindow . center')
      root.mainloop()

      if edit_pan_tilt == "y":
        root = Tk()
        root.title("COPIS Path Editor")
        Label(root, text = "Enter your pan and tilt values and press Submit").grid(row = 0, sticky= N)
        Label(root, text = "Pan").grid(row = 1, sticky = W)
        Label(root, text = "Tilt").grid(row = 2, sticky = W)
        p=Entry(root)
        t=Entry(root)
        p.grid(row = 1, column = 0)
        t.grid(row = 2, column = 0)
        Button(root, text = "Submit", command=lambda *args: getPT()).grid(row = 5, column = 0)
        root.eval('tk::PlaceWindow . center')
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
    root.title("COPIS Path Editor")
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
    root.eval('tk::PlaceWindow . center')
    root.mainloop()

    root = Tk()
    root.title("COPIS Path Editor")
    f= Frame(root)
    label = Label(root, text = "Would you like to fix pan and tilt?")
    Button(f, text = "Yes", command=lambda *args: pan_tilt_ask("y")).pack(side = LEFT, padx = 10, pady =10)
    Button(f, text = "No", command=lambda *args: pan_tilt_ask("n")).pack(side = RIGHT, padx = 10, pady = 10)
    label.pack(pady = 10)
    f.pack()
    root.eval('tk::PlaceWindow . center')
    root.mainloop()

    if edit_pan_tilt == "y":
      root = Tk()
      root.title("COPIS Path Editor")
      Label(root, text = "Enter your pan and tilt values and press Submit").grid(row = 0, sticky= N)
      Label(root, text = "Pan").grid(row = 1, sticky = W)
      Label(root, text = "Tilt").grid(row = 2, sticky = W)
      p=Entry(root)
      t=Entry(root)
      p.grid(row = 1, column = 0)
      t.grid(row = 2, column = 0)
      Button(root, text = "Submit", command=lambda *args: getPT()).grid(row = 5, column = 0)
      root.eval('tk::PlaceWindow . center')
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
  root.title("COPIS Path Editor")
  Label(root, text = "Enter 'NewFilename' or leave blank to generate automatically").grid(row = 0, sticky= N)
  Label(root, text = "Filename").grid(row = 1, sticky = W)
  file=Entry(root)
  file.grid(row = 1, column = 0)
  Button(root, text = "Submit and Save", command=lambda *args: getFilename()).grid(row = 2, column = 0)
  root.eval('tk::PlaceWindow . center')
  root.mainloop()

  #automatic file naming  
  if name == "":
      new_filename = filename[:len(filename)-6] + "_edited" + ".cproj"
      print(new_filename)

      with open(new_filename, 'w') as convert_file:
        convert_file.write(json.dumps(path))

  #setting user inputed filename
  else:
    
    new_filename = filename.rsplit("/", 1)[0] + "/" + name + ".cproj"
    with open(new_filename, 'w') as convert_file:
      convert_file.write(json.dumps(path))


#COMBINING PATHS
elif edit_or_combine_test == "b":

  root = Tk()
  root.title("COPIS Path Editor")
  root.attributes('-topmost',True)
  f=Frame(root)
  label = Label(root, text = "How many paths would you like to combine? All settings besides \n poses (proxies, profiles  etc.) will be taken from the first path chosen").pack(side = TOP, pady = 5)
  path_num = Entry(root)
  path_num.pack(pady = 5)
  Button(root, text = "Submit", command=lambda *args: getPaths()).pack(side = BOTTOM, pady = 5)
  root.eval('tk::PlaceWindow . center')
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
        root = Tk()
        root.title("COPIS Path Editor")
        root.attributes('-topmost',True)
        label = Label(text = "Sorry, that file is not a COPIS path, please choose another file").pack(side = TOP, pady = 10)
        Button(root, text = "Try again", command=Close).pack(side = BOTTOM, pady = 10)
        root.eval('tk::PlaceWindow . center')
        root.mainloop()

        root = Tk()
        root.withdraw()
        filename = askopenfilename()
        root.destroy()
        
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
  root.title("COPIS Path Editor")
  root.eval('tk::PlaceWindow . center')
  root.attributes('-topmost',True)
  Label(root, text = "Enter 'NewFilename' or leave blank to generate automatically").grid(row = 0, sticky= N)
  Label(root, text = "Filename").grid(row = 1, sticky = W)
  file=Entry(root)
  file.grid(row = 1, column = 0)
  Button(root, text = "Submit and Save", command=lambda *args: getFilename()).grid(row = 2, column = 0)
  root.mainloop()

  for i in range(len(paths)):
    for j in range(len(paths[i]['imaging_path'])):

      combined_path['imaging_path'].append(paths[i]['imaging_path'][j])

  if name == "":
    new_filename = path1name[:len(path1name)-6] + "_combined" + ".cproj"
    print(new_filename)

    with open(new_filename, 'w') as convert_file:
      convert_file.write(json.dumps(combined_path))

  else:
    new_filename = path1name.rsplit("/", 1)[0] + "/" + name + ".cproj"
    print(new_filename)
    with open(new_filename, 'w') as convert_file:
      convert_file.write(json.dumps(combined_path))
      print(new_filename)


else:
  
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

  inverted_path = {"imaging_path" : [] , "profile": {}, "proxies":{}}

  inverted_path['profile'] = path['profile']
  inverted_path['proxies'] = path['proxies']

  #getting filename settings
  root = Tk()
  root.title("COPIS Path Editor")
  Label(root, text = "Enter 'NewFilename' or leave blank to generate automatically").grid(row = 0, sticky= N)
  Label(root, text = "Filename").grid(row = 1, sticky = W)
  file=Entry(root)
  file.grid(row = 1, column = 0)
  Button(root, text = "Submit and Save", command=lambda *args: getFilename()).grid(row = 2, column = 0)
  root.eval('tk::PlaceWindow . center')
  root.mainloop()

  #inverting the path
  for i in range(0,poses): 
    cams = len(path['imaging_path'][i])
    for j in range(0,cams):

      inverted_path['imaging_path'].append(path['imaging_path'][i][j])

      if path['imaging_path'][i][j][0]['device'] == 0:
        path['imaging_path'][i][j][0]['device'] = 3
        path['imaging_path'][i][j][1][0]['device'] = 3

      elif path['imaging_path'][i][j][0]['device'] == 1:
        path['imaging_path'][i][j][0]['device'] = 4
        path['imaging_path'][i][j][1][0]['device'] = 4
      
      elif path['imaging_path'][i][j][0]['device'] == 2:
        path['imaging_path'][i][j][0]['device'] = 5
        path['imaging_path'][i][j][1][0]['device'] = 5
      
      elif path['imaging_path'][i][j][0]['device'] == 3:
        path['imaging_path'][i][j][0]['device'] = 0
        path['imaging_path'][i][j][1][0]['device'] = 0
      
      elif path['imaging_path'][i][j][0]['device'] == 4:
        path['imaging_path'][i][j][0]['device'] = 1 
        path['imaging_path'][i][j][1][0]['device'] = 1 
      
      else:
        path['imaging_path'][i][j][0]['device'] = 2 
        path['imaging_path'][i][j][1][0]['device'] = 2

      inverted_z = -1 * float(path['imaging_path'][i][j][0]['args'][2][1])
      path['imaging_path'][i][j][0]['args'][2][1] = str(inverted_z)

      inverted_path['imaging_path'].append(path['imaging_path'][i][j])

  #automatic file naming  
  if name == "":
      new_filename = filename[:len(filename)-6] + "_inverted" + ".cproj"
      print(new_filename)

      with open(new_filename, 'w') as convert_file:
        convert_file.write(json.dumps(inverted_path))

  #setting user inputed filename
  else:
    new_filename = filename.rsplit("/", 1)[0] + "/" + name + ".cproj"
    with open(new_filename, 'w') as convert_file:
      convert_file.write(json.dumps(inverted_path))