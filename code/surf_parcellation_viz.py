"""

Example usage:

TODO:

inputs:
 - parcellation
 - side (L/R)
 - pial
 - sulc
 - view (lateral, etc)

"""

import nilearn
import sys
import matplotlib
from nilearn import plotting

def main():

  
  parcellation = sys.argv[2]
  fsaverage = datasets.fetch_surf_fsaverage() # surface dataset for surface background ?
  fig = plotting.plot_surf_roi (fsaverage['pial_left'], roi_map=parcellation, 
                        hemi='left', view='lateral',
                        bg_map=fsaverage['sulc_left'], bg_on_data=True, 
                        darkness=0.5)

  fig.figure.show()

if __name__ == "__main__":
    main()
