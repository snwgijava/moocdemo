__author__ = 'yangjian'
__date__ = '2018/4/28 15:15'

from django import forms

from captcha.fields import CaptchaField

#登录表单验证
class LoginForm(forms.Form):
    #用户名密码不能为空
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)

#注册表单
class RegisterForm(forms.Form):
    # 此处email与前端name需保持一致。
    email = forms.EmailField(required=True)
    #密码不能小于5位
    password = forms.CharField(required=True,min_length=5)
    #验证码
    captcha = CaptchaField()

#激活时验证码实现
class ActiveForm(forms.Form):
    #激活时不对邮箱密码做验证
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})
