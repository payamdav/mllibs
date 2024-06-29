import numpy as np


def forward_first_swing_type(rates, threshold=0.0001, *, percent=True, window=None):
  if not window or window >= len(rates):
    r = rates
    if percent:
      r = (r / r[0]) - 1
    else:
      r = r - r[0]
    
    for i in range(1, len(r)):
      if r[i] > threshold:
        return 1
      if r[i] < -threshold:
        return -1
    return 0
  else:
    ret = np.zeros(len(rates), dtype='int8')
    for i in range(len(rates)):
      s = np.s_[i:min(i + window, len(rates))]
      ret[i] = forward_first_swing_type(rates[s], threshold, percent=percent)
    return ret


def backward_last_swing_type(rates, threshold=0.0001, *, percent=True, window=None):
  if not window or window >= len(rates):
    r = rates
    if percent:
      r = (r / r[-1]) - 1
    else:
      r = r - r[-1]
    
    for i in range(len(r) - 2, -1, -1):
      if r[i] > threshold:
        return -1
      if r[i] < -threshold:
        return 1
    return 0
  else:
    ret = np.zeros(len(rates), dtype='int8')
    for i in range(len(rates)):
      s = np.s_[max(0, i - window): i + 1]
      ret[i] = backward_last_swing_type(rates[s], threshold, percent=percent)
    return ret


