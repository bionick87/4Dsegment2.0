####################
## Nicolo Savioli ##
####################
import os
import numpy as np
import ntpath
import shutil
##################

def get_label_replacement(img):
    img[img == 4] = 3
    return img

def get_new_labels(filename):
    img_list    = []
    load_file  = nib.load(filename)
    open_file  = load_file.get_fdata()
    open_np    = open_file.transpose(2,0,1)
    for i in range(open_np.shape[0]):    
        img_list.append(get_label_replacement(open_np[i]))
    out_img = np.asarray(img_list).transpose(2,1,0).transpose(1,0,2)
    return nib.Nifti1Image(out_img, load_file.affine, load_file.header)

def save_nii(file,basepath,namefile):
    file.to_filename(os.path.join(basepath,'tmp',namefile))

def make_dir(file_path):
    file_path = os.path.join(file_path,"tmp")
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def fixlabels(segs_dir):
  make_dir (segs_dir)
  for fr in ['ED', 'ES']:
      DLSeg      = '{0}/segmentation_{1}.gipl'.format(segs_dir, fr)
      nameDLSeg  = ntpath.basename (DLSeg)
      newDLSeg   = get_new_labels  (DLSeg)
      save_nii                     (newDLSeg,segs_dir,nameDLSeg)
      os.remove                    (DLSeg)
      shutil.move                  (os.path.join(segs_dir,"tmp",nameDLSeg), segs_dir)
  shutil.rmtree(os.path.join(segs_dir,"tmp"))

def run(dir_data):
  for subject in sorted(os.listdir(dir_data)):
      print("...." + subject)
      fixlabels(os.path.join(dir_data,subject))
       

if __name__ == "__main__":
  dir_data = "/home/nsavioli@isd.csc.mrc.ac.uk/cardiac/patchmatchSegmentation/test_test"
  run(dir_data)
