#!/usr/bin/env python
# -*- coding:utf-8-*-
import os
import glob
import shutil
import datetime
import schedule
import time 
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler('/data/logs/upload_py.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

src = '/data/backup/'
upload_log_dir = '/data/logs/appgallery_china/'
log_path = '/data/logs/save_log/'
com = 'ansible AppgalleryVisitLog -m shell -a "python /data/copy_log.py"'
cmd = 'ansible AppgalleryVisitLog -m synchronize -a "src={src} dest={log_path} mode=pull"'
cos = 'coscmd upload -rs {upload_log_dir} /appgallery_china/'.format(upload_log_dir=upload_log_dir)
rs = 'rsync -az {upload_log_dir} hadoop@52.77.55.25:/data/archlog/homepage/appgallery_china/'.format(upload_log_dir=upload_log_dir)

T_dir = upload_log_dir + datetime.datetime.now().strftime('%Y/%m/')
if not os.path.exists(T_dir):
  os.makedirs(T_dir)

#收集远程主机的日志
def collection_log():
  if os.system(com) == 0:
    logger.info('节点采集日志成功~1')
  cmds = cmd.format(src=src, log_path=log_path)
  if os.system(cmds) == 0:
    logger.info('本机采集节点日志成功~2')
  return True

#log mv upload_dir
def mv_log():
  loger = glob.iglob(log_path + '*')
  for logs in loger:
    y_time, m_time, d_time = logs.split(".")[-1].split("-")
    time_dir = ''.join(list([upload_log_dir, y_time, '/', m_time, '/', d_time, '/']))
    if not os.path.exists(time_dir):
      os.makedirs(time_dir)
    shutil.copy2(logs, time_dir)
  logger.info('log mv upload_dir Successfully')
  return True

  # for d, m, f in os.walk(log_path):
  #   for file_name in f:
  #     time = file_name.split(".")[-1]
  #     y_time, m_time, d_time = time.split("-")
  #     time_dir = ''.join(list([upload_log_dir, y_time, '/', m_time, '/', d_time, '/']))
  #     if not os.path.exists(time_dir):
  #       os.makedirs(time_dir)
  #     log = log_path + file_name
  #     shutil.copy2(log, time_dir)
  # logger.info('log mv upload_dir Successfully')
  # return True

#log upload cos and push hadoop
def upload_cos():
  if os.system(cos) == 0:
    logger.info('log upload cos Successfully')
  if os.system(rs) == 0:
    logger.info('log push hadoop Successfully')
  return True

def main():
  logger.info('============================')
  collection_log()
  mv_log()    
  upload_cos()
  
if __name__ == '__main__':
  schedule.every().day.at("00:02").do(main)
  while 1:
      schedule.run_pending()
      time.sleep(60)
