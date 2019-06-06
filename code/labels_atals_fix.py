####################
## Nicolo Savioli ##
####################
import os
import numpy as np
import ntpath
import shutil
from   medpy.io import load
from   medpy.io import save

def get_label_replacement(img):
    img[img == 4] = 3
    return img

def get_new_labels(filename):
    img_list   = []
    open_file, image_header = load(filename)
    open_np    = open_file.transpose(2,0,1)
    for i in range(open_np.shape[0]):    
        img_list.append(get_label_replacement(open_np[i]))
    out_img = np.asarray(img_list).transpose(2,1,0).transpose(1,0,2)
    return out_img,image_header
    
def savedata(file,basepath,namefile,image_header):
    save(file, os.path.join(basepath,'tmp',namefile), image_header)

def make_dir(file_path):
    file_path = os.path.join(file_path,"tmp")
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def fixlabels(segs_dir):
  make_dir (segs_dir)
  for fr in ['ED', 'ES']:
      DLSeg                   = '{0}/segmentation_{1}.gipl'.format(segs_dir, fr)
      fixed_DLSeg             = '{0}/segmentation_{1}_fixedup.gipl'.format(segs_dir, fr)
      nameDLSeg               = ntpath.basename (DLSeg)
      newDLSeg,image_header   = get_new_labels  (DLSeg)
      savedata (newDLSeg,segs_dir,fixed_DLSeg,image_header)

def run(dir_data):
  for subject in sorted(os.listdir(dir_data)):
      print("\n ..." + subject)
      fixlabels(os.path.join(dir_data,subject))
       
if __name__ == "__main__":
  dir_data = "/home/nsavioli@isd.csc.mrc.ac.uk/cardiac/patchmatchSegmentation/test_test"
  run(dir_data)
