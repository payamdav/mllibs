import numpy as np
import pandas as pd
from contextlib import contextmanager
from lib.tools.timer import TimerProfiler


class Explorer:
  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)

  @contextmanager
  def set(self, **kwargs):
    toDelete = []
    cache = {}
    try:
      for k,v in kwargs.items():
        if hasattr(self, k):
          cache[k] = getattr(self, k)
        else:
          toDelete.append(k)
        setattr(self, k, v)
      yield self
    except Exception as e:
      print(f'Error: {e}')
    finally:
      for k,v in cache.items():
        setattr(self, k, v)
      for k in toDelete:
        delattr(self, k)
    return self
  
  def init(self):
    pass
  
  def iter(self):
    for self.idx in range(len(self.rates)):
      self.index()
    return self
  
  def index(self):
    return self
  
  def finalize(self):
    return self


  