import glob
from scipy import ndimage
import nibabel as nib
import numpy as np
import math
from PIL import Image
def normalizeImage(scan):
    scan[scan<=0]=0
    scan=np.divide(scan, np.max(scan))
    scan=np.multiply(scan, 255)
    return scan
def convertoImage(scans,folder):
  data=np.transpose(scans, (0,3,1,2 ))
  print(data.shape)
  train=math.floor(data.shape[0]*0.7)
  for idx,i in enumerate(data[:train]):
    for jdx,j in enumerate(i):
      Image.fromarray(normalizeImage(j)).convert("L").save(folder+"/"+str(idx)+'_'+str(jdx)+'.jpg')
  for idx,i in enumerate(data[train:]):
    for jdx,j in enumerate(i):
      Image.fromarray(normalizeImage(j)).convert("L").save(folder+"/"+str(idx)+'_'+str(jdx)+'.jpg')

def read_nifti_file(filepath):
    """Read and load volume"""
    # Read file
    scan = nib.load(filepath)
    # Get raw data
    scan = scan.get_fdata()
    return scan


def normalize(volume):
    """Normalize the volume"""
    min = -1000
    max = 400
    volume[volume < min] = min
    volume[volume > max] = max
    volume = (volume - min) / (max - min)
    volume = volume.astype("float32")
    return volume


def resize_volume(img):
    """Resize across z-axis"""
    # Set the desired depth
    desired_depth = 64
    desired_width = 256
    desired_height = 256
    # Get current depth
    current_depth = img.shape[-1]
    current_width = img.shape[0]
    current_height = img.shape[1]
    # Compute depth factor
    depth = current_depth / desired_depth
    width = current_width / desired_width
    height = current_height / desired_height
    depth_factor = 1 / depth
    width_factor = 1 / width
    height_factor = 1 / height
    # Rotate
    img = ndimage.rotate(img, 90, reshape=False)
    # Resize across z-axis
    img = ndimage.zoom(img, (width_factor, height_factor, depth_factor), order=1)
    return img


def process_scan(path,i,total):
    """Read and resize volume"""
    # Read scan
    volume = read_nifti_file(path)
    # Normalize
    # volume = normalize(volume)
    # Resize width, height and depth
    # volume = resize_volume(volume)
    print("completed {}/{} ".format(i,total))
    return volume

def ExtractImagesFromNii(niifilepath,destination):

  scans = np.array([process_scan(path,idx,len(niifilepath)) for idx,path in enumerate([niifilepath])])
  convertoImage(scans,destination)

ExtractImagesFromNii("C:\\Users\\admin\\Downloads\\CC0021_philips_15_48_F.nii.gz","D:\\mri")