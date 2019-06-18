#######################
# Nicolo Savioli 2019 #
#######################

import os 
import shutil


def mkdir_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def getExE(path,patient,targetfile):
    exe = filename = ""
    for file in os.listdir(os.path.join(path,patient,"LVSA")):
        if ("LVSA" in file or "lvsa" in file) and len(file.split(".")[0]) == 4:
            filename = file.split(".")[0]
            exe      = file.split(".")[1]
    return filename,exe
                

def deletefolders(path_main,patient):
    if os.path.isdir(os.path.join(path_main,patient)):
        for folder in os.listdir(os.path.join(path_main,patient)):
            if folder == "TMP":
                continue 
            else:
                if os.path.isfile(os.path.join(path_main,patient,folder)):
                    os.remove(os.path.join(path_main,patient,folder))
                else:
                    shutil.rmtree(os.path.join(path_main,patient,folder))

def movetargetfile(pathdir,target):
    print("\n\n ~ CleanFold 1.0 ~ \n\n")
    for patient in os.listdir(pathdir): 
        if os.path.isdir(os.path.join(pathdir,patient)):
            print("..."+patient)
            targetfile = ""
            filename,exe     = getExE(pathdir,patient,target)
            if exe == "nii":
                targetfile   = filename + "." + exe + "." + "gz"
            else:
                targetfile   = filename + "." + exe 
            # create a tmp folder
            tmp_path   = os.path.join(pathdir,patient,"TMP") 
            mkdir_dir(tmp_path)
            # move in tmp folder 
            shutil.move(os.path.join(pathdir,patient,"LVSA",targetfile), tmp_path)
            # delete all folders in main folder
            deletefolders(pathdir,patient)
            # move target file in main folder 
            shutil.move(os.path.join(pathdir,patient,"TMP",targetfile), os.path.join(pathdir,patient))
            # rm tmp folder
            shutil.rmtree(os.path.join(pathdir,patient,"TMP"))
           
def main(pathdir,targetfile):
    movetargetfile(pathdir,targetfile)
    
if __name__ == "__main__":
    pathdir    = "/home/wyedemaa/cardiac/DL_segmentation/HVOL_completed_to_segment2" #frankie
    #pathdir    = "/home/wyedemaa@isd.csc.mrc.ac.uk/cardiac/DL_segmentation/HVOL_completed_to_segment2"
    #pathdir    = "/home/nsavioli@isd.csc.mrc.ac.uk/cardiac/DL_segmentation/Test_for_nicolo"
    targetfile = "LVSA"
    main(pathdir,targetfile)



