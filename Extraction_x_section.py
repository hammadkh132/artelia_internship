# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:56:17 2024

@author: hammad.khalid
"""

### Functionality
## The script creates cross sectional profiles for visualizing the outputs from Telemac2D simulations
## It plots the bed evolution for all the frames which could be used for visualizing the temporal evolution at 1 cross section
## For spatial evolution, we can input multiple of polylines which are also integrated into the script.

#Instruction for usage
#1. Follow the comments where the input is written give that input

#Instruction for extracting the experimental bed evolution
# 1. uncomment the section you want to extract
# 2. uncomment the polyline corresponding to the section
# 3. change the data frame name on line 132


from os import path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from data_manip.extraction.telemac_file import TelemacFile
from data_manip.extraction.parser_selafin import get_value_polyline
# from postel.parser_output import get_latest_output_files, OutputFileData
# from postel.plot_actions import plot_vertical_slice
from postel.plot_vnv import  vnv_plot2d
from postel.plot2d import *
from postel.plot1d import plot1d
import plot
from mpl_toolkits.mplot3d import Axes3D
from postel.plot3d import plot3d_scalar_map
import pandas as pd

# # #=============================================================================
# #     #reading the  CSV File for plotting x_section from DEM for section 1,2,3 (makesure to chnage the RUN#) 
##    This is an input
# # # =============================================================================
# csv_dem_section1 = pd.read_csv("C:/Users/hammad.khalid/Telemac_practice/Lancey/Experimental/Profiles/Essai7/FinalDTM/xsection1_zvalues_DEM_At7000s.csv", sep=";")
# x_section1_dem = np.array("csv_dem_section1")
# csv_dem_section2 = pd.read_csv("C:/Users/hammad.khalid/Telemac_practice/Lancey/Experimental/Profiles/Essai7/FinalDTM/xsection2_zvalues_DEM_At7000s.csv", sep=";")
# x_section2_dem = np.array("csv_dem_section2")
# csv_dem_section3 = pd.read_csv("C:/Users/hammad.khalid/Telemac_practice/Lancey/Experimental/Profiles/Essai7/FinalDTM/xsection3_zvalues_DEM_At7000s.csv", sep=";")
# x_section3_dem = np.array("csv_dem_section3")

# # #=============================================================================
# #     #reading the  GAIRESFILE (makesure to change the RUN#, Run# represents different simulations 
##    This is an input
# # # =============================================================================
#GAIRES_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN5_V8P5R0" , "GAIARES7000.slf")
#GAIRES_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN7_V8P5R0_Apslay" , "GAIARES1000.slf")
#GAIRES_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN8_V8P5R0_Apslay" , "GAIARES1000.slf")
#GAIRES_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN9_V8P5R0_Apslay_25Deg" , "GAIARES_Apsleyl_25Deg.slf")
#GAIRES_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN10_V8P5R0_Apslay" ,"GAIARES1000.slf")
#GAIRES_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN10_V8P5R0_Apslay_30Deg" , "GAIARES_Apsley_30Deg.slf")
#GAIRES_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN8mas2_V8P5R0_Apslay" , "GAIARES1000.slf")
#GAIRES_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN11_V8P5R0_Apslay_40Deg" , "GAIARES_Apsley_40Deg.slf")
#GAIRES_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN12_V8P5R0_Talmon_B2_1.6" , "GAIARES_Talmon_B2_1.6")
#GAIRES_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN15_V8P5R0_Talmon_B2_0.7" , "GAIARES_Talmon_B2_0.7")
GAIRES_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN5mas2_V8P5R0" , "GAIARES7000.slf") # this is Talmon B2 = 0.85



# #=============================================================================
#     #reading the  T2D file (makesure to change the RUN#) # Use this when  needed (T2D files are output of Telemac2D- hydrodynamic files)
# # =============================================================================
# T2D_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN5_V8P5R0" , "lancey_coupled.slf")
# #T2D_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN7_V8P5R0_Apslay" , "lancey_coupled.slf")
# #T2D_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN8_V8P5R0_Apslay" , "lancey_coupled.slf")
# #T2D_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN9_V8P5R0_Apslay" , "lancey_coupled.slf")
# #T2D_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN10_V8P5R0_Apslay", "lancey_coupled.slf")


# #creating telemac files
GAIRES = TelemacFile(GAIRES_path)
# #T2D = TelemacFile(T2D_path)


# # # #=============================================================================
# # #     #reading the  polyline file 
# # # # =============================================================================
Polyline_path =  path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "X-section_files" , "")  # Input
 

Input_polyline = np.genfromtxt(Polyline_path + 'xsection_polyline.i2s', delimiter=' ', usecols = (0, 1), skip_header=16) #Input
#Input_polyline = np.genfromtxt(Polyline_path + 'xsection2.i2s', delimiter=' ', usecols = (0, 1), skip_header=16) # Input
#Input_polyline = np.genfromtxt(Polyline_path + 'xsection3.i2s', delimiter=' ', usecols = (0, 1), skip_header=16) # Input

# # # #=============================================================================
# # #     # reading variable names (For identifying the output variables) (Optional)
# # # # =============================================================================
#var = T2D.varnames
GAIRES_var = GAIRES.varnames

# # # #=============================================================================
# # #    1.getting values on water surface, bed evolution(bottom) and rigidbed on polyline for single record (Uncomment To run)
# # # # =============================================================================
# optional arguments
GAIRES.get_closest_record()  input time
GAIRES.get_data_time() input record

record = 140   #Input record
points_rb, distance_rb, RigidBed = GAIRES.get_data_on_polyline("RIGID BED", record , Input_polyline, [5000]) #input the variables and points to discretize here it is 5000 points
polygone_discretized_points_bottom, abs_curv_bottom, zb_bottom = GAIRES.get_data_on_polyline("BOTTOM", record , Input_polyline, [5000]) #input the variables and points to discretize here it is 5000 points
polygone_discretized_points_zb, abs_curv_zb, zb = GAIRES.get_data_on_polyline("ZS CLIPPED", record , Input_polyline, [5000]) #input the variables and points to discretize here it is 5000 points

#### Code for plotting of 1 figure only
### List of var we what to display

data_list = [zb_bottom,zb]
fig, ax = plt.subplots(figsize = (10,7))

plot1d(ax, abs_curv_bottom, zb_bottom, 
      x_label='Distance',
      y_label='Elevation (m)',
      plot_label='Bottom',
      color='green', linestyle='dashed', linewidth=2)

plot1d(ax, abs_curv_zb, zb, 
      x_label='Distance',
      y_label='Elevation (m)',
      plot_label='Water Surface')

plot1d(ax, distance_rb, RigidBed, 
      x_label='Distance',
      y_label='Elevation (m)',
      plot_label='Rigid Bed',
      color='black', linestyle='solid', linewidth=1)
 
plot1d(ax, csv_dem_section3["Distance"] , csv_dem_section3["z_values"],
      x_label='Distance',
      y_label='Elevation (m)',
      plot_label='Experimental',
      color='orange', linestyle='solid', linewidth=2)

legend = ax.legend(loc='upper center', shadow=True)

plt.show()


#### for saving the plot make sure to change this when you chnage the working folder
output_path = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN5_V8P5R0" , "Pictures")

plt.savefig(output_path,'RUN5_V8P5R0')
plt.close()
            

# # # #=============================================================================
# # #    2. Applying loop to extract section at all timesteps and plotting of figures (Uncomment to run)
# # # # =============================================================================

RIGID BED _ rb  (It remains constant for all the frames)
points_rb, distance_rb, RigidBed = GAIRES.get_data_on_polyline("RIGID BED", 0 , Input_polyline, [5000])

for i in GAIRES.times:
    rec = GAIRES.get_closest_record(i)
    polygone_discretized_points, abs_curv, zb = GAIRES.get_data_on_polyline("ZS CLIPPED", rec , Input_polyline, [5000])
    polygone_discretized_points_bottom, abs_curv_bottom, zb_bottom = GAIRES.get_data_on_polyline("BOTTOM", rec , Input_polyline, [5000])
    
    fig, ax = plt.subplots()
    ax.set_title('Water Level at Time: %d s'% GAIRES.times[int(rec)])
    
    Line1 = plot1d(ax, abs_curv, zb_bottom, 
          x_label='Distance',
          y_label='Elevation (m)',
          plot_label='Bottom',
          color='green', linestyle='dashed', linewidth=2)
    
    plot1d(ax, abs_curv, zb, 
          x_label='Distance',
          y_label='Elevation  (m)',
          plot_label='Water Surface')
    
    plot1d(ax, distance_rb, RigidBed, 
          x_label='Distance',
          y_label='Elevation (m)',
          plot_label='Rigid Bed',
          color='black', linestyle='solid', linewidth=1)
    
    legend = ax.legend(loc='best', shadow=True)
    
    plt.show()










