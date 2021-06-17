#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 12:15:49 2021

@author: antton
"""

from fpdf import FPDF
import os, sys

if len(sys.argv) != 4:
    raise ValueError('Wrong input. Expected usage: collectPDF_antton.py input_folder_path output_folder_path sample_number')

input_folder_name = sys.argv[1]  #Where to take the images from (parent folder)
output_folder_name = sys.argv[2]
input_sample_name = sys.argv[3]  #NUMBER ONLY!

general_path = "/home/antton/TFM/output/"+input_folder_name

folder_list = [general_path+"/01-Viable",
    general_path+"/02-Singlet",
    general_path+"/03-PBMCs",
    general_path+"/04-CD45high",        
    general_path+"/05-CD45posCD34pos",
    general_path+"/06-CD3negBACKGATE",
    general_path+"/07-CD4posBACKGATE",
    general_path+"/08-CD19negBACKGATE",       
    general_path+"/09-CD14negBACKGATE",
    
    general_path+"/10-CD16CD56/10A-CD16neg_56negBACKGATE",
    general_path+"/10-CD16CD56/10B-CD16pospos_56posposBACKGATE",
    general_path+"/10-CD16CD56/10C-CD16neg_56posposBACKGATE",
 
    general_path+"/11-LinnegCD34pos",   
    general_path+"/12-CD38neg",    
    general_path+"/13-HSC_MLP_MPP",
    general_path+"/14-B_NK",
    general_path+"/15-CD10pos(MLP)",
    general_path+"/16-CMP_GMP_MEP"]



datePlate_sampleName_list = []  # List filled with '190819 CB-B7 715' format sample info
for image_file in os.listdir("/home/antton/TFM/output/"+input_folder_name+"/01-Viable"):
    datePlate_sampleName_list.append('-'.join(image_file.split('-')[:2]))

for datePlate_sampleName in datePlate_sampleName_list:
    single_sample_image_list = []
    sample_id = datePlate_sampleName.split('-')[1][3:]
    if input_sample_name == sample_id:
        print('Sample selected: ', datePlate_sampleName)
        for folder in folder_list:
            gateName = folder.split('-')[-1]
            filename = datePlate_sampleName + '-' + gateName + '.jpeg'
            single_sample_image_list.append(folder+'/'+filename)
    
        pdf = FPDF()
        pdf.set_font('Arial','',18)
        # imagelist is the list with all image filenames
        for image in single_sample_image_list:
            if os.path.exists(image):
                pdf.add_page()
                sample_name = image.split('/')[-1]
                pdf.write(5,sample_name)
                pdf.image(image,x=10,y=25)
        pdf.output(output_folder_name+'/'+datePlate_sampleName.split("-")[-1]+".pdf", "F")
