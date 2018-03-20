from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render,HttpResponse
from django.core import serializers
from django.template import RequestContext
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from order import models
import json
from datetime import datetime
# Create your views here.

#/api/setUser接口测试
def csSetUser(request):         #设置cookic
   # response=render(request,"csSetUser.html")
    #response = HttpResponseRedirect('/api/setUser')
    response=render(request, "login/index.html")
    response.set_cookie('name', "sun",36000)
    response.set_cookie('type', "3",36000)
    return response
#/api/getUser接口测试
def csGetUser(request):         #设置cookic
   # response=render(request,"csSetUser.html")
    #response = HttpResponseRedirect('/api/setUser')
    response=render(request, "csGetUser.html")
    response.set_cookie('name', "sun1",36000)
    response.set_cookie('type', "3",36000)
    return response
#/api/removeUser接口测试
def csRemoveUser(request):         #设置cookic
    response=render(request, "csRemoveUser.html")
    response.set_cookie('name', "sun",36000)
    response.set_cookie('pk',"31",36000)
    response.set_cookie('type', "3",36000)
    return response

def csForm(request):
    response=render(request, "csForm.html")
    response.set_cookie('name', "sun",36000)
    response.set_cookie('pk',"32",36000)
    response.set_cookie('type', "3",36000)
    return response


#获得用户信息接口，根据不同用户的类型。返回不同数据。
def getUser(requset):
    try:
        if requset.method == "POST":         #判断是否是POST请求
            type= requset.COOKIES.get("type")#获取COOKIES
            if type == "3":#如果用户类型是“3”
                #all_list= list(models.User.objects.filter(type="3"))+list(models.User.objects.filter(type="2"))+list(models.User.objects.filter(type="1"))
                all_list=models.User.objects.all()
                #数据库取出的是对象,因为“3”是最高权限的管理员，所以取出所有的用户
                data=serializers.serialize("json",all_list)#将取出的数据转换成json的字典格式
                status=0
                msg=""
            elif type == "2":#如果用户类型是“2”
                all_list=models.User.objects.filter(type="1")
                #list(models.User.objects.filter(name=name))
                #取出用户类型为“1”的用户
                data=serializers.serialize("json",all_list)
                status=0
                msg=""
            else :
                status=1
                msg="请求错误，无法获取用户信息"
                data="[]"
            re =json.dumps({
            "status": status,
            "msg": msg,
            "data":json.loads(data),
        })
            return HttpResponse(re,content_type="application/json")
        else:
            status = 1
            msg = "数据提交错误，无法获取有效的数据，请以正确的方法访问接口"
            data = ""
            re = req(status, msg, data)#生成返回的json格式数据
        return HttpResponse(re, content_type="application/json")
    except:
        status =1
        msg = "数据提交错误，请以正确的方法访问接口,或者提交数据不完整"
        data=""
        re = req(status, msg, data)
        return HttpResponse(re,content_type="application/json")




#函数req用来向前端返回json数据
def req(status,msg,data):
    re = json.dumps({
        "status": status,
        "msg": msg,
        "data": data
    })
    return re

#添加用户，只有管理员登录才可以访问。
def setUser(request):

    # print(request.COOKIES.get('name'))
    # print(request.COOKIES.get('type'))
#    a=(response.cookies.get("name"))

    try:
        if request.method=="POST":#需要请求是POST
            status = 0
            msg = ""
            data = ""
            re=req(status,msg,data)#构建返回数据
            name=request.POST.get("name",None)          #从前端拿到需要创建用户的信息
            password=request.POST.get("password",None)
            type=request.POST.get("type",None)          #获取用户的类型。根据权限，返回不同的值
            # print(name)
            if models.User.objects.filter(name=name):#首先判断添加用户不能重名
                status = 1
                msg = "用户信息已经存在，重复添加"
                data = ""
                re = req(status, msg, data)
            elif (type == "2" or type=="1") and request.COOKIES.get('type')=="3":#判断前端需要添加的用户类型，超级管理员只有一个。判断当前管理员类型
                models.User.objects.create(
                name=name,
                password=password,
                type=type,
                )
            elif type == "1" and request.COOKIES.get('type') == "2":#管理员类型为“2”，只能添加用户类型为“1”
                models.User.objects.create(
                    name=name,
                    password=password,
                    type=type,
                )

            else:
                status = 1
                msg = "数据提交错误，不能设置管理员"
                data = ""
                re = req(status, msg, data)
            return HttpResponse(re, content_type="application/json")

        else:
            status = 1
            msg = "数据提交错误，无法获取有效的数据，请以正确的方法访问接口"
            data = ""
            re=req(status,msg,data)
        return HttpResponse(re, content_type="application/json")
    except:
        status =1
        msg = "数据提交错误，请以正确的方法访问接口,或者提交数据不完整"
        data=""
        re = req(status, msg, data)
        return HttpResponse(re,content_type="application/json")

#根据前端给的主键和用户类型，结合当前用户的类型，删除用户。
def removeUser(request):
    try:
        if request.method == "POST":
            status = 0
            msg = ""
            data = ""
            uid=request.POST.get("id",None)#从前端接收主键id
            pk =request.COOKIES.get("pk")#从cookie接收当前管理员pk
            type = request.COOKIES.get("type")#从cookie接收当前管理员类型
            if (uid != pk) and type=="3":#如果接收的id与当前管理员不相等，才可以删除，避免自己吧自己删除
                area = models.User.objects.get(pk=uid)
    #            print(area)
                area.delete()
                re=req(status,msg,data)
            elif(uid != pk) and type=="2" and models.User.objects.get(pk=uid,type="1"):
              #  if not models.User.objects.get(pk=uid,type="2")#如果前端传给的id，不是管理员的话
                area = models.User.objects.get(pk=uid)
                area.delete()
                re = req(status, msg, data)
            else:
                status = 1
                msg = "数据提交错误，管理员不能删除自己"
                data = ""
                re = req(status, msg, data)
                return HttpResponse(re, content_type="application/json")
        else:
            status = 1
            msg = "数据提交错误，不能设置管理员"
            data = ""
            re = req(status, msg, data)
            return HttpResponse(re, content_type="application/json")
        return HttpResponse(re,content_type="application/json")
    except:
        status =1
        msg = "数据提交错误，请以正确的方法访问接口,或者提交数据不完整"
        data=""
        re = req(status, msg, data)
        return HttpResponse(re,content_type="application/json")

#提交数据接口
def form(request):
    try:
        if request.method == "POST":
            status = 0
            msg = ""
            data = ""
            type = request.POST.get("type",None)#首先获取操作类型
            print(type)
            time = datetime.now()#后端控制字段
            print(time)
            name = request.COOKIES.get("name", None)  # 使用cookies获取操作人姓名
            if type=="1":  #编辑类型为增加的时候
                danger = request.POST.get("danger", None)  # 前端提交数据
                thing = request.POST.get("thing", None)
                desc = request.POST.get("desc", None)
                money = request.POST.get("money", None)
                level = request.POST.get("level", None)
                models.List.objects.create(
                    danger=danger,
                    thing=thing,
                    desc=desc,
                    money=money,
                    level=level,
                    time=time,
                    name=name,
                )
                re = req(status, msg, data)
                all_list = models.List.objects.all()
                print(serializers.serialize("json",all_list))


            elif type=="2":#编辑类型为修改的时候
                id = request.POST.get("id",None)#前端提交修改后的数据
                danger = request.POST.get("danger", None)  # 前端提交数据
                thing = request.POST.get("thing", None)
                desc = request.POST.get("desc", None)
                money = request.POST.get("money", None)
                level = request.POST.get("level", None)
                if models.User.objects.filter(pk=id):#确认数据库中是否有这条信息
                    models.List.objects.update(
                    danger=danger,
                    thing=thing,
                    desc=desc,
                    money=money,
                    level=level,
                    )
                    print("lalala")
                    re = req(status, msg, data)
                else:
                    status = 1
                    msg = "数据提交错误，数据库中无订单信息，无法更改"
                    data = ""
                    re = req(status, msg, data)
                    return HttpResponse(re, content_type="application/json")

            elif type=="3":#删除
                id = request.POST.get("id", None)  # 前端提交删除数据的主键
                if models.List.objects.filter(pk=id):
                    data=models.List.objects.get(pk=id)
                    data.delete()
                    print("ssssssssssssss")
                    status = 0
                    msg = ""
                    data = ""
                    re = req(status, msg, data)
                else:
                    status = 1
                    msg = "数据提交错误，无法删除"
                    data = ""
                    re = req(status, msg, data)
                    return HttpResponse(re, content_type="application/json")
                return HttpResponse(re, content_type="application/json")
            else:
                status = 1
                msg = "数据提交错误"
                data = ""
                re = req(status, msg, data)
            return HttpResponse(re,content_type="application/json")
        else:
            status = 1
            msg = "数据提交错误，使用get方法"
            data = ""
            re = req(status, msg, data)
            return HttpResponse(re, content_type="application/json")
    except:
        status =1
        print(status)
        msg = "数据提交错误，请以正确的方法访问接口,或者提交数据不完整"
        data=""
        re = req(status, msg, data)
        return HttpResponse(re,content_type="application/json")


# 李启蒙接口部分代码
def login(request):
    return render(request, 'index.html')

def api_login(request):
    '''
        用户登录接口
        0. 判断请求
        1. 接收用户数据
        2. 操作数据库数据
        3. 进行数据验证
        4. 逻辑判断，若是则跳转至管理页面，若不是则跳转至登陆页面
    '''
    judge = request.is_ajax()
    if judge:# 登陆是ajax请求
        # 对ajax传入的数据进行格式的处理
        # mid = request.body.decode('utf8')
        # data = json.loads(mid)
        # # get到用户输入的数据
        # cur_user_name = data['name']
        # cur_user_pwd = data['password']
        # 对用户传入的数据进行验证
        cur_user_name = request.POST.get('name',None)
        cur_user_pwd = request.POST.get('password',None)
        # print(name,pwd)
        # return HttpResponse('ok')
        result_info = list(models.User.objects.filter(name=cur_user_name).values())
        # print(result_info,type(result_info))
        if result_info:# 如果获取到数据库数据
            # print(result_info[0]['password'],cur_user_pwd)
            sql_pwd = result_info[0]['password']
            result = cur_user_pwd == sql_pwd
            if result:# 进行验证
                    switcher = {
                        1: 'Manager',
                        2: 'Middle-Manager',
                        3: 'User',
                    }
                    result_type = int(result_info[0]['type'])
                    # print(result_type,type(result_type))
                    User_Type = switcher[result_type]
                    yes = {
                        'status': 0,
                        'msg': User_Type,
                        'data': {
                            'uid': result_info[0]['uid'],
                            'username': result_info[0]['name'],
                            'type': User_Type,
                        }
                    }
                    request.session['username'] = cur_user_name
                    request.session['password'] = cur_user_pwd
                    request.session['type'] = User_Type
                    right = HttpResponse(yes)
                    right.set_cookie('name',result_info[0]['name'])
                    right.set_cookie('type',result_info[0]['type'])
                    return right
            else:
                no = {
                    'status': 1,
                    'msg': 'Wrong password!!',
                    'data': {}
                }
                error = HttpResponse(no)
                return error
        else:
            no = {
                'status': 1,
                'msg': 'Not Found!',
                'data': {}
            }
            error = HttpResponse(no)
            return error
    else:
        return render(request, 'index.html')
        # return HttpResponse('ok')

def api_check(request):
    '''
    0.判断请求方式是不是ajax
    1.从用户的session中获取信息
    1.5. 可选，根据用户的session信息获取其他信息并返回
    2.将用户携带的session信息返回给用户
    '''
    judge = request.is_ajax()
    if judge:
        # cur_user_info = {
        #     1: request.session.get('username'),
        #     2: request.session.get('password'),
        #     3: request.session.get('type'),
        # }
        login_username = request.session.get('username')
        login_password = request.session.get('password')
        login_type = request.session.get('type')
        if login_username:
            right = {
                'status': 0,
                'msg': '',
                'data': {
                    'type':login_type,
                    'name':login_username,
                }
            }
            yes = HttpResponse(right)
            return yes
        else:
            return render(request, 'index.html')
    else:
        info = {
            'status': 1,
            'msg': 'Request method error!',
            'data': {}
        }
        no = HttpResponse(info)
        return no

def api_getall(request):
    judge = request.is_ajax()
    if judge:
        pass
    else:
        info = {
            'status': 1,
            'msg': 'Request method error!',
            'data': {}
        }
        no = HttpResponse(info)
        return no

def home(request):
    return render(request,'home.html')

def logout(request):
    request.session.clear()
    return render(request,'index.html')
# def index(request):
#     # 登陆个人后台管理页面，登陆页面逻辑测试
#     username = request.COOKIES.get('name')
#     # 用户访问自己的管理页面
#     if username:
#         # 如果用户的name是这是的值那么允许访问
#         return render(request,'index.html')
#     else:
#         # 如果用户的name值不存在，俺么重新返回登陆页面
#         return redirect('/api/login')