#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/1 14:46
# @File    : Form.py
"""
表单类
"""

from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from flask_wtf import FlaskForm
from .models import Users


# 登录表单
class Login_Form(FlaskForm):
    name = StringField('name', validators=[DataRequired(message='用户名不能为空'), Length(2, 6, message='用户名只能在2~6个字符之间')])
    pwd = PasswordField('pwd', validators=[DataRequired(message='密码不能为空'), Length(6, 20, message='密码只能在6~20个字符之间')])
    remember_me = BooleanField('remember me', default=False)
    submit = SubmitField('Login In')





# 注册表单
class Register_Form(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    pwd = PasswordField('pwd', validators=[DataRequired()])
    # confirm = PasswordField('确认密码', validators=[EqualTo('pwd', message='两次密码不一致')])
    submit = SubmitField('Sign up')


