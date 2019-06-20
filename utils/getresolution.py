###################
# Nicolo Savioli  #
###################

import os 
from shutil import copyfile


def mkdir_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def get_new_folders(new_path,patientname):
    mkdir_dir(os.path.join(new_path,patientname))
    high_path = os.path.join(new_path,patientname,"high_grayscale")
    high_seg  = os.path.join(new_path,patientname,"high_segmentation")
    low_path  = os.path.join(new_path,patientname,"low_grayscale")
    mkdir_dir               (high_path)
    mkdir_dir               (low_path)
    mkdir_dir               (high_seg)
    return high_path,low_path,high_seg

def scan_high_paths(high_path,target):
    list_high_res_paths = os.listdir(high_path)
    get_path            = ""
    flag                = False
    for path in list_high_res_paths:
        if target in path.split("_"):
           get_path = path
           flag     = True 
           break
    return  get_path,flag

def getnii(low_path,high_path,\
           new_path,low_files,\
           high_files,seg_files):
    list_not = []   
    for patient in os.listdir(low_path):
        print("\n ..." + patient)
        old_high_path,flag = scan_high_paths(high_path,patient)
        if os.path.isdir(os.path.join(high_path,old_high_path)):
            if flag==True:
                high_new_path,\
                low_new_path,\
                high_seg = get_new_folders(new_path,patient)
                for fr in low_files:
                    copyfile(os.path.join(low_path,patient,fr), os.path.join(low_new_path,fr))
                for fr in high_files:
                    copyfile(os.path.join(high_path,old_high_path,fr), os.path.join(high_new_path,fr))
                for fr in seg_files:
                    copyfile(os.path.join(high_path,old_high_path,fr), os.path.join(high_seg,fr))
            else:
                list_not.append(patient)
                continue
        else:
            continue
    return list_not

def main(low_path,high_path,\
         new_path,low_files,\
         high_files,seg_files):
    list_not = getnii(low_path,high_path,new_path,low_files,high_files,seg_files)
    print("\n\n\n\n\n ... Total missing are: "+ len(list_not))

if __name__ == "__main__":
    low_files  = ["lvsa_ED.nii.gz","lvsa_ES.nii.gz"]
    high_files = ["lvsa_ED_enlarged.nii.gz","lvsa_ES_enlarged.nii.gz"]
    seg_files  = ["segmentation_ED.gipl","segmentation_ES.gipl"]
    low_path   = "/home/nsavioli@isd.csc.mrc.ac.uk/cardiac/DL_segmentation/HVOL_to_seg"
    high_path  = "/home/nsavioli@isd.csc.mrc.ac.uk/cardiac/3datlas2"
    new_path   = "/home/nsavioli@isd.csc.mrc.ac.uk/cardiac/UKBB_40616/dataset_new_project" 
    main (low_path,high_path,new_path,low_files,high_files,seg_files)