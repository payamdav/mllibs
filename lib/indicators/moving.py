import numpy as np


def ms_backward_inclusive(a, n):
  return np.convolve(np.insert(a, 0, np.tile(a[0], n-1)), np.ones(n), 'full')[n-1:-n+1]

def ms_backward_exclusive(a, n):
  return np.convolve(np.insert(a, 0, np.tile(a[0], n)), np.ones(n), 'full')[n-1:-n]
  
def ms_forward_inclusive(a, n):
  return np.convolve(np.append(a, np.tile(a[-1], n-1)), np.ones(n), 'full')[n-1:-(n-1)]
  
def ms_forward_exclusive(a, n):
  return np.convolve(np.append(a, np.tile(a[-1], n)), np.ones(n), 'full')[n:-n+1]

def ma_backward_inclusive(a, n):
  return ms_backward_inclusive(a, n) / n

def ma_backward_exclusive(a, n):
  return ms_backward_exclusive(a, n) / n

def ma_forward_inclusive(a, n):
  return ms_forward_inclusive(a, n) / n

def ma_forward_exclusive(a, n):
  return ms_forward_exclusive(a, n) / n

def ma_backward_inclusive_weighted(a, n, w):
  return ms_backward_inclusive(a * w, n) / ms_backward_inclusive(w, n)

def ma_backward_exclusive_weighted(a, n, w):
  return ms_backward_exclusive(a * w, n) / ms_backward_exclusive(w, n)

def ma_forward_inclusive_weighted(a, n, w):
  return ms_forward_inclusive(a * w, n) / ms_forward_inclusive(w, n)

def ma_forward_exclusive_weighted(a, n, w):
  return ms_forward_exclusive(a * w, n) / ms_forward_exclusive(w, n)
