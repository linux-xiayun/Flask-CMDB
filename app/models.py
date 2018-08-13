#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/1 14:45
# @File    : Model.py
"""
数据模型
"""

from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required
from app import login_manager
from app import db


class Users(UserMixin, db.Model):
    __tablename__ = 'py_user'  # 对应mysql数据库表
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    pwd = db.Column(db.String(64))

    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.name

    def is_authenticated(self):
        return True

    def is_active(self):
        if Users.query.filter_by(name=self.name).first():
            return True
        else:
            return False

    def is_anonymous(self):
        return False

class Ecs(db.Model):
    __tablename__ = 'py_ecs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    desc = db.Column(db.String(128))
    zone = db.Column(db.String(64))
    ip1 = db.Column(db.String(64), unique=True)
    ip2 = db.Column(db.String(64), unique=True)
    type = db.Column(db.String(64))
    cpu = db.Column(db.String(64))
    mem = db.Column(db.String(64))
    status = db.Column(db.String(64))
    ip1type = db.Column(db.String(64))
    tags = db.Column(db.String(64))

    def __init__(self, name, desc, zone, ip1, ip2, type, cpu, mem, status, ip1type, tags):
        self.name = name
        self.desc = desc
        self.zone = zone
        self.ip1 = ip1
        self.ip2 = ip2
        self.type = type
        self.cpu = cpu
        self.mem = mem
        self.status = status
        self.ip1type = ip1type
        self.tags = tags

    def is_active(self):
        if Ecs.query.filter_by(ip1 = self.ip1).first():
            return True
        else:
            return False



