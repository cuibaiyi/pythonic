#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'cuiby'
__version__ = 'v1.0'

from subprocess import Popen, PIPE
import shutil
import glob
import datetime
import requests
import json
import os
import sys
import ConfigParser
import time

try:
    config = ConfigParser.ConfigParser()
    config.read("/home/aiadmin/yx_prod_images/.prod.conf")
    environment = config.get("config", "environment")
    pass_url = config.get("config", "cicd_api")
    Harbor_url = config.get("config", "harbor_url")
    code_dir = config.get("config", "code_dir")
    upload_dir = config.get("config", "upload_dir")
    runexe = config.get("config", "run_md5")
except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
    raise Exception("配置文件错误或不存在,请检查: /data/.prod.conf")

print("请输入执行脚本秘钥")
passwd = str(input(":"))
if passwd.strip() != runexe:
    print("输入秘钥有误,退出脚本!")
    sys.exit(1)

print("###################################")
print("1 xx门户 aibap")
print("2 xx用户 aiuu")
print("3 xx待办 aiut")
print("4 xx文档 aiud")
print("5 xx通知 aiun")
print("6 robot aisr")
print("7 xx aiir")
print("8 xx平台 aipp")
print("9 微服务 aicsf")
print("10 xx分析 aiaa")
print("###################################")

projet_name_list = {
    1: ("aibap", ("baseportal",), ("base-server",)),
    2: ("aiuu", ("uniusr",), ("m-uni-user-job", "m-uni-user-rest", "m-uni-user-inter", "m-uni-user-srv", "m-uni-sso-base", "m-uni-sso-resource", "m-uni-sso-srv")),
    3: ("aiut", ("unitodo",), ("unitodo-m-server", "unitodo-m-job", "unitodo-m-web")),
    4: ("aiud", ("unidoc",), ("unidoc-m-server", "unidoc-m-job", "unidoc-m-web")),
    5: ("aiun", ("uninoti",), ("uninoti-m-server", "uninoti-m-job", "uninoti-m-web")),
    6: ("aisr", ("unirobo",), ("unirobo-m-server", "unirobo-m-web")),
    7: ("aiir", ("uniinfo",), ("uniinfo-m-server", "uniinfo-m-job", "uniinfo-m-web")),
    8: ("aipp", ("unitpro",), ("unitpro-server", "unitpro-web", "unitpro-job")),
    9: ("aicsf", ("aicsf",), ("csf-console",)),
    10: ("aiaa", ("malarm",), ("malarm-server", "malarm-web", "malarm-job", "malarm-collection")),
}

pipelineId = {
    "base-server": "xxxxxxxxxxx",
    "m-uni-user-job": "xxxxxxxxxxx",
    "m-uni-user-rest": "xxxxxxxxxxx",
}

ftime = datetime.datetime.now().strftime('%Y%m%d')
baktime = datetime.datetime.now().strftime('%Y%m%d%M')

def Shell(cmd):
    cmd_list = cmd.split()
    cmd_shell = Popen(cmd_list, stdout=PIPE, stderr=PIPE)
    return cmd_shell.communicate()[1]

def rollback():
    try:
        projet_id = int(input("请选择项目名序号:"))
        for id, app in enumerate(projet_name_list[projet_id][2], start=1):
            print(id, app)
        projet_app_id = int(input("请选择应用序号:"))
        projet_dir = projet_name_list[projet_id][1][0]
        projet_app = projet_name_list[projet_id][2][projet_app_id-1]
        src_dir = ''.join([code_dir, projet_dir, '/', projet_app, '/'])
        image_log_file = ''.join([src_dir, "image.log"])
        print("请选择回退版本的方式!")
        print("###################################")
        print("1 回滚上一个版本")
        print("2 重新发部当前版本")
        print("3 指定历史版本回滚")
        print("4 退出脚本")
        print("###################################")
        history_version = int(input("请选择序号:"))
    except (KeyError, NameError, IndexError, ValueError):
        raise Exception("没有这个序号!")

    if not os.path.exists(image_log_file):
        raise Exception("由于还没有记录版本日志的文件,还不支持回滚功能!")

    page_cmd = "wc -l %s |awk '{print $1}'" % image_log_file
    page = int(os.popen(page_cmd).read())

    if history_version == 1:
        if page < 2:
            raise Exception("记录版本的日志小于2行,不能回退上一个版本,请到cicd流水线手动回退版本!") 
        get_image_cmd = "tail -2 %s |awk -F '.com/' '{print $2}'|head -1" % image_log_file
        image_name = os.popen(get_image_cmd).read()
    elif history_version == 2:
        if page < 1:
            raise Exception("日志没有记录版本,请到cicd流水线手动发部!")
        get_image_cmd = "tail -1 %s |awk -F '.com/' '{print $2}'" % image_log_file
        image_name = os.popen(get_image_cmd).read()
    elif history_version == 3:
        if page < 1:
            raise Exception("日志没有记录版本,请到cicd流水线手动发部!")
        all_image_version = "awk -F '.com/' '{print $2}' %s" % image_log_file
        image_version_list = os.popen(all_image_version).read().split()
        print("可回退的版本号列表")
        for i, v in enumerate(image_version_list, 1):
            print(i, v)
        print("退出脚本程序请按Ctrl+c或任意非数字键!")
        try:
            n = int(input("请选择回退版本的序号:"))
            image_name = image_version_list[n-1]
        except (KeyError, KeyboardInterrupt, IndexError, ValueError):
            raise Exception("选择的序号不存在,脚本程序已退出~")
    else:
        raise Exception("脚本程序已退出~")
        
    return {
        'projet_app': projet_app,
        'image_name': image_name,
        'src_dir': src_dir,
        } 

def get_info():
    try:
        projet_id = int(input("请选择项目名序号:"))
        projet_name = projet_name_list[projet_id][0]
        projet_dir = projet_name_list[projet_id][1][0]
        for id, app in enumerate(projet_name_list[projet_id][2], start=1):
            print(id, app)
        projet_app_id = int(input("请选择应用序号:"))
        projet_app = projet_name_list[projet_id][2][projet_app_id-1]
    except (KeyError, NameError, IndexError, ValueError):
        raise Exception("没有这个序号!")
        
    src_dir = ''.join([code_dir, projet_dir, '/', projet_app, '/'])
    last_version = float(0)
    image_log_file = ''.join([src_dir, "image.log"])
    if os.path.exists(image_log_file):
        is_image = "grep {TIME} {IMAGE_LOG_FILE}".format(TIME=ftime, IMAGE_LOG_FILE=image_log_file)
        code_status = os.popen(is_image).read()
        if code_status not in '':
            get_version_cmd = "tail -1 %s |awk -F '[ ]+' '{print $2}'" % image_log_file
            last_image = os.popen(get_version_cmd).read()
            last_version = float(last_image.split("v")[-1].strip())
    projet_version = 'v' + str(last_version + 0.1)
    image_name = ''.join([projet_name, "/", projet_app, ":", environment, "-", ftime, "-", projet_version])
    image = ''.join([Harbor_url, '/', image_name])
    print("镜像名是:{IMAGE_NAME}".format(IMAGE_NAME=image))
    print("如果正确输入y推送镜像并发部服务，退出按n")
    go = str(input(":"))
    if go not in ('y', 'Y'):
        raise Exception("脚本已退出~")

    data = {
        'projet_id': projet_id,
        'projet_name': projet_name,
        'projet_dir': projet_dir,
        'projet_app': projet_app,
        'projet_version': projet_version,
        'image': image,
        'image_name': image_name,
        'src_dir': src_dir,
        'image_log_file': image_log_file,
    }

    return data

def mv_code():
    projet_dir, projet_app, src_dir = data['projet_dir'], data['projet_app'], data['src_dir']
    tar = ''.join([upload_dir, projet_dir, '/', projet_app, '/', '*gz'])
    jar = ''.join([upload_dir, projet_dir, '/', projet_app, '/', '*jar'])
    code_file = glob.glob(tar)
    if len(code_file) == 0:
        code_file = glob.glob(jar)
    if len(code_file) == 1:
        src_tar = src_dir + '{app}*.gz'.format(app=projet_app)
        src_jar = src_dir + '{app}*.jar'.format(app=projet_app)
        src_file = glob.glob(src_tar)
        if len(src_file) == 0:
            src_file = glob.glob(src_jar)
        if len(src_file) == 1:
            backup_path = ''.join([src_dir, 'backup/'])
            backup_file = ''.join([baktime, '-', src_file[0].split('/')[-1]])
            if not os.path.exists(backup_path):
                os.makedirs(backup_path)
            print("是否备份上一版的代码包,y or n")
            backup = str(input(":"))
            if backup in ('y', 'Y'):
                shutil.move(src_file[0], ''.join([backup_path, backup_file]))
                print("备份成功,名称是:{backup_name}".format(backup_name=backup_file))
        if len(src_file) > 1:
            raise Exception("源代码目录存在多余的code文件,请进入{dir}目录清理多余的文件!".format(dir=src_dir))
        try:
            if '-release' in code_file[0]:
                # src_code_file = code_file[0].replace("-release", "")
                a, b = code_file[0].split('/')[-1].split('-release')
                src_code_file = ''.join([src_dir, a, b])
                shutil.copy2(code_file[0], src_code_file)
                os.remove(code_file[0])
                print("代码包名release的字符串已去除掉")
                print("代码已移动到部署目录,正在构建镜像...")
                return
            else:
                shutil.copy2(code_file[0], src_dir)
                os.remove(code_file[0])
                print("代码已移动到部署目录,正在构建镜像...")
                return
        except FileNotFoundError as e:
            print("代码包移动失败!")
            raise Exception(e)
    else:
        raise Exception("上传目录代码包不等于1,请检查上传代码目录:{Dir}".format(Dir=''.join([upload_dir, projet_dir, '/', projet_app, '/'])))

def push_images():
    projet_name, projet_app, projet_version, src_dir, image = data['projet_name'], data['projet_app'], data['projet_version'], data['src_dir'], data['image']
    build_cmd = "sudo docker build --no-cache -t {HARBOR_URL}/{PROJET_NAME}/{PROJET_APP}:{ENVIRONMENT}-{TIME}-{VERSION} -f {DOCKERFILE} {BUILD_PATH}".format(
        HARBOR_URL = Harbor_url,
        PROJET_NAME = projet_name,
        PROJET_APP = projet_app,
        ENVIRONMENT = environment,
        TIME = ftime,
        VERSION = projet_version,
        DOCKERFILE = ''.join([src_dir, "Dockerfile"]),
        BUILD_PATH = src_dir
    )
    push_cmd = "sudo docker push {HARBOR_URL}/{PROJET_NAME}/{PROJET_APP}:{ENVIRONMENT}-{TIME}-{VERSION}".format(
        HARBOR_URL = Harbor_url,
        PROJET_NAME = projet_name,
        PROJET_APP = projet_app,
        ENVIRONMENT = environment,
        TIME = ftime,
        VERSION = projet_version
    )
    
    code_tag = Shell(build_cmd)
    if code_tag is '':
        print("镜像已完成构建")
    else:
        if 'too many links' in code_tag:
            print("镜像仓库满了,正在清理镜像,请稍等...")
            Shell("sh /home/aiadmin/yx_images/rm_image_all.sh")
            print("镜像清理完毕，正在重新构建镜像")
            code_tag = Shell(build_cmd)
            if code_tag is '':
                print("镜像已完成构建")
            else:
                print(code_tag)
                Shell("touch {image_dir}push.lock".format(image_dir=src_dir))
                raise Exception("镜像build失败!请进入[{image_dir}]目录手动执行[{shell}]命令检查错误!".format(image_dir=src_dir, shell=build_cmd))
        else:
            print(code_tag)
            Shell("touch {image_dir}push.lock".format(image_dir=src_dir))
            raise Exception("镜像build失败!请进入[{image_dir}]目录手动执行[{shell}]命令检查错误!".format(image_dir=src_dir, shell=build_cmd))

    code_tag = Shell(push_cmd)
    if code_tag is '':
        print("已推送到镜像仓库,镜像版本是: {IMAGE_NAME}".format(IMAGE_NAME=image))
        file_path = data['image_log_file'] 
        with open(file_path, 'a') as f:
            f.write("{TIME} {IMAGE_NAME}\n".format(TIME=ftime, IMAGE_NAME=image))
    else:
        print(code_tag)
        Shell("touch {image_dir}push.lock".format(image_dir=src_dir))
        raise Exception("harbor仓库不可达!")

def deploy_api():
    try:
        projet_app, image_name, src_dir = data['projet_app'], data['image_name'], data['src_dir']
        headers = {"Content-Type": "application/json"}
        parameter = {
            "pipelineId": pipelineId[projet_app],
            "${imageName}": image_name,
        }
        json_data = json.dumps(parameter).encode(encoding='utf-8')
        result = requests.post(pass_url, data=json_data, headers=headers)
        print(result)
        json_data = result.json()
        print(json_data)
    except ValueError:
        print("调用paas接口过于频繁,请登录pass平台手动编辑镜像版本发部,或者稍后重新执行脚本尝试~")
        print("1 登录pass平台手动发部镜像")
        print("2 稍后重新执行脚本尝试")
        runid = int(input("请选择序号:"))
        if runid == 2:
            Shell("touch {image_dir}push.lock".format(image_dir=src_dir))
        return

def code_jar_or_tar():
    mv_code()
    push_images()
    time.sleep(10)
    deploy_api()

def reload_push(lock_file):
    push_images()
    os.remove(lock_file)
    time.sleep(10)
    deploy_api()

def main():
    global data
    print("是否回滚应用版本,y or n:")
    y = str(input(":"))
    if y in 'yY':
        data = rollback()
        deploy_api()
        sys.exit(0)        
    data = get_info()
    projet_app, src_dir = data['projet_app'], data['src_dir']
    if not os.path.exists(''.join([src_dir, "Dockerfile"])):
        print("没有Dockerfile文件,请查看工程目录:{JobDir}".format(JobDir=src_dir))
        sys.exit(1)
    if os.path.exists(''.join([src_dir, "push.lock"])):
        print("由于上一次镜像构建或推送失败,正在重新推送镜像...")
        reload_push(''.join([src_dir, "push.lock"]))
    else:
        code_jar_or_tar()

if __name__ == '__main__':
    main()
