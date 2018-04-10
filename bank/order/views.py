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
import time
from django.http import JsonResponse
from datetime import datetime



def submit(request):
    return render(request,"submit/submit.html")
def data(request):
    return render(request,"data/item4.html")
def edit(request):
    return render(request,"edit/item3.html")
def welcome(request):
    return render(request,"welcome/welcome.html")
def search(request):
    return render(request,"search/item2.html")
def tab(request):
    return render(request,"search/tab.html")
def editUser(request):
    return render(request,"edit/editUser.html")
def editu(request):
    return render(request,"edit/addu.html")


def cs(request):
    # 切片查询

    limit=2
    page=1

    # count=7
    count=models.User.objects.count()
    res=models.User.objects.reverse()[count-limit*page:count-(page-1)*limit]
    # count=models.User.objects.count()
    data=[]
    for i in res:
        d = {}
        d["id"] = i.uid
        d["name"] = i.name
        d["password"] = i.password
        d["type"] = i.type
        data.append(d)
        
def getUser(requset):
    try:

        if requset.method == "GET":
            #判断是否是POST请求
            type= requset.COOKIES.get("type")
            #获取COOKIES.判断用户的类型

            limit =int(requset.GET.get("limit",None))     #每页数据
            page = int(requset.GET.get("page",None))     #第几页
            if type == "3":                                 #如果用户类型是“3”
                count = models.User.objects.count()
                all_list=models.User.objects.order_by("uid").reverse()[limit*(page-1):page*limit]         #all_list= list(models.User.objects.filter(type="3"))+list(models.User.objects.filter(type="2"))+list(models.User.objects.filter(type="1"))
                # all_list=models.User.objects.reverse()[:count]         #all_list= list(models.User.objects.filter(type="3"))+list(models.User.objects.filter(type="2"))+list(models.User.objects.filter(type="1"))

                data=[]
                for i in all_list:
                    d={}
                    d["id"]=i.uid
                    d["name"]=i.name
                    d["password"]=i.password
                    d["type"]=i.type
                    data.append(d)
                status=0
                msg=""
            elif type == "2":                                   #如果用户类型是“2”
                count = models.User.objects.filter(type="1").count()
                all_list = models.User.objects.filter(type="1").order_by("uid").reverse()[limit * (page - 1):page * limit]   #取出用户类型为“1”的用户
                data=[]                                         #list(models.User.objects.filter(name=name))
                for i in all_list:
                    d={}
                    d["id"]=i.uid
                    d["name"]=i.name
                    d["password"]=i.password
                    d["type"]=i.type
                    data.append(d)
                status=0
                msg=""
            elif type == "1":  # 如果用户类型是“2”
                status=1
                msg="请求错误，无法获取用户信息"
                data="[]"
                count=0


                re=req(status,msg,data,count)

            else :
                status=1
                msg="请求错误，无法获取用户信息"
                data="[]"
                count=0
            re=req(status,msg,data,count)                             #调用函数req()将返回数据进行json封装
            return HttpResponse(re,content_type="application/json")
        # else:
        #     status = 1
        #     msg = "数据提交错误，无法获取有效的数据，请以正确的方法访问接口"
        #     data = ""
        #     re = req(status, msg, data)                         #生成返回的json格式数据
        # return HttpResponse(re, content_type="application/json")
    except:
        status =1
        msg = "数据提交错误，请以正确的方法访问接口,或者提交数据不完整"
        data=""
        count=0
        re = req(status, msg, data,count)
        return HttpResponse(re,content_type="application/json")

#函数req用来向前端返回json数据
def req(status,msg,data,count):
    re = json.dumps({
        "status": status,
        "msg": msg,
        "code":0,
        "data": data,
        "count":count
    })
    return re

#请求参数   cookie中的type
#添加用户，只有管理员登录才可以访问。
def setUser(request):
    try:
        if request.method=="POST":#需要请求是POST
            status = 0
            msg = ""
            data = ""

            username =request.COOKIES.get("name")#从cookie得到当前登录管理员姓名
            uid=int(request.POST.get("id",None))#从前端接收要修改用户的主键id
            result_info = list(models.User.objects.filter(name=username).values())
            pk = result_info[0]['uid']          #得到当前登录管理员的主键pk
            count=0
            re=req(status,msg,data,count)       #构建返回数据

            name=request.POST.get("name",None)          #从前端拿到需要创建用户的数据
            password=request.POST.get("password",None)
            id=request.POST.get("id",None)
            type=request.POST.get("type",None)


            if type !="3" and not models.User.objects.filter(name=name):
                if models.User.objects.filter(pk=id) and (type=="2" or type=="1") and request.COOKIES.get('type')=="3" and (pk!=uid):#首先判断添加用户不能重名
                    models.User.objects.filter(pk=id).update(
                        name=name,
                        password=password,
                        type=type,
                    )


                    # status = 1
                    # msg = "用户信息已经存在，重复添加"
                    # data = ""
                    re = req(status, msg, data,count)
                elif models.User.objects.filter(pk=id) and type == "1" and request.COOKIES.get('type') == "2":  # 首先判断添加用户不能重名
                        models.User.objects.filter(pk=id).update(
                            name=name,
                            password=password,

                        )

                        # status = 1
                        # msg = "用户信息已经存在，重复添加"
                        # data = ""
                        re = req(status, msg, data,count)
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
                    msg = "数据提交错误，权限问题，不能设置管理员"
                    data = ""
                    re = req(status, msg, data,count)
                return HttpResponse(re, content_type="application/json")
            else:
                status = 1
                msg = "数据提交错误，无法获取有效的数据，请以正确的方法访问接口"
                data = ""
                count = 0
                re = req(status, msg, data, count)
            return HttpResponse(re, content_type="application/json")

        else:
            status = 1
            msg = "数据提交错误，无法获取有效的数据，请以正确的方法访问接口"
            data = ""
            count=0
            re=req(status,msg,data,count)
        return HttpResponse(re, content_type="application/json")
    except:
        status =1
        msg = "数据提交错误，请以正确的方法访问接口,或者提交数据不完整"
        data=""
        count=0
        re = req(status, msg, data,count)
        return HttpResponse(re,content_type="application/json")

#根据前端给的主键和用户类型，结合当前用户的类型，删除用户。
def removeUser(request):
    try:
        if request.method == "POST":
            status = 0
            msg = ""
            data = ""


            name =request.COOKIES.get("name")#从cookie接收当前管理员pk
            uid=int(request.POST.get("id",None))#从前端接收主键id

            result_info = list(models.User.objects.filter(name=name).values())
            pk = result_info[0]['uid']



            # pk = models.User.objects.filter(name="name")
            type1 = request.COOKIES.get("type")#从cookie接收当前管理员类型
            # print("result_info="+ str(result_info))
            # print("uid="+str(uid))
            # print(type(uid))
            # print(type(pk))
            count=0
            if (uid != pk) and type1=="3":#如果接收的id与当前管理员不相等，才可以删除，避免自己吧自己删除
                area = models.User.objects.get(pk=uid)
                area.delete()
                re=req(status,msg,data,count)
            elif(uid != pk) and type1=="2" and models.User.objects.get(pk=uid,type="1"):
            #  if not models.User.objects.get(pk=uid,type="2")#如果前端传给的id，不是管理员的话
                area = models.User.objects.get(pk=uid)
                area.delete()
                re = req(status, msg, data,count)
            else:
                status = 1
                msg = "数据提交错误，管理员不能删除自己"
                data = ""
                re = req(status, msg, data,count)
                return HttpResponse(re, content_type="application/json")
        else:
            status = 1
            msg = "数据提交错误，不能设置管理员"
            data = ""
            count=0
            re = req(status, msg, data,count)
            return HttpResponse(re, content_type="application/json")
        return HttpResponse(re,content_type="application/json")
    except:
        status =1
        msg = "数据提交错误，请以正确的方法访问接口,或者提交数据不完整"
        data=""
        count=0
        re = req(status, msg, data,count)
        return HttpResponse(re,content_type="application/json")

#提交数据接口
def form(request):
    try:
        if request.method == "POST":
            status = 0
            msg = ""
            data = ""
            type = request.POST.get("type",None)#首先获取操作类型
            count = 0

            times = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            name = request.COOKIES.get("name", None)  # 使用cookies获取操作人姓名
            # name="sunmingming"           #-------------------------伪造数据
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
                    time=times,
                    name=name,
                )
                count=0
                re = req(status, msg, data,count)
                all_list = models.List.objects.all()
                # print(serializers.serialize("json",all_list))


            elif type=="2":#编辑类型为修改的时候
                id = request.POST.get("id",None)#前端提交修改后的数据
                danger = request.POST.get("danger", None)  # 前端提交数据
                thing = request.POST.get("thing", None)
                desc = request.POST.get("desc", None)
                money = request.POST.get("money", None)
                level = request.POST.get("level", None)
                if models.List.objects.filter(pk=id):#确认数据库中是否有这条信息
                    models.List.objects.filter(pk=id).update(
                    danger=danger,
                    thing=thing,
                    desc=desc,
                    money=money,
                    level=level,
                    )
                    re = req(status, msg, data,count)
                else:
                    status = 1
                    msg = "数据提交错误，数据库中无订单信息，无法更改"
                    data = ""
                    re = req(status, msg, data,count)
                    return HttpResponse(re, content_type="application/json")

            elif type=="3":#删除
                # username = request.COOKIES.get("name")  # 从cookie得到当前登录管理员姓名
                # # uid = int(request.POST.get("id", None))  # 从前端接收要修改用户的主键id
                # result_info = list(models.User.objects.filter(name=username).values())
                # pk = result_info[0]['uid']  # 得到当前登录管理员的主键pk

                id = request.POST.get("id", None)  # 得到数据的主键
                # reqs=list(models.List.objects.filter(lid=id).values())
                # name1=reqs[0]['name']     #得到需要删除   数据的用户名
                # req1 = list(models.User.objects.filter(name=name1).values())
                # type1 = req1[0]['type']  # 得到  创建订单的 用户类型
                # typeUser=request.COOKIES.get("type",None)
                # if (typeUser=="2" and type1=="3")or(typeUser=="1" and type1==("2"or"3")):  #如果管理员想删除超级管理员创建的订单
                #     id=0

                if models.List.objects.filter(pk=id):
                    data=models.List.objects.get(pk=id)
                    data.delete()
                    status = 0
                    msg = ""
                    data = ""
                    re = req(status, msg, data,count)
                else:
                    status = 1
                    msg = "数据提交错误，无法删除"
                    data = ""
                    re = req(status, msg, data,count)
                    return HttpResponse(re, content_type="application/json")
                return HttpResponse(re, content_type="application/json")
            else:
                status = 1
                msg = "数据提交错误"
                data = ""
                re = req(status, msg, data,count)
            return HttpResponse(re,content_type="application/json")
        else:
            status = 1
            msg = "数据提交错误，使用get方法"
            data = ""
            count=0
            re = req(status, msg, data,count)
            return HttpResponse(re, content_type="application/json")
    except:
        status =1
        msg = "数据提交错误，请以正确的方法访问接口,或者提交数据不完整"
        data=""
        count=0
        re = req(status, msg, data,count)
        return HttpResponse(re,content_type="application/json")


#####################################################################################################################

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
    if judge:
        cur_user_name = request.POST.get('name',None)
        cur_user_pwd = request.POST.get('password',None)
        result_info = list(models.User.objects.filter(name=cur_user_name).values())
        if result_info:
            sql_pwd = result_info[0]['password']
            result = cur_user_pwd == sql_pwd
            if result:
                    switcher = {
                        3: 'Manager',
                        2: 'Middle-Manager',
                        1: 'User',
                    }
                    result_type = int(result_info[0]['type'])
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
                    right = JsonResponse(yes)
                    right.set_cookie('name',result_info[0]['name'])
                    right.set_cookie('type',result_info[0]['type'])
                    return right
            else:
                no = {
                    'status': 1,
                    'msg': 'Wrong password!!',
                    'data': {}
                }
                return JsonResponse(no)
        else:
            no = {
                'status': 1,
                'msg': 'Not Found!',
                'data': {}
            }
            return JsonResponse(no)
    else:
        return render(request, 'login/index.html')

def home(request):
    username = request.session.get("username")
    if username:
        return render(request,"Home/home.html")
    else:
        return render(request,'login/index.html')

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
        # login_password = request.session.get('password')
        login_type = request.session.get('type')
        if login_username:
            right = {
                'status': 0,
                'msg': '',
                'data': {
                    'type':login_type,
                    'username':login_username,
                }
            }
            yes = JsonResponse(right)
            return yes
        else:
            return render(request, 'login/index.html')
    else:
        info = {
            'status': 1,
            'msg': 'Request method error!',
            'data': {}
        }
        no = JsonResponse(info)
        return no

def logout(request):
    request.session.clear()
    return render(request,'login/index.html')

def api_getall(request):
        '''
            用户后去订单的接口
            0.api_check中已经验证过当前登录的用户(不验证当前用户身份)
            1.从session中获取当前登录用户的重要信息
            2.对信息进行判断，根据身份然后进行数据库的查询和操作
            3.将数据库中返回的数据进行整理，以一定的格式进行返回
        '''
        # judge = request.is_ajax()
        # if judge:
        if request.method == "GET":
            login_username = request.session.get('username')
            login_password = request.session.get('password')
            login_type = request.session.get('type')
            if login_type == 3:
                data = list(models.List.objects.all().values())
                return_info = {
                    'status': 0,
                    'code': 0,
                    'msg': 'Return Success!',
                    'data': data,
                }
                data = JsonResponse(return_info)
                return data
            elif login_type == 2:
                data = list(models.List.objects.all().values())
                return_info = {
                    'status': 0,
                    'msg': 'Return Success!',
                    'code': 0,
                    'data': data,
                }
                data = JsonResponse(return_info)
                return data
            elif login_type == 1:
                data = list(models.List.objects.filter(name=login_username).values())
                return_info = {
                    'status': 0,
                    'msg': 'Return Success!',
                    'code': 0,
                    'data': data,
                }
                data = JsonResponse(return_info)
                return data
            else:
                info = {
                    'status': 1,
                    'msg': 'No Match Data!',
                    'code': 0,
                    'data': [],
                }
                data = JsonResponse(info)
                return data
        else:
            info = {
                'status': 1,
                'msg': 'Request method error!',
                'code': 0,
                'data': {}
            }
            no = JsonResponse(info)
            return no

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
