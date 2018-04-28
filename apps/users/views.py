from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.db.models import Q #并集运算
from django.views.generic.base import View

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ActiveForm, ForgetForm, ModifyPwdForm
from utils.send_email import send_register_email


# Create your views here.

#登录
def user_login(request):
    if request.method == 'POST':
        #获取前端数据，取不到时为空
        user_name = request.POST.get('username','')
        pass_word = request.POST.get('password','')
        #成功返回user对象，失败返回null
        user = authenticate(username=user_name,password=pass_word)
        #验证用户名和密码是否正确,如果不为Null说明验证成功
        if user is not None:
            login(request,user)
            #跳转到首页，user,request会被带回首页
            return render(request,'index.html')
        else:
            return render(request,'login.html',{'msg':'用户名或密码错误！'})
    elif request.method == 'GET':
        #get请求就获取登录页面
        return render(request,'login.html',{})

#类视图登录
class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{})

    def post(self,request):
        # 类实例化需要一个字典参数dict:request.POST就是一个QueryDict所以直接传入
        # POST中的usernamepassword，会对应到form中
        login_form = LoginForm(request.POST)
        # is_valid判断字段是否有错执行我们原有逻辑，验证失败跳回login页面
        if login_form.is_valid():
            user_name = request.POST.get('username','')
            pass_word = request.POST.get('password','')
            # 成功返回user对象,失败返回null
            user = authenticate(username=user_name,password=pass_word)
            #如果不为null说明验证成功
            if user is not None:
                login(request,user)
                return render(request,'index.html')
            #验证不成功返回登录页面
            else:
                return render(request,'login.html',{'msg':'用户名或密码错误！'})
        else:
            return render(request,'login.html',{'login_form':login_form})

#注册功能
class RegisterView(View):
    def get(self,request):
        #添加验证码
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email','')
            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{'register_form':register_form,'msg':'用户已存在'})
            pass_word = request.POST.get('password','')
            #实例化一个user_profile对象，将前台值存入
            # user_profile = UserProfile.objects.create_user(user_name, user_name, pass_word)
            # user_profile.save()

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False

            #加密password进行保存
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name,'register')
            return render(request,'login.html',{'msg':'注册邮件已发送至你的邮箱，请查收！'})
        else:
            return render(request,'register.html',{'register_form':register_form})

#忘记密码功能
class ForgetPwdView(View):
    def get(self,request):
        forgetform = ForgetForm()
        return render(request,'forgetpwd.html',{'forgetform':forgetform})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            #发送找回密码邮件
            send_register_email(email,'forget')
            #发送完毕返回登录页面并显示邮件发送成功
            return render(request,'login.html',{'msg':'重置密码邮件已发送，请注意查收'})
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})

#重置密码功能
class ResetView(View):
    def get(self,request,active_code):
        #查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        #如果不为空就表示存在
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                #获取对应的邮箱
                email = record.email
                return render(request,'password_reset.html',{'email':email})
        else:
            return render(request,'forgetpwd.html',{'msg':'您的重置密码链接无效，请重新请求','active_form':active_form})

#修改密码
class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            #如果两次密码不相等，返回错误信息
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':'两次输入密码不相同'})
            #如果密码一样
            user = UserProfile.objects.get(email=email)
            #密码加密
            user.password = make_password(pwd2)
            user.save()
            return render(request,'login.html',{'msg':'密码修改成功，请重新登录'})
        else:
            email = request.POST.get('email','')
            return render(request,'password_reset.html',{'email':email,'modify_form':modify_form})

#激活用户功能
class ActiveUserView(View):
    def get(self,request,active_code):
        #查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 激活form负责给激活跳转进来的人加验证码
        active_form = ActiveForm(request.GET)
        #如果不为空表示有用户
        if all_record:
            for record in all_record:
                #获取对应邮箱
                email = record.email
                #查找邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                #激活成功跳转登录页面
                return render(request,'login.html')
        else:
            return render(request,'register.html',{'msg':'您的激活链接无效','active_form':active_form})

#实现用户名和邮箱都可以登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None