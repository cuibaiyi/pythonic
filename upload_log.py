#!/usr/bin/env python
# -*- coding:utf-8-*-
import os
import shutil
import datetime
import schedule
import time 

com = 'ansible AppgalleryVisitLog -m shell -a "python /data/copy_log.py"'
cmd = 'ansible AppgalleryVisitLog -m synchronize -a "src={src} dest={log_path} mode=pull"'
cos = 'coscmd upload -rs /root/appgallery_visit_log/ /appgallery_visit_log/'
src = '/data/backup/'
upload_log_dir = '/root/appgallery_visit_log/'
log_path = '/root/save_log/'

y_dir = upload_log_dir + datetime.datetime.now().strftime('%Y') + '/'
if not os.path.exists(y_dir):
  os.mkdir(y_dir)

#收集远程主机的日志
def collection_log():
  if os.system(com) == 0:
    print '本机采集日志成功~'
  cmds = cmd.format(src=src, log_path=log_path)
  if os.system(cmds) == 0:
    print '采集日志成功~'
  return True

#把收集的日子移动到上传目录里
def mv_log():
  for d,m,f in os.walk(log_path):
    for file_name in f:
      time = file_name.split(".")[-1]
      y_time = time.split("-")[0]
      time_dir = upload_log_dir + y_time + '/' + time + '/'
      if not os.path.exists(time_dir):
        os.mkdir(time_dir)
      log = log_path + file_name
      shutil.copy2(log, time_dir)
  print '日志移动到上传目录成功~'
  return True

#把日志上传到cos
def upload_cos():
  if os.system(cos) == 0:
    print '日志上传cos完成'
  return True

def main():
  collection_log()
  mv_log()    
  upload_cos()
  
if __name__ == '__main__':
  schedule.every().day.at("00:30").do(main)
  while True:
      schedule.run_pending()
      time.sleep(1)
