#!/usr/bin/env python
# coding: utf-8

import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import RamRoleArnCredential
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from aliyunsdkrds.request.v20140815 import DescribeBackupsRequest,DescribeBinlogFilesRequest
import urllib
import datetime


class AliyunEcs(object):
    def __init__(self):
        self.ram_role_arn_credential = RamRoleArnCredential('*******', '**********', '********', '*****')
        self.acs_client = AcsClient(region_id='cn-beijing', credential=self.ram_role_arn_credential)

    def InfoList(self):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_PageSize(100)
        request.set_accept_format('json')
        response = json.loads(self.acs_client.do_action_with_exception(request).decode('utf-8'))
        info_list = response.get('Instances').get('Instance')
        return info_list

    def Ecsinfo(self):
        #遍历获取到的结果
        global ecs_list
        info_list = self.InfoList()
        ecs_list = []
        for info in info_list:
            region = info.get('RegionId') #cn-beijing
            description = info.get('Description') #功能描述
            primaryIpAddress = info.get('NetworkInterfaces').get('NetworkInterface')[0]['PrimaryIpAddress'] #私有ip
            ecsName = info.get('InstanceName') #实例名字
            hostName = info.get('HostName')  #主机名
            zone = info.get('ZoneId') #cn-beijing-e
            ecsType = info.get('InstanceType') #ecs规格类型
            cpu = str(info.get('Cpu')) #cpu
            mem = str(info.get('Memory')) #mem
            status = info.get('Status') #运行状态
            instanceNetworkType = info.get('InstanceNetworkType') #内网网络类型
            osName = info.get('OSName') #系统类型
            eipAddress = info.get('EipAddress').get('IpAddress') #弹性ip
            tags = info.get('Tags').get('Tag')[0]['TagKey'] #标签
            if info.get('EipAddress').get('IpAddress'):
                ipAddress = info.get('EipAddress').get('IpAddress')
            else:
                ipAddress = ''
            ecs_list.append({'region':region, 'description':description, 'primaryIpAddress':primaryIpAddress, 'ecsName':ecsName,
                             'hostName':hostName, 'zone':zone, 'ecsType':ecsType, 'cpu':cpu, 'mem':mem, 'status':status,
                             'instanceNetworkType':instanceNetworkType, 'osName':osName, 'eipAddress':eipAddress, 'tags':tags})
        return ecs_list

class AliyunRds(object):
    def __init__(self):
        self.ram_role_arn_credential = RamRoleArnCredential('******', '*****', '*****', '****')
        self.acs_client = AcsClient(region_id='cn-beijing', credential=self.ram_role_arn_credential)

    #获得时间需要备份的时间范围
    def getdate(self):
        today_time = datetime.datetime.now()
        date1 = datetime.datetime.strftime(today_time, '%Y-%m-%d')  # +‘T00:00:00Z‘
        yes_time = today_time + datetime.timedelta(days=-2)
        date2 = datetime.datetime.strftime(yes_time, '%Y-%m-%d') #  +‘T00:00:00Z‘
        # print(date1)
        # print(date2)
        global start_date
        global end_date
        start_date = date2
        end_date = date1

        return 0

    # 拉取指定db_instanceid的备份文件
    def downfullbackupfile(slef, db_instanceid):
        startdate = start_date + 'T00:00Z'
        enddate = end_date + 'T00:00Z'
        request = DescribeInstancesRequest.DescribeInstancesRequest()


if __name__ == '__main__':
    obj = AliyunRds()
    obj.getdate()
