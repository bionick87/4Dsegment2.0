import os
import numpy as np

def fixedheader(segmentation,grayscale):
    os.system('headertool '
            '{0} '
            '{0} '
            '-target {1}'
            .format(segmentation, grayscale))

def fixlabels(segs_dir):
  for fr in ['ED', 'ES']:
      fixed_DLSeg    = '{0}/segmentation_{1}_fixedup.gipl'.format(segs_dir, fr)
      enlargedfile   = '{0}/lvsa_{1}_enlarged.nii.gz'.format(segs_dir, fr)
      fixedheader(fixed_DLSeg,enlargedfile)
      print("\n ... done")

def run(dir_data):
  for subject in sorted(os.listdir(dir_data)):
      print("\n ..." + subject)
      fixlabels(os.path.join(dir_data,subject))

if __name__ == "__main__":
  dir_data = "/cardiac/patchmatchSegmentation/test_test"
  run(dir_data)
