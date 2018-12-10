import random

def sort_list(l):
  stop = len(l) - 1
  for _ in range(stop):
    for i in range(stop):
     if l[i] > l[i+1]:
       l[i+1], l[i] = l[i], l[i+1]
    stop -= 1
  return l

l = list(set([random.randint(1, 100) for _ in range(10)]))
sort_list(l)
