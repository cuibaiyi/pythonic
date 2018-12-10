import random

def kp(l):
  if len(l) < 2:
    return l
  else:
    tag = len(l) // 2
    n, x = l[tag], l[:tag] + l[tag + 1:]
    lt, gt = [i for i in x if i <= n], [i for i in x if i > n]
    return kp(lt) + [n] + kp(gt)

l = list(set([random.randint(1,100) for _ in range(10)]))
kp(l)
