import nibabel as nib, vtk 
import numpy as np
import os



def checkLabels(seg,labels):
    list_labels = []
    flag = True
    for i in range(5):

        if seg[seg == i] != []:
            list_labels.append(i)
        else:
             continue
    if labels in list_labels:
       flag = True 
    else:
        flaf = False
    return flag 
    

def extract_landmarks(path, segmentation_filename, landmarks_filename, labels):
    # """ Extract landmarks from a LVSA nifti segmentation """
    # path: working directory
    # segmentation_filename: name of the segmentation file
    # landmarks_filename: output landmarks filename
    # labels: label numbers of the structures on which you want to compute the lankmarks
    # Load the segmentation nifti
    nim = nib.load(os.path.join(path,segmentation_filename))
    affine = nim.affine
    seg = nim.get_data()

    if checkLabels(seg,labels):
            # Extract the z axis from the nifti header
            lm = []
            z_axis = np.copy(nim.affine[:3, 2])


            
            # loop on all the segmentation labels of interest
            for l in labels:
                # Determine the z range
                print(l)
                z = np.nonzero(seg == l)[2]

                print(z)
                z_min, z_max = z.min(), z.max()
                z_mid = int(round(0.5 * (z_min + z_max)))

                # compute landmarks positions
                if z_axis[2] < 0:
                    # z_axis starts from base
                    zs = [z_min, z_mid, z_max]
                else:
                    # z_axis starts from apex
                    zs = [z_max, z_mid, z_min]

                for z in zs:
                    seg = np.squeeze(seg)
                    x, y = [np.mean(i) for i in np.nonzero(seg[:, :, z] == l)]
#                    x, y = [np.mean(i) for i in np.nonzero(seg[:, :, z, 0] == l)]
                    # this might need to be changed depending on the segmentation data structure
                    p = np.dot(affine, np.array([x, y, z, 1]).reshape((4, 1)))[:3, 0]
                    lm.append(p)
            # Write the landmarks
            points = vtk.vtkPoints()
            for p in lm:
                points.InsertNextPoint(p[0], p[1], p[2])
            poly = vtk.vtkPolyData()
            poly.SetPoints(points)
            writer = vtk.vtkPolyDataWriter()
            writer.SetInputData(poly)
            writer.SetFileName(os.path.join(path,landmarks_filename))
            writer.Write()
    else:
        print("\n ... Error in labels")
    

def landmarking(cur_path, segmentation_filename="LVSA_seg_ED.nii.gz", landmarks_filename="landmarks2.vtk"):

    for s in os.listdir(cur_path):
    #    os.system('convert {0}/segmentation_ED.gipl {0}/segmentation_ED.nii.gz'.format(os.path.join(cur_path,s)))
        extract_landmarks(os.path.join(cur_path,s),segmentation_filename,landmarks_filename,labels = [2,4])
    
