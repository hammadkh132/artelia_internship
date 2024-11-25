# -*- coding: utf-8 -*-
"""
Created on Thu May 23 15:51:37 2024

@author: hammad.khalid
"""

# Functionality
### Main functionality of this script is to calculate Bed Relief Index (BRI), a tool used for gauging the transverse slope change due to morpogological evolution, based on a polline.


# =============================================================================
# Baic Steps For creating BRI 
# 1. Adding Path to the file & Reading the file
# 2. Reading the polyline
# 3. Extracting the value from polyline
## There are many Sub-scripts so uncomment what you want to use.
# =============================================================================

# =============================================================================
# Detailed steps
# 1. Uncomment the path to the cases (If multiple cases you can add multiple maths) and makesure to replicate the name of path variables in the File variable defined after
# 2. Uncomment the polyline path (The code doesnt allow computation for multiple polylines at the same time)
# 3. Extracting the value of water surface, bed and discretization points based on discretization from polyline (For single record/single time step)
# 4.1 & 4.2 Calculating BRI and Active BRI (For single record/single time step)
# 5.1 & 5.2 Calculating BRI and Active BRI (For all timesteps)
# 6. Plotting BRI and Active BRI for a single simulation together.

# =============================================================================


from os import path
import matplotlib.pyplot as plt
import numpy as np
from data_manip.extraction.telemac_file import TelemacFile
# from postel.parser_output import get_latest_output_files, OutputFileData
# from postel.plot_actions import plot_vertical_slice
from postel.plot1d import plot1d


# # =============================================================================
# # 1. Adding Path to the file 
# # =============================================================================
# GAIRES_CASE1 = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN5_V8P5R0" , "GAIARES7000.slf")
# GAIRES_CASE2 = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN7_V8P5R0_Apslay" , "GAIARES1000.slf")
# GAIRES_CASE3 = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN8_V8P5R0_Apslay" , "GAIARES1000.slf")
# GAIRES_CASE4 = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN9_V8P5R0_Apslay" , "GAIARES1000.slf")
# GAIRES_CASE5 = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN10_V8P5R0_Apslay" ,"GAIARES1000.slf")
GAIRES_CASE6 = path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "RUN8mas2_V8P5R0_Apslay" , "GAIARES1000.slf")


### It allows you multiple functionality of either working for a single case at a time or plotting multiple cases at the same time.
Files = [#GAIRES_CASE1,
          #GAIRES_CASE2,
          #GAIRES_CASE3,
          #GAIRES_CASE4,
          #GAIRES_CASE5
          GAIRES_CASE6
          ]


# # # # #=============================================================================
# # ## 2. reading the  polyline file (makesure to chnage the RUN#)
# # # # # =============================================================================
Polyline_path =  path.join("Z:\\" , "02_RD_lancey" , "01_Calcul" , "Essai_7_hammad" , "X-section_files" , "") 
 
### Selecting the polyline (if there are multiple polylines)
#Input_polyline = np.genfromtxt(Polyline_path + 'xsection_polyline.i2s', delimiter=' ', usecols = (0, 1), skip_header=16)
#Input_polyline = np.genfromtxt(Polyline_path + 'xsection2.i2s', delimiter=' ', usecols = (0, 1), skip_header=16)
Input_polyline = np.genfromtxt(Polyline_path + 'xsection3.i2s', delimiter=' ', usecols = (0, 1), skip_header=16)

# # =============================================================================
# #  3. Extracting the value of free surface from polyline for a single record
# # 5000 is the values of discretization points and can be modified if wanted
# # =============================================================================
GAIRES = TelemacFile(GAIRES_CASE1)
record = 3
points_rb, distance_rb, values_RigidBed = GAIRES.get_data_on_polyline("RIGID BED", record , Input_polyline, [5000])
points_bottom, distance_bottom, values_bottom = GAIRES.get_data_on_polyline("BOTTOM", record , Input_polyline, [5000])
points_freeSurface, distance_freeSurface, values_freeSurface = GAIRES.get_data_on_polyline("ZS CLIPPED", record , Input_polyline,[5000])

# =============================================================================
##  4. Creating BRI For a single record/Time step
# =============================================================================

width  = abs(distance_rb[0]-distance_rb[-1])

# loop on Z and X values

Sum = 0
for i in range(len(values_bottom) - 1):
    print(i)
    zi_square = values_bottom[i]**2 
    zi_successive = values_bottom[i+1]**2
    z_mean_sqrt = np.sqrt((zi_square+zi_successive)/2)
    xi = distance_rb[i] 
    xi_successive = distance_rb[i+1]
    diff_x = abs(xi_successive-xi)
    prod = (z_mean_sqrt)*(diff_x)
    Sum =  Sum + prod
    print(Sum)         
BRI = Sum/width
print(BRI)


# =============================================================================
##  4. Creating Active_BRI For a single record/Time step
# =============================================================================

width  = abs(distance_rb[0]-distance_rb[-1])
Z_mean = np.average(values_bottom)

# # loop on Z and X values
       
Active_sum = 0
dh = 0.01

for j in range(len(values_bottom) - 1):
    if abs((values_bottom[j]-values_freeSurface[j])) > dh and abs((values_bottom[j+1]-values_freeSurface[j+1])) > dh:
        zi_square_Z = (values_bottom[j]-Z_mean)**2 
        zi_successive_Z = (values_bottom[j+1]-Z_mean)**2
        z_mean_sqrt = np.sqrt((zi_square_Z+zi_successive_Z)/2)
        xi = distance_rb[j] 
        xi_successive = distance_rb[j+1]
        diff_x = abs(xi_successive-xi)
        prod = (z_mean_sqrt)*(diff_x)
        Active_sum =  Active_sum + prod
        print(Active_sum)
Active_BRI = Active_sum/width   

for i in range(len(values_bottom) - 1):
    #print(i)
    dhi = abs(values_bottom[i]-values_freeSurface[i])
    dhiplus1 =abs(values_bottom[i+1]-values_freeSurface[i+1])
    print(dhi)
    print(dhiplus1)


# =============================================================================
# Comparision of All simulations
#  5.1 Creating BRI for all the time series for all the cases together  (Correct)
# By cases here means simulations, let say I had 6 test cases as defined by the list named as Files above
# 5000 is the values of discreytization points and can be modified if want
# =============================================================================
BRI_list = []

for file in Files:
    
    GAIRES = TelemacFile(file)
        
    BRI_db = []
    
    for n in GAIRES.times:
        print(n)
        rec = GAIRES.get_closest_record(n)
        points_rb, distance_rb, values_RigidBed = GAIRES.get_data_on_polyline("RIGID BED", rec , Input_polyline, [5000])
        points_bottom, distance_bottom, values_bottom = GAIRES.get_data_on_polyline("BOTTOM", rec , Input_polyline, [5000])
        points_freeSurface, distance_freeSurface, values_freeSurface = GAIRES.get_data_on_polyline("ZS CLIPPED", rec , Input_polyline,[5000])

        width  = abs(distance_rb[0]-distance_rb[-1])
        Z_mean = np.average(values_bottom)
       
        Sum = 0
    
        for i in range(len(values_bottom) - 1):
            print(i)
            zi_square = (values_bottom[i]-Z_mean)**2 
            zi_successive = (values_bottom[i+1]-Z_mean)**2
            z_mean_sqrt = np.sqrt((zi_square+zi_successive)/2)
            xi = distance_rb[i] 
            xi_successive = distance_rb[i+1]
            diff_x = abs(xi_successive-xi)
            prod = (z_mean_sqrt)*(diff_x)
            Sum =  Sum + prod
            BRI = Sum/width
        BRI_db = np.append(BRI_db, BRI)
    BRI_list.append(BRI_db)

colors = ['blue', 'green', 'red', 'yellow', 'black']
label = ['Case 1','Case 2','Case 3', 'Case 4', 'Case 5']
 
fig, ax = plt.subplots(figsize = (7,4))         
for index, j in enumerate(BRI_list): 
    plot1d(ax, GAIRES.times, j, 
            x_label='Time',
            y_label='BRI',
            plot_label= label [index % len(label)],
            linewidth=1,
            color = colors [index % len(colors)]
            )
 
legend = ax.legend(loc='lower left' , shadow=True)    


# =============================================================================
# Comparision of All simulations
#   5.2 Creating Active BRI for all the time series for all the cases together (Correct)
# 5000 is the values of discreytization points and can be modified if want
# =============================================================================
Active_BRI_list = []

for file in Files:
    
    GAIRES = TelemacFile(file)
        
    Active_BRI_db = []
    
    for n in GAIRES.times:
        print(n)
        rec = GAIRES.get_closest_record(n)
        points_rb, distance_rb, values_RigidBed = GAIRES.get_data_on_polyline("RIGID BED", rec , Input_polyline, [5000])
        points_bottom, distance_bottom, values_bottom = GAIRES.get_data_on_polyline("BOTTOM", rec , Input_polyline, [5000])
        points_freeSurface, distance_freeSurface, values_freeSurface = GAIRES.get_data_on_polyline("ZS CLIPPED", rec , Input_polyline,[5000])

        width  = abs(distance_rb[0]-distance_rb[-1])
        Z_mean = np.average(values_bottom)
       
        Active_sum = 0
        dh = 0.002
    
        for i in range(len(values_bottom) - 1):
            #print(i)
            #dhi = (values_bottom[i]-values_freeSurface[i])
            #dhiplus1 =(values_bottom[i+1]-values_freeSurface[i+1])
            if abs((values_bottom[i]-values_freeSurface[i])) > dh and abs((values_bottom[i+1]-values_freeSurface[i+1])) > dh:
                zi_square_Z = (values_bottom[i]-Z_mean)**2 
                zi_successive_Z = (values_bottom[i+1]-Z_mean)**2
                z_mean_sqrt = np.sqrt((zi_square_Z+zi_successive_Z )/2)
                xi = distance_rb[i] 
                xi_successive = distance_rb[i+1]
                diff_x = abs(xi_successive-xi)
                prod = (z_mean_sqrt)*(diff_x)
                Active_sum =  Active_sum + prod
                Active_BRI = Active_sum/width
        Active_BRI_db = np.append(Active_BRI_db, Active_BRI)
    Active_BRI_list.append(Active_BRI_db)
                
colors = ['blue', 'green', 'red', 'yellow', 'black']
label = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5']

fig, ax = plt.subplots(figsize = (7,4))         
for index, j in enumerate(Active_BRI_list): 
    plot1d(ax, GAIRES.times, j, 
            x_label='Time',
            y_label='Active BRI',
            linewidth=1,
            plot_label= label [index % len(label)],
            color = colors [index % len(colors)]
            )
 
legend = ax.legend(loc='upper right', shadow=True) 

for i in range(len(values_bottom) - 1):
    #print(i)
    dhi = (values_bottom[i]-values_freeSurface[i])
    dhiplus1 =(values_bottom[i+1]-values_freeSurface[i+1])
    print(dhi)
    print(dhiplus1)

 #=============================================================================
 #  6. CREATING AND PLOTTING BRI AND ACTIVE BRI FOR INDIVIDUAL CASE ONE GRAPH
 # 5000 is the values of discretization points and can be modified if wanted
 # =============================================================================   
BRI_list = []
Active_BRI_list = []

#colors = ['blue','red', 'yellow', 'black']
#label = ['Case 1','Case 2','Case 3','Case 4','Case 5']

for idx, file in enumerate(Files):
    print(idx)
    print(file)
  
    GAIRES = TelemacFile(file)
      
    BRI_db = []
    Active_BRI_db = []
    dh = 0.002
  
    for n in GAIRES.times:
        print(n)
        rec = GAIRES.get_closest_record(n)
        points_rb, distance_rb, values_RigidBed = GAIRES.get_data_on_polyline("RIGID BED", rec , Input_polyline, [5000])
        points_bottom, distance_bottom, values_bottom = GAIRES.get_data_on_polyline("BOTTOM", rec , Input_polyline, [5000])
        points_freeSurface, distance_freeSurface, values_freeSurface = GAIRES.get_data_on_polyline("ZS CLIPPED", rec , Input_polyline,[5000])

        width  = abs(distance_rb[0]-distance_rb[-1])
        Z_mean = np.average(values_bottom)
     
        Sum = 0
        Active_sum = 0
  
        for i in range(len(values_bottom) - 1):
            #print(i)
            zi_square = (values_bottom[i]-Z_mean)**2 
            zi_successive = (values_bottom[i+1]-Z_mean)**2
            z_mean_sqrt = np.sqrt((zi_square+zi_successive)/2)
            xi = distance_rb[i] 
            xi_successive = distance_rb[i+1]
            diff_x = abs(xi_successive-xi)
            prod = (z_mean_sqrt)*(diff_x)
            Sum =  Sum + prod
            BRI = Sum/width
        BRI_db = np.append(BRI_db, BRI)
        
             
        for j in range(len(values_bottom) - 1):
            #print(j)
            if abs((values_bottom[j]-values_freeSurface[j])) > dh and abs((values_bottom[j+1]-values_freeSurface[j+1])) > dh:
                zi_square_Z = (values_bottom[j]-Z_mean)**2 
                zi_successive_Z = (values_bottom[j+1]-Z_mean)**2
                z_mean_sqrt = np.sqrt((zi_square_Z+zi_successive_Z )/2)
                xi = distance_rb[j] 
                xi_successive = distance_rb[j+1]
                diff_x = abs(xi_successive-xi)
                prod = (z_mean_sqrt)*(diff_x)
                Active_sum = Active_sum + prod
                Active_BRI = Active_sum/width
        Active_BRI_db = np.append(Active_BRI_db, Active_BRI)
    BRI_list.append(BRI_db) 
    Active_BRI_list.append(Active_BRI_db)
    
  
    fig, ax = plt.subplots(figsize = (6,4)) 
    ax.plot(GAIRES.times,BRI_list[idx], label = "BRI", 
            color='orange', linewidth = 1) 
    ax.plot(GAIRES.times,Active_BRI_list[idx], label = "Active BRI", 
            color='blue', linestyle='dashed')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('BRI & ACTIVE BRI (m)')
    #for idx, file in enumerate(file):
    #ax.set_title('%s' % label[idx])
    legend = ax.legend(loc='upper right', shadow=True) 










  