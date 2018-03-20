#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, flash
from flask import request, session
from .. import db
from ..models import AccountInfo, Function, Back_Up, BidWord, Manage,TaoKouLin, Optimization,BidWord,Control

from . import admin

import random  
import string
from functools import wraps
import time
import json
  

# 生成key  
def gene_activation_code():  
    ''''' 
    @number:生成激活码的个数 
    @length:生成激活码的长度 
    '''  
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
  


#用户登录
def authorize(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs): # 这里就像过滤器，有了那个修饰器标志的视图函数都必须经过这个函数才可以返回请求
        
        user = session.get('key',None)#取得登录标志
        if user:
            return fn(*args, **kwargs)#登录了就返回请求
        else:
            response = {
                'code':404,
                'msg':'访问该网页需要登录！',
                }
            return jsonify(response)
    return wrapper

class User_login(object):

    def __init__(self):
        pass
        
    
    
    def login(self,data):
        
        
        key = AccountInfo.query.all()
        
        session['key'] = data['key']
    
        response = {
          'code':200,
          'msg':'登录成功',
          'result': [[i.key, i.TB_ID, i.description, i.start_time, i.end_time] for i in key]
          } 
          
        return response
    
    def pt(self,data):
        key = AccountInfo.query.all()
        for i in key:
            if i.key == data['key'] and i.TB_ID == data['TB_ID']:
                session['key'] = data['key']
                session['TB_ID'] = data['TB_ID']
                response = {
                            'code':200,
                            'msg':'登录成功',
                            
                            }
                return jsonify(response)
        return "请重新登录"
        

class Bid_word(object):
    
    def __init__(self):
        pass
    
    def get_bid_word_yun_word_data(self,data):
        

        q = BidWord.query.all()
        data = []
        result = {}
        for obj in q:
            ls = {}
            for i in obj.__dict__.keys():
                if i.startswith('_') or i.startswith('__'):
                    continue
                ls[i] = getattr(obj,i)
            data.append(ls)
        #print data
        response = {
            'code':200,
            'msg':'',
            'result': data if data else []
            }
        return jsonify(response)

    def save_bid_word_yun_word_data(self,item):
        ImpDate = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        item['ImpDate'] = ImpDate
        q = BidWord(**item)
        
        db.session.add(q)
        db.session.commit()
        
        
        
        q = BidWord.query.all()
        #print q
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
                    'code':200,
                    'msg':'',
                    'result':data
                    }
        
        
        return jsonify(response)



    def del_bid_word_yun_word(self,data):
        CategoryId = data['CategoryId']
        adGroupId = data['adGroupId']
        campaignId = data['campaignId']
        itemId = data['itemId']
        nickName = data['nickName']
        operName = data['operName']
        token = data['token']
        id = data['id']

        BidWord.query.filter_by(id = id).delete()
        db.session.commit()
        
        q = BidWord.query.all()
        data = []
        result = {}
        for obj in q:
            ls = {}
            for i in obj.__dict__.keys():
                if i.startswith('_') or i.startswith('__'):
                    continue
                ls[i] = getattr(obj,i)
            data.append(ls)
        print data    
        response = {
            'code':200,
            'msg':'',
            'result':data
            }

        return jsonify(response)

#云人群备份功能
class Yun_backup(object):
   
    def __init__(self):
        pass

    #获取云备份
    def get_crowd_yun_data(self,data):
        
        
        
        q = Back_Up.query.all()
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
            'code':200,
            'msg':'',
            'result': data if data else []
            }
        
        return jsonify(response)

    def save_crowd_yun_data(self,item):
        ImpDate = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        item['ImpDate'] = ImpDate
          
        q = Back_Up(**item)
        db.session.add(q)
        db.session.commit()
        
        
        q = Back_Up.query.all()
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
            'code':200,
            'msg':'',
            'result':data if data else []
            }

        return jsonify(response)

    def del_crowd_yun_data(self,data):
        CategoryId = data['CategoryId']
        custId = data['custId']
        id = data['id']
        itemId = data['itemId']
        nickName = data['nickName']
        operName = data['operName']
        token = data['token']
        
        
        
        Back_Up.query.filter_by(id = id).delete()
        db.session.commit()
         
        q = Back_Up.query.all()
        
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
            'code':200,
            'msg':'',
            'result': data
            }

        return jsonify(response)

#淘口令功能
class Tao_word(object):

    def __init__(self):
        pass

    #获取淘口令状态权限
    def get_tkl_item_tag_info(self,data):
        categoryId = data['CategoryId']
        itemId = data['ItemId']
        nickName = data['nickName']
        operName = data['operName']
        title = data['Title']
        token = data['token']
        custId = data['custId']
        
        q = TaoKouLin.query.all()
        
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
            'code':200,
            'msg':1000, 
            'result': data
            
                
            }

        return jsonify(response)

    #生成淘口令
    def get_tkl_batch_create_tkl_data(self,data):
        CategoryId = data['CategoryId']
        ImgUrl = data['ImgUrl']
        ItemId = data['ItemId']
        ItemUrl = data['ItemUrl']
        Nick = data['Nick']
        ShopTitle = data['ShopTitle']
        ShopType = data['ShopType']
        TagString = data['TagString']
        Title = data['Title']
        auctionTag = data['auctionTag']
        custId = data['custId']
        keyWords = data['keyWords']
        nickName = data['nickName']
        operName = data['operName']
        tagNum = data['tagNum']
        token = data['token']
        
        q = TaoKouLin.query.all()
        
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
            'code':200,
            'msg':"",
            'result': data 
            }

        

        return jsonify(response)
        
        

    #获取已有的淘口令
    def get_tkl_list_data(self,data):
        custId = data['custId']
        itemId = data['itemId']
        nickName = data['nickName']
        operName = data['operName']
        tklType = data['tklType']
        token = data['token']
        
        q = TaoKouLin.query.all()
        
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
            'code':200,
            'msg':"",
            'result':[result]
            }

        return jsonify(response)



#地区管理
class Area_yun(object):

    def __init__(self):
        pass

    def get_area_yun_data(self,data):
        custId = data['custId']
        nickName = data['nickName']
        operName = data['operName']
        token = data['token']
        
        q = Manage.query.all()
        
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
            'code':200,
            'msg':'',
            'result':data if data else []
            }
        return jsonify(response)
        

    def save_area_yun_data(self,item):
        
        ImpDate = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        item['ImpDate'] = ImpDate
        
        
            
        q = Manage(**item)
        
        db.session.add(q)
        db.session.commit()
        
        q = Manage.query.all()
        data = []
        result = {}
        ls = {}
        for obj in q:
            
            for i in obj.__dict__.keys():
                if i.startswith('_') or i.startswith('__'):
                    continue
                ls[i] = getattr(obj,i)
            data.append(ls)
        
        
        response = {
            'code':200,
            'msg':'',
            'result': data
            }
        return jsonify(response)

    def del_area_yun_data(self,data):
        id = data['id']
       
       
        
        Manage.query.filter_by(id = id).delete()
        db.session.commit()
        
        q = Manage.query.all()
        data = []
        result = {}
        ls = {}
        for obj in q:
            
            for i in obj.__dict__.keys():
                if i.startswith('_') or i.startswith('__'):
                    continue
                ls[i] = getattr(obj,i)
            data.append(ls)
       
        
        
        
        
        response = {
            'code':200,
            'msg':'',
            'result':data
            }

        return jsonify(response)



#自动：规则优化助手
class Auto_rule(object):

    def __init__(self):
        pass

    def get_rule_yun_data(self,data):
        custId = data['custId']
        nickName = data['nickName']
        operName = data['operName']
        token = data['token']
        
        q = Optimization.query.all()
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
                    'code':200,
                    'msg':'',
                    'result':data
                    }

        return jsonify(response)

    def get_rule_add_rule_yun_data(self,data):
        custId = data['custId']
        nickName = data['nickName']
        operName = data['operName']
        ruleName = data['ruleName']
        ruleObject = data['ruleObject']
        ruleRate = data['ruleRate']
        ruleTime = data['ruleTime']
        ruleTodo = data['ruleTodo']
        rules = data['rules']
        token = data['token']
        
        q = Optimization(ruleName=ruleName, token=token, nickName=nickName,
                        ruleObject=ruleObject,ruleRate=ruleRate,ruleTime=ruleTime,
                        ruleTodo=ruleTodo,rules=rules,
                      operName=operName, custId=custId)
        
        db.session.add(q)
        db.session.commit()
        
        q = Optimization.query.all()
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
            'code':200,
            'msg':'成功添加规则',
            'result':data if data else []
            }

        return jsonify(response)
        

    def get_rule_delete_rule_yun_data(self,data):
       
        id = data['id']
        
        Optimization.query.filter_by(id = id).delete()
        db.session.commit()
        
        q = Optimization.query.all()
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
            'code':200,
            'msg':'',
            'result': data
            }

        return jsonify(response)

    def get_rule_last_do_rule(self,data):
        
        id = data['id']
        Optimization.query.filter_by(id=id).update()

        
        q = Optimization.query.all()
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
            'code':200,
            'msg':'更新规则成功',
            'result': data
        }

        return jsonify(response)
        


#监控程序：神车无人值守
class Heiche(object):
    
    def __init__(self):
        pass

    def get_heiche_rsetsubway(self,data):
        operName = data['operName']
        
        q = Control.query.filter_by(operName = operName).first()
        
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
            'code':200,
            'msg':'成功添加规则',
            'result': data.pop(-1)
            }
        return jsonify(response)

    def get_heiche_bid_word_yun_data(self,data):

    
        
        q = BidWord.query.all()
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
            'code':200,
            'msg':'成功添加规则',
            'result':data
            }
            
        return jsonify(response)
        

    def get_heiche_crowd_yun_data(self, data):
        
        q = BidWord.query.all()
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
            'code':200,
            'msg':'',
            'result':data
            }

        return jsonify(response)

    def save_heiche_rsetsubway(self, item):
        
        q = Control(**item)
        
        db.session.add(q)
        db.session.commit()
        
        q = Control.query.all()
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
            'code':200,
            'msg':'保存配置成功',
            'result':data
            }

        return jsonify(response)
        
        




bid_word = Bid_word()#关键词功能
yun_backup = Yun_backup()#云人群备份功能
heiche = Heiche()#监控程序：神车无人值守
auto_rule = Auto_rule()#自动：规则优化助手
area_yun = Area_yun()#地区管理
tao_word = Tao_word()#淘口令功能
user_login = User_login()#用户登录

taobao_url = {
    #'site/login':user_login.pt,
    'site/get-bid-word-yun-word-data':bid_word.get_bid_word_yun_word_data,
    'site/save-bid-word-yun-word-data':bid_word.save_bid_word_yun_word_data,
    'site/del-bid-word-yun-word':bid_word.del_bid_word_yun_word,
    'site/get-crowd-yun-data':yun_backup.get_crowd_yun_data,
    'site/save-crowd-yun-data':yun_backup.save_crowd_yun_data,
    'site/del-crowd-yun-data':yun_backup.del_crowd_yun_data,
    'site/get-tkl-item-tag-info':tao_word.get_tkl_item_tag_info,
    'site/get-tkl-batch-create-tkl-data':tao_word.get_tkl_batch_create_tkl_data,
    'site/get-tkl-list-data':tao_word.get_tkl_list_data,
    'site/get-area-yun-data':area_yun.get_area_yun_data,
    'site/save-area-yun-data':area_yun.save_area_yun_data,
    'site/del-area-yun-data':area_yun.del_area_yun_data,
    'site/get-rule-yun-data':auto_rule.get_rule_yun_data,
    'site/get-rule-add-rule-yun-data':auto_rule.get_rule_add_rule_yun_data,
    'site/get-rule-delete-rule-yun-data':auto_rule.get_rule_delete_rule_yun_data,
    'site/get-rule-last-do-rule':auto_rule.get_rule_last_do_rule,
    'heiche/get-heiche-rsetsubway':heiche.get_heiche_rsetsubway,
    'heiche/get-heiche-crowd-yun-data':yun_backup.get_crowd_yun_data,
    'heiche/save-heiche-rsetsubway':heiche.save_heiche_rsetsubway,
    'heiche/get-heiche-bid-word-yun-data':bid_word.get_bid_word_yun_word_data,
    'site/gene-activation-code':gene_activation_code,
    'heiche/get-heiche-bid-word-yun-data':bid_word.get_bid_word_yun_word_data
    
    }


 


@admin.route('/taobao/api', methods=['GET', 'POST'])
@authorize
def get_users():
    #print(request.json)
    #return jsonify({'users': users}, {'r': request.args.get('r')})
    
    if request.args.get('r') in taobao_url:
        return taobao_url[request.args.get('r')](request.json)
        
        
    else:
        print(request.args.get('r'))
        return None


@admin.route('/taobao/apis', methods=['GET', 'POST'])
def user():
    if request.args.get('r') == 'site/login':
        return user_login.pt(request.json)

