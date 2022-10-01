import copy

from django.shortcuts import render
from rest_framework.views import APIView,status

import Main.models
from Main import models
from django.core import serializers
from django.http import HttpResponse,JsonResponse
import json
import jwt
import datetime
from jwt import exceptions
import time

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkiot.request.v20180120.QueryDevicePropertyStatusRequest import QueryDevicePropertyStatusRequest

# Create your views here.

import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "防疫小程序.settings")
django.setup()

class signIn(APIView):
    def post(self,request,*args,**kwargs):
        phone = request.data.get('phone')
        password = request.data.get('password')
        record = models.UserInfo.objects.filter(phone = phone)
        recorda = models.UserInfo.objects.filter(password =
                                                 password)
        if len(record) == 0:
            return HttpResponse("账号错误")
        else:
            info = models.UserInfo.objects.get(phone=phone)
            dict = []
            if len(recorda) == 0:
                return HttpResponse("密码错误")
            else:
                dict.insert(0,info.name)
                dict.insert(1,",")
                dict.insert(2,info.phone)
                dict.insert(3,",")
                dict.insert(4,info.Identify)
                dict.insert(5,",")
                dict.insert(6,info.address)
                dict.insert(7,",")
                dict.insert(8,info.picture)
                print(dict)
                return HttpResponse(dict)

class CheckPassward(APIView):
    def post(self,requset,*args,**kwargs):
        name = requset.data.get('name')
        newpassward = requset.data.get('newpassward')
        Info = models.UserInfo.objects.get(name=name)
        Info.password = newpassward
        Info.save()
        return HttpResponse("Success")

class EpidmicOrder(APIView):
    def post(self,request,*args,**kwargs):
        model = request.data.get('model')
        name = model['children']['children']['name']
        phone = model['children']['children']['phone']
        identify = model['children']['children']['idNum']
        address = model['children']['children']['address']
        mapaddress = model['mapaddress']
        time = model['children']['time']
        models.EpidmicPrevention.objects.create(name=name,phone=phone,identify=identify,adress=address,epidmedicStation=mapaddress,time=time)
        return HttpResponse("Success")

class Register(APIView):
    def post(self,request,*args,**kwargs):
        phone = request.data.get('phoneNumber')
        password = request.data.get('password')

class HealthyPost(APIView):
    def post(self,request,*args,**kwargs):
        name = request.data.get('name')
        phone = request.data.get('phone')
        identify = request.data.get('idNum')
        address = request.data.get('address')
        time1 = time.strftime('%Y.%m.%d.%H.%M', time.localtime(time.time()))
        status = request.data.get('status')
        temperature = request.data.get('temperature')
        comment = request.data.get('comment')
        if status == '0':
            status_true = '正常'
        else:
            status_true = '发烧'
        models.Healthy.objects.create(name=name,phone=phone,Identify=identify,address=address,status=status_true,temperature=temperature,comment=comment,time=time1)
        return HttpResponse("Success")

class urgencyPost(APIView):
    def post(self,request,*args,**kwargs):
        content = request.data.get('content')
        phone = request.data.get('phone')
        time1 = time.strftime('%Y.%m.%d.%H.%M', time.localtime(time.time()))
        models.urgency.objects.create(phone=phone,content=content,time=time1)
        return HttpResponse("添加成功")


class loginWeb(APIView):
    def post(self,request,*args,**kwargs):
        print(222)
        usernames = request.data.get('username')
        password = request.data.get('password')
        record = models.info.objects.filter(usernames=usernames)
        recorda = models.info.objects.filter(password = password)
        if len(record) == 0:
            return HttpResponse("账号错误")
        else:
            info = models.info.objects.get(usernames=usernames)
            dict = []
            if len(recorda) == 0:
                return HttpResponse("密码错误")
            else:

                SALT = 'django-insecure-^x9h()pfn8%i!$03*d3y-$5zqb7euh4#w2&^87v*x!f16ull*7'
                headers = {
                    'typ': 'jwt',
                    'alg': 'HS256'
                }
                # 构造payload
                payload = {
                    'id': 1,  # 自定义用户ID
                    'username': 'admin',  # 自定义用户名
                    'code':20000,
                    'password':111111,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)  # 超时时间
                }

                result = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers).encode('utf-8').decode('utf-8')
                print(result)

                dictoo = {
                    "code":20000,
                    "data":{
                        "token": result}
                }
                print(dictoo)
                return JsonResponse(dictoo)

class getWebtoken(APIView):
    def get(self,request,*args,**kwargs):
        token = request.query_params.get('token')
        print(token)
        SALT = 'django-insecure-^x9h()pfn8%i!$03*d3y-$5zqb7euh4#w2&^87v*x!f16ull*7'
        vpayload = None
        msg = None
        try:
            print("h")
            vpayload = jwt.decode(token, SALT,"HS256")
        except exceptions.ExpiredSignatureError:
            msg = 'token已失效'
        except jwt.DecodeError:
            msg = '认证失败'
        except jwt.InvalidTokenError:
            msg = '非法认证'
        if not vpayload:
            return HttpResponse({'code':1003,'error':msg})

        print(vpayload['id'],vpayload['username'])
        print(vpayload)
        return JsonResponse(vpayload)

class webLogout(APIView):
    def post(self,request,*args,**kwargs):
        token = request.query_params.get('token')
        print(token)
        token = None
        dictoo = {
            "code": 20000,
            "data":"推出成功"
        }
        return JsonResponse(dictoo)

class webHealthy_get(APIView):
    def get(self,request,*args,**kwargs):
        datas = models.Healthy.objects.all()
        print(datas)
        return HttpResponse(datas)

class showNews(APIView):
    def get(self,request,*args,**kwargs):
        allnews = serializers.serialize("json",models.New.objects.all())
        news = json.loads(allnews)
        dict = {'id':0,'title':'','content':'','Date':''}
        length = len(news)
        data = []
        for i in range(length):
            # print(i)
            dict['id'] = i + 1
            dict['title'] = news[i]['fields']['title']
            dict['content'] = news[i]['fields']['content']
            dict['Date'] = news[i]['fields']['Date']
            # print(dict)
            data.append(dict.copy())
        # print(data)
        dictoo = {
            "code": 20000,
            "data":data
        }
        return JsonResponse(dictoo)

class addNews(APIView):
    def post(self,request,*args,**kwargs):
        title = request.data.get('title')
        content = request.data.get('content')
        time1 = time.strftime('%Y.%m.%d.%H.%M',time.localtime(time.time()))
        models.New.objects.create(title=title,content=content,Date=time1)
        dictoo = {
            "code": 20000,
            "data":"添加成功"
        }
        return JsonResponse(dictoo)

class editNews(APIView):
    def post(self,request,*args,**kwargs):
        title = request.data.get('title')
        content = request.data.get('content')
        time1 = time.strftime('%Y.%m.%d.%H.%M',time.localtime(time.time()))
        try:
            tem = models.New.objects.get(title=title)
        except Main.models.New.DoesNotExist:
            try:
                tem = models.New.objects.get(content=content)
            except:
                print("不能这样操作")

        tem.title = title
        tem.content = content
        tem.Date = time1
        tem.save()
        dictoo = {
            "code": 20000,
            "data":"编辑成功"
        }
        return JsonResponse(dictoo)

class deletNews(APIView):
    def post(self,request,*args,**kwargs):
        title1 = request.data.get('title')
        models.New.objects.filter(title=title1).delete()
        dictoo = {
            "code": 20000,
            "data":"删除成功"
        }
        return JsonResponse(dictoo)

class showUrgency(APIView):
    def get(self,request,*args,**kwargs):
        allurgency = serializers.serialize("json", models.urgency.objects.all())
        urgency = json.loads(allurgency)
        dict = {'id':0,'time':'','title':'','phone':''}
        length = len(urgency)
        data = []
        for i in range(length):
            print(i)
            dict['id'] = i + 1
            dict['time'] = urgency[i]['fields']['time']
            dict['title'] = urgency[i]['fields']['content']
            dict['phone'] = urgency[i]['fields']['phone']
            print(dict)
            data.append(dict.copy())
        print(data)
        dictoo = {
            "code": 20000,
            "data":data
        }
        return JsonResponse(dictoo)

class deletUrgency(APIView):
    def post(self,request,*args,**kwargs):
        content = request.data.get('title')
        models.urgency.objects.filter(content=content).delete()
        dictoo = {
            "code": 20000,
            "data":"删除成功"
        }
        return JsonResponse(dictoo)

class addJumin(APIView):
    def post(self,request,*args,**kwargs):
        name = request.data.get('name')
        idNum = request.data.get('idNum')
        phone = request.data.get('phone')
        address = request.data.get('address')
        models.JuMin.objects.create(name=name,identify=idNum,phone=phone,address=address)
        dictoo = {
            "code": 20000,
            "data":"添加成功"
        }
        return JsonResponse(dictoo)

class showJumin(APIView):
    def get(self,request,*args,**kwargs):
        alljumin = serializers.serialize("json", models.JuMin.objects.all())
        jumin = json.loads(alljumin)
        dict = {'id':0,'name':'','idNum':'','phone':'','address':''}
        print(jumin)
        length = len(jumin)
        data = []
        for i in range(length):
            # print(i)
            dict['id'] = i + 1
            dict['name'] = jumin[i]['fields']['name']
            dict['idNum'] = jumin[i]['fields']['identify']
            dict['phone'] = jumin[i]['fields']['phone']
            dict['address'] = jumin[i]['fields']['address']
            # print(dict)
            data.append(dict.copy())
        # print(data)
        dictoo = {
            "code": 20000,
            "data":data
        }
        return JsonResponse(dictoo)

class webOrder(APIView):
    def get(self,request,*args,**kwargs):
        all = models.EpidmicPrevention.objects.all()
        allstation = models.Stationinfo.objects.all()
        # name = ['计算机学院','东餐厅']
        name = []
        for i in allstation:
            name.append(i.station)
        station = {}
        for i in name:
            station[i] = []
        already = []
        # station = {'计算机学院':[],'东餐厅':[]}
        for i in all:
            if len(station[i.epidmedicStation]) != 0:
                index2 = 0
                for j in station[i.epidmedicStation]:
                    if i.time == j:

                        index2 = -1

                        continue
                if index2 == 0:
                    station[i.epidmedicStation].append(i.time)

                    # else:
                    #     station[i.epidmedicStation].append(i.time)
            else:
                station[i.epidmedicStation].append(i.time)
        print(station)
        for i in name:
            if len(station[i]) == 0:
                station.pop(i)
        print(station)
        tableDate = []
        Date1 = {'mapaddress':'','sum':0,'children':[]}
        Date2 = {'time':'','yuyue':0,'csum':1000,'children':[]}
        Date3 = {'name':'','idNum':'','phone':'','address':''}
        for i in all:
            if len(tableDate) == 0:
                Date1['mapaddress'] = i.epidmedicStation
                Date1['sum'] = Date1['sum'] + 1
                Date2['time'] = i.time
                Date2['yuyue'] = Date2['yuyue'] + 1
                Date3['name'] = i.name
                Date3['idNum'] = i.identify
                Date3['phone'] = i.phone
                Date3['address'] = i.adress
                Date2['children'].append(Date3.copy())
                Date1['children'].append(Date2.copy())
                tableDate.append(Date1.copy())
                Date1 = {'mapaddress': '', 'sum': 0, 'children': []}
                Date2 = {'time': '', 'yuyue': 0, 'csum': 1000, 'children': []}
                Date3 = {'name': '', 'idNum': '', 'phone': '', 'address': ''}
                index1 = 0
                for r in already:
                    if i.epidmedicStation == r:
                        index1 = -1
                if index1 == 0:
                    already.append(i.epidmedicStation)
                # print(tableDate)
            else:
                v = copy.deepcopy(tableDate)
                for j in v:
                    if i.epidmedicStation == j['mapaddress']:
                        k = copy.deepcopy(j['children'])
                        index4 = 0
                        for t in k:
                            # print(i.time)
                            # print(t['time'])
                            if i.time == t['time']:
                                u = j
                                tableDate[tableDate.index(j)]['children'][j['children'].index(t)]['yuyue'] = tableDate[tableDate.index(j)]['children'][j['children'].index(t)]['yuyue'] + 1
                                j['children'][j['children'].index(t)]['yuyue'] = j['children'][j['children'].index(t)]['yuyue'] + 1
                                t['yuyue'] = t['yuyue'] + 1
                                tableDate[tableDate.index(j)]['sum'] = tableDate[tableDate.index(j)]['sum'] + 1
                                j['sum'] = j['sum'] + 1
                                Date3['name'] = i.name
                                Date3['idNum'] = i.identify
                                Date3['phone'] = i.phone
                                Date3['address'] = i.adress
                                tableDate[tableDate.index(j)]['children'][j['children'].index(t)]['children'].append(Date3.copy())
                                j['children'][j['children'].index(t)]['children'].append(Date3.copy())
                                # t['children'].append(Date3.copy())
                                Date1 = {'mapaddress': '', 'sum': 0, 'children': []}
                                Date2 = {'time': '', 'yuyue': 0, 'csum': 1000, 'children': []}
                                Date3 = {'name': '', 'idNum': '', 'phone': '', 'address': ''}
                                index4 = -1
                                break
                        if index4 == 0:
                            Date2['yuyue'] = Date2['yuyue'] + 1
                            tableDate[tableDate.index(j)]['sum'] = tableDate[tableDate.index(j)]['sum'] + 1
                            j['sum'] = j['sum'] + 1
                            Date2['time'] = i.time
                            Date3['name'] = i.name
                            Date3['idNum'] = i.identify
                            Date3['phone'] = i.phone
                            Date3['address'] = i.adress
                            Date2['children'].append(Date3.copy())
                            tableDate[tableDate.index(j)]['children'].append(Date2.copy())
                            j['children'].append(Date2.copy())
                            Date1 = {'mapaddress': '', 'sum': 0, 'children': []}
                            Date2 = {'time': '', 'yuyue': 0, 'csum': 1000, 'children': []}
                            Date3 = {'name': '', 'idNum': '', 'phone': '', 'address': ''}
                            # else:
                            #     Date2['yuyue'] = Date2['yuyue'] + 1
                            #     tableDate[tableDate.index(j)]['sum'] = tableDate[tableDate.index(j)]['sum'] + 1
                            #     j['sum'] = j['sum'] + 1
                            #     Date2['time'] = i.time
                            #     Date3['name'] = i.name
                            #     Date3['idNum'] = i.identify
                            #     Date3['phone'] = i.phone
                            #     Date3['address'] = i.adress
                            #     Date2['children'].append(Date3.copy())
                            #     tableDate[tableDate.index(j)]['children'].append(Date2.copy())
                            #     j['children'].append(Date2.copy())
                            #     Date1 = {'mapaddress': '', 'sum': 0, 'children': []}
                            #     Date2 = {'time': '', 'yuyue': 0, 'csum': 1000, 'children': []}
                            #     Date3 = {'name': '', 'idNum': '', 'phone': '', 'address': ''}
                        break
                    else:
                        for q in already:
                            index = 0
                            if q == i.epidmedicStation:
                                continue
                            else:
                                index = -1
                        if index == -1:
                            Date1['mapaddress'] = i.epidmedicStation
                            Date1['sum'] = Date1['sum'] + 1
                            Date2['time'] = i.time
                            Date3['name'] = i.name
                            Date3['idNum'] = i.identify
                            Date3['phone'] = i.phone
                            Date3['address'] = i.adress
                            Date2['yuyue'] = Date2['yuyue'] + 1
                            Date2['children'].append(Date3.copy())
                            Date1['children'].append(Date2.copy())
                            tableDate.append(Date1.copy())
                            Date1 = {'mapaddress': '', 'sum': 0, 'children': []}
                            Date2 = {'time': '', 'yuyue': 0, 'csum': 1000, 'children': []}
                            Date3 = {'name': '', 'idNum': '', 'phone': '', 'address': ''}
                            already.append(i.epidmedicStation)

        print(tableDate)
        dictoo = {
            "code": 20000,
            "data":tableDate
        }


        return JsonResponse(dictoo)


class setJumin(APIView):
    def post(self,request,*args,**kwargs):
        name = request.data.get('name')
        idNum = request.data.get('idNum')
        phone = request.data.get('phone')
        address = request.data.get('address')
        try:
            tep = models.JuMin.objects.get(name=name)
        except Main.models.JuMin.DoesNotExist:
            try:
                tep = models.JuMin.objects.get(identify=idNum)
            except Main.models.JuMin.DoesNotExist:
                try:
                    tep = models.JuMin.objects.get(phone=phone)
                except Main.models.JuMin.DoesNotExist:
                    tep = models.JuMin.objects.get(address=address)

        tep.name = name
        tep.identify = idNum
        tep.phone = phone
        tep.address = address
        tep.save()
        dictoo = {
            "code": 20000,
            "data":"修改成功"
        }
        return JsonResponse(dictoo)

class deletJumin(APIView):
    def post(self,request,*args,**kwargs):
        name = request.data.get('name')
        models.JuMin.objects.filter(name=name).delete()
        dictoo = {
            "code": 20000,
            "data":"删除成功"
        }
        return JsonResponse(dictoo)

class addClock(APIView):
    def post(self,request,*args,**kwargs):
        name = request.data.get('name')
        temperature = request.data.get('temperature')
        status = request.data.get('status')
        address = request.data.get('address')
        comment = request.data.get('comment')
        time1 = time.strftime('%Y.%m.%d.%H.%M', time.localtime(time.time()))
        models.Healthy.objects.create()

class addSelfCheck(APIView):
    def post(self,request,*args,**kwargs):
        name = request.data.get('name')
        phone = request.data.get('phone')
        identify = request.data.get('idNum')
        status = request.data.get('status')
        address = request.data.get('address')
        if status == '0':
            status_true = '阴性'
        else:
            status_true = '阳性'
        models.SelfChecked.objects.create(name=name,phone=phone,identify=identify,status=status_true,address=address)
        dictoo = {
            "code": 20000,
            "data":"添加成功"
        }
        return JsonResponse(dictoo)

class showzijian(APIView):
    def get(self,request,*args,**kwargs):
        allselfs = serializers.serialize("json", models.SelfChecked.objects.all())
        selfs = json.loads(allselfs)
        dict = {'name': '', 'idNum': '', 'phone': '', 'address': '','jieguo':''}
        length = len(selfs)
        data = []
        for i in range(length):
            # print(i)
            dict['id'] = i + 1
            dict['name'] = selfs[i]['fields']['name']
            dict['idNum'] = selfs[i]['fields']['identify']
            dict['phone'] = selfs[i]['fields']['phone']
            dict['jieguo'] = selfs[i]['fields']['status']
            dict['address'] = selfs[i]['fields']['address']
            # print(dict)
            data.append(dict.copy())
        # print(data)
        dictoo = {
            "code": 20000,
            "data":data
        }
        return JsonResponse(dictoo)

class deletzijian(APIView):
    def post(self,request,*args,**kwargs):
        name = request.data.get('name')
        models.SelfChecked.objects.filter(name=name).delete()
        dictoo = {
            "code": 20000,
            "data":"添加成功"
        }
        return JsonResponse(dictoo)

class showHealthy(APIView):
    def get(self,request,*args,**kwargs):
        allhealthy = serializers.serialize("json", models.Healthy.objects.all())
        selfs = json.loads(allhealthy)
        dict = {'name': '', 'temperature': '', 'phone': '', 'address': '', 'time': '','comment':'','status':''}
        length = len(selfs)
        data = []
        for i in range(length):
            # print(i)
            dict['name'] = selfs[i]['fields']['name']
            dict['temperature'] = selfs[i]['fields']['temperature']
            dict['phone'] = selfs[i]['fields']['phone']
            dict['idNum'] = selfs[i]['fields']['Identify']
            dict['address'] = selfs[i]['fields']['address']
            dict['time'] = selfs[i]['fields']['time']
            dict['comment'] = selfs[i]['fields']['comment']
            dict['status'] = selfs[i]['fields']['status']
            # print(dict)
            data.append(dict.copy())
        # print(data)
        dictoo = {
            "code": 20000,
            "data":data
        }
        return JsonResponse(dictoo)

class addhealthy(APIView):
    def post(self,request,*args,**kwargs):
        name = request.data.get('name')
        temperature = request.data.get('temperature')
        address = request.data.get('address')
        status = request.data.get('status')
        phone = request.data.get('phone')
        idNum = request.data.get('idNum')
        comment = request.data.get('comment')
        time1 = time.strftime('%Y.%m.%d.%H.%M', time.localtime(time.time()))
        models.Healthy.objects.create(name=name,temperature=temperature,address=address,status=status,phone=phone,comment=comment,time=time1,Identify=idNum)
        dictoo = {
            "code": 20000,
            "data":"添加成功"
        }
        return JsonResponse(dictoo)

class addStation(APIView):
    def post(self,request,*args,**kwarfs):
        station = request.data.get('mapaddress')
        longtiude = request.data.get('lng')
        latitude = request.data.get('lat')
        models.Stationinfo.objects.create(station=station,longitude=longtiude,latitude=latitude)
        dictoo = {
            "code": 20000,
            "data":"添加成功"
        }
        return JsonResponse(dictoo)

class showStation(APIView):
    def get(self,request,*args,**kwargs):
        allstation = models.Stationinfo.objects.all()
        maps = []
        dict = {'id':0,'lng':'','lat':'','mapaddress':''}
        for i in allstation:
            dict['id'] = i.id
            dict['lng'] = i.longitude
            dict['lat'] = i.latitude
            dict['mapaddress'] = i.station
            maps.append(dict.copy())
        print(maps)
        dictoo = {
            "code": 20000,
            "data":maps
        }
        return JsonResponse(dictoo)

class getStation(APIView):
    def get(self,request,*args,**kwargs):
        allstation = models.Stationinfo.objects.all()
        stations = []
        j = 0
        for i in allstation:
            if j == 2 * len(allstation) - 2:
                stations.insert(j, i.station)
                j = j + 1
            else:
                stations.insert(j, i.station)
                j = j + 1
                stations.insert(j, ',')
                j = j + 1
        print(stations)
        return HttpResponse(stations)

class getmaps(APIView):
    def get(self,request,*args,**kwargs):
        all = models.Stationinfo.objects.all()
        dict = []
        map = {'id':0,'lng':'','lat':'','mapaddress':''}
        for i in all:
            map['id'] = i.id
            map['lng'] = i.longitude
            map['lat'] = i.latitude
            map['mapaddress'] = i.station
            dict.append(map.copy())
            map = {'id': 0, 'lng': '', 'lat': '', 'mapaddress': ''}
        return HttpResponse(dict)

class getHardware(APIView):
    def get(self,request,*args,**kwargs):
        credentials = AccessKeyCredential('LTAI5tD6DKegrbT9BezFUNGp', 'Abjc7CgKhLeNie7Gw8OyP0fyOxwlh9')
        # use STS Token
        # credentials = StsTokenCredential('<your-access-key-id>', '<your-access-key-secret>', '<your-sts-token>')
        client = AcsClient(region_id='cn-shanghai', credential=credentials)

        request = QueryDevicePropertyStatusRequest()
        request.set_accept_format('json')

        request.set_IotInstanceId("iot-06z00b42m3qyvpt")
        request.set_ProductKey("h0uyFCd1W9t")
        request.set_DeviceName("STM32")

        response = client.do_action_with_exception(request)
        # python2:  print(response)
        status = json.loads(response)
        status_True = status['Data']['List']['PropertyStatusInfo'][1]['Value']
        print(status['Data']['List']['PropertyStatusInfo'][1]['Value'])
        demo = models.Hardware.objects.get(id=1)
        demo.temperature = status_True
        demo.save()
        # print(str(response, encoding='utf-8'))
        data = []
        dict = {'id':0,'name':'','tep':'','Rnum':'','Cnum':''}
        all = models.Hardware.objects.all()
        for i in all:
            dict['id'] = i.id
            dict['name'] = i.hardWareName
            dict['tep'] = i.temperature
            dict['Rnum'] = i.Rnum
            dict['Cnum'] = i.Cnum
            data.append(dict.copy())
        dictoo = {
            "code": 20000,
            "data":data
        }
        return JsonResponse(dictoo)