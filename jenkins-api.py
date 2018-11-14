# -*- coding: utf-8 -*-
import jenkins

class Jenkins_Api():
    def __init__(self, url, user, passwd):
        self.url = url
        self.name = user
        self.passwd = passwd
        
       
    def Build_jenkins(self, jobname, demo='master'):
        j = jenkins.Jenkins(self.url, username=self.name, password=self.passwd)
        if isinstance(demo, str):
            data = {'demo': demo}
        job_all = j.get_all_jobs()
        job = [i['name'] for i in job_all if i['name'] == jobname][0]
        if j.build_job(job, parameters=data):
           return "{job_name} 构建成功~".format(job_name=job)
        else:
           return "{job_name} 构建失败!".format(job_name=job)

obj = Jenkins_Api(url, user, passwd)                #写上自己的jenkins URL 用户和密码
print obj.Build_jenkins('ansible-cby', demo='test') #构建项目，第一个参数是项目名称，第二个是自定义的变量，我把分支作为变量
