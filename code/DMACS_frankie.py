import time
import numpy as np, nibabel as nib, pandas as pd
import tensorflow as tf
from deepseg import *
from p1processing import *
from p2processing import *
from meshfitting import *
from motionEstimation import *


FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_integer('coreNo', 16, 'Number of CPUs.')
tf.app.flags.DEFINE_string('test_dir', '/home/wyedemaa/cardiac/DL_segmentation/Test2',
                           'Path to the test set directory, under which images are organised in '
                           'subdirectories for each subject.')
tf.app.flags.DEFINE_string('model_path',  '/home/wyedemaa/temp/DeepLearning/DL_2DVol_5_markers/saver/model/cross_entropy_loss_HCM_4_markers/cross_entropy_loss_HCM_4_markers.ckpt-50', 'Path to the saved trained model.')
tf.app.flags.DEFINE_string('atlas_dir',  '/home/wyedemaa/cardiac/PHpatchmatchSegmentation/3datlas2', 'Path to the atlas.')
tf.app.flags.DEFINE_string('param_dir', '/home/wyedemaa/cardiac/PHpatchmatchSegmentation/par', 'Path to the registration parameters.')
tf.app.flags.DEFINE_string('template_dir', '/home/wyedemaa/cardiac/PHpatchmatchSegmentation/3datlas2', 'Path to the template.')
tf.app.flags.DEFINE_string('template_PH', '/home/wyedemaa/cardiac/PHpatchmatchSegmentation/3datlas2', 'Path to the template.')



if __name__ == '__main__':
        
    print('Start evaluating on the test set ...')
    table_time = []
    start_time = time.time()

    deeplearningseg(FLAGS.model_path, FLAGS.test_dir, FLAGS.atlas_dir)  
       
#    multiatlasreg2D(FLAGS.test_dir, FLAGS.atlas_dir, FLAGS.param_dir, FLAGS.coreNo, False, True) # parallel, irtk
                        
    multiatlasreg3D(FLAGS.test_dir, FLAGS.atlas_dir, FLAGS.param_dir, FLAGS.coreNo, True, True) # parallel, irtk
#          
    meshCoregstration(FLAGS.test_dir, FLAGS.param_dir, FLAGS.template_dir, FLAGS.coreNo, True, False) # parallel, irtk
#        
#    motionTracking(FLAGS.test_dir, FLAGS.param_dir, FLAGS.template_PH, FLAGS.coreNo, True) # parallel

    process_time = time.time() - start_time 
    print('Including image I/O, CUDA resource allocation, '
          'it took {:.3f}s in total for processing all the subjects).'.format(process_time))                                