from matplotlib import pyplot as plt, style
from lib.charting.crosshair import CrossHair
import numpy as np


def chart_single(r):
  style.use('dark_background')
  fig = plt.figure(layout='constrained')
  gs = fig.add_gridspec(14, 14, wspace=0, hspace=0)
  ax = fig.add_subplot(gs[0:14, 0:14])
  plt.get_current_fig_manager().__dict__['window'].showMaximized()
  indexes = np.arange(len(r))
  ax.scatter(indexes, r, c='b', s=1)
  cross = CrossHair(fig)
  plt.show()      
  

def chart_single_2(r,r2):
  style.use('dark_background')
  fig = plt.figure(layout='constrained')
  gs = fig.add_gridspec(14, 14, wspace=0, hspace=0)
  ax = fig.add_subplot(gs[0:14, 0:14])
  plt.get_current_fig_manager().__dict__['window'].showMaximized()
  indexes = np.arange(len(r))
  ax.scatter(indexes, r, c='b', s=1)
  ax.scatter(indexes, r2, c='r', s=1)
  cross = CrossHair(fig)
  plt.show()      
