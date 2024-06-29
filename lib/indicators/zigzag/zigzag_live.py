import numpy as np

H = 1
L = -1
N = 0

class ZigZag:
  def __init__(self, d, c):
    self.d = d
    self.c = c
    self.i = -1
    
    self.z = np.zeros(c, dtype=int)
    self.trend_reversal = np.zeros(c, dtype=int)
    self.trend = N
    
    self.lastType = N
    self.nextValue = None
    self.nextIndex = None
    
    self.firstMin = float('inf')
    self.firstMax = float('-inf')
    self.firstMinIndex = 0
    self.firstMaxIndex = 0
    
    self.temp_last = True
    self.temp_last_index = None
    
  def push(self, h, l=None):
    l = l if l is not None else h
    self.i += 1
    if self.lastType == N:
      if h > self.firstMax:
        self.firstMax = h
        self.firstMaxIndex = self.i
      if l < self.firstMin:
        self.firstMin = l
        self.firstMinIndex = self.i
      if self.firstMax - self.firstMin >= self.d:
        if self.firstMaxIndex < self.firstMinIndex:
          self.z[self.firstMaxIndex] = H
          self.lastType = H
          self.nextValue = self.firstMin
          self.nextIndex = self.firstMinIndex
          self.trend_reversal[self.i] = L
          self.trend = L
          if self.temp_last:
            self.temp_last_index = self.i
            self.z[self.temp_last_index] = L
        else:
          self.z[self.firstMinIndex] = L
          self.lastType = L
          self.nextValue = self.firstMax
          self.nextIndex = self.firstMaxIndex
          self.trend_reversal[self.i] = H
          self.trend = H
          if self.temp_last:
            self.temp_last_index = self.i
            self.z[self.temp_last_index] = H
    elif self.lastType == H:
      if l < self.nextValue:
        if self.temp_last_index is not None:
          self.z[self.temp_last_index] = N
          self.temp_last_index = None
        self.nextValue = l
        self.nextIndex = self.i
        if self.temp_last:
          self.temp_last_index = self.i
          self.z[self.temp_last_index] = L
      elif h >= self.nextValue + self.d:
        if self.temp_last_index is not None:
          self.z[self.temp_last_index] = N
          self.temp_last_index = None
        self.z[self.nextIndex] = L
        self.lastType = L
        self.nextIndex = self.i
        self.nextValue = h
        self.trend_reversal[self.i] = H
        self.trend = H
        if self.temp_last:
          self.temp_last_index = self.i
          self.z[self.temp_last_index] = H
    elif self.lastType == L:
      if h > self.nextValue:
        if self.temp_last_index is not None:
          self.z[self.temp_last_index] = N
          self.temp_last_index = None
        self.nextValue = h
        self.nextIndex = self.i
        if self.temp_last:
          self.temp_last_index = self.i
          self.z[self.temp_last_index] = H
      elif l <= self.nextValue - self.d:
        if self.temp_last_index is not None:
          self.z[self.temp_last_index] = N
          self.temp_last_index = None
        self.z[self.nextIndex] = H
        self.lastType = H
        self.nextIndex = self.i
        self.nextValue = l
        self.trend_reversal[self.i] = L
        self.trend = L
        if self.temp_last:
          self.temp_last_index = self.i
          self.z[self.temp_last_index] = L
    return self
  
  def run(self, h, l=None):
    l = l if l is not None else h
    for i in range(len(h)):
      self.push(h[i], l[i])
    return self
  
  def __len__(self):
    return np.count_nonzero(self.z) - 1
  
  def __getitem__(self, k):
    # return (Trend Type -1 or 1, Start Index, End Index, Trend Reversal Index)
    nz = np.nonzero(self.z)[0]
    tr = np.nonzero(self.trend_reversal)[0]
    if isinstance(k, int):
      if k >= nz.shape[0] - 1 or k <= -nz.shape[0]:
        raise IndexError('Index out of bounds')
      elif k >= 0:
        return (self.z[nz[k+1]], nz[k], nz[k+1], tr[k])
      else:
        return (self.z[nz[k]], nz[k-1], nz[k], tr[k-1])
    else:
      raise TypeError('Index must be an integer')
    


class Chocher:
  def __init__(self, d1:float, d2:float, c):
    self.c = c
    self.d1 = d1
    self.d2 = d2
    self.i = -1        
    self.zz1 = ZigZag(d1, self.c)
    self.zz2 = ZigZag(d2, self.c)
    self.choch = np.zeros(self.c, dtype=int)
    self.unitrend = np.zeros(self.c, dtype=int)
  
  def push(self, h, l):
    self.i += 1
    self.zz1.push(h, l)
    self.zz2.push(h, l)
    if self.zz1.trend == H and self.zz2.trend_reversal[self.i] == L:
      self.choch[self.i] = L
    elif self.zz1.trend == L and self.zz2.trend_reversal[self.i] == H:
      self.choch[self.i] = H
    if self.zz1.trend == H and self.zz2.trend_reversal[self.i] == H:
      self.unitrend[self.i] = H
    elif self.zz1.trend == L and self.zz2.trend_reversal[self.i] == L:
      self.unitrend[self.i] = L
    return self
  
  def run(self, h, l=None):
    l = l if l is not None else h
    for i in range(len(h)):
      self.push(h[i], l[i])
    return self

  def __len__(self):
    return np.count_nonzero(self.choch)
  
  def __getitem__(self, k) -> tuple[int, int]:
    # return (Choch Type: -1 for choch down or 1 for choch up, Index)
    nz = np.nonzero(self.choch)[0]
    if isinstance(k, int):
      if k > nz.shape[0] - 1 or k < -nz.shape[0]:
        raise IndexError('Index out of bounds')
      elif k >= 0:
        return (self.choch.item(nz[k]), nz[k])
      else:
        return (self.choch.item(nz[k]), nz[k])
    else:
      raise TypeError('Index must be an integer')


class UniTrend:
  def __init__(self, d1:float, d2:float, c):
    self.c = c
    self.d1 = d1
    self.d2 = d2
    self.i = -1        
    self.zz1 = ZigZag(d1, self.c)
    self.zz2 = ZigZag(d2, self.c)
    self.unitrend = np.zeros(self.c, dtype=int)
  
  def push(self, h, l):
    self.i += 1
    self.zz1.push(h, l)
    self.zz2.push(h, l)
    if self.zz1.trend == H and self.zz2.trend_reversal[self.i] == H:
      self.unitrend[self.i] = H
    elif self.zz1.trend == L and self.zz2.trend_reversal[self.i] == L:
      self.unitrend[self.i] = L
    return self
  
  def run(self, h, l=None):
    l = l if l is not None else h
    for i in range(len(h)):
      self.push(h[i], l[i])
    return self

  def __len__(self):
    return np.count_nonzero(self.unitrend)
  
  def __getitem__(self, k) -> tuple[int, int]:
    # return (Choch Type: -1 for choch down or 1 for choch up, Index)
    nz = np.nonzero(self.unitrend)[0]
    if isinstance(k, int):
      if k > nz.shape[0] - 1 or k < -nz.shape[0]:
        raise IndexError('Index out of bounds')
      elif k >= 0:
        return (self.unitrend.item(nz[k]), nz[k])
      else:
        return (self.unitrend.item(nz[k]), nz[k])
    else:
      raise TypeError('Index must be an integer')

