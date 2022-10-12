""" 

Example usage:
python surface_viz.py /path/to/img.gii

"""

import nilearn
import sys
import matplotlib
from nilearn import plotting

def main():

  
  img = sys.argv[1]
  fig = nilearn.plotting.plot_surf(img)
  fig.figure.show()

  
if __name__ == "__main__":
  main()
