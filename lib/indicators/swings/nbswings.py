from numba import jit, guvectorize, float64, float32, int64, int32, int16, int8


@guvectorize([(float64[:], float64[:], int32, int8[:])], '(n),(n),()->(n)', nopython=True)
def forward_first_swing_type_nb(r, t, w, out):
  l = len(r)
  tim = 0 if len(t) == 1 else 1
  for i in range(l-w+1):
    out[i] = 0
    for j in range(i, i+w):
      if r[j] > r[i] + t[i*tim]:
        out[i] = 1
        break
      if r[j] < r[i] - t[i*tim]:
        out[i] = -1
        break
  for i in range(l-w+1, l):
    out[i] = 0


@guvectorize([(float64[:], float64[:], int32, int8[:])], '(n),(n),()->(n)', nopython=True)
def backward_last_swing_type_nb(r, t, w, out):
  l = len(r)
  tim = 0 if len(t) == 1 else 1
  for i in range(l-1, w-1-1, -1):
    out[i] = 0
    for j in range(i, i-w, -1):
      if r[j] > r[i] + t[i*tim]:
        out[i] = 1
        break
      if r[j] < r[i] - t[i*tim]:
        out[i] = -1
        break
  for i in range(w-1-1, -1 , -1):
    out[i] = 0

