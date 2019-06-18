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
    for file in os.listdir(os.path.join(path,patient)):
        if ("SA" in file or "sa" in file) and len(file.split(".")[0]) == 2:
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
                targetfile   = filename + "." + exe 
            else:
                targetfile   = filename + "." + exe 
            # create a tmp folder
            tmp_path   = os.path.join(pathdir,patient,"TMP") 
            mkdir_dir(tmp_path)
            # move in tmp folder 
            shutil.move(os.path.join(pathdir,patient,targetfile), tmp_path)
            # delete all folders in main folder
            deletefolders(pathdir,patient)
            # move target file in main folder 
            shutil.move(os.path.join(pathdir,patient,"TMP",targetfile), os.path.join(pathdir,patient))
            # rm tmp folder
            shutil.rmtree(os.path.join(pathdir,patient,"TMP"))
           
def main(pathdir,targetfile):
    movetargetfile(pathdir,targetfile)
    
if __name__ == "__main__":
    pathdir    = "/home/nsavioli@isd.csc.mrc.ac.uk/cardiac/UKBB_40616/test_clean" 
    targetfile = "sa"
    main(pathdir,targetfile)


