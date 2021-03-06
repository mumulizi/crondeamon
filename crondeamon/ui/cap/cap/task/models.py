#coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/6/15.
# ---------------------------------
from django.db import  models
import  datetime



def int_to_hexstring(intvalue):
    result=hex(intvalue)
    result=result.strip("L")
    result=result.strip("0x")
    return  result

class Task(models.Model):
    "后台任务的抽象"
    tid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,db_index=True,verbose_name="名称")
    ip=models.IPAddressField(db_index=True,verbose_name="IP")
    addtime=models.IntegerField(verbose_name="创建时间")
    edittime=models.IntegerField(verbose_name="修改时间")
    status=models.SmallIntegerField(verbose_name="状态")    # -1 停止    1 正在运行   0待部署  2 正在部署  3 部署失败
    svnpath=models.CharField(verbose_name="代码库svn路径",max_length=500)
    version=models.IntegerField(verbose_name="版本",default=0)
    svnuser=models.CharField(verbose_name="SVN用户",max_length=30)
    svnpasswd=models.CharField(verbose_name="SVN密码",max_length=50)
    info=models.CharField(verbose_name="说明",max_length=500)
    owner=models.CharField(verbose_name="所属人",db_index=True,max_length=200)
    args=models.CharField(verbose_name="参数",max_length=500)   #运行参数
    filename=models.CharField(verbose_name="执行文件名",max_length=500)




    class Meta:
        verbose_name="后台任务"
        verbose_name_plural="所有后台任务"
    def get_status(self):
        return {-1:"禁用",1:"启用",0:"待部署",2:"正在部署",3:"部署失败"}[self.status]
    def get_info(self):
        info=""
        num=0
        for i  in self.info:
            if 0<=ord(i)<=255:
                num+=1
            else:
                num+=2
            info+=i
            if num>=24:
                info+=".."
                break
        return info

    def get_name(self):
        name=""
        num=0
        for i  in self.name:
            if 0<=ord(i)<=255:
                num+=1
            else:
                num+=2
            #name+=i
            if num>18:
                #name+=".."
                break
            else:
                name+=i
        else:
            return self.name
        return name[0:-1]+".."

class Runlog(models.Model):
    "后台任务运行日志"
    rid=models.AutoField(primary_key=True)
    tid=models.IntegerField(db_index=True,verbose_name="task id")
    svnpath=models.CharField(verbose_name="代码库svn路径",max_length=100)
    version=models.IntegerField(verbose_name="版本",default=0)
    crontime=models.IntegerField(verbose_name="下发时间",default=0)
    begintime=models.IntegerField(verbose_name="开始时间戳",default=0)
    endtime=models.IntegerField(verbose_name="结束时间戳",default=0)
    status=models.IntegerField(verbose_name="状态",default=0)  #  0 待运行  1 正在运行  2 运行正常完成  3  运行异常退出
    stderror=models.TextField(verbose_name="标准错误")
    stdout=models.TextField(verbose_name="标准输出")
    type=models.SmallIntegerField(verbose_name="类型",default=0)   #0  Auto运行   1  手动触发
    class Meta:
        verbose_name="运行日志"
        verbose_name_plural="所有运行日志"
    def get_code_info(self,task=None):
        "获取代码信息"
        if task==None:
            pass
        return "版本{0}".format(self.version)

    def get_crondatetime(self):
        _time=datetime.datetime.fromtimestamp(self.crontime)
        return  _time.strftime("%Y-%m-%d %H:%M:%S")
    def get_begindatetime(self):
        if self.begintime!=0:
            _time=datetime.datetime.fromtimestamp(self.begintime)
            return  _time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return "--"
    def get_enddatetime(self):
        if self.endtime!=0:
            _time=datetime.datetime.fromtimestamp(self.endtime)
            return  _time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return  "--"
    def get_status(self):
        _config={0:"待运行",1:"正在运行",2:"运行正常完成",3:"运行异常退出"}
        return  _config[self.status]
    def get_type(self):
        _config={0:"Auto",1:"custom"}
        return  _config[self.type]
