#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/1 14:45
# @File    : Views.py
"""
视图模型
"""

from  flask import render_template, Blueprint, redirect, url_for, flash, request, make_response, session
from app import login_manager, db
from .forms import Login_Form, Register_Form
from .models import Users
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required
from hashlib import md5
from .aliyun import AliyunEcs


cmdb = Blueprint('cmdb', __name__)  # 蓝图


@cmdb.route('/')
@cmdb.route('/index')
def index():
    if request.cookies.get('name'):
        return render_template('index.html', name=request.cookies.get('name'))
    else:
        form = Login_Form()
        return render_template('login.html', form=form)

@cmdb.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        name = form.name.data
        pwd = form.pwd.data
        user = Users.query.filter_by(name=name).first()
        if user is not None and user.pwd == form.pwd.data:
            login_user(user)
            resp = make_response(redirect(url_for('cmdb.index', name=name)))
            resp.set_cookie(key='name', value=name, expires=None)
            resp.set_cookie(key='sessionId', value=str(md5((name+pwd).encode('utf8'))), expires=None)
            return resp
        else:
            flash('用户或密码错误')
            return render_template('login.html', form=form)


# 用户登出
@cmdb.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出登录')
    resp = redirect(url_for('cmdb.index'))
    resp.delete_cookie('name')
    resp.delete_cookie('sessionId')
    resp.delete_cookie('session')
    return resp


@cmdb.route('/register', methods=['GET', 'POST'])
def register():
    form = Register_Form()
    if form.validate_on_submit():
        user = Users(name=form.name.data,pwd=form.pwd.data)
        if user.is_active():
            flash("用户名已存在！")
        else:
            db.session.add(user)
            db.session.commit()
            flash('注册成功')
            return redirect(url_for('cmdb.register'))
    return render_template('register.html', form=form)

@login_manager.user_loader
def load_user(id):
     return Users.query.get(int(id))

@cmdb.route('/ecslist')
@login_required
def ecslist():
    aliyun_ecs = AliyunEcs()
    ecs_info = aliyun_ecs.Ecsinfo()
    return render_template('ecs.html', ecs_info=ecs_info)

