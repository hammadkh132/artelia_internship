# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:18:16 2024

@author: hammad.khalid
"""

#### Functionality
## It takes the frames from the Telemac2D files (Selafin) and combines them into a video output.

# =============================================================================
# Instruction on Running the file
 # 1. Change the path for reading the file 
 # 2. Change the name of the variable for which you want to create the video
 # 3. Create output directory for storing the frame
 # 4. Storing the output directory path to a variable
 # 5. Code block for extracting frames from the listing file
 # 6. COMBINING OF FRAMES INTO A VIDEO
 # The steps 5 and 6 has been repeated twice, once for output from the hydrodynamic file and the other time for output from hydrosedimentary listing file
# =============================================================================



from os import path, environ, makedirs, listdir
from data_manip.extraction.telemac_file import TelemacFile
from postel.parser_output import get_latest_output_files, OutputFileData
from postel.plot_vnv import  vnv_plot2d
from postel.plot2d import *
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from postel.deco_default import decoDefault
import numpy as np
import plot
#import moviepy.video.io.ImageSequenceClip
#import imageio as img


#=============================================================================
    # 1.reading the file  GAIRESFILE (GAIA sediment transport output)
# =============================================================================
GAIRES_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN10_V8P5R0_Apslay" , "GAIARES1000.slf")
GAIRES = TelemacFile(GAIRES_path)
print(GAIRES)

#=============================================================================
    #1. reading the  T2D file (Telemac2D hydrodynamic outut)
# =============================================================================
T2D_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN10_V8P5R0_Apslay" , "lancey_coupled.slf")
T2D = TelemacFile(T2D_path)
print(T2D)

#=============================================================================
   #printing of image on 1 timeframe
# =============================================================================
#print(file.times)

#This piece of code is OK
# for i in file.times:
#       plot.plot_var(file, var='CUMUL BED EVOL', time= i)

#=============================================================================
   ### For printing the var (For identifying the output from the simulation files) Optional
# =============================================================================
# var_GAIRES = GAIRES.varnames
# var_T2D = T2D.varnames

#=============================================================================
   ### 2. variable name (Input the name of the variables fo which you want to extract the data)
# =============================================================================
var_GAIRES_name = 'CUMUL BED EVOL'
var_T2D_name = "HAUTEUR D'EAU"

#=============================================================================
# 3.Making new directory for image output frame by frame
#=============================================================================
import os
var_GAIRES_Path = 'Z://02_RD_lancey/01_Calcul/Essai_7_hammad/RUN10_V8P5R0_Apslay/output/'f'{var_GAIRES_name}'
if not os.path.exists(var_GAIRES_Path):
  os.mkdir(var_GAIRES_Path)
  print("Folder %s created!" % var_GAIRES_Path)
else:
  print("Folder %s already exists" % var_GAIRES_Path)

var_T2D_Path = 'Z://02_RD_lancey/01_Calcul/Essai_7_hammad/RUN10_V8P5R0_Apslay/output/'f'{var_T2D_name}'
if not os.path.exists(var_T2D_Path):
  os.mkdir(var_T2D_Path)
  print("Folder %s created!" % var_T2D_Path)
else:
  print("Folder %s already exists" % var_T2D_Path)

            
#=============================================================================
# 4. creating an output directory for saving the frames
#=============================================================================
output_GAIRES_dir = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN10_V8P5R0_Apslay", "output", f'{var_GAIRES_name}')
output_T2D_dir = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN10_V8P5R0_Apslay" , "output", f'{var_T2D_name}')
            
##### #=============================================================================
  #testing Output visualization Record 100 is at time 5000 (For just verifying the direct output in python)
# =============================================================================
# test_var_data = file.get_data_value(var_name, record=140)


# fig, ax = plt.subplots(1, 1, figsize=(10, 7),)
# ax.set_title('Lancey, result at time: %d s'% file.times[140])
# ax.set_aspect('equal')
# plot2d_scalar_map(fig, ax, file.tri, test_var_data, x_label= 'X(M)', y_label= 'Y(M)', data_name= var_name)
# outputimage = print('At time :%d' % file.times[140])
# plt.savefig(os.path.join(output_dir, str(outputimage)))

#print('At time :%d' % file.times[140]))

#################################################################################################################

#### =============================================================================
  # 5. ORIGINAL CODE FOR ALL THE FRAMES (GAIRES)
#### =============================================================================
iframe1  = 0
for i in GAIRES.times:
    rec1 = GAIRES.get_closest_record(i)
    var_data1 = GAIRES.get_data_value(var_GAIRES_name, rec1)
#    print(var_data)
    
    fig1, ax1 = plt.subplots(1, 1, figsize=(10, 7))
    ax1.set_title('Lancey at time: %d s'% GAIRES.times[int(rec1)])
    ax1.set_aspect('equal')
    plot2d_scalar_map(fig1, ax1, GAIRES.tri, var_data1, x_label= 'X(M)', y_label= 'Y(M)', data_name= var_GAIRES_name, nv=10)
#   iframe = file.times[rec]
    iframe1 = iframe1 + 1
    filename1 = f'{iframe1:.0f}.png'
    plt.savefig(os.path.join(output_GAIRES_dir, filename1))
    plt.close()

# ##### =============================================================================
#   # 6. COMBINING OF FRAMES INTO A VIDEO
# ##### =============================================================================

import moviepy.video.io.ImageSequenceClip
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

fps=5

import re
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
    
image_files1 = [os.path.join(output_GAIRES_dir,img)
                for img in sorted_alphanumeric(os.listdir(output_GAIRES_dir))
                if img.endswith(".png")]
#print(image_files)
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files1, fps=fps)
output_video_GAIRES = 'Z://02_RD_lancey/01_Calcul/Essai_7_hammad/RUN10_V8P5R0_Apslay/video/'
clip.write_videofile(output_video_GAIRES + f'{var_GAIRES_name}.mp4')



#########################################################################################################

#### =============================================================================
#### ORIGINAL CODE FOR ALL THE FRAMES (T2D)  repeating the same code for T2D
#### =============================================================================
iframe2  = 0
for i in T2D.times:
    rec2 = T2D.get_closest_record(i)
    var_data2 = T2D.get_data_value(var_T2D_name, rec2)
#    print(var_data)
    
    fig2, ax2 = plt.subplots(1, 1, figsize=(10, 7))
    ax2.set_title('Lancey at time: %d s'% T2D.times[int(rec2)])
    ax2.set_aspect('equal')
    plot2d_scalar_map(fig2, ax2, T2D.tri, var_data2, x_label= 'X(M)', y_label= 'Y(M)', data_name= var_T2D_name, nv=10)
#   iframe = file.times[rec]
    iframe2 = iframe2 + 1
    filename2 = f'{iframe2:.0f}.png'
    plt.savefig(os.path.join(output_T2D_dir, filename2))
    plt.close()

##### =============================================================================
  #COMBINING OF FRAMES INTO A VIDEO
##### =============================================================================

import moviepy.video.io.ImageSequenceClip
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

fps=5

import re
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

image_files2 = [os.path.join(output_T2D_dir,img)
                for img in sorted_alphanumeric(os.listdir(output_T2D_dir))
                if img.endswith(".png")]
#print(image_files)
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files2, fps=fps)
output_video_T2D = 'Z://02_RD_lancey/01_Calcul/Essai_7_hammad/RUN10_V8P5R0_Apslay/video/'
clip.write_videofile(output_video_T2D + f'{var_T2D_name}.mp4')

###########################################################################################################



    

    
    





