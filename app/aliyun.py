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
        self.ram_role_arn_credential = RamRoleArnCredential('LTAIfu2302ttWJwj', 'ajuLGBtgvZAHI0sYZyGt91Ko8kEtv9', 'acs:ram::1141210562526049:role/ramecs', 'ramecs')
        self.acs_client = AcsClient(region_id='cn-beijing', credential=self.ram_role_arn_credential)
# ram_role_arn_credential = RamRoleArnCredential('LTAIfu2302ttWJwj', 'ajuLGBtgvZAHI0sYZyGt91Ko8kEtv9', 'acs:ram::1141210562526049:role/ramecs', 'ramecs')
# acs_client = AcsClient(region_id='cn-beijing', credential=ram_role_arn_credential)
    def InfoList(self):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_PageSize(100)
        request.set_accept_format('json')
        response = json.loads(self.acs_client.do_action_with_exception(request).decode('utf-8'))
        info_list = response.get('Instances').get('Instance')
        return info_list

    def Ecsinfo(self):
        #遍历获取到的结果
        '''
        {'SerialNumber': '2468aff9-b44e-432a-b30d-03859592540c', 'PublicIpAddress': {'IpAddress': []}, 
        'SpotPriceLimit': 0.0, 'CreationTime': '2018-02-05T06:51Z', 'RegionId': 'cn-beijing', 'Description': 'tvgateway_test', 
        'NetworkInterfaces': {'NetworkInterface': [{'MacAddress': '00:16:3e:0a:23:39', 'PrimaryIpAddress': '192.168.102.154', 
        'NetworkInterfaceId': 'eni-2ze2cmj721802z9xjxro'}]}, 'IoOptimized': True, 'StoppedMode': 'Not-applicable', 'Memory': 1024, 
        'InternetMaxBandwidthOut': 0, 'InstanceTypeFamily': 'ecs.xn4', 'GPUSpec': '', 'Status': 'Stopped', 'StartTime': '2018-02-05T07:05Z', 
        'ZoneId': 'cn-beijing-e', 'InstanceChargeType': 'PrePaid', 'VlanId': '', 'AutoReleaseTime': '', 'InternetChargeType': '', 
        'Tags': {'Tag': [{'TagValue': '', 'TagKey': 'dev'}]}, 'SpotStrategy': 'NoSpot', 'OperationLocks': {'LockReason': []}, 
        'HostName': 'tvgateway-test', 'ResourceGroupId': 'rg-aekz5bt6czidtdq', 'SaleCycle': '', 'DedicatedHostAttribute': {'DedicatedHostId': '', 'DedicatedHostName': ''}, 
        'InternetMaxBandwidthIn': -1, 'InstanceType': 'ecs.xn4.small', 'SecurityGroupIds': {'SecurityGroupId': ['sg-2ze2ciofo1tuo0452xh2']}, 
        'VpcAttributes': {'PrivateIpAddress': {'IpAddress': ['192.168.102.154']}, 'NatIpAddress': '', 'VSwitchId': 'vsw-2zevp6jgoywfhtc4j7baa', 
        'VpcId': 'vpc-2zeho9i16trggvxmhwipf'}, 'InstanceName': 'del_tvgateway_dev', 'Recyclable': False, 'ClusterId': '', 'Cpu': 1,
         'GPUAmount': 0, 'OSType': 'linux', 'ImageId': 'm-2ze8d4bgjt9168bmdyfj', 'ExpiredTime': '2018-08-29T16:00Z', 'DeviceAvailable': True, 
         'InnerIpAddress': {'IpAddress': []}, 'InstanceNetworkType': 'vpc', 'OSName': 'CentOS  7.3 64位', 'InstanceId': 'i-2ze0q1y5411u30f464qi', 
         'EipAddress': {'InternetChargeType': 'PayByBandwidth', 'IpAddress': '39.106.182.84', 'Bandwidth': 1, 'IsSupportUnassociate': True, 
         'AllocationId': 'eip-2zeaahd7kosc5yenxgovm'}}
        '''
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
        self.ram_role_arn_credential = RamRoleArnCredential('LTAIfu2302ttWJwj', 'ajuLGBtgvZAHI0sYZyGt91Ko8kEtv9', 'acs:ram::1141210562526049:role/ramecs', 'ramecs')
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
