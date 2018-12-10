def find_sum(l, n):
  start = 0
  stop = len(l)-1
  while start <= stop:
    s = (stop - start) // 2 + start  #或者(stop + start) // 2
    tag = l[s]
    if tag == n:
      return s
    if tag > n:
      stop = s - 1
    else:
      start = s + 1
  else:
    return None

l = [i for i in range(10)]
find_sum(l, 6)
