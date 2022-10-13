""" 

Example usage:
python surface_viz.py /path/to/img.gii

"""

import nilearn
import sys
from nilearn import plotting

def main():

  
  img = sys.argv[1]
  fig = nilearn.plotting.plot_surf(img)
  plotting.show()

  
if __name__ == "__main__":
  main()
