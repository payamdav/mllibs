import numpy as np

def zigzag_start_0(h: np.ndarray, l:np.ndarray, d:np.ndarray | float, *, percent=False, extendToLast=False, singleArray=True):
  if not isinstance(d, np.ndarray):
    dl = np.full(len(h), d)
    dh = np.full(len(h), d)
  else:
    dl = d
    dh = d
  
  if percent:
    dl = l * dl
    dh = h * dh

  oh = np.zeros(len(h), dtype=bool)
  ol = np.zeros(len(h), dtype=bool)

  lastType = None
  lastValue = None
  nextValue = None
  nextIndex = None

  for i in range(0+1, len(h)):
    if l[i] < h[0] - dl[i]:
      oh[0] = True
      lastValue = h[0]
      lastType = 1
      nextIndex = i
      nextValue = l[i]
      break
    if h[i] > l[0] + dh[i]:
      ol[0] = True
      lastValue = l[0]
      lastType = -1
      nextIndex = i
      nextValue = h[i]
      break
  
  if nextIndex is not None:
    for i in range(nextIndex + 1, len(h)):
      if lastType == 1:
        if (l[i] < lastValue - dl[i] and nextIndex is None) or (nextIndex is not None and l[i] < nextValue):
          nextValue = l[i]
          nextIndex = i
        elif nextIndex is not None and h[i] > nextValue + dh[i]:
          ol[nextIndex] = True
          lastValue = nextValue
          lastType = -1
          nextIndex = i
          nextValue = h[i]
      elif lastType == -1:
        if (h[i] > lastValue + dh[i] and nextIndex is None) or (nextIndex is not None and h[i] > nextValue):
          nextValue = h[i]
          nextIndex = i
        elif nextIndex is not None and l[i] < nextValue - dl[i]:
          oh[nextIndex] = True
          lastValue = nextValue
          lastType = 1
          nextIndex = i
          nextValue = l[i]
  if nextIndex is not None:
    if lastType == 1:
      ol[nextIndex] = True
      lastType = -1
    else:
      oh[nextIndex] = True
      lastType = 1
  if extendToLast and lastType == 1 and ol[-1] == False and oh[-1] == False:
    ol[-1] = True
  if extendToLast and lastType == -1 and ol[-1] == False and oh[-1] == False:
    oh[-1] = True
  
  if singleArray:
    return oh.astype(int) - ol.astype(int)
  else:
    return oh, ol
