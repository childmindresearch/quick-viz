""" 

Example usage:

python plot_gii_surface.py /path/to/my/mesh /path/to/my/map.gii \
                          <hemisphere> /path/to/my/img.png \
                          [view]

"""

import nilearn
import sys
from nilearn import plotting

def main():

  
  in_mesh = sys.argv[1]    # Surface mesh (.gii or Freesurfer specific files such as .orig, 
                           #                 .pial, .sphere, .white, .inflated
  in_map = sys.argv[2]     # Surface map (Can be a file (valid formats are .gii, .mgz, .nii, .nii.gz, 
                           #                 or Freesurfer specific files such as .thickness, .area, 
                           #                 .curv, .sulc, .annot, .label) or a Numpy array with a 
                           #                 value for each vertex of the surf_mesh
  hem = sys.argv[3]        # Hemisphere ('right' or 'left')
  plot_loc = sys.argv[4]   # Target location of plot
  
  if len(sys.argv) == 6:
    view = sys.argv[5]     # Brain view - ‘lateral’, ‘medial’, ‘dorsal’, 
                           #                 ‘ventral’, ‘anterior’, ‘posterior’
                           #                 (Default = lateral)
  else:
    view = 'lateral'
  
  fig = nilearn.plotting.plot_surf(in_mesh, surf_map=in_map, hemi=hem, 
                                    view=view, output_file=plot_loc) 

if __name__ == "__main__":
  main()
