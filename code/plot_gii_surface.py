#!/usr/bin/env python

""" 

Example usage:
python plot_gii_surface.py /path/to/my/mesh /path/to/my/map.gii \
                          <hemisphere> /path/to/my/img.png \
                          <view>

"""

import nilearn
from argparse import ArgumentParser

def main():

  parser = ArgumentParser("Visualize surface data")
  parser.add_argument('in_mesh', help="Surface mesh: .gii or Freesurfer specific files \
                                      such as .orig, .pial, .sphere, .white, .inflated")
  parser.add_argument('in_map', help="Data to visualize: valid formats are .gii, .mgz, .nii, \
                                      .nii.gz, or Freesurfer specific files such as .thickness, \
                                      .area, .curv, .sulc, .annot, .label")
  parser.add_argument("hem", help="Hemisphere: 'right' or 'left'")
  parser.add_argument("plot_loc", help="Target location of plot")
  parser.add_argument("view", help="Brain view: ‘lateral’, ‘medial’, ‘dorsal’, 'ventral', \
                                        'anterior', 'posterior' (Default = Lateral)") 
  
  results = parser.parse_args()
  fig = nilearn.plotting.plot_surf(results.in_mesh, surf_map=results.in_map, 
                                    hemi=results.hem, view=results.view, 
                                    output_file=results.plot_loc) 

  
if __name__ == "__main__":
  main()

