#二分查找必须满足一个条件，查找的列表必须是有序的。
#当查找一个无序的列表时，如果只查找一次，使用线性查找(list中内置的index方法)；当需要查找多次时，先排序，再使用二分查找！
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
