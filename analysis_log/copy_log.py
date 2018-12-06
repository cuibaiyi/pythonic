#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
import glob

host_name = os.popen('hostname').read().strip()
log_path = '/data/logs/api/'
target_path = '/data/backup/'

def source_log(log_path):
  logs = glob.iglob(log_path + 'appgallery-visit?log?*')
  log_file = [ log for log in logs ]
  return log_file

def backup_log(log_path, target_path):
  for i in source_log(log_path):
    src = ''.join(list([target_path, host_name, '-', i.split("/")[-1]]))
    shutil.copy2(i, src)
  return True

backup_log(log_path, target_path)
