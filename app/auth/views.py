#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template, url_for, request, jsonify, request
from . import auth
from flask_login import login_required, login_user, logout_user, current_user
from .. import db
from ..models import Admin, AccountInfo
import time
import random  
import string
import json
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 

@auth.route('/login', methods=['GET', 'POST'])
def gene_activation_code():  
    
    p = []
    result = {}  
    source = list(string.ascii_uppercase)  
    for index in range(0,10):  
        source.append(str(index))  
    while len(result) < 2:  
        key1 = random.sample(source, 8)
        key2 = random.sample(source, 12)
        key = ''.join(key1) + '-' + ''.join(key2)
        if key in result:  
            pass  
        else:
            result[key] = 1
        print(result)
        for key in result:
            p.append(key)
          

        
    return jsonify({"key":p[0]})




@auth.route('/')
def index():
    return render_template('index.html')
    

    
@auth.route('/KT/Admin/Api', methods=['GET', 'POST']) 
def insert():
    Action_String = request.args.get('Action_String')
    
    
    if Action_String == "insert":
        ImpDate = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        datax = request.form.to_dict()
        datax['ImpDate'] = ImpDate
        
        print type(datax)
        print datax
        q = AccountInfo(**datax)
        
        
        db.session.add(q)
        db.session.commit()
        response = {
            'code':200,
            'msg':'添加成功',
            
        
        }
     
        return jsonify(response)
    
    if Action_String == "query":
        q = AccountInfo.query.all() 
        data = []
        result = {}
        for obj in q:
            ls = {}
            for i in obj.__dict__.keys():
                if i.startswith('_') or i.startswith('__'):
                    continue
                ls[i] = getattr(obj,i)
            
            data.append(ls)
       
        response = {
            'code':0,
            'msg':'',
            'count':len(q),
            'data':data
            }

        return json.dumps(response) 
        
    if Action_String == "edit":
        datax = request.form.to_dict()
        q = AccountInfo(**datax)

        db.session.add(q)
        db.session.commit()
        
        return "修改成功" 
    
    if Action_String == "delete":
        AccountInfo.query.filter_by(id = id).delete()
        db.session.commit()
        return "删除成功" 
    

    

@auth.route('/KT/Admin/Api', methods=['GET', 'POST'])

def edit(Action_String):
    if Action_String == "edit":
        datax = request.form.to_dict()
        q = AccountInfo(**datax)

        db.session.add(q)
        db.session.commit()
        
    return "修改成功"
    

@auth.route('/KT/Admin/Api', methods=['GET', 'POST'])

def delete(Action_String):
    if Action_String == "delete":
        AccountInfo.query.filter_by(id = id).delete()
        db.session.commit()
    return "删除成功"