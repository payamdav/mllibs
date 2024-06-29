import numpy as np

def zigzag(h: np.ndarray, l:np.ndarray, d:np.ndarray | float, *, percent=False, extendToLast=False, singleArray=True, choch=False):
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

  choch_up = np.zeros(len(h), dtype=bool)
  choch_down = np.zeros(len(h), dtype=bool)

  start_point = np.argmax(h)
  oh[start_point] = True
  lastType = 1
  lastValue = h[start_point]
  nextValue = None
  nextIndex = None

  for i in range(start_point+1, len(h)):
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
        choch_up[i] = True
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
        choch_down[i] = True
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

  lastType = 1
  lastValue = h[start_point]
  nextValue = None
  nextIndex = None
  for i in range(start_point-1, -1, -1):
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
        choch_up[i] = True
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
        choch_down[i] = True
  if nextIndex is not None:
    if lastType == 1:
      ol[nextIndex] = True
      lastType = -1
    else:
      oh[nextIndex] = True
      lastType = 1
  if extendToLast and lastType == 1 and ol[0] == False and oh[0] == False:
    ol[0] = True
  if extendToLast and lastType == -1 and ol[0] == False and oh[0] == False:
    oh[0] = True
  
  if singleArray:
    if choch:
      return oh.astype(int) - ol.astype(int), choch_up.astype(int) - choch_down.astype(int)
    else:
      return oh.astype(int) - ol.astype(int)
  else:
    if choch:
      return oh, ol, choch_up, choch_down
    else:
      return oh, ol
