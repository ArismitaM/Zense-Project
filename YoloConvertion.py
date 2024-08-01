# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:55:43 2015
This script is to convert the txt annotation files to appropriate format needed by YOLO 
@author: Guanghan Ning
Email: gnxr9@mail.missouri.edu

Code to convert boxed data to Yolo format. Takes the classes to be auto filled in.
"""

import pathlib
import os
import re
import sys
from os import walk, getcwd
from PIL import Image

classes = ["001"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
    
    
"""-------------------------------------------------------------------""" 

""" Configure Paths"""   
mypathPrefix ="Labels/" 
outpathPrefix = "LabelsYolov2/"

if (len(sys.argv) < 3):
    print('Usage: python Convert2Yolo.py imageDirName labelDirName classNumber [Mnist?]')
    sys.exit()

cls = sys.argv[1]
mypath = sys.argv[2]
nameOfClass = sys.argv[3]
pathComps = pathlib.Path(mypath)
labelPath = pathlib.Path(*pathComps.parts[1:]).as_posix()
print("LabelPath:", labelPath)

#mypath = mypathPrefix + labelPath + "/"
outpath = outpathPrefix + labelPath + "/"
print("OutPath;", outpath)


#if cls not in classes:
#   print("unknown class: " + cls)
#    exit(0)
#cls_id = classes.index(cls)
#print(cls_id)

if (len(sys.argv) == 5):
    cls_id = os.path.basename(labelPath)
else:
    cls_id = nameOfClass

print(cls_id)
print(outpath)

if not os.path.exists(outpath):
    os.makedirs(outpath)

wd = getcwd()
list_file = open('%s/%s_list.txt'%(wd, cls_id), 'w')

""" Get input text file list """
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    txt_name_list.extend(filenames)
    break
print(txt_name_list)

""" Process """
for txt_name in txt_name_list:
    # txt_file =  open("Labels/stop_sign/001.txt", "r")
    
    """ Open input text files """
    txt_path = mypath + txt_name
    print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    lines = txt_file.read().split('\r\n')   #for ubuntu, use "\r\n" instead of "\n"
    
    """ Open output text files """
    txt_outpath = outpath + txt_name
    print("Output:" + txt_outpath)
    txt_outfile = open(txt_outpath, "w")
    
    
    """ Convert the data to YOLO format """
    ct = 0
    for line in lines:
        #print('lenth of line is: ')
        #print(len(line))
        #print('\n')
        #
        img_path_JPEG = str('%s/%s/%s.JPEG'%(wd, cls, os.path.splitext(txt_name)[0]))
        img_path_JPG = str('%s/%s/%s.JPG'%(wd, cls, os.path.splitext(txt_name)[0]))
        img_path_PNG = str('%s/%s/%s.PNG'%(wd, cls, os.path.splitext(txt_name)[0]))
        img_path_jpeg = str('%s/%s/%s.jpeg'%(wd, cls, os.path.splitext(txt_name)[0]))
        img_path_jpg = str('%s/%s/%s.jpg'%(wd, cls, os.path.splitext(txt_name)[0]))
        img_path_png = str('%s/%s/%s.png'%(wd, cls, os.path.splitext(txt_name)[0]))
        img_path = ''
        if os.path.isfile(img_path_JPEG):
            img_path = img_path_JPEG
        if os.path.isfile(img_path_JPG):
            img_path = img_path_JPG
        if os.path.isfile(img_path_PNG):
            img_path = img_path_PNG
        if os.path.isfile(img_path_jpeg):
            img_path = img_path_jpeg
        if os.path.isfile(img_path_jpg):
            img_path = img_path_jpg
        if os.path.isfile(img_path_png):
            img_path = img_path_png
        #t = magic.from_file(img_path)
        #wh= re.search('(\d+) x (\d+)', t).groups()
        if (img_path == ''):
            continue
        im=Image.open(img_path)
        w= int(im.size[0])
        h= int(im.size[1])
        #w = int(xmax) - int(xmin)
        #h = int(ymax) - int(ymin)
        # print(xmin)
        print(w, h)
            
        if(len(line.strip().split(" ")) >= 2):
            ct = ct + 1
            print(line)
            elems = list(filter(bool, re.split(' |\n', line)))
            elemsLen = len(elems)
            print("LENGTH: ")
            print(elemsLen)
            y = 1
            while (y < elemsLen) :
                xmin = elems[y]
                y = y + 1
                ymin = elems[y]
                y = y + 1
                xmax = elems[y]
                y = y + 1
                ymax = elems[y]
                y = y + 1
                b = (float(xmin), float(xmax), float(ymin), float(ymax))
                bb = convert((w,h), b)
                print(bb)
                txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

                

    """ Save those images with bb into list"""
    if(ct != 0):
        list_file.write('%s/%s/%s.JPEG\n'%(wd, cls, os.path.splitext(txt_name)[0]))
                
