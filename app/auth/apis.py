#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, flash
from flask import request, session
from . import auth
import random  
import string
from functools import wraps
import time
import json

def authorize(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs): # 这里就像过滤器，有了那个修饰器标志的视图函数都必须经过这个函数才可以返回请求
        if request.args.get('name') == 'jm':
            return fn(*args, **kwargs)
            
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

wrzs = """
if (!getUrlInfo()) { return false };
            var cf_openRunHeicheWindow = function () {
                var divUI = '<div style="padding: 15px; line-height: 22px; background-color: #fff; color: #000;">'
                    + '开始运行:<span id="jk_StartTime"></span><br>' + '当前监控计划ID：<input type="text" class="input" style="width:150px;" id="ipt_campaignId" />'
                    + '--监控宝贝ID：<input type="text" class="input" style="width:150px;" id="ipt_itemId" /> '
                    + '类目标识：<input type="text" class="input" style="width:150px;" id="ipt_CatID" /><br>'
                    + '云关键词：<span id="lb_YunWordInfo"></span> -- 云人群包：<span id="lb_YunRenqunInfo"></span><br>'
                    + '创意标题：<input type="text" class="input" style="width:500px;"id="ipt_cyTitle" /><br>'
                    + '创意图片：<input type="text" class="input" style="width:500px;"id="ipt_cyPic_1" /><br>'
                    + '监控条件：关键词(<b id="lb_jkWord"></b>)当前首条出价(<b id="lb_jkWordFristPrice"></b>)--'
                    + '当首条出价高于:<input type="text" class="input" style="width:50px;" id="ipt_jkWordMaxPrice" /> 执行恢复宝贝！<br> '
                    + '<label for="ck_IsUpdatecy"><input type="checkbox" id="ck_IsUpdatecy" checked="true" value=""/><b>删除前修改创意图片：</b></label>'
                    + '<input type="text" class="input" style="width:500px;" id="ipt_UpdatecyPic"><br> '
                    + '每隔<input type="text" class="input" style="width:50px;" value="300" id="ipt_jkWordTime" />秒检查！'
                    + '<label for="ck_IsTime"><input type="checkbox" id="ck_IsTime" checked="true" value=""/><b>宝贝在线时间段：</b></label>(<input type="text" class="input" style="width:60px;" value="8:00" id="ipt_jksTime" />--<input type="text" class="input" style="width:60px;" value="23:00" id="ipt_jkeTime" />)<b>非时段将删除宝贝维护计划！</b><br>'
                    + '<label for="ck_IsQAdd"><input type="checkbox" id="ck_IsQAdd" checked="true" value=""/><b>极速添加--等待</b></label><input type="text" class="input" style="width:60px;" value="3" id="ipt_QWait" />秒(必须小于监控步长时间)<br>'
                    + '服务信息:<span id="jk_LastTime"></span><br>' + '<button class="layui-btn" id="bt_StartJianKong">开始监控</button>'
                    + '<button class="layui-btn layui-btn-primary" id="bt_StopJianKong">暂停监控</button>' + '<button class="layui-btn layui-btn-primary" id="bt_SaveConfigHeicheYUN">保存配置</button><br>'
                    + '恢复记录:<span id="lb_jkInfomsg"></span>' + '</div>';
                var index = layer.open({
                    type: 1, content: divUI,
                    area: ["850px", "600px"],
                    title: ['监控程序-神车无人值守', 'font-size:18px;'],
                    success: function (layero) {
                        var JianKongMian = function () {
                            getBidWordFristPrice = function () {
                                $.ajax({
                                    type: "post",
                                    url: "https://subway.simba.taobao.com/bidword/tool/bidword/getPriceBatchStrategy.htm",
                                    data: 'adGroupId=' + adGroupId + '&bidwordIds=' + fristWord['keywordId'] + '&type=mobile&sla=json&isAjaxRequest=true&token=' + User.token,
                                    async: false,
                                    success: function (data) {
                                        if (data.code == 200) {
                                            var res = data.result;
                                            fristWord['FristPrice'] = (res[0].wireless_fp_price) / 100;
                                            $("#lb_jkWordFristPrice").text(fristWord['FristPrice']);
                                        };
                                    },
                                    error: function () { }
                                });
                            }//new Function(getcfService("heiche/get-heiche-bid-word-frist-price-js", User));
                            getFristBidWord = function () {
                                //获取关键词表
                                $.ajax({
                                    type: "POST",
                                    url: "https://subway.simba.taobao.com/bidword/list.htm",
                                    data: "campaignId=" + campaignId + "&adGroupId=" + adGroupId + "&queryWord=&queryType=0&sla=json&isAjaxRequest=true&token=" + User.token,
                                    datatype: "json",
                                    async: false,
                                    success: function (data) {
                                        if (data.code == 200) {
                                            var bidWordList = data.result;
                                            if (bidWordList.length > 0) {
                                                fristWord['keywordId'] = bidWordList[0].keywordId;
                                                fristWord['word'] = bidWordList[0].word;
                                                $("#lb_jkWord").text(fristWord['word']);
                                                getBidWordFristPrice();

                                            };
                                        };
                                    },
                                });
                            }//new Function(getcfService("heiche/get-heiche-first-bid-word-js", User));
                            var myDate = new Date();
                            campaignId = getQueryString('campaignId');
                            adGroupId = getQueryString('adGroupId');
                            var cf_getItemNumId = function (adgid) {
                                var itemId = "";
                                $.ajax({
                                    type: "POST",
                                    url: "https://subway.simba.taobao.com/adgroup/get.htm?adGroupId=" + adgid,
                                    data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                    datatype: "json",
                                    async: false,
                                    success: function (data) {
                                        if (data.code == 200) { itemId = data.result.outsideItemNumId; }
                                        else {
                                            layer.msg(data.msg);
                                        }

                                    },
                                    error: function () { }
                                });
                                return itemId;
                            }//new Function("adgid", getcfService("comm/subway-get-item-num-id-js", User));

                            var itemId = cf_getItemNumId(adGroupId);
                            //var cf_getCatID=new Function("adGroupId",getcfService("Subway.getCatID",User));***
                            var cf_getCatID = function () {
                                var categoryId;
                                $.ajax({
                                    type: "POST",
                                    url: "https://subway.simba.taobao.com/adgroup/getAdGroupWithCategory.htm?adGroupId=" + adGroupId,
                                    data: null,
                                    async: false,
                                    dataType: "json",
                                    success: function (data) { if (data.code == 200) { categoryId = data.result.adGroupDTO.categoryId; }; },
                                    error: function () { alert("error:getCatID"); }
                                });
                                return categoryId;
                            }//new Function("adGroupId", getcfService("comm/subway-get-cat-ids", User));
                            var categoryId = cf_getCatID(adGroupId);
                            var getYunHeicheConfig = function () {
                                var resData = {};
                                var cf_getRsetSubway = function (itemId) {
                                    var ret = {};
                                    var postdata = { itemId: itemId };
                                    $.extend(postdata, User);
                                    console.log(postdata)
                                    $.ajax({
                                        type: "post",
                                        //url: "https://zhitongche.yiyoushi.net/index.php?r=heiche/get-heiche-rsetsubway",
                                        url: server_url + '/taobao/api?r=heiche/get-heiche-rsetsubway',
                                        contentType: 'application/json',
                                        data: JSON.stringify(postdata),
                                        async: false,
                                        dataType: "json",
                                        success: function (data, status) {
                                            ret = data;
                                            if (data.code != 200) {
                                                layer.alert(data.msg)
                                            }
                                        }
                                    });
                                    return ret;
                                };//new Function("itemId", getcfService("heiche/get-heiche-rset-subway-js", User));
                                var obj = cf_getRsetSubway(itemId);
                                if (obj.code == 200) {
                                    resData["itemId"] = obj.result.ItemId;
                                    resData["cybt"] = obj.result.CreativeTitle;
                                    resData["cytp_1"] = obj.result.CreativeImgUrl_1;
                                    resData["cytp_UpdatecyPic"] = obj.result.CreativeImgUrl_reset;

                                    resData["id"] = obj.result.id;
                                    resData["maxppc"] = obj.result.MaxPrice; resData["deletecy"] = obj.result.IsDelCreative;
                                    resData["editTime"] = obj.result.UpdateDate;
                                    resData["jkstep"] = obj.result.Step; resData["istime"] = obj.result.IsCheckTime;
                                    resData["stime"] = obj.result.StartTime; resData["etime"] = obj.result.EndTime;
                                    resData["expdate"] = obj.result.ExpDate;
                                    resData["IsQAdd"] = obj.result.IsQAdd;
                                    resData["QWait"] = obj.result.QWait
                                } else if (obj.code == "300") {
                                    resData["itemId"] = itemId;
                                    resData["cybt"] = '当前宝贝无监控值守权限，请联系管理员申请开通！';
                                    resData["id"] = "0"
                                };
                                return resData;
                            };//new Function("itemId", getcfService("heiche/get-heiche-config-js", User));
                            itemConfig = getYunHeicheConfig(itemId);

                            $("#jk_StartTime").text(myDate.toLocaleString() + '(授权有效期:[' + itemConfig["expdate"] + '])');

                            $("#ipt_campaignId").val(campaignId);
                            $("#ipt_itemId").val(itemId); $("#ipt_CatID").val(categoryId);
                            cf_getYunData = function (itemId) {
                                var cf_getWordYun = function (itemId, User) {
                                    var ret = {};
                                    var postdata = { itemId: itemId };
                                    $.extend(postdata, User);
                                    $.ajax({
                                        type: "post",
                                        //url: "https://zhitongche.yiyoushi.net/index.php?r=heiche/get-heiche-bid-word-yun-data",
                                        url: server_url + '/taobao/api?r=heiche/get-heiche-bid-word-yun-data',
                                        contentType: 'application/json',
                                        data: JSON.stringify(postdata),
                                        async: false,
                                        dataType: "json",
                                        success: function (data, status) {
                                            ret = data;
                                            if (data.code != 200) {
                                                layer.alert(data.msg)
                                            }
                                        }
                                    });
                                    return ret;
                                }//new Function("itemId", "User", getcfService("heiche/get-heiche-yun-bid-word-data-js", User));
                                BDData = { 'code': 1 };
                                BDData = cf_getWordYun(itemId, User);
                                //itemId == aList[id].ItemId ?

                                if (BDData['code'] == 200) {
                                    BDData = BDData.result;
                                    var new_date = new Date(BDData[0].ImpDate);
                                    var new_model = BDData[0];
                                    var if_this = false;
                                    for (var i = 0; i < BDData.length; i++) {
                                        if (itemId == BDData[i].itemId) {
                                            if (new_date < new Date(BDData[i].ImpDate) ) {
                                                new_date = new Date(BDData[i].ImpDate);
                                                new_model = BDData[i];
                                            }
                                            if_this = true;
                                        }
                                    }
                                    if (!if_this) {
                                        $("#lb_YunWordInfo").text("(数量【0】，更新时间【未知】)");
                                        layer.alert("未备份自身关键词，不能操作！");
                                        return;
                                    }
                                    $("#lb_YunWordInfo").text("(数量【" + new_model.count + "】，更新时间【" + new_model.ImpDate + "】)");
                                } else {
                                    $("#lb_YunWordInfo").text("(数量【0】，更新时间【未知】)");
                                    layer.alert("未备份关键词，不能操作！");

                                }




                                RQData = { 'code': 1 };
                                var cf_getTargetYun = function (itemId, User) {
                                    var ret = {};
                                    var postdata = { itemId: itemId };
                                    $.extend(postdata, User);
                                    $.ajax({
                                        type: "post",
                                        //url: "https://zhitongche.yiyoushi.net/index.php?r=heiche/get-heiche-crowd-yun-data",
                                        url: server_url + '/taobao/api?r=heiche/get-heiche-crowd-yun-data',
                                        contentType: 'application/json',
                                        data: JSON.stringify(postdata),
                                        async: false,
                                        dataType: "json",
                                        success: function (data, status) {
                                            ret = data;
                                            if (data.code != 200) {
                                                layer.alert(data.msg)
                                            }
                                        }
                                    });
                                    return ret;
                                };//new Function("itemId", "User", getcfService("heiche/get-heiche-yun-crowd-data-js", User));
                                RQData = cf_getTargetYun(itemId, User);
                                if (RQData['code'] == 200) {
                                    RQData = RQData.result;
                                    var new_date = new Date(RQData[0].ImpDate);
                                    var new_model = RQData[0];
                                    var if_this = false;
                                    for (var i = 0; i < RQData.length; i++) {
                                        if (itemId == RQData[i].itemId) {
                                            if (new_date < new Date(RQData[i].ImpDate)) {
                                                new_date = new Date(RQData[i].ImpDate);
                                                new_model = RQData[i];
                                            }
                                            if_this = true;
                                        }
                                    }
                                    if (!if_this) {
                                        $("#lb_YunWordInfo").text("(数量【0】，更新时间【未知】)");
                                        layer.alert("未备份自身人群，不能操作！");
                                        return;
                                    }
                                    $("#lb_YunRenqunInfo").text("(数量【" + new_model.count + "】，更新时间【" + new_model.ImpDate + "】)");
                                } else {
                                    $("#lb_YunRenqunInfo").text("(数量【0】，更新时间【未知】)");
                                    layer.alert("未备份人群，不能操作！");

                                }


                            };//new Function("itemId", getcfService("heiche/get-heiche-yun-data-js", User));
                            cf_getYunData(itemId);
                            /*var cf_getTargetTags = function () {
                                var TargetTags = {};
                                var cf_getCatID = function (arGroupId) {
                                    var categoryId;
                                    $.ajax({
                                        type: "POST",
                                        url: "https://subway.simba.taobao.com/adgroup/getAdGroupWithCategory.htm?adGroupId=" + adGroupId,
                                        data: null,
                                        async: false,
                                        dataType: "json",
                                        success: function (data) { if (data.code == 200) { categoryId = data.result.adGroupDTO.categoryId; }; },
                                        error: function () { alert("error:getCatID"); }
                                    });
                                    return categoryId;

                                };// new Function("adGroupId", getcfService("comm/subway-get-cat-ids", User));
                                var catId = cf_getCatID(UriInfo.adGroupId);
                                if (!catId) return;
                                var fristCat = catId.split(' ')[0];
                                //
                                节日人群  同类店铺人群 付费广告 / 活动人群
                                for (var crowdType = 0; crowdType <= 3; crowdType++) {
                                    var cf_crowdTemplateGetLayoutExt = function (crowdType, UriInfo, User) {
                                        var result = {};
                                        $.ajax({
                                            type: "POST", url: "https://subway.simba.taobao.com/crowdTemplate/getLayoutExt.htm?bizType=1&productId=101001005&crowdType=" + crowdType + "&adgroupId=" + UriInfo.adGroupId,
                                            data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                            async: false, dataType: "json",
                                            success: function (data) {
                                                if (data.code == 200) { result = data.result; };
                                            },
                                            error: function () { }
                                        });
                                        return result;
                                    };// new Function("crowdType", "UriInfo", "User", getcfService("comm/subway-crowd-template-get-layout-ext", User));
                                    var result = cf_crowdTemplateGetLayoutExt(crowdType, UriInfo, User);
                                    for (var indx in result) {
                                        var templateId = result[indx].id;
                                        var dimDTOs = result[indx].dimDTOs;
                                        for (var dd in dimDTOs) {
                                            var tagOptions = dimDTOs[dd].tagOptions;
                                            for (var tp in tagOptions) {
                                                var tagName = tagOptions[tp].tagName;
                                                var tagCode = '{"dimId":"' + tagOptions[tp].dimId + '","tagId":"' + tagOptions[tp].tagId + '","tagName":"' + tagOptions[tp].tagName + '","optionGroupId":"' + tagOptions[tp].optionGroupId + '"}';
                                                if (!TargetTags[tagName]) {
                                                    TargetTags[tagName] = {
                                                        "tagName": tagName,
                                                        "templateId": templateId,
                                                        "tagCode": tagCode
                                                    };
                                                };
                                            };
                                        };
                                    };
                                };
                                //天气人群  人口属性人群
                                var cf_crowdTemplateGetLayoutExtCat = function (firstCat, User) {
                                    var result = {};
                                    $.ajax({
                                        type: "POST",
                                        url: "https://subway.simba.taobao.com/crowdTemplate/getLayoutExt.htm?productId=101001005&bizType=1&firstCat=" + fristCat,
                                        data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                        async: false, dataType: "json",
                                        success: function (data) {
                                            if (data.code == 200) {
                                                result = data.result;
                                            };
                                        },
                                        error: function () { }
                                    });
                                    return result;
                                };// new Function("fristCat", "User", getcfService("comm/subway-crowd-template-get-layout-ext-cat", User));
                                var result = cf_crowdTemplateGetLayoutExtCat(fristCat, User);
                                for (var indx in result) {
                                    var templateId = result[indx].id;
                                    var dimDTOs = result[indx].dimDTOs;
                                    for (var dd in dimDTOs) {
                                        var tagOptions = dimDTOs[dd].tagOptions;
                                        for (var tp in tagOptions) {
                                            var tagName = tagOptions[tp].tagName;
                                            var tagCode = '{"dimId":"' + tagOptions[tp].dimId + '","tagId":"' + tagOptions[tp].tagId + '","tagName":"' + tagOptions[tp].tagName + '","optionGroupId":"' + tagOptions[tp].optionGroupId + '"}';
                                            if (!TargetTags[tagName]) {
                                                TargetTags[tagName] = {
                                                    "tagName": tagName,
                                                    "templateId": templateId,
                                                    "tagCode": tagCode
                                                };
                                            };
                                        };
                                    };
                                };
                                return TargetTags;
                            };*///new Function(getcfService("heiche/get-heiche-yun-target-tags-js", User));
                            TargetTags = app.cf_getTargetTags();
                            getFristBidWord();
                            $("#bt_StopJianKong").attr({ "disabled": "disabled" });
                            if (itemConfig["id"] == "0") {
                                $("#bt_StopJianKong").attr({ "disabled": "disabled" });
                                $("#bt_StartJianKong").attr({ "disabled": "disabled" });
                                $("#ipt_cyTitle").val(itemConfig["cybt"])
                            } else {

                                $("#ipt_cyTitle").val(itemConfig["cybt"]);
                                $("#ipt_cyPic_1").val(itemConfig["cytp_1"]);
                                $("#ipt_UpdatecyPic").val(itemConfig["cytp_UpdatecyPic"]);
                                $("#ipt_jkWordMaxPrice").val(itemConfig["maxppc"]);
                                if (itemConfig["deletecy"] == "1") { $("#ck_IsUpdatecy").attr("checked", true) } else { $("#ck_IsUpdatecy").attr("checked", false) };
                                $("#ipt_jkWordTime").val(itemConfig["jkstep"]);
                                if (itemConfig["istime"] == "1") { $("#ck_IsTime").attr("checked", true) } else { $("#ck_IsTime").attr("checked", false) };
                                $("#ipt_jksTime").val(itemConfig["stime"]); $("#ipt_jkeTime").val(itemConfig["etime"]);
                                if (itemConfig["IsQAdd"] == "1") { $("#ck_IsQAdd").attr("checked", true) } else { $("#ck_IsQAdd").attr("checked", false) };
                                $("#ipt_QWait").val(itemConfig["QWait"])
                            };
                            var StepTime = 60 * 1000;
                            var jiankongDoNew = function () {
                                var myDate = new Date();
                                //防退出
                                getServerDate();

                                //监控推广
                                if (IsRuning) {
                                    if (IsOnlineTime()) {
                                        if (IsHave()) {
                                            //推广单元存在
                                            if (fristWord['keywordId'] == "") {
                                                getFristBidWord();
                                            };
                                            if (!fristWord['FristPrice'] || fristWord['FristPrice'] == "-0.01") {
                                                getBidWordFristPrice();
                                            };
                                        } else {
                                            //推广单元不存在 添加推广
                                            saveItemSmartSolution();
                                            //刷新推广单元ID
                                            //获取首条出价
                                            window.setTimeout(function () { IsHave(); getFristBidWord(); }, 5000);

                                        };
                                    } else {
                                        //不在推广时段 删除维护
                                        if (IsHave()) {
                                            //====删除宝贝======
                                            IsUpdateCy = $('#ck_IsUpdatecy').prop('checked');
                                            if (IsUpdateCy) {
                                                updateCreative(adGroupId);
                                                var dateStart = new Date(),
                                                    dateEnd;
                                                while (((dateEnd = new Date()) - dateStart) <= 5000) {
                                                };
                                            };
                                            deleteAdGroup(adGroupId);
                                        };
                                    };
                                };
                                $("#jk_LastTime").text(myDate.toLocaleString() + ' NewAdGroupId:' + adGroupId);
                            };//new Function(getcfService("heiche/get-heiche-jian-kong-do-new-js", User));
                            jiankongDoNew();
                            timeId = window.setInterval(jiankongDoNew, StepTime);
                        }//new Function(getcfService("heiche/get-heiche-jian-kong-mian-js", User));
                        JianKongMian();
                    },
                    cancel: function (index, layero) {
                        var jiankongStop = function () {
                            layer.msg("停止监控！");
                            $("#bt_StartJianKong").text("开始监控");
                            $("#bt_StartJianKong").removeAttr("disabled");//将按钮可用
                            $("#bt_StopJianKong").attr({ "disabled": "disabled" });
                            IsRuning = false;
                            window.clearInterval(timeId2);
                        }//new Function(getcfService("heiche/get-heiche-stop-js", User));
                        jiankongStop(); layer.close(index)
                    }
                });
                $("#bt_StartJianKong").click(function () {
                    var jiankongAdgroup = function () {
                        if (Version == 'test') {
                            jiankongAdgroup();
                            return;
                        };
                        //if (itemConfig["id"] == "0") {
                        //    layer.msg('无人值守功能仅对指定宝贝开通！<br/>需要对当前宝贝ID（' + itemConfig["itemId"] + '）授权！<br/> 请联系交流群管理授权！');
                        //    return;
                        //};
                        IsOnlineTime = function () {
                            var isonline = true;
                            var obj = document.getElementById("ck_IsTime");//
                            if (obj.checked) { isonline = false; } else { isonline = true; };
                            if (!isonline) {
                                var st = $("#ipt_jksTime").val();
                                var et = $("#ipt_jkeTime").val();
                                var ar = [st, et];
                                isonline = checkTime(ar);
                            };
                            return isonline;
                        };// new Function(getcfService("heiche/get-heiche-is-online-time-js", User));
                        IsHave = function () {
                            var haveing = false;
                            var cam_id = $("#ipt_campaignId").val();
                            var item_id = $("#ipt_itemId").val();
                            var url = 'https://subway.simba.taobao.com/adgroup/adGroupList.htm?queryVO={"pageNumber":1,"pageSize":200,"queryTitle":"","queryState":"","campaignId":"' + cam_id + '"}';
                            var postdata = "sla=json&isAjaxRequest=true&token=" + User.token;
                            $.ajax({
                                type: 'POST',
                                url: url,
                                data: postdata,
                                async: false,
                                success: function (data) {
                                    var items = data.result.items;
                                    for (var idx in items) {
                                        if (items[idx].adGroupDTO.outsideItemNumId == item_id) {
                                            haveing = true;
                                            itemPicUrl = items[idx].adGroupDTO.imgUrl;
                                            adGroupId = items[idx].adGroupDTO.adGroupId;
                                        };
                                    };
                                },
                                error: function () { }
                            });
                            return haveing;
                        };// new Function(getcfService("heiche/get-heiche-is-have-js", User));
                        saveItemSmartSolution = function () {
                            var cam_id = $("#ipt_campaignId").val();
                            var item_id = $("#ipt_itemId").val();
                            var cat_id = $("#ipt_CatID").val();


                            var cyTile = $("#ipt_cyTitle").val();
                            var cyPic = $("#ipt_cyPic_1").val();
                            cf_getYunData(item_id);



                            cf_getYunData(item_id);
                            if (BDData['code'] == 1) {
                                layer.alert('关键词备份数据获取失败，不能操作');
                                return false;
                            }
                            if (RQData['code'] == 1) {
                                layer.alert('人群备份数据获取失败，不能操作');
                                return false;
                            }


                            var addWords = BDData.BidWordData;
                            if (addWords != '' && addWords != null) { addWords = addWords.replace(/maxPrice/g, 'bidPrice').replace(/maxMobilePrice/g, 'mobileBidPrice'); }


                            if (addWords == '' || addWords == null) {
                                layer.alert('关键词没有备份，不能操作');
                                return;
                            }



                            var addCrowds = '[]';
                            if (typeof RQData.CrowdData == 'undefined' || typeof RQData.CrowdData == undefined || RQData.CrowdData == '') {
                                addCrowds = '[]';
                            } else {


                                var targetArr = RQData.CrowdData.split("#");
                                var targetings = new Array();
                                var e = 0;
                                for (var i = 0; i < targetArr.length; i++) {
                                    var tag = targetArr[i].split('$');
                                    var tagName = tag[0].split(',');
                                    var discount = tag[1];
                                    var onlineStatus = tag[2];
                                    var tagList = new Array();
                                    var templateId;
                                    if (typeof TargetTags[tagName[0]] == 'undefined' || TargetTags[tagName[0]] == '' || TargetTags[tagName[0]] == null) { continue; }

                                    for (var j = 0; j < tagName.length; j++) {
                                        tagList.push(TargetTags[tagName[j]].tagCode);
                                        templateId = TargetTags[tagName[j]].templateId;
                                    };
                                    targetings.push('{"crowdDTO":{"templateId":"' + templateId
                                        + '","name":"' + tag[0]
                                        + '","tagList":[' + tagList.join(',') + ']}'
                                        + ',"discount":' + discount + ',"targetingType":1}');
                                }
                                addCrowds = '[' + targetings.join(',') + ']';

                            }

                            if (cyPic != '') {
                                cyPic = cyPic.replace(/https:/, '');
                                cyPic = cyPic.replace(/http:/, '');
                                cyPic = cyPic.replace(/\/\/img./, '//gd1.');
                            }

                            var postData = {
                                itemADGroupVO: '{"campaignId":"' + cam_id + '","itemNumId":"' + item_id + '","sortId":"' + cat_id + '","creativeElementList":[{"cname":"TITLE","cvalue":"' + cyTile + '"},{"cname":"IMGURL","cvalue":"' + cyPic + '"},{"cname":"SUBTITLE","cvalue":""},{"cname":"DESCRIPTION","cvalue":""},{"cname":"LINKURL","cvalue":"http://item.taobao.com/item.htm?id=' + item_id + '"},{"cname":"DISPLAYURL","cvalue":""},{"cname":"NPXSCORE","cvalue":""},{"cname":"MINISTORY","cvalue":""},{"cname":"DOCUMENTS","cvalue":""}],"elementTId":"1","creativeImgUrl":"' + cyPic + '","creativeTitle":"' + cyTile + '","qualityflag":0,"defaultPrice":"10","autoMatchState":1,"nonSearchState":1,"logsBidwordStr":""}',
                                addWords: addWords,
                                analyseTraceId: 'ac1dc00514974263452964085e',
                                sla: 'json',
                                isAjaxRequest: true,
                                token: User.token
                            };
                            if (addCrowds != '') {
                                postData['addCrowds'] = addCrowds
                            }
                            $.ajax({
                                type: "POST",
                                url: "https://subway.simba.taobao.com/smartsolution2/saveItemSmartSolution.htm",
                                data: postData,
                                async: false,
                                success: function (data) {
                                    var ret = data;
                                    var myDate = new Date();
                                    $("#lb_jkInfomsg").prepend(myDate.toLocaleString() + ':添加推广单元<br>');
                                    var infoHtml = $("#lb_jkInfomsg").html();
                                    var pos = infoHtml.indexOf("<br>", 500);
                                    if (pos > 0) {
                                        $("#lb_jkInfomsg").html(infoHtml.substring(0, pos));
                                    };
                                },
                                error: function () {
                                    alert('error:saveItemSmartSolution');
                                }
                            });
                        };// new Function(getcfService("heiche/get-save-item-smart-solution-js", User));
                        updateCreative = function (adgid) {
                            var creativeId;
                            $.ajax({
                                type: 'POST',
                                url: 'https://subway.simba.taobao.com/creative/list.htm?adGroupId=' + adgid,
                                data: 'sla=json&isAjaxRequest=true&token=' + User.token,
                                async: false,
                                success: function (data) {
                                    if (data.code == 200) {
                                        if (data.result.length > 0) { creativeId = data.result[0].creativeId; }

                                    };
                                },
                            });
                            if (!creativeId) {
                                return;
                            };

                            var cyTile = $("#ipt_cyTitle").val();
                            var item_id = $("#ipt_itemId").val();
                            if ($.trim($('#ipt_UpdatecyPic').val()) != '') {
                                itemPicUrl = $('#ipt_UpdatecyPic').val();
                            }
                            if (typeof itemPicUrl == 'undefined' || itemPicUrl == '') { itemPicUrl = $('#ipt_cyPic').val(); }
                            if (itemPicUrl == '') { return; }

                            itemPicUrl = itemPicUrl.replace(/https:/, '');
                            itemPicUrl = itemPicUrl.replace(/http:/, '');
                            itemPicUrl = itemPicUrl.replace(/\/\/img./, '//gd1.');





                            var postdata = 'creative={"creativeElementList":[{"cname":"TITLE","cvalue":"' + cyTile + '"},{"cname":"IMGURL","cvalue":"' + itemPicUrl + '"},{"cname":"SUBTITLE","cvalue":""},{"cname":"DESCRIPTION","cvalue":""},{"cname":"LINKURL","cvalue":"http://item.taobao.com/item.htm?id=' + item_id + '"},{"cname":"DISPLAYURL","cvalue":""},{"cname":"NPXSCORE","cvalue":""},{"cname":"MINISTORY","cvalue":""},{"cname":"DOCUMENTS","cvalue":""}],"campaignId":"' + campaignId + '","adGroupId":"' + adgid + '","creativeId":"' + creativeId + '","elementTId":"1","qualityflag":0,"creativeAdvancedSettingDTO":{"channel":{"pc":"1","wireless":"1"}},"templateData":null,"creativeCenterTemplateId":null,"sailingType":null}'
                                + '&sla=json&isAjaxRequest=true&token=' + User.token;

                            //修改创意
                            $.ajax({
                                type: "POST",
                                url: 'https://subway.simba.taobao.com/creative/updateCreative.htm',
                                data: postdata,
                                async: false,
                                success: function (data) {
                                    var ret = data.code;
                                },
                                error: function () { }
                            });
                        };// new Function("adgid", getcfService("heiche/get-heiche-update-creative-js", User));
                        deleteAdGroup = function (adgid) {
                            $.ajax({
                                type: "POST",
                                url: "https://subway.simba.taobao.com/adgroup/deleteAdGroup.htm",
                                data: 'campaignId=' + campaignId + '&adGroupIds=["' + adgid + '"]&sla=json&isAjaxRequest=true&token=' + User.token,
                                async: false,
                                success: function (data) {
                                    var ret = data.code;
                                    fristWord['keywordId'] = "";
                                    var myDate = new Date();
                                    $("#lb_jkInfomsg").prepend(myDate.toLocaleString() + ':删除推广单元(' + adgid + ')--当前首条出价:' + fristWord['FristPrice'] + '元<br>');
                                    adGroupId = "";
                                },
                                error: function () { }
                            });
                        };// new Function("adgid", getcfService("heiche/get-heiche-delete-ad-group-js", User));

                        layer.msg("监控程序打开！");
                        var maxPrice = $("#ipt_jkWordMaxPrice").val();
                        fristWord['MaxPrice'] = maxPrice;
                        var dit = parseInt($("#ipt_jkWordTime").val());
                        $("#bt_StartJianKong").text("监控中...");
                        $("#bt_StartJianKong").attr({ "disabled": "disabled" });
                        $("#bt_StopJianKong").removeAttr("disabled");//将按钮可用
                        var obj = document.getElementById("ck_IsUpdatecy");//
                        if (obj.checked) { IsUpdateCy = true; } else { IsUpdateCy = false; };
                        var obj1 = document.getElementById("ck_IsQAdd");//
                        if (obj1.checked) { IsQAdd = true; } else { IsQAdd = false; };
                        QWait = $("#ipt_QWait").val();
                        IsRuning = true;
                        var runingAdgroup = function () {
                            if (!IsOnlineTime()) return;
                            if (adGroupId == "") return;
                            var maxPrice = $("#ipt_jkWordMaxPrice").val();
                            fristWord['MaxPrice'] = maxPrice;
                            getBidWordFristPrice();
                            if (parseFloat(fristWord['FristPrice']) >= parseFloat(fristWord['MaxPrice'])) {
                                //执行恢复宝贝！
                                layer.msg("需要执行恢复宝贝！");
                                //====删除宝贝======
                                IsUpdateCy = $('#ck_IsUpdatecy').prop('checked');
                                if (IsUpdateCy) {
                                    updateCreative(adGroupId);
                                    var dateStart = new Date(),
                                        dateEnd;
                                    while (((dateEnd = new Date()) - dateStart) <= 5000) {
                                    };
                                };
                                deleteAdGroup(adGroupId);
                                //极速添加宝贝
                                if (IsQAdd) {
                                    var dt = QWait * 1000;
                                    var dateStart = new Date(),
                                        dateEnd;

                                    while (((dateEnd = new Date()) - dateStart) <= dt) {
                                    };
                                    saveItemSmartSolution();
                                };
                            } else {
                                layer.msg("当前无需恢复，等待下轮检查！");
                            };
                        };// new Function(getcfService("heiche/get-heiche-runing-ad-group-js", User));
                        timeId2 = window.setInterval(runingAdgroup, dit * 1000);
                    };//new Function(getcfService("heiche/get-heiche-jian-kong-adgroup-js", User));
                    jiankongAdgroup()
                });

                $("#bt_StopJianKong").click(function () {
                    var BtjkStop = function () {
                        layer.msg("停止监控！");
                        $("#bt_StartJianKong").text("开始监控");
                        $("#bt_StartJianKong").removeAttr("disabled");//将按钮可用
                        $("#bt_StopJianKong").attr({ "disabled": "disabled" });
                        IsRuning = false;
                        window.clearInterval(timeId2);
                    };//new Function(getcfService("heiche/get-heiche-stop-js", User));
                    BtjkStop()
                });

                $("#bt_SaveConfigHeicheYUN").click(function () {
                    var SaveConfigHeicheYUN = function () {
                        //if (itemConfig["id"] == "0") {
                        //    layer.msg("当前宝贝未授权此功能,可以联系管理员申请开通！"); return
                        //};
                        itemConfig["cybt"] = $("#ipt_cyTitle").val();
                        itemConfig["cytp_1"] = $("#ipt_cyPic_1").val();
                        itemConfig["maxppc"] = $("#ipt_jkWordMaxPrice").val();
                        var obj = document.getElementById("ck_IsUpdatecy");
                        if (obj.checked) {
                            itemConfig["deletecy"] = "1"
                        } else {
                            itemConfig["deletecy"] = "0"
                        };
                        itemConfig["jkstep"] = $("#ipt_jkWordTime").val();
                        var obj2 = document.getElementById("ck_IsTime");
                        if (obj2.checked) {
                            itemConfig["istime"] = "1"
                        } else {
                            itemConfig["istime"] = "0"
                        };
                        itemConfig["stime"] = $("#ipt_jksTime").val();
                        itemConfig["etime"] = $("#ipt_jkeTime").val();
                        var obj3 = document.getElementById("ck_IsQAdd");
                        if (obj3.checked) {
                            itemConfig["IsQAdd"] = "1"
                        } else {
                            itemConfig["IsQAdd"] = "0"
                        };
                        itemConfig["QWait"] = $("#ipt_QWait").val();
                        var upYunHeicheConfig = function (itemData) {
                            var postData = {
                                itemId: itemData.itemId,
                                md5: User.md5,
                                nickName: User.nickName,
                                creativeImgUrl_1: itemData.cytp_1,
                                creativeImgUrl_reset: $('#ipt_UpdatecyPic').val(),

                                creativeTitle: itemData.cybt,
                                maxPrice: itemData.maxppc,
                                isDelCreative: itemData.deletecy,
                                step: itemData.jkstep,
                                isCheckTime: itemData.istime,
                                startTime: itemData.stime,
                                endTime: itemData.etime,
                                isQAdd: itemData.IsQAdd,
                                qWait: itemData.QWait
                            };
                            var pubRsetSubway = function (postdata) {
                                var ret = {};

                                $.extend(postdata, User);
                                $.ajax({
                                    type: "post",
                                    //url: "https://zhitongche.yiyoushi.net/index.php?r=heiche/save-heiche-rsetsubway",
                                    url: 'http://192.168.0.102:5000/taobao/api?r=heiche/save-heiche-rsetsubway',
                                    contentType: 'application/json',
                                    data: JSON.stringify(postdata),
                                    async: false,
                                    dataType: "json",
                                    success: function (data, status) {
                                        ret = data;
                                    }
                                });
                                return ret;
                            };// new Function("postdata", getcfService("heiche/get-heiche-update-config-yun-ajax-js", User));
                            var ret = pubRsetSubway(postData);
                            layer.msg(ret.msg);
                        };// new Function("itemData", getcfService("heiche/get-heiche-update-config-yun-js", User));
                        upYunHeicheConfig(itemConfig);
                    };//new Function(getcfService("heiche/get-heiche-save-config-yun-js", User));
                    SaveConfigHeicheYUN()
                });
            }//new Function(getcfService("heiche/window", User));
            cf_openRunHeicheWindow();
"""
rqyh = """
if (!getUrlInfo()) { return };
            cf_outerTargetingDataUI = function () {
                if (!adTargetingList) return;
                var bdDataTable = new Array();
                for (var iid in adTargetingList) {
                    bdDataTable.push(adTargetingList[iid]);
                };
                jQuery("#list2").jqGrid("clearGridData");
                jQuery("#list2").jqGrid("setGridParam", { data: bdDataTable });
                jQuery("#list2").trigger("reloadGrid");
            };//new Function(getcfService("site/get-crowd-outer-targeting-data-ui-js", User));
            var cf_openCrowdWindow = function () {
                var w = $(window).width() - 3 + 10;
                var h = $(window).height() - 5 + 10;
                var openArea = [w + 'px', h + 'px'];
                var index = layer.open({
                    type: 1,
                    content: '<div>' +
                        '   <div class="layui-form-item" style="margin-bottom: 2px;">    '
                        + '     <label class="layui-form-label layui-btn" id="lb_selectDate">范围选择</label>'
                        + '       <div class="layui-input-inline">'
                        + '            <input class="layui-input" placeholder="开始日" id="LAY_rqrange_s">'
                        + '       </div>'
                        + '        <div class="layui-input-inline">'
                        + '            <input class="layui-input" placeholder="截止日" id="LAY_rqrange_e"> '
                        + '        </div>'
                        + '        <div class="layui-input-inline">'
                        + '             <button class="layui-btn layui-btn-primary" id="bt_getrenqunRpt">拉取数据</button>'
                        + '        </div>'
                        + '             <div><div class="layui-btn-group">'
                        + '<button class="layui-btn layui-btn-normal" id="bt_getrenqunNums">标签词频</button>'
                        + '<button id="bt_editDiscount" class="layui-btn">修改溢价</button>'
                        + '<button id="bt_RqSart" class="layui-btn">参与推广</button>'
                        + '<button id="bt_RqStop" class="layui-btn">暂停推广</button>'
                        + '<button id="bt_RqDelete" class="layui-btn">删除</button>'
                        + '<button class="layui-btn layui-btn-danger" id="bt_TargetingYun">云人群包</button>'
                        + '</div></div>'
                        + '    </div>'
                        + '</div>'
                        + '<table id="list2"></table>'
                        + '<div id="pager2"></div>'
                        + '',
                    area: openArea,
                    offset: ['5px', '1px'],
                    title: ['人群优化', 'font-size:18px;'],
                    scrollbar: false,
                    //禁止浏览器滚动条
                    maxmin: false,
                });
                //layer.full(index);
                var start = {
                    min: laydate.now(-30),
                    //-1代表昨天，-2代表前天，以此类推
                    max: laydate.now(),
                    istoday: true,
                    choose: function (datas) {
                        end.min = datas; //开始日选好后，重置结束日的最小日期
                        end.start = datas //将结束日的初始值设定为开始日
                    }
                };
                var end = {
                    min: laydate.now(-30),
                    //-1代表昨天，-2代表前天，以此类推
                    max: laydate.now(),
                    istoday: true,
                    choose: function (datas) {
                        start.max = datas;
                        //结束日选好后，重置开始日的最大日期
                    }
                };

                $("#lb_selectDate").click(function () {
                    var strSUI = '<button class="layui-btn layui-btn-mini layui-btn-primary datebt" data=0>今天</button>'
                        + '<button class="layui-btn layui-btn-mini layui-btn-primary datebt" data=-1>昨天</button>'
                        + '<button class="layui-btn layui-btn-mini layui-btn-primary datebt" data=-2>过去2天</button>'
                        + '<button class="layui-btn layui-btn-mini layui-btn-primary datebt" data=-3>过去3天</button>'
                        + '<button class="layui-btn layui-btn-mini layui-btn-primary datebt" data=-7>过去7天</button>'
                        + '<button class="layui-btn layui-btn-mini layui-btn-primary datebt" data=-14>过去14天</button>'
                        + '<button class="layui-btn layui-btn-mini layui-btn-primary datebt" data=-30>过去30天</button>';
                    layer.tips(strSUI, '#lb_selectDate', {
                        tips: [3, "#009688"]
                    });
                    $(".datebt").click(function () {
                        var sDt = $(this).attr("data");
                        $("#LAY_rqrange_s").val(laydate.now(sDt));
                        $("#LAY_rqrange_e").val(laydate.now(sDt < 0 ? -1 : 0));
                    });
                });
                document.getElementById('LAY_rqrange_s').onclick = function () {
                    start.elem = this;
                    laydate(start);
                }
                document.getElementById('LAY_rqrange_e').onclick = function () {
                    end.elem = this;
                    laydate(end);
                };
                document.getElementById('bt_getrenqunRpt').onclick = function () {
                    var cf_do = function () {
                        var index = layer.load(0, { shade: false });
                        var startDate = $("#LAY_rqrange_s").val();
                        var endDate = $("#LAY_rqrange_e").val();
                        var theDate = laydate.now();
                        var postUrl;
                        if (startDate == "" && endDate == "") {
                            startDate = theDate;
                            endDate = theDate;
                            $("#LAY_rqrange_s").val(startDate);
                            $("#LAY_rqrange_e").val(endDate);
                        };
                        var rptBpp4pCrowdSubwayList = {};
                        if (startDate == theDate) {
                            rptBpp4pCrowdSubwayList = rptBpp4pCrowdRealtimeSubwayList(theDate, UriInfo, User);
                        } else {
                            if (startDate > endDate) {
                                layer.msg("开始日期不能大于结束日期！请重新选择！");
                                layer.close(index);
                                return;
                            } else {
                                if (endDate >= theDate) {
                                    layer.msg("报表数据不能于实时(今日)同时拉取！请设置截止日期早于今日！");
                                    layer.close(index);
                                    return;
                                };
                                rptBpp4pCrowdSubwayList = rptBpp4pCrowdSubwayListFun(startDate, endDate, UriInfo, User);
                            };
                        };
                        for (var iid in adTargetingList) {
                            adTargetingList[iid].impression = null;
                            adTargetingList[iid].click = null
                            adTargetingList[iid].ctr = null;
                            adTargetingList[iid].cost = null;
                            adTargetingList[iid].cpc = null;
                            adTargetingList[iid].transactiontotal = null;
                            adTargetingList[iid].roi = null;
                            adTargetingList[iid].coverage = null;
                            adTargetingList[iid].transactionshippingtotal = null;
                            adTargetingList[iid].carttotal = null;
                            adTargetingList[iid].favtotal = null;
                            adTargetingList[iid].cpm = null;
                        };
                        for (var i = 0; i < rptBpp4pCrowdSubwayList.length; i++) {
                            var iid = rptBpp4pCrowdSubwayList[i].crowdid;
                            if (adTargetingList[iid]) {
                                adTargetingList[iid].impression = rptBpp4pCrowdSubwayList[i].impression ? (rptBpp4pCrowdSubwayList[i].impression / 1).toFixed(0) : 0;
                                adTargetingList[iid].click = rptBpp4pCrowdSubwayList[i].click ? (rptBpp4pCrowdSubwayList[i].click / 1).toFixed(0) : 0;
                                adTargetingList[iid].ctr = rptBpp4pCrowdSubwayList[i].ctr ? (rptBpp4pCrowdSubwayList[i].ctr / 1).toFixed(2) : "0.00";
                                adTargetingList[iid].cost = rptBpp4pCrowdSubwayList[i].cost ? (parseFloat(rptBpp4pCrowdSubwayList[i].cost) / 100).toFixed(2) : "0.00";
                                adTargetingList[iid].cpc = rptBpp4pCrowdSubwayList[i].cpc ? (parseFloat(rptBpp4pCrowdSubwayList[i].cpc) / 100).toFixed(2) : "0.00";
                                adTargetingList[iid].transactiontotal = rptBpp4pCrowdSubwayList[i].transactiontotal ? (parseFloat(rptBpp4pCrowdSubwayList[i].transactiontotal) / 100).toFixed(2) : "0.00";
                                adTargetingList[iid].roi = rptBpp4pCrowdSubwayList[i].roi ? parseFloat(rptBpp4pCrowdSubwayList[i].roi).toFixed(2) : "0.00";
                                adTargetingList[iid].coverage = rptBpp4pCrowdSubwayList[i].coverage ? parseFloat(rptBpp4pCrowdSubwayList[i].coverage).toFixed(2) : "0.00";
                                adTargetingList[iid].transactionshippingtotal = rptBpp4pCrowdSubwayList[i].transactionshippingtotal ? (rptBpp4pCrowdSubwayList[i].transactionshippingtotal / 1).toFixed(0) : 0;
                                adTargetingList[iid].carttotal = rptBpp4pCrowdSubwayList[i].carttotal ? (rptBpp4pCrowdSubwayList[i].carttotal / 1).toFixed(0) : 0;
                                adTargetingList[iid].favtotal = rptBpp4pCrowdSubwayList[i].favtotal ? (rptBpp4pCrowdSubwayList[i].favtotal / 1).toFixed(0) : 0;
                                adTargetingList[iid].cpm = rptBpp4pCrowdSubwayList[i].cpm ? (parseFloat(rptBpp4pCrowdSubwayList[i].cpm) / 100).toFixed(2) : "0.00";
                            };
                        };
                        //打印数据
                        cf_outerTargetingDataUI();
                        layer.close(index);

                    };//new Function(getcfService("site/get-crowd-rpt-data-js", User));
                    cf_do();
                    return;
                };
                //获取名称标签组合出现个数
                $("#bt_getrenqunNums").click(function () {
                    var cf_do = function () {
                        var sIds = getjqGridSelarrrow("#list2");
                        if (sIds.length < 1) {
                            layer.msg("未选中任何标签！");
                            return;
                        };
                        var mkName = "";
                        for (var i = 0; i < sIds.length; i++) {
                            if (mkName == "") {
                                mkName = jQuery("#list2").jqGrid("getCell", sIds[i], "name");
                            } else {
                                mkName = mkName + "," + jQuery("#list2").jqGrid("getCell", sIds[i], "name");
                            };
                        };
                        var mks = mkName.split(",");
                        var fres = {};
                        //用来记录所有的字符的出现频次
                        for (var i = 0; i < mks.length; i++) {
                            var wd = mks[i];
                            if (!fres[wd]) {
                                fres[wd] = 0;
                            }
                            fres[wd]++;
                        }
                        var msgHtml = "";
                        for (var p in fres) { msgHtml = msgHtml + "属性【" + p + "】出现次数：" + fres[p] + " 。</br>" };
                        layer.alert(msgHtml, { icon: 1 });
                    };//new Function(getcfService("site/get-crowd-renqun-nums", User));
                    cf_do();
                    return;
                });
                //批量修改溢价
                $("#bt_editDiscount").click(function () {
                    var cf_do = function () {
                        /*
    if (!getUserRank(2,UserRank)) {
        layer.msg("批量调整人群包标签功能仅对授权用户开放！<br/>需要对当前店铺（" + User.nickName + "）授权！<br/> 请联系交流群管理授权！");
        return;
    };
    */
                        layer.prompt({ title: "输入修改的溢价[5-300]之间，并确认", formType: 0 }, function (nds, index) {
                            layer.close(index);
                            var sIds = getjqGridSelarrrow("#list2");
                            if (sIds.length < 1) {
                                layer.msg("未选中任何人群包标签！");
                                return;
                            };
                            var int_nds = parseInt(nds);
                            if (int_nds < 5 || int_nds > 300) {
                                layer.msg("输入的溢价不在允许范围，请输入5-300的整数！");
                                return;
                            };
                            var targetings = new Array();
                            for (var i = 0; i < sIds.length; i++) {
                                var id = jQuery("#list2").jqGrid("getCell", sIds[i], "cid");
                                var iid = jQuery("#list2").jqGrid("getCell", sIds[i], "iid");
                                var nStr = '{"adgroupId":"' + UriInfo.adGroupId + '","crowdDTO":{"id":"' + iid + '"},"id":"' + id + '","isDefaultPrice":0,"discount":' + (int_nds + 100) + '}';
                                adTargetingList[iid].discount = int_nds;
                                targetings.push(nStr);
                            };
                            var cf_adgroupTargetingUpdate = function (targetings, User) {
                                var ret = false;
                                $.ajax({
                                    type: "POST",
                                    url: "https://subway.simba.taobao.com/adgroupTargeting/update.htm",
                                    data: "productId=101001005&bizType=1&targetings=[" + targetings.join(",") + "]&sla=json&isAjaxRequest=true&token=" + User.token,
                                    dataType: "json", async: false,
                                    success: function (data) {
                                        if (data.code == 200) { ret = true; };
                                    }, error: function () { alert("error:subway-crowd-edit-discount-js"); }
                                });
                                return ret;
                            };//new Function("targetings", "User", getcfService("site/subway-crowd-edit-discount-js", User));
                            if (cf_adgroupTargetingUpdate(targetings, User)) {
                                cf_outerTargetingDataUI();
                                layer.msg("溢价已更新！");
                                return;
                            } else {
                                layer.msg("更新数据失败；请刷新页面后重试！"); return;
                            };
                        });
                    };//new Function(getcfService("site/get-crowd-edit-discount-js", User));
                    cf_do();
                    return;
                });
                //批量参与推广
                $("#bt_RqSart").click(function () {
                    var cf_do = function () {
                        /*
    if (!getUserRank(2,UserRank)) {
        layer.msg("批量调整人群包标签功能仅对授权用户开放！<br/>需要对当前店铺（" + User.nickName + "）授权！<br/> 请联系交流群管理授权！");
        return;
    };
    */
                        var sIds = getjqGridSelarrrow("#list2");
                        if (sIds.length < 1) {
                            layer.msg("未选中任何标签！");
                            return;
                        };
                        var cf_changeCrowdOnlineStatus = function (sIds, Onlinestatus) {
                            var targetings = new Array();
                            for (var i = 0; i < sIds.length; i++) {
                                var id = jQuery("#list2").jqGrid("getCell", sIds[i], "cid");
                                var iid = jQuery("#list2").jqGrid("getCell", sIds[i], "iid");
                                var nStr = '{"adgroupId":"' + UriInfo.adGroupId + '","crowdDTO":{"id":"' + iid + '"},"id":"' + id + '","onlineStatus":"' + Onlinestatus + '"}';
                                targetings.push(nStr);
                                adTargetingList[iid].onlineStatus = Onlinestatus;
                            };
                            var cf_adgroupTargetingUpdate = function (targetings, User) {
                                var ret = false;
                                $.ajax({
                                    type: "POST", url: "https://subway.simba.taobao.com/adgroupTargeting/update.htm",
                                    data: "productId=101001005&bizType=1&targetings=[" + targetings.join(",") + "]&sla=json&isAjaxRequest=true&token=" + User.token,
                                    dataType: "json",
                                    async: false,
                                    success: function (data) {
                                        if (data.code == 200) {
                                            ret = true;
                                        };
                                    }, error: function () { }
                                });
                                return ret;
                            };// new Function("targetings", "User", getcfService("site/subway-crowd-adgroup-targeting-update", User));
                            if (cf_adgroupTargetingUpdate(targetings, User)) {
                                cf_outerTargetingDataUI();
                                layer.msg("推广状态已更新！");
                                return;
                            } else { layer.msg("更新数据失败；请刷新页面后重试！"); return; };
                        };// new Function("sIds", "Onlinestatus", getcfService("site/change-crowd-online-status", User));
                        cf_changeCrowdOnlineStatus(sIds, "1");
                    };//new Function(getcfService("site/get-crowd-rq-start", User));
                    cf_do();
                    return;
                });
                //批量暂停推广
                $("#bt_RqStop").click(function () {
                    var cf_do = function () {
                        /*
    if (!getUserRank(2,UserRank)) {
layer.msg("批量调整人群包标签功能仅对授权用户开放！<br/>需要对当前店铺（"+ User.nickName + "）授权！<br/> 请联系交流群管理授权！");
return;
};
    */
                        var sIds = getjqGridSelarrrow("#list2");
                        if (sIds.length < 1) {
                            layer.msg("未选中任何标签！");
                            return;
                        };
                        var cf_changeCrowdOnlineStatus = function (sIds, Onlinestatus) {
                            var targetings = new Array();
                            for (var i = 0; i < sIds.length; i++) {
                                var id = jQuery("#list2").jqGrid("getCell", sIds[i], "cid");
                                var iid = jQuery("#list2").jqGrid("getCell", sIds[i], "iid");
                                var nStr = '{"adgroupId":"' + UriInfo.adGroupId + '","crowdDTO":{"id":"' + iid + '"},"id":"' + id + '","onlineStatus":"' + Onlinestatus + '"}';
                                targetings.push(nStr);
                                adTargetingList[iid].onlineStatus = Onlinestatus;
                            };
                            var cf_adgroupTargetingUpdate = function (targetings, User) {
                                var ret = false;
                                $.ajax({
                                    type: "POST", url: "https://subway.simba.taobao.com/adgroupTargeting/update.htm",
                                    data: "productId=101001005&bizType=1&targetings=[" + targetings.join(",") + "]&sla=json&isAjaxRequest=true&token=" + User.token,
                                    dataType: "json",
                                    async: false,
                                    success: function (data) {
                                        if (data.code == 200) {
                                            ret = true;
                                        };
                                    }, error: function () { }
                                });
                                return ret;
                            };//new Function("targetings", "User", getcfService("site/subway-crowd-adgroup-targeting-update", User));
                            if (cf_adgroupTargetingUpdate(targetings, User)) {
                                cf_outerTargetingDataUI();
                                layer.msg("推广状态已更新！");
                                return;
                            } else { layer.msg("更新数据失败；请刷新页面后重试！"); return; };
                        };//new Function("sIds", "Onlinestatus", getcfService("site/change-crowd-online-status", User));
                        cf_changeCrowdOnlineStatus(sIds, "0");
                    };//new Function(getcfService("site/get-crowd-rq-stop", User));
                    cf_do(); return;
                });
                //批量删除
                $("#bt_RqDelete").click(function () {
                    var cf_do = function () {
                    	/*
		if (!getUserRank(2,UserRank)) {
	layer.msg("批量调整人群包标签功能仅对授权用户开放！<br/>需要对当前店铺（"+ User.nickName + "）授权！<br/> 请联系交流群管理授权！");
	return;
};
		*/
                        var sIds = getjqGridSelarrrow("#list2");
                        if (sIds.length < 1) {
                            layer.msg("未选中任何标签！");
                            return;
                        };
                        layer.confirm("确定要删除这些人群包数据?一旦删除，所有数据将无法恢复！", { icon: 3, title: "确认删除" }, function (index) {
                            layer.close(index);
                            var crowds = new Array();
                            var ids = new Array();
                            for (var i = 0; i < sIds.length; i++) {
                                var id = jQuery("#list2").jqGrid("getCell", sIds[i], "cid");
                                var iid = jQuery("#list2").jqGrid("getCell", sIds[i], "iid");
                                delete adTargetingList[iid];
                                var nStr_iid = '"' + iid + '"';
                                var nStr_id = '"' + id + '"';
                                crowds.push(nStr_iid);
                                ids.push(nStr_id);
                            };
                            var postData = 'adgroupId=' + UriInfo.adGroupId + '&crowds=[' + crowds.join(",") + ']&productId=101001005&bizType=1&ids=[' + ids.join(",") + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                            var cf_adgroupTargetingDelete = function (postData) {
                                var ret = false;
                                $.ajax({
                                    type: "POST",
                                    url: "https://subway.simba.taobao.com/adgroupTargeting/delete.htm",
                                    data: postData,
                                    async: false,
                                    dataType: "json",
                                    success: function (data) {
                                        if (data.code == 200) {
                                            ret = true;
                                        };
                                    },
                                    error: function () { }
                                });
                                return ret;
                            };//new Function("postData", getcfService("site/subway-crowd-adgroup-targeting-delete", User));
                            if (cf_adgroupTargetingDelete(postData)) {
                                cf_outerTargetingDataUI();
                                layer.msg("标签已删除！");
                                return;
                            } else {
                                layer.msg("更新数据失败；请刷新页面后重试！");
                                return;
                            };
                        });
                    };//new Function(getcfService("site/get-crowd-rq-detele", User));
                    cf_do();
                    return;
                });
                //人群标签云处理 备份
                $("#bt_TargetingYun").click(function () {
                    var cf_do = function () {
                        var cf_getAdgroup = function (UriInfo, User) {
                            var ret;
                            $.ajax({
                                type: "POST",
                                url: "https://subway.simba.taobao.com/adgroup/get.htm?adGroupId=" + UriInfo.adGroupId,
                                data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                dataType: "json",
                                async: false,
                                success: function (data) {
                                    ret = data.result;
                                },
                                error: function () {
                                    alert("error:getAdgroup");
                                }
                            });
                            return ret;
                        };//new Function("UriInfo", "User", getcfService("site/get-adgroup", User));
                        var AdgroupInfo = cf_getAdgroup(UriInfo, User);
                        var itemId = AdgroupInfo.outsideItemNumId; if (itemId != "") { } else { layer.msg("获取宝贝数据失败，请重新登陆！"); return };

                        var strUI = '<div style="padding: 15px; line-height: 22px; background-color: #fff; color: #000;">' + '<div id="uaList" style="height:245px">'
                            + '<span id="ua01">'
                            + '青色分线 <button class="layui-btn layui-btn-mini layui-btn-normal">应用到当前计划</button><button class="layui-btn layui-btn-mini layui-btn-danger">删除</button>'
                            + '<hr class="layui-bg-cyan">'
                            + '</span>'
                            + '<span id="ua02">'
                            + '青色分割线 <button class="layui-btn layui-btn-mini layui-btn-normal">应用到当前计划</button><button class="layui-btn layui-btn-mini layui-btn-danger">删除</button>'
                            + '<hr class="layui-bg-cyan">' + '</span>' + '</div>' + '<button class="layui-btn layui-btn-small layui-btn-normal" id="BakUserCrowdBt">备份人群包</button>'
                            + '</div>';
                        layer.open({
                            type: 1, area: ['600px', '350px'], id: 'LAY_layuipro', moveType: 1, content: strUI,
                            success: function (layero, index) {
                                var GetUserCrowdList = function (postData) {
                                    var ret = new Array();
                                    $.ajax({
                                        type: "post",
                                        //url: "https://zhitongche.libangjie.com/index.php?r=site/get-crowd-yun-data",
                                        url: server_url + '/taobao/api?r=site/get-crowd-yun-data',
                                        contentType: "application/json",
                                        data: JSON.stringify(postData),
                                        async: false,
                                        dataType: "json",
                                        success: function (data, status) {
                                            if (data.code == 200) {
                                                ret = data.result;
                                            } else {
                                                layer.msg(data.msg);
                                            }
                                        }
                                    }); return ret;
                                };//new Function("postData", getcfService("site/get-crowd-yun-data-js", User));
                                var postData = { itemId: AdgroupInfo.outsideItemNumId, CategoryId: AdgroupInfo.categoryId };
                                //User.nickName = "莞淘电子商务公司";
                                //User.operName = "莞淘电子商务公司";
                                $.extend(postData, User);
                                var aList = GetUserCrowdList(postData);
                                //getcfService("site/set-crowd-yun-data-js",User)
                                app.SetUserCrowdList(aList, AdgroupInfo.outsideItemNumId, AdgroupInfo.categoryId)
                            }, title: ['人群包云功能', 'font-size:18px;']
                        });
                        $("#BakUserCrowdBt").click(function () {
                            layer.prompt({ formType: 0, title: '请输入备份名称' }, function (value, index, elem) {

                                //更新UriInfo
                                getUrlInfo();

                                var aData = {
                                    campaignId: UriInfo.campaignId, adGroupId: UriInfo.adGroupId, "title": value, "categoryId": AdgroupInfo.categoryId, "itemImgUrl": AdgroupInfo.imgUrl,
                                    "itemLinkUrl": AdgroupInfo.linkUrl, "itemTitle": AdgroupInfo.title
                                };
                                var Targets = new Array();
                                var i = 0; var sIds = getjqGridSelarrrow("#list2"); var tagIds = new Array();
                                for (var s = 0; s < sIds.length; s++) { var tagId = jQuery("#list2").jqGrid('getCell', sIds[s], 'iid'); tagIds.push(tagId) };
                                for (var tg in adTargetingList) {
                                    if (tagIds.length > 0 && tagIds.indexOf(tg) == -1) continue;
                                    var tagName = adTargetingList[tg].name;
                                    var discount = parseInt(adTargetingList[tg].discount) + 100;
                                    var onlineStatus = adTargetingList[tg].onlineStatus; Targets.push(tagName + '$' + discount + '$' + onlineStatus); i++
                                };
                                var itemDt = { itemId: itemId, data: Targets.join('#'), count: i };
                                $.extend(aData, itemDt);
                                $.extend(aData, User);
                                var SaveUserCrowd = function (postData) {
                                    var ret = new Array();
                                    $.ajax({
                                        type: "post",
                                        //url: "https://zhitongche.libangjie.com/index.php?r=site/save-crowd-yun-data",
                                        url: server_url + '/taobao/api?r=site/save-crowd-yun-data',
                                        contentType: "application/json", data: JSON.stringify(postData),
                                        async: false, dataType: "json",
                                        success: function (data, status) { if (data.code == 200) { ret = data.result } }
                                    });
                                    return ret;

                                };//new Function("postData", getcfService("site/save-crowd-yun-data-js", User));
                                var aList = SaveUserCrowd(aData);
                                //var SetUserCrowdList = //new Function("aList", "itemId", "categoryId", getcfService("site/set-crowd-yun-data-js", User));
                                app.SetUserCrowdList(aList, itemId, AdgroupInfo.categoryId); layer.close(index);
                            })
                        });

                    };//new Function(getcfService("site/get-crowd-yun-window-js", User));
                    cf_do();
                    return;
                });
                var cf_pageInitCrowd = function (w, h) {
                    jQuery("#list2").jqGrid({
                        datatype: "local",
                        //请求数据返回的类型。可选json,xml,txt
                        colNames: ['状态', '搜索推广', '溢价', '展现量', '点击量', '点击率', '花费', 'CPC',
                            '总成交金额', 'ROI', 'CVR', '总成交数', '总购物车数', '总收藏数',
                            'cid', 'iid', '千次展现花费'],//jqGrid的列显示名字
                        colModel: [
                            //jqGrid每一列的配置信息。包括名字，索引，宽度,对齐方式.....
                            { name: 'onlineStatus', index: 'onlineStatus', width: 80, stype: 'select', formatter: 'select', editoptions: { value: ":All;0:暂停;1:推广中" }, frozen: true },
                            { name: 'name', index: 'name', width: 250, sorttype: 'string', searchoptions: { sopt: ['cn', 'bw', 'eq'] }, frozen: true },
                            { name: 'discount', index: 'discount', width: 80, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] }, frozen: true },
                            { name: 'impression', index: 'impression', width: 90, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            { name: 'click', index: 'click', width: 80, sorttype: 'int', searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            { name: 'ctr', index: 'ctr', width: 80, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            { name: 'cost', index: 'cost', width: 80, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            { name: 'cpc', index: 'cpc', width: 80, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            { name: 'transactiontotal', index: 'transactiontotal', width: 100, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            { name: 'roi', index: 'roi', width: 80, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            { name: 'coverage', index: 'coverage', width: 80, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            { name: 'transactionshippingtotal', index: 'transactionshippingtotal', width: 80, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            { name: 'carttotal', index: 'carttotal', width: 80, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            { name: 'favtotal', index: 'favtotal', width: 80, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            { name: 'cid', index: 'cid', hidden: true },
                            { name: 'iid', index: 'iid', hidden: true },
                            { name: 'cpm', index: 'cpm', width: 80, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } }
                        ],
                        rowNum: 100,
                        //一页显示多少条
                        rowList: [20, 50, 100, 200],//可供用户选择一页显示多少条
                        pager: '#pager2',//表格页脚的占位符(一般是div)的id
                        sortname: 'id',//初始化的时候排序的字段
                        sortorder: "desc",//排序方式,可选desc,asc
                        viewrecords: true, //定义是否要显示总记录数
                        multiselect: true, //允许多选
                        loadonce: true, //客服端执行
                        height: (h - 235),  //定义表格高度
                        width: (w - 5),
                        //autowidth: true,
                        rownumbers: true,
                        shrinkToFit: false,
                        caption: "人群数据报表"
                        //表格的标题名字
                    });
                    /*创建jqGrid的操作按钮容器*/
                    /*可以控制界面上增删改查的按钮是否显示*/
                    jQuery("#list2").jqGrid('navGrid', '#pager2', { del: false, add: false, edit: false }, {}, {}, {}, { multipleSearch: true });
                    jQuery("#list2").jqGrid('filterToolbar', { stringResult: true, searchOnEnter: false, searchOperators: true });
                    jQuery("#list2").jqGrid('setGroupHeaders', {
                        useColSpanStyle: true,
                        groupHeaders: [
                            { startColumnName: 'impression', numberOfColumns: 14, titleText: '报表数据' }
                        ]
                    });
                    jQuery("#list2").jqGrid('setFrozenColumns');
                    var cf_getCrowdList = function () {
                        var index = layer.load(0, { shade: false });
                        var cf_getCrowdListData = function (UriInfo, User) {
                            var TargetingList = {};
                            $.ajax({
                                type: "POST",
                                url: "https://subway.simba.taobao.com/adgroupTargeting/findAdgroupTargetingList.htm?adgroupId=" + UriInfo.adGroupId + "&productId=101001005&bizType=1",
                                data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                dataType: "json",
                                async: false,
                                success: function (data) {
                                    if (data.code == 200) { TargetingList = data.result; };
                                }, error: function () { alert("error"); }
                            });
                            return TargetingList;
                        };// new Function("UriInfo", "User", getcfService("site/subway-get-crowd-list-js", User));
                        var TargetingList = cf_getCrowdListData(UriInfo, User);
                        adTargetingList = {};
                        for (var i = 0; i < TargetingList.length; i++) {
                            var iid = TargetingList[i].crowdDTO.id;
                            if (!adTargetingList[iid]) {
                                adTargetingList[iid] = {
                                    "cid": TargetingList[i].id,
                                    "iid": TargetingList[i].crowdDTO.id,
                                    "onlineStatus": TargetingList[i].onlineStatus,
                                    "onlineState": TargetingList[i].crowdDTO.onlineState,
                                    "discount": parseInt(TargetingList[i].discount - 100).toFixed(0),
                                    "name": TargetingList[i].crowdDTO.name
                                };
                            };
                        };
                        //var cf_getCwrodRptData = new Function(getcfService("site/get-crowd-rpt-js", User));
                        app.cf_getCwrodRptData();
                    };// new Function(getcfService("site/get-crowd-list-js", User));

                    cf_getCrowdList();

                };// new Function("w", "h", getcfService("site/get-crowd-page-init-js", User));
                cf_pageInitCrowd(w, h);

            };//new Function(getcfService("site/get-crowd-window-js", User));
            cf_openCrowdWindow();
"""
dqcs = """
var cf_AreaCityParse = function () {
                if (!getUrlInfo()) { return };
                var BtUI = '<button id="bt_AreaCityParse_01" class="layui-btn layui-btn-danger layui-btn-mini">今日实时</button>'
                    + '<br><button id="bt_AreaCityParse_02" class="layui-btn layui-btn-danger layui-btn-mini">昨日数据</button>'
                    + '<br><button id="bt_AreaCityParse_03" class="layui-btn layui-btn-danger layui-btn-mini">过去2天</button>'
                    + '<br><button id="bt_AreaCityParse_04" class="layui-btn layui-btn-danger layui-btn-mini">所有(3天内)</button>';
                layer.tips(BtUI, '#AreaCityParse', {
                    tips: [3, '#3595CC']
                });
                var cf_OpenAreaCityParse = function (s, e, title) {
                    var DivUI = '<div>'
                        + '<table id="AreaCityParselist"></table>'
                        + '<div id="AreaCityParsepager"></div>'
                        + '<button id="bt_UpdateAreaCityToCam" class="layui-btn layui-btn-danger layui-btn-mini">将所选城市应用到当前计划设置</button>'
                        + '</div>';
                    var index = layer.open({
                        type: 1,
                        content: DivUI,
                        area: ["832px", "700px"],
                        title: false,
                        success: function (layero) {
                            $("#bt_UpdateAreaCityToCam").click(function () {
                                if (!getUrlInfo()) { return };
                                var cf_UpdateAreaCityToCampaign = function () {
                                    var sIds = getjqGridSelarrrow("#AreaCityParselist");
                                    if (sIds.length < 1) {
                                        layer.msg("至少设置一个地区！");
                                        return;
                                    };
                                    var ACode = new Array();
                                    for (var i in sIds) {
                                        var code = jQuery("#AreaCityParselist").jqGrid('getCell', sIds[i], 'code');
                                        if (code != '不可设置')
                                            ACode.push(code);
                                    };
                                    var postdata = "sla=json&isAjaxRequest=true&token=" + User.token;
                                    $.ajax({
                                        type: "POST",
                                        url: 'https://subway.simba.taobao.com/area/update.htm?campaignId=' + UriInfo.campaignId + '&areaState=' + ACode.join(','),
                                        data: postdata,
                                        async: false,
                                        datatype: "json",
                                        success: function (data) {
                                            if (data.code == 200) {
                                                layer.msg('地区设置已更新！');
                                            };
                                        },
                                        error: function () {
                                            alert('n');
                                        }
                                    });
                                };// new Function(getcfService("site/get-area-city-to-campaign-js", User));
                                cf_UpdateAreaCityToCampaign();
                            });
                        }
                    });
                    var cf_pageInitAreaCityParse = function (s, e, title) {
                        var bidGrid = jQuery("#AreaCityParselist").jqGrid({
                            datatype: "local",
                            colNames: [
                                '城市', '省份', '花费', '点击量', '平均点击花费', '反馈量',
                                '点击占比', '反馈率', '代码'
                            ],
                            colModel: [
                                { name: 'cityname', index: 'cityname', width: 90, sorttype: 'string', searchoptions: { sopt: ['cn', 'bw', 'eq'] } },
                                { name: 'provincename', index: 'provincename', width: 90, sorttype: "string", searchoptions: { sopt: ['cn', 'bw', 'eq'] } },
                                { name: 'cost', index: 'cost', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                { name: 'click', index: 'click', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                { name: 'avgPrice', index: 'avgPrice', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                { name: 'effect', index: 'effect', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                { name: 'clickRank', index: 'clickRank', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                { name: 'effectvr', index: 'effectvr', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                { name: 'code', index: 'code', width: 50, sorttype: "string", searchoptions: { sopt: ['cn', 'bw', 'eq'] } }
                            ],
                            rowNum: 100,
                            rowList: [20, 50, 100, 200],
                            pager: '#AreaCityParsepager',
                            sortname: 'click',
                            sortorder: "desc",
                            multiselect: true, //允许多选
                            viewrecords: true,
                            loadonce: true,
                            rownumbers: true,
                            height: 540,
                            width: 830,
                            caption: title
                        });
                        jQuery("#AreaCityParselist").jqGrid('filterToolbar', { stringResult: true, searchOnEnter: false, searchOperators: true });

                        //载入默认推荐词
                        if (getUrlInfo()) {
                            var index = layer.load(1); //换了种风格
                            var cf_DoAreaCityParseForDate = function (s, e, index) {
                                rptAdgroupClickList = new Array();
                                var cf_GetAreaCityParseForDate = function (theDate, offSet, pageSize) {
                                    var result;
                                    var url = 'https://subway.simba.taobao.com/rtreport/rptAdgroupClickList.htm?theDate=' + theDate + '&campaignid=' + UriInfo.campaignId + '&adgroupid=' + UriInfo.adGroupId + '&offSet=' + offSet + '&pageSize=' + pageSize + '&traffictype=&mechanism=&filter=&bidword=';
                                    var postData = "sla=json&isAjaxRequest=true&token=" + User.token;
                                    $.ajax({
                                        type: "POST",
                                        url: url,
                                        data: postData,
                                        datatype: "json",
                                        async: false,
                                        success: function (data) {
                                            if (data.code == 200) {
                                                result = data.result;
                                            };
                                        },
                                        error: function () {
                                            alert("error:GetAreaCityParseForDate");
                                        }
                                    });
                                    return result;
                                };// new Function("theDate", "offSet", "pageSize", getcfService("site/get-area-city-parse-for-date-js", User));
                                for (var i = s; i >= e; i--) {
                                    var offSet = 0;
                                    var pageSize = 200;
                                    var theDate = laydate.now(i);
                                    while (true) {
                                        var result = cf_GetAreaCityParseForDate(theDate, offSet, pageSize);
                                        rptAdgroupClickList = rptAdgroupClickList.concat(result);
                                        if (result.length < pageSize) {
                                            break;
                                        }
                                        else {
                                            offSet = offSet + pageSize;
                                        };
                                    };

                                };
                                var cf_AreaCityAdGroupCityOutUI = function () {
                                    var cityClickList = {};
                                    var clickCount = rptAdgroupClickList.length;
                                    var cf_getAreaCode = function () {
                                        return [{
                                            name: "华北地区",
                                            contains: [{
                                                name: "北京",
                                                code: 19
                                            },
                                            {
                                                name: "天津",
                                                code: 461
                                            },
                                            {
                                                name: "河北",
                                                code: 125,
                                                contains: [{
                                                    code: 126,
                                                    name: "保定"
                                                },
                                                {
                                                    code: 129,
                                                    name: "沧州"
                                                },
                                                {
                                                    code: 132,
                                                    name: "承德"
                                                },
                                                {
                                                    code: 133,
                                                    name: "邯郸"
                                                },
                                                {
                                                    code: 134,
                                                    name: "衡水"
                                                },
                                                {
                                                    code: 135,
                                                    name: "廊坊"
                                                },
                                                {
                                                    code: 137,
                                                    name: "秦皇岛"
                                                },
                                                {
                                                    code: 138,
                                                    name: "石家庄"
                                                },
                                                {
                                                    code: 140,
                                                    name: "唐山"
                                                },
                                                {
                                                    code: 141,
                                                    name: "邢台"
                                                },
                                                {
                                                    code: 144,
                                                    name: "张家口"
                                                }]
                                            },
                                            {
                                                name: "山西",
                                                code: 393,
                                                contains: [{
                                                    code: 394,
                                                    name: "长治"
                                                },
                                                {
                                                    code: 395,
                                                    name: "大同"
                                                },
                                                {
                                                    code: 396,
                                                    name: "晋城"
                                                },
                                                {
                                                    code: 398,
                                                    name: "临汾"
                                                },
                                                {
                                                    code: 401,
                                                    name: "朔州"
                                                },
                                                {
                                                    code: 402,
                                                    name: "太原"
                                                },
                                                {
                                                    code: 403,
                                                    name: "忻州"
                                                },
                                                {
                                                    code: 404,
                                                    name: "阳泉"
                                                },
                                                {
                                                    code: 405,
                                                    name: "运城"
                                                },
                                                {
                                                    code: 597,
                                                    name: "晋中"
                                                },
                                                {
                                                    code: 598,
                                                    name: "吕梁"
                                                }]
                                            },
                                            {
                                                name: "内蒙",
                                                code: 333,
                                                contains: [{
                                                    code: 321,
                                                    name: "呼伦贝尔"
                                                },
                                                {
                                                    code: 328,
                                                    name: "阿拉善"
                                                },
                                                {
                                                    code: 336,
                                                    name: "包头"
                                                },
                                                {
                                                    code: 337,
                                                    name: "赤峰"
                                                },
                                                {
                                                    code: 339,
                                                    name: "呼和浩特"
                                                },
                                                {
                                                    code: 344,
                                                    name: "通辽"
                                                },
                                                {
                                                    code: 346,
                                                    name: "乌海"
                                                },
                                                {
                                                    code: 586,
                                                    name: "鄂尔多斯"
                                                },
                                                {
                                                    code: 587,
                                                    name: "乌兰察布"
                                                },
                                                {
                                                    code: 588,
                                                    name: "巴彦淖尔"
                                                },
                                                {
                                                    code: 589,
                                                    name: "兴安盟"
                                                },
                                                {
                                                    code: 590,
                                                    name: "锡林郭勒"
                                                }]
                                            }]
                                        },
                                        {
                                            name: "东北地区",
                                            contains: [{
                                                name: "辽宁",
                                                code: 294,
                                                contains: [{
                                                    code: 295,
                                                    name: "鞍山"
                                                },
                                                {
                                                    code: 297,
                                                    name: "本溪"
                                                },
                                                {
                                                    code: 298,
                                                    name: "朝阳"
                                                },
                                                {
                                                    code: 300,
                                                    name: "大连"
                                                },
                                                {
                                                    code: 303,
                                                    name: "丹东"
                                                },
                                                {
                                                    code: 304,
                                                    name: "抚顺"
                                                },
                                                {
                                                    code: 305,
                                                    name: "阜新"
                                                },
                                                {
                                                    code: 306,
                                                    name: "葫芦岛"
                                                },
                                                {
                                                    code: 308,
                                                    name: "锦州"
                                                },
                                                {
                                                    code: 309,
                                                    name: "辽阳"
                                                },
                                                {
                                                    code: 310,
                                                    name: "盘锦"
                                                },
                                                {
                                                    code: 311,
                                                    name: "沈阳"
                                                },
                                                {
                                                    code: 312,
                                                    name: "铁岭"
                                                },
                                                {
                                                    code: 314,
                                                    name: "营口"
                                                }]
                                            },
                                            {
                                                name: "吉林",
                                                code: 234,
                                                contains: [{
                                                    code: 235,
                                                    name: "白城"
                                                },
                                                {
                                                    code: 237,
                                                    name: "白山"
                                                },
                                                {
                                                    code: 238,
                                                    name: "长春"
                                                },
                                                {
                                                    code: 239,
                                                    name: "吉林市"
                                                },
                                                {
                                                    code: 241,
                                                    name: "辽源"
                                                },
                                                {
                                                    code: 242,
                                                    name: "四平"
                                                },
                                                {
                                                    code: 244,
                                                    name: "松原"
                                                },
                                                {
                                                    code: 246,
                                                    name: "通化"
                                                },
                                                {
                                                    code: 249,
                                                    name: "延边朝鲜族自治州"
                                                }]
                                            },
                                            {
                                                name: "黑龙江",
                                                code: 165,
                                                contains: [{
                                                    code: 166,
                                                    name: "大庆"
                                                },
                                                {
                                                    code: 167,
                                                    name: "哈尔滨"
                                                },
                                                {
                                                    code: 169,
                                                    name: "鹤岗"
                                                },
                                                {
                                                    code: 170,
                                                    name: "黑河"
                                                },
                                                {
                                                    code: 173,
                                                    name: "鸡西"
                                                },
                                                {
                                                    code: 174,
                                                    name: "佳木斯"
                                                },
                                                {
                                                    code: 176,
                                                    name: "牡丹江"
                                                },
                                                {
                                                    code: 178,
                                                    name: "七台河"
                                                },
                                                {
                                                    code: 179,
                                                    name: "齐齐哈尔"
                                                },
                                                {
                                                    code: 180,
                                                    name: "双鸭山"
                                                },
                                                {
                                                    code: 181,
                                                    name: "绥化"
                                                },
                                                {
                                                    code: 183,
                                                    name: "伊春"
                                                },
                                                {
                                                    code: 622,
                                                    name: "大兴安岭"
                                                }]
                                            }]
                                        },
                                        {
                                            name: "华东地区",
                                            contains: [{
                                                code: 417,
                                                name: "上海"
                                            },
                                            {
                                                name: "江苏",
                                                code: 255,
                                                contains: [{
                                                    code: 256,
                                                    name: "常州"
                                                },
                                                {
                                                    code: 257,
                                                    name: "淮安"
                                                },
                                                {
                                                    code: 259,
                                                    name: "连云港"
                                                },
                                                {
                                                    code: 260,
                                                    name: "南京"
                                                },
                                                {
                                                    code: 261,
                                                    name: "南通"
                                                },
                                                {
                                                    code: 262,
                                                    name: "苏州"
                                                },
                                                {
                                                    code: 265,
                                                    name: "宿迁"
                                                },
                                                {
                                                    code: 266,
                                                    name: "泰州"
                                                },
                                                {
                                                    code: 269,
                                                    name: "无锡"
                                                },
                                                {
                                                    code: 272,
                                                    name: "徐州"
                                                },
                                                {
                                                    code: 273,
                                                    name: "盐城"
                                                },
                                                {
                                                    code: 275,
                                                    name: "扬州"
                                                },
                                                {
                                                    code: 277,
                                                    name: "镇江"
                                                }]
                                            },
                                            {
                                                name: "浙江",
                                                code: 508,
                                                contains: [{
                                                    code: 509,
                                                    name: "杭州"
                                                },
                                                {
                                                    code: 511,
                                                    name: "湖州"
                                                },
                                                {
                                                    code: 512,
                                                    name: "嘉兴"
                                                },
                                                {
                                                    code: 514,
                                                    name: "金华"
                                                },
                                                {
                                                    code: 518,
                                                    name: "丽水"
                                                },
                                                {
                                                    code: 519,
                                                    name: "宁波"
                                                },
                                                {
                                                    code: 522,
                                                    name: "绍兴"
                                                },
                                                {
                                                    code: 523,
                                                    name: "台州"
                                                },
                                                {
                                                    code: 526,
                                                    name: "温州"
                                                },
                                                {
                                                    code: 528,
                                                    name: "舟山"
                                                },
                                                {
                                                    code: 529,
                                                    name: "衢州"
                                                }]
                                            },
                                            {
                                                name: "福建",
                                                code: 39,
                                                contains: [{
                                                    code: 40,
                                                    name: "福州"
                                                },
                                                {
                                                    code: 41,
                                                    name: "龙岩"
                                                },
                                                {
                                                    code: 42,
                                                    name: "南平"
                                                },
                                                {
                                                    code: 44,
                                                    name: "宁德"
                                                },
                                                {
                                                    code: 45,
                                                    name: "莆田"
                                                },
                                                {
                                                    code: 46,
                                                    name: "泉州"
                                                },
                                                {
                                                    code: 48,
                                                    name: "三明"
                                                },
                                                {
                                                    code: 50,
                                                    name: "厦门"
                                                },
                                                {
                                                    code: 51,
                                                    name: "漳州"
                                                }]
                                            },
                                            {
                                                name: "安徽",
                                                code: 1,
                                                contains: [{
                                                    code: 2,
                                                    name: "安庆"
                                                },
                                                {
                                                    code: 3,
                                                    name: "蚌埠"
                                                },
                                                {
                                                    code: 4,
                                                    name: "巢湖"
                                                },
                                                {
                                                    code: 5,
                                                    name: "池州"
                                                },
                                                {
                                                    code: 6,
                                                    name: "滁州"
                                                },
                                                {
                                                    code: 7,
                                                    name: "阜阳"
                                                },
                                                {
                                                    code: 8,
                                                    name: "合肥"
                                                },
                                                {
                                                    code: 9,
                                                    name: "淮北"
                                                },
                                                {
                                                    code: 10,
                                                    name: "淮南"
                                                },
                                                {
                                                    code: 11,
                                                    name: "黄山"
                                                },
                                                {
                                                    code: 12,
                                                    name: "六安"
                                                },
                                                {
                                                    code: 13,
                                                    name: "马鞍山"
                                                },
                                                {
                                                    code: 14,
                                                    name: "宿州"
                                                },
                                                {
                                                    code: 15,
                                                    name: "铜陵"
                                                },
                                                {
                                                    code: 16,
                                                    name: "芜湖"
                                                },
                                                {
                                                    code: 17,
                                                    name: "宣城"
                                                },
                                                {
                                                    code: 18,
                                                    name: "亳州"
                                                }]
                                            },
                                            {
                                                name: "山东",
                                                code: 368,
                                                contains: [{
                                                    code: 369,
                                                    name: "滨州"
                                                },
                                                {
                                                    code: 370,
                                                    name: "德州"
                                                },
                                                {
                                                    code: 371,
                                                    name: "东营"
                                                },
                                                {
                                                    code: 372,
                                                    name: "菏泽"
                                                },
                                                {
                                                    code: 373,
                                                    name: "济南"
                                                },
                                                {
                                                    code: 374,
                                                    name: "济宁"
                                                },
                                                {
                                                    code: 376,
                                                    name: "莱芜"
                                                },
                                                {
                                                    code: 377,
                                                    name: "聊城"
                                                },
                                                {
                                                    code: 379,
                                                    name: "临沂"
                                                },
                                                {
                                                    code: 380,
                                                    name: "青岛"
                                                },
                                                {
                                                    code: 381,
                                                    name: "日照"
                                                },
                                                {
                                                    code: 382,
                                                    name: "泰安"
                                                },
                                                {
                                                    code: 384,
                                                    name: "威海"
                                                },
                                                {
                                                    code: 386,
                                                    name: "潍坊"
                                                },
                                                {
                                                    code: 389,
                                                    name: "烟台"
                                                },
                                                {
                                                    code: 390,
                                                    name: "枣庄"
                                                },
                                                {
                                                    code: 392,
                                                    name: "淄博"
                                                }]
                                            }]
                                        },
                                        {
                                            name: "华中地区",
                                            contains: [{
                                                name: "河南",
                                                code: 145,
                                                contains: [{
                                                    code: 146,
                                                    name: "安阳"
                                                },
                                                {
                                                    code: 147,
                                                    name: "鹤壁"
                                                },
                                                {
                                                    code: 148,
                                                    name: "焦作"
                                                },
                                                {
                                                    code: 149,
                                                    name: "开封"
                                                },
                                                {
                                                    code: 150,
                                                    name: "洛阳"
                                                },
                                                {
                                                    code: 151,
                                                    name: "南阳"
                                                },
                                                {
                                                    code: 152,
                                                    name: "平顶山"
                                                },
                                                {
                                                    code: 153,
                                                    name: "三门峡"
                                                },
                                                {
                                                    code: 155,
                                                    name: "商丘"
                                                },
                                                {
                                                    code: 156,
                                                    name: "新乡"
                                                },
                                                {
                                                    code: 157,
                                                    name: "信阳"
                                                },
                                                {
                                                    code: 159,
                                                    name: "许昌"
                                                },
                                                {
                                                    code: 160,
                                                    name: "郑州"
                                                },
                                                {
                                                    code: 161,
                                                    name: "周口"
                                                },
                                                {
                                                    code: 162,
                                                    name: "驻马店"
                                                },
                                                {
                                                    code: 163,
                                                    name: "漯河"
                                                },
                                                {
                                                    code: 164,
                                                    name: "濮阳"
                                                },
                                                {
                                                    code: 621,
                                                    name: "济源"
                                                }]
                                            },
                                            {
                                                name: "湖北",
                                                code: 184,
                                                contains: [{
                                                    code: 185,
                                                    name: "鄂州"
                                                },
                                                {
                                                    code: 186,
                                                    name: "恩施"
                                                },
                                                {
                                                    code: 188,
                                                    name: "黄冈"
                                                },
                                                {
                                                    code: 191,
                                                    name: "黄石"
                                                },
                                                {
                                                    code: 192,
                                                    name: "荆门"
                                                },
                                                {
                                                    code: 193,
                                                    name: "荆州"
                                                },
                                                {
                                                    code: 196,
                                                    name: "十堰"
                                                },
                                                {
                                                    code: 198,
                                                    name: "随州"
                                                },
                                                {
                                                    code: 200,
                                                    name: "武汉"
                                                },
                                                {
                                                    code: 203,
                                                    name: "咸宁"
                                                },
                                                {
                                                    code: 205,
                                                    name: "襄阳"
                                                },
                                                {
                                                    code: 207,
                                                    name: "孝感"
                                                },
                                                {
                                                    code: 210,
                                                    name: "宜昌"
                                                },
                                                {
                                                    code: 623,
                                                    name: "潜江"
                                                },
                                                {
                                                    code: 624,
                                                    name: "神农架"
                                                },
                                                {
                                                    code: 199,
                                                    name: "天门"
                                                },
                                                {
                                                    code: 202,
                                                    name: "仙桃"
                                                }]
                                            },
                                            {
                                                name: "湖南",
                                                code: 212,
                                                contains: [{
                                                    code: 213,
                                                    name: "常德"
                                                },
                                                {
                                                    code: 214,
                                                    name: "长沙"
                                                },
                                                {
                                                    code: 215,
                                                    name: "郴州"
                                                },
                                                {
                                                    code: 216,
                                                    name: "衡阳"
                                                },
                                                {
                                                    code: 218,
                                                    name: "怀化"
                                                },
                                                {
                                                    code: 220,
                                                    name: "娄底"
                                                },
                                                {
                                                    code: 223,
                                                    name: "邵阳"
                                                },
                                                {
                                                    code: 224,
                                                    name: "湘潭"
                                                },
                                                {
                                                    code: 227,
                                                    name: "益阳"
                                                },
                                                {
                                                    code: 228,
                                                    name: "永州"
                                                },
                                                {
                                                    code: 230,
                                                    name: "岳阳"
                                                },
                                                {
                                                    code: 232,
                                                    name: "张家界"
                                                },
                                                {
                                                    code: 233,
                                                    name: "株洲"
                                                },
                                                {
                                                    code: 585,
                                                    name: "湘西"
                                                }]
                                            },
                                            {
                                                name: "江西",
                                                code: 279,
                                                contains: [{
                                                    code: 280,
                                                    name: "抚州"
                                                },
                                                {
                                                    code: 282,
                                                    name: "赣州"
                                                },
                                                {
                                                    code: 283,
                                                    name: "吉安"
                                                },
                                                {
                                                    code: 285,
                                                    name: "景德镇"
                                                },
                                                {
                                                    code: 286,
                                                    name: "九江"
                                                },
                                                {
                                                    code: 288,
                                                    name: "南昌"
                                                },
                                                {
                                                    code: 289,
                                                    name: "萍乡"
                                                },
                                                {
                                                    code: 290,
                                                    name: "上饶"
                                                },
                                                {
                                                    code: 291,
                                                    name: "新余"
                                                },
                                                {
                                                    code: 292,
                                                    name: "宜春"
                                                },
                                                {
                                                    code: 293,
                                                    name: "鹰潭"
                                                }]
                                            }]
                                        },
                                        {
                                            name: "华南地区",
                                            contains: [{
                                                name: "广东",
                                                code: 68,
                                                contains: [{
                                                    code: 69,
                                                    name: "潮州"
                                                },
                                                {
                                                    code: 70,
                                                    name: "东莞"
                                                },
                                                {
                                                    code: 71,
                                                    name: "佛山"
                                                },
                                                {
                                                    code: 73,
                                                    name: "广州"
                                                },
                                                {
                                                    code: 74,
                                                    name: "河源"
                                                },
                                                {
                                                    code: 75,
                                                    name: "惠州"
                                                },
                                                {
                                                    code: 76,
                                                    name: "江门"
                                                },
                                                {
                                                    code: 77,
                                                    name: "揭阳"
                                                },
                                                {
                                                    code: 78,
                                                    name: "茂名"
                                                },
                                                {
                                                    code: 79,
                                                    name: "梅州"
                                                },
                                                {
                                                    code: 80,
                                                    name: "清远"
                                                },
                                                {
                                                    code: 81,
                                                    name: "汕头"
                                                },
                                                {
                                                    code: 83,
                                                    name: "汕尾"
                                                },
                                                {
                                                    code: 84,
                                                    name: "韶关"
                                                },
                                                {
                                                    code: 85,
                                                    name: "深圳"
                                                },
                                                {
                                                    code: 86,
                                                    name: "阳江"
                                                },
                                                {
                                                    code: 87,
                                                    name: "云浮"
                                                },
                                                {
                                                    code: 88,
                                                    name: "湛江"
                                                },
                                                {
                                                    code: 89,
                                                    name: "肇庆"
                                                },
                                                {
                                                    code: 90,
                                                    name: "中山"
                                                },
                                                {
                                                    code: 91,
                                                    name: "珠海"
                                                }]
                                            },
                                            {
                                                name: "海南",
                                                code: 120,
                                                contains: [{
                                                    code: 121,
                                                    name: "海口"
                                                },
                                                {
                                                    code: 122,
                                                    name: "三亚"
                                                },
                                                {
                                                    code: 609,
                                                    name: "白沙"
                                                },
                                                {
                                                    code: 610,
                                                    name: "昌江"
                                                },
                                                {
                                                    code: 611,
                                                    name: "澄迈"
                                                },
                                                {
                                                    code: 612,
                                                    name: "安定"
                                                },
                                                {
                                                    code: 613,
                                                    name: "东方"
                                                },
                                                {
                                                    code: 614,
                                                    name: "乐东"
                                                },
                                                {
                                                    code: 615,
                                                    name: "琼海"
                                                },
                                                {
                                                    code: 616,
                                                    name: "万宁"
                                                },
                                                {
                                                    code: 617,
                                                    name: "文昌"
                                                },
                                                {
                                                    code: 618,
                                                    name: "五指山"
                                                },
                                                {
                                                    code: 619,
                                                    name: "保亭"
                                                },
                                                {
                                                    code: 620,
                                                    name: "陵水"
                                                }]
                                            },
                                            {
                                                name: "广西",
                                                code: 92,
                                                contains: [{
                                                    code: 93,
                                                    name: "百色"
                                                },
                                                {
                                                    code: 94,
                                                    name: "北海"
                                                },
                                                {
                                                    code: 96,
                                                    name: "防城港"
                                                },
                                                {
                                                    code: 98,
                                                    name: "桂林"
                                                },
                                                {
                                                    code: 99,
                                                    name: "贵港"
                                                },
                                                {
                                                    code: 100,
                                                    name: "河池"
                                                },
                                                {
                                                    code: 102,
                                                    name: "贺州"
                                                },
                                                {
                                                    code: 104,
                                                    name: "柳州"
                                                },
                                                {
                                                    code: 105,
                                                    name: "南宁"
                                                },
                                                {
                                                    code: 106,
                                                    name: "钦州"
                                                },
                                                {
                                                    code: 107,
                                                    name: "梧州"
                                                },
                                                {
                                                    code: 108,
                                                    name: "玉林"
                                                },
                                                {
                                                    code: 581,
                                                    name: "来宾"
                                                },
                                                {
                                                    code: 580,
                                                    name: "崇左"
                                                }]
                                            }]
                                        },
                                        {
                                            name: "西南地区",
                                            contains: [{
                                                name: "重庆",
                                                code: 532
                                            },
                                            {
                                                name: "四川",
                                                code: 438,
                                                contains: [{
                                                    code: 440,
                                                    name: "巴中"
                                                },
                                                {
                                                    code: 441,
                                                    name: "成都"
                                                },
                                                {
                                                    code: 442,
                                                    name: "达州"
                                                },
                                                {
                                                    code: 443,
                                                    name: "德阳"
                                                },
                                                {
                                                    code: 444,
                                                    name: "甘孜"
                                                },
                                                {
                                                    code: 445,
                                                    name: "广安"
                                                },
                                                {
                                                    code: 447,
                                                    name: "广元"
                                                },
                                                {
                                                    code: 448,
                                                    name: "乐山"
                                                },
                                                {
                                                    code: 450,
                                                    name: "眉山"
                                                },
                                                {
                                                    code: 451,
                                                    name: "绵阳"
                                                },
                                                {
                                                    code: 452,
                                                    name: "南充"
                                                },
                                                {
                                                    code: 453,
                                                    name: "内江"
                                                },
                                                {
                                                    code: 454,
                                                    name: "攀枝花"
                                                },
                                                {
                                                    code: 455,
                                                    name: "遂宁"
                                                },
                                                {
                                                    code: 456,
                                                    name: "雅安"
                                                },
                                                {
                                                    code: 457,
                                                    name: "宜宾"
                                                },
                                                {
                                                    code: 458,
                                                    name: "资阳"
                                                },
                                                {
                                                    code: 459,
                                                    name: "自贡"
                                                },
                                                {
                                                    code: 460,
                                                    name: "泸州"
                                                },
                                                {
                                                    code: 600,
                                                    name: "凉山"
                                                },
                                                {
                                                    code: 601,
                                                    name: "阿坝"
                                                }]
                                            },
                                            {
                                                name: "云南",
                                                code: 488,
                                                contains: [{
                                                    code: 489,
                                                    name: "保山"
                                                },
                                                {
                                                    code: 490,
                                                    name: "楚雄"
                                                },
                                                {
                                                    code: 491,
                                                    name: "大理"
                                                },
                                                {
                                                    code: 492,
                                                    name: "德宏"
                                                },
                                                {
                                                    code: 497,
                                                    name: "昆明"
                                                },
                                                {
                                                    code: 499,
                                                    name: "丽江"
                                                },
                                                {
                                                    code: 500,
                                                    name: "临沧"
                                                },
                                                {
                                                    code: 502,
                                                    name: "曲靖"
                                                },
                                                {
                                                    code: 503,
                                                    name: "普洱"
                                                },
                                                {
                                                    code: 504,
                                                    name: "文山"
                                                },
                                                {
                                                    code: 506,
                                                    name: "玉溪"
                                                },
                                                {
                                                    code: 507,
                                                    name: "昭通"
                                                },
                                                {
                                                    code: 605,
                                                    name: "西双版纳"
                                                },
                                                {
                                                    code: 606,
                                                    name: "红河"
                                                },
                                                {
                                                    code: 607,
                                                    name: "怒江"
                                                },
                                                {
                                                    code: 608,
                                                    name: "迪庆"
                                                }]
                                            },
                                            {
                                                name: "贵州",
                                                code: 109,
                                                contains: [{
                                                    code: 110,
                                                    name: "安顺"
                                                },
                                                {
                                                    code: 111,
                                                    name: "毕节"
                                                },
                                                {
                                                    code: 112,
                                                    name: "贵阳"
                                                },
                                                {
                                                    code: 113,
                                                    name: "六盘水"
                                                },
                                                {
                                                    code: 117,
                                                    name: "铜仁"
                                                },
                                                {
                                                    code: 118,
                                                    name: "遵义"
                                                },
                                                {
                                                    code: 582,
                                                    name: "黔东南"
                                                },
                                                {
                                                    code: 583,
                                                    name: "黔南"
                                                },
                                                {
                                                    code: 584,
                                                    name: "黔西"
                                                }]
                                            },
                                            {
                                                name: "西藏自治区",
                                                code: 463,
                                                contains: [{
                                                    code: 464,
                                                    name: "阿里"
                                                },
                                                {
                                                    code: 465,
                                                    name: "昌都"
                                                },
                                                {
                                                    code: 466,
                                                    name: "拉萨"
                                                },
                                                {
                                                    code: 467,
                                                    name: "林芝"
                                                },
                                                {
                                                    code: 468,
                                                    name: "那曲"
                                                },
                                                {
                                                    code: 469,
                                                    name: "日喀则"
                                                },
                                                {
                                                    code: 470,
                                                    name: "山南"
                                                }]
                                            }]
                                        },
                                        {
                                            name: "西北地区",
                                            contains: [{
                                                name: "陕西",
                                                code: 406,
                                                contains: [{
                                                    code: 407,
                                                    name: "安康"
                                                },
                                                {
                                                    code: 408,
                                                    name: "宝鸡"
                                                },
                                                {
                                                    code: 409,
                                                    name: "汉中"
                                                },
                                                {
                                                    code: 410,
                                                    name: "商洛"
                                                },
                                                {
                                                    code: 411,
                                                    name: "铜川"
                                                },
                                                {
                                                    code: 412,
                                                    name: "渭南"
                                                },
                                                {
                                                    code: 413,
                                                    name: "西安"
                                                },
                                                {
                                                    code: 414,
                                                    name: "咸阳"
                                                },
                                                {
                                                    code: 415,
                                                    name: "延安"
                                                },
                                                {
                                                    code: 416,
                                                    name: "榆林"
                                                }]
                                            },
                                            {
                                                name: "甘肃",
                                                code: 52,
                                                contains: [{
                                                    code: 53,
                                                    name: "白银"
                                                },
                                                {
                                                    code: 54,
                                                    name: "定西"
                                                },
                                                {
                                                    code: 55,
                                                    name: "嘉峪关"
                                                },
                                                {
                                                    code: 56,
                                                    name: "金昌"
                                                },
                                                {
                                                    code: 57,
                                                    name: "酒泉"
                                                },
                                                {
                                                    code: 59,
                                                    name: "兰州"
                                                },
                                                {
                                                    code: 60,
                                                    name: "临夏"
                                                },
                                                {
                                                    code: 61,
                                                    name: "陇南"
                                                },
                                                {
                                                    code: 62,
                                                    name: "平凉"
                                                },
                                                {
                                                    code: 63,
                                                    name: "庆阳"
                                                },
                                                {
                                                    code: 65,
                                                    name: "天水"
                                                },
                                                {
                                                    code: 66,
                                                    name: "武威"
                                                },
                                                {
                                                    code: 67,
                                                    name: "张掖"
                                                },
                                                {
                                                    code: 579,
                                                    name: "甘南"
                                                }]
                                            },
                                            {
                                                name: "青海",
                                                code: 357,
                                                contains: [{
                                                    code: 361,
                                                    name: "海东"
                                                },
                                                {
                                                    code: 366,
                                                    name: "西宁"
                                                },
                                                {
                                                    code: 367,
                                                    name: "玉树"
                                                },
                                                {
                                                    code: 592,
                                                    name: "海北"
                                                },
                                                {
                                                    code: 593,
                                                    name: "海南"
                                                },
                                                {
                                                    code: 594,
                                                    name: "黄南"
                                                },
                                                {
                                                    code: 595,
                                                    name: "果洛"
                                                },
                                                {
                                                    code: 596,
                                                    name: "海西"
                                                }]
                                            },
                                            {
                                                name: "宁夏回族自治区",
                                                code: 351,
                                                contains: [{
                                                    code: 352,
                                                    name: "固原"
                                                },
                                                {
                                                    code: 353,
                                                    name: "石嘴山"
                                                },
                                                {
                                                    code: 354,
                                                    name: "吴忠"
                                                },
                                                {
                                                    code: 356,
                                                    name: "银川"
                                                },
                                                {
                                                    code: 591,
                                                    name: "中卫"
                                                }]
                                            },
                                            {
                                                name: "新疆",
                                                code: 471,
                                                contains: [{
                                                    code: 472,
                                                    name: "阿克苏"
                                                },
                                                {
                                                    code: 473,
                                                    name: "阿勒泰"
                                                },
                                                {
                                                    code: 476,
                                                    name: "昌吉"
                                                },
                                                {
                                                    code: 477,
                                                    name: "哈密"
                                                },
                                                {
                                                    code: 478,
                                                    name: "和田"
                                                },
                                                {
                                                    code: 479,
                                                    name: "喀什"
                                                },
                                                {
                                                    code: 480,
                                                    name: "克拉玛依"
                                                },
                                                {
                                                    code: 483,
                                                    name: "塔城"
                                                },
                                                {
                                                    code: 484,
                                                    name: "吐鲁番"
                                                },
                                                {
                                                    code: 485,
                                                    name: "乌鲁木齐"
                                                },
                                                {
                                                    code: 486,
                                                    name: "伊犁"
                                                },
                                                {
                                                    code: 602,
                                                    name: "克孜勒苏柯尔克孜"
                                                },
                                                {
                                                    code: 603,
                                                    name: "博尔塔拉"
                                                },
                                                {
                                                    code: 604,
                                                    name: "巴音郭楞"
                                                },
                                                {
                                                    code: 625,
                                                    name: "五家渠"
                                                },
                                                {
                                                    code: 626,
                                                    name: "阿拉尔"
                                                }]
                                            }]
                                        },
                                        {
                                            name: "其他地区",
                                            contains: [{
                                                code: 578,
                                                name: "台湾"
                                            },
                                            {
                                                code: 599,
                                                name: "香港"
                                            },
                                            {
                                                name: "澳门",
                                                code: 576
                                            },
                                            {
                                                name: "国外",
                                                code: 574
                                            }]
                                        }];
                                    };// new Function(getcfService("site/get-area-code", User));
                                    var codeList = cf_getAreaCode();
                                    var codeNameList = {};
                                    for (var i in codeList) {
                                        //大地区
                                        var contains = codeList[i].contains;
                                        for (var j in contains) {
                                            //省份地区
                                            codeNameList[contains[j].name] = {
                                                "name": contains[j].name,
                                                "code": contains[j].code
                                            };
                                            //判断是够有下级城市
                                            if (contains[j].contains) {
                                                //地区城市
                                                var kc = contains[j].contains;
                                                for (var k in kc) {
                                                    codeNameList[kc[k].name] = {
                                                        "name": kc[k].name,
                                                        "code": kc[k].code
                                                    };
                                                };
                                            };
                                        };
                                    };

                                    for (var i = 0; i < rptAdgroupClickList.length; i++) {
                                        var cname = rptAdgroupClickList[i].cityname;
                                        var pname = rptAdgroupClickList[i].provincename;
                                        if (!cityClickList[cname]) {
                                            var code = "不可设置";
                                            if (codeNameList[cname]) {
                                                code = codeNameList[cname].code;
                                            };
                                            cityClickList[cname] = {
                                                "cityname": cname,
                                                "code": code,
                                                "provincename": pname,
                                                "cost": parseFloat(rptAdgroupClickList[i].cost),
                                                "click": 1,
                                                "effect": rptAdgroupClickList[i].hasEffectData == true ? 1 : 0,
                                                "clickRank": parseFloat((1 * 100) / clickCount).toFixed(2),
                                                "effectvr": ((rptAdgroupClickList[i].hasEffectData == true ? 1 : 0) * 100 / 1).toFixed(2),
                                                "avgPrice": parseFloat(rptAdgroupClickList[i].cost)
                                            };
                                        }
                                        else {
                                            cityClickList[cname].cost = cityClickList[cname].cost + parseFloat(rptAdgroupClickList[i].cost);
                                            cityClickList[cname].click++;
                                            if (rptAdgroupClickList[i].hasEffectData == true) cityClickList[cname].effect++;
                                            cityClickList[cname].clickRank = parseFloat((cityClickList[cname].click * 100) / clickCount).toFixed(2);
                                            cityClickList[cname].effectvr = (cityClickList[cname].effect * 100 / cityClickList[cname].click).toFixed(2);
                                            cityClickList[cname].avgPrice = cityClickList[cname].cost / cityClickList[cname].click;
                                        };
                                    };
                                    var bdDataTable = new Array();
                                    for (var city in cityClickList) {
                                        var cityData = cityClickList[city];
                                        cityData.cost = (cityData.cost / 100).toFixed(2);
                                        cityData.avgPrice = (cityData.avgPrice / 100).toFixed(2);
                                        bdDataTable.push(cityData);
                                    };

                                    jQuery("#AreaCityParselist").jqGrid("clearGridData");
                                    jQuery("#AreaCityParselist").jqGrid("setGridParam", { data: bdDataTable });
                                    jQuery("#AreaCityParselist").trigger("reloadGrid");
                                };// new Function(getcfService("site/get-area-city-ad-group-city-out-ui-js", User));
                                cf_AreaCityAdGroupCityOutUI();
                                layer.close(index);
                            };//new Function("s", "e", "index", getcfService("site/get-area-city-parse-do-for-date-js", User));
                            window.setTimeout(function () { cf_DoAreaCityParseForDate(s, e, index); }, 10);
                        };
                    };//new Function("s", "e", "title", getcfService("site/get-area-city-parse-page-init-js", User));
                    cf_pageInitAreaCityParse(s, e, title);
                };//new Function("s", "e", "title", getcfService("site/get-area-city-parse-window-js", User));
                $("#bt_AreaCityParse_01").click(function () {
                    cf_OpenAreaCityParse(0, 0, "城市数据-今日实时");
                });
                $("#bt_AreaCityParse_02").click(function () {
                    cf_OpenAreaCityParse(-1, -1, "城市数据-昨日数据");
                });
                $("#bt_AreaCityParse_03").click(function () {
                    cf_OpenAreaCityParse(-1, -2, "城市数据-过去2天数据");
                });
                $("#bt_AreaCityParse_04").click(function () {
                    cf_OpenAreaCityParse(0, -2, "城市数据-所有点击（3天内）");
                });
            };//new Function(getcfService("site/get-area-city-parse-js", User));
                        cf_AreaCityParse()

"""
gjwr = """
if (!getUrlInfo()) { return false };
            var cf_openRunHeicheWindow = function () {
                var divUIjson = {
                    "html": `<div style=\"padding: 15px; line-height: 22px; background-color: #fff; color: #000;\">开始运行:<span id=\"jk_StartTime\"><\/span><br>\r\n  当前监控计划ID：\r\n  <input type=\"text\" class=\"input\" style=\"width:150px;\" id=\"ipt_campaignId\" \/>\r\n  --监控宝贝ID：\r\n  <input type=\"text\" class=\"input\" style=\"width:150px;\" id=\"ipt_itemId\" \/>\r\n  类目标识：\r\n  <input type=\"text\" class=\"input\" style=\"width:150px;\" id=\"ipt_CatID\" \/>\r\n  <br>\r\n  操作：\r\n  <label>\r\n    <input name=\"caozuo_heiche\" type=\"radio\" value=\"1\" checked=\"checked\" \/>\r\n    全部<\/label>\r\n  &nbsp;&nbsp;&nbsp;\r\n  <label>\r\n    <input name=\"caozuo_heiche\" type=\"radio\" value=\"2\" \/>\r\n    只关键词<\/label>\r\n  &nbsp;&nbsp;&nbsp;\r\n  <label>\r\n    <input name=\"caozuo_heiche\" type=\"radio\" value=\"3\" \/>\r\n    只创意图<\/label>\r\n  <br>\r\n  云关键词：<span id=\"lb_YunWordInfo\"><\/span> -- 云人群包：<span id=\"lb_YunRenqunInfo\"><\/span><br>\r\n  创意标题：\r\n  <input type=\"text\" class=\"input\" style=\"width:500px;\" id=\"ipt_cyTitle\" \/>\r\n  <br>\r\n  <div style=\"position:relative\">\r\n    <div style=\"position:absolute; left:0; top:0;\">创意图片：<\/div>\r\n    <div style=\" padding-left:60px;\">\r\n      1、\r\n      <input type=\"text\" class=\"input\" id=\"ipt_cyPic_1\" \/>\r\n\r\n      &nbsp;2、\r\n      <input type=\"text\" class=\"input\" id=\"ipt_cyPic_2\" \/>\r\n      &nbsp;3、\r\n      <input type=\"text\" class=\"input\" id=\"ipt_cyPic_3\" \/>\r\n      <br>\r\n      4、\r\n      <input type=\"text\" class=\"input\" id=\"ipt_cyPic_4\" \/>\r\n      &nbsp;5、\r\n      <input type=\"text\" class=\"input\" id=\"ipt_cyPic_5\" \/>\r\n   \r\n    <\/div>\r\n  <\/div>\r\n  监控条件：关键词(<b id=\"lb_jkWord\"><\/b>)当前首条出价(<b id=\"lb_jkWordFristPrice\"><\/b>)\r\n  <div style=\"display:none;\">--当首条出价高于:\r\n  <input type=\"text\" class=\"input\" style=\"width:50px;\" id=\"ipt_jkWordMaxPrice\" \/>\r\n  执行恢复宝贝！<\/div>\r\n  <br>\r\n  <label for=\"ck_IsUpdatecy\"><input type=\"checkbox\" id=\"ck_IsUpdatecy\" checked=\"true\" value=\"\"\/><b>删除前修改创意图片：<\/b><\/label>\r\n  <input type=\"text\" class=\"input\" style=\"width:500px; \" id=\"ipt_UpdatecyPic\" >\r\n  <label for=\"ck_IsWs\"><input type=\"checkbox\" id=\"ck_IsWs\" checked=\"true\" value=\"\"\/><b>使用游览器（只有操作:全部）<\/b><\/label>\r\n\r\n  <br>\r\n  每隔\r\n  <input type=\"text\" class=\"input\" style=\"width:50px;\" value=\"300\" id=\"ipt_jkWordTime\" \/>\r\n  秒检查！\r\n  <label for=\"ck_IsTime\">\r\n    <input type=\"checkbox\" id=\"ck_IsTime\" checked=\"true\" value=\"\"\/>\r\n    <b>宝贝在线时间段：<\/b><\/label>\r\n  (\r\n  <input type=\"text\" class=\"input\" style=\"width:60px;\" value=\"8:00\" id=\"ipt_jksTime\" \/>\r\n  --\r\n  <input type=\"text\" class=\"input\" style=\"width:60px;\" value=\"23:00\" id=\"ipt_jkeTime\" \/>\r\n  )<b>非时段将删除宝贝维护计划！<\/b><br>\r\n  <label for=\"ck_IsQAdd\">\r\n    <input type=\"checkbox\" id=\"ck_IsQAdd\" checked=\"true\" value=\"\"\/>\r\n    <b>极速添加--等待<\/b><\/label>\r\n  <input type=\"text\" class=\"input\" style=\"width:60px;\" value=\"3\" id=\"ipt_QWait\" \/>\r\n  秒(必须小于监控步长时间)<br>\r\n  服务信息:<span id=\"jk_LastTime\"><\/span><br>\r\n  <button class=\"layui-btn\" id=\"bt_StartJianKong\">开始监控<\/button>\r\n  <button class=\"layui-btn layui-btn-primary\" id=\"bt_StopJianKong\">暂停监控<\/button>\r\n  <button class=\"layui-btn layui-btn-primary\" id=\"bt_SaveConfigHeicheYUN\">保存配置<\/button>\r\n  <br>\r\n  恢复记录:<span id=\"lb_jkInfomsg\"><\/span><\/div>\r\n`
                };
                var divUI = divUIjson.html;

                var index = layer.open({
                    type: 1, content: divUI,
                    area: ["850px", "600px"],
                    title: ['监控程序-神车.高级无人值守', 'font-size:18px;'],
                    success: function (layero) {
                        var JianKongMian = function () {
                            getBidWordFristPrice = function () {
                                $.ajax({
                                    type: "post",
                                    url: "https://subway.simba.taobao.com/bidword/tool/bidword/getPriceBatchStrategy.htm",
                                    data: 'adGroupId=' + adGroupId + '&bidwordIds=' + fristWord['keywordId'] + '&type=mobile&sla=json&isAjaxRequest=true&token=' + User.token,
                                    async: false,
                                    success: function (data) {
                                        if (data.code == 200) {
                                            var res = data.result;
                                            fristWord['FristPrice'] = (res[0].wireless_fp_price) / 100;
                                            $("#lb_jkWordFristPrice").text(fristWord['FristPrice']);
                                        };
                                    },
                                    error: function () { }
                                });
                            };// new Function(getcfService("heiche-gaoji/get-heiche-bid-word-frist-price-js", User));
                            getFristBidWord = function () {
                                //获取关键词表
                                $.ajax({
                                    type: "POST",
                                    url: "https://subway.simba.taobao.com/bidword/list.htm",
                                    data: "campaignId=" + campaignId + "&adGroupId=" + adGroupId + "&queryWord=&queryType=0&sla=json&isAjaxRequest=true&token=" + User.token,
                                    datatype: "json",
                                    async: false,
                                    success: function (data) {
                                        if (data.code == 200) {
                                            var bidWordList = data.result;
                                            if (bidWordList.length > 0) {
                                                fristWord['keywordId'] = bidWordList[0].keywordId;
                                                fristWord['word'] = bidWordList[0].word;
                                                $("#lb_jkWord").text(fristWord['word']);
                                                getBidWordFristPrice();

                                            };
                                        };
                                    },
                                });
                            };// new Function(getcfService("heiche-gaoji/get-heiche-first-bid-word-js", User));
                            var myDate = new Date();
                            campaignId = getQueryString('campaignId');
                            adGroupId = getQueryString('adGroupId');
                            var cf_getItemNumId = function (adgid) {
                                var itemId = "";
                                $.ajax({
                                    type: "POST",
                                    url: "https://subway.simba.taobao.com/adgroup/get.htm?adGroupId=" + adgid,
                                    data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                    datatype: "json",
                                    async: false,
                                    success: function (data) {
                                        if (data.code == 200) { itemId = data.result.outsideItemNumId; }
                                        else {
                                            layer.msg(data.msg);
                                        }

                                    },
                                    error: function () { }
                                });
                                return itemId;
                            };// new Function("adgid", getcfService("comm/subway-get-item-num-id-js", User));
                            var itemId = cf_getItemNumId(adGroupId);
                            //var cf_getCatID=new Function("adGroupId",getcfService("Subway.getCatID",User));
                            var cf_getCatID = function (adGroupId) {
                                var categoryId;
                                $.ajax({
                                    type: "POST",
                                    url: "https://subway.simba.taobao.com/adgroup/getAdGroupWithCategory.htm?adGroupId=" + adGroupId,
                                    data: null,
                                    async: false,
                                    dataType: "json",
                                    success: function (data) { if (data.code == 200) { categoryId = data.result.adGroupDTO.categoryId; }; },
                                    error: function () { alert("error:getCatID"); }
                                });
                                return categoryId;

                            };// new Function("adGroupId", getcfService("comm/subway-get-cat-ids", User));
                            var categoryId = cf_getCatID(adGroupId);
                            var getYunHeicheConfig = function (itemId) {
                                var resData = {};
                                var cf_getRsetSubway = function (itemId) {
                                    var ret = {};
                                    var postdata = { itemId: itemId };
                                    $.extend(postdata, User);
                                    $.ajax({
                                        type: "post",

                                        //url: "https://zhitongche.yiyoushi.net/index.php?r=heiche-gaoji/get-heiche-rsetsubway",
                                        url: server_url + '/taobao/api?r=heiche-gaoji/get-heiche-rsetsubway',
                                        //url: "https://www.chebaochajian.com/api/getrsetsubway/" + itemId,

                                        contentType: 'application/json',
                                        data: JSON.stringify(postdata),
                                        async: false,
                                        dataType: "json",
                                        success: function (data, status) {
                                            ret = data;
                                            if (data.code != 200) {
                                                layer.alert(data.msg)
                                            }
                                        }
                                    });
                                    return ret;
                                };// new Function("itemId", getcfService("heiche-gaoji/get-heiche-rset-subway-js", User));
                                var obj = cf_getRsetSubway(itemId);
                                if (obj.code == 200) {
                                    resData["itemId"] = obj.result.ItemId;
                                    resData["cybt"] = obj.result.CreativeTitle;

                                    resData["cytp_1"] = obj.result.CreativeImgUrl_1;
                                    resData["cytp_2"] = obj.result.CreativeImgUrl_2;
                                    resData["cytp_3"] = obj.result.CreativeImgUrl_3;
                                    resData["cytp_4"] = obj.result.CreativeImgUrl_4;
                                    resData["cytp_5"] = obj.result.CreativeImgUrl_5;
                                    resData["cytp_UpdatecyPic"] = obj.result.CreativeImgUrl_reset;


                                    resData["id"] = obj.result.id;
                                    resData["maxppc"] = obj.result.MaxPrice;
                                    resData["deletecy"] = obj.result.IsDelCreative;
                                    resData["editTime"] = obj.result.UpdateDate;
                                    resData["jkstep"] = obj.result.Step; resData["istime"] = obj.result.IsCheckTime;
                                    resData["stime"] = obj.result.StartTime; resData["etime"] = obj.result.EndTime;
                                    resData["expdate"] = obj.result.ExpDate;
                                    resData["IsQAdd"] = obj.result.IsQAdd;
                                    resData["QWait"] = obj.result.QWait
                                } else if (obj.code == "300") {
                                    resData["itemId"] = itemId; resData["cybt"] = '当前宝贝无监控值守权限，请联系管理员申请开通！';
                                    resData["id"] = "0"
                                };
                                return resData;
                            };// new Function("itemId", getcfService("heiche-gaoji/get-heiche-config-js", User));
                            itemConfig = getYunHeicheConfig(itemId);

                            $("#jk_StartTime").text(myDate.toLocaleString() + '(授权有效期:[' + itemConfig["expdate"] + '])');

                            $("#ipt_campaignId").val(campaignId);
                            $("#ipt_itemId").val(itemId); $("#ipt_CatID").val(categoryId);
                            cf_getYunData = function (itemId) {
                                var cf_getWordYun = function (itemId, User) {
                                    var ret = {};
                                    var postdata = { itemId: itemId };
                                    $.extend(postdata, User);
                                    $.ajax({
                                        type: "post",
                                        //url: "https://zhitongche.yiyoushi.net/index.php?r=heiche-gaoji/get-heiche-bid-word-yun-data",
                                        url: server_url + '/taobao/api?r=heiche-gaoji/get-heiche-bid-word-yun-data',
                                        contentType: 'application/json',
                                        data: JSON.stringify(postdata),
                                        async: false,
                                        dataType: "json",
                                        success: function (data, status) {
                                            ret = data;
                                            if (data.code != 200) {
                                                layer.alert(data.msg)
                                            }
                                        }
                                    });
                                    return ret;
                                };// new Function("itemId", "User", getcfService("heiche-gaoji/get-heiche-yun-bid-word-data-js", User));
                                BDData = { 'code': 1 };
                                BDData = cf_getWordYun(itemId, User);
                                if (BDData['code'] == 200) {
                                    BDData = BDData.result;
                                    $("#lb_YunWordInfo").text("(数量【" + BDData.count +
                                    "】，更新时间【" + BDData.impDate + "】)");
                                } else {
                                    $("#lb_YunWordInfo").text("(数量【0】，更新时间【未知】)");
                                    layer.alert("未备份关键词，不能操作！");

                                }




                                RQData = { 'code': 1 };
                                var cf_getTargetYun = function (itemId, User) {
                                    var ret = {};
                                    var postdata = { itemId: itemId };
                                    $.extend(postdata, User);
                                    $.ajax({
                                        type: "post",
                                        //url: "https://zhitongche.yiyoushi.net/index.php?r=heiche-gaoji/get-heiche-crowd-yun-data",
                                        url: server_url + '/taobao/api?r=heiche-gaoji/get-heiche-crowd-yun-data',
                                        contentType: 'application/json',
                                        data: JSON.stringify(postdata),
                                        async: false,
                                        dataType: "json",
                                        success: function (data, status) {
                                            ret = data;
                                            if (data.code != 200) {
                                                layer.alert(data.msg)
                                            }
                                        }
                                    });
                                    return ret;
                                };// new Function("itemId", "User", getcfService("heiche-gaoji/get-heiche-yun-crowd-data-js", User));
                                RQData = cf_getTargetYun(itemId, User);
                                if (RQData['code'] == 200) {
                                    RQData = RQData.result;
                                    $("#lb_YunRenqunInfo").text("(数量【" + RQData.Count + "】，更新时间【" + RQData.UpdateDate + "】)");
                                } else {
                                    $("#lb_YunRenqunInfo").text("(数量【0】，更新时间【未知】)");
                                    layer.alert("未备份人群，不能操作！");

                                }
                            };// new Function("itemId", getcfService("heiche-gaoji/get-heiche-yun-data-js", User));
                            cf_getYunData(itemId);
                            //var cf_getTargetTags = new Function(getcfService("heiche-gaoji/get-heiche-yun-target-tags-js", User));
                            TargetTags = app.cf_getTargetTags(); getFristBidWord(); $("#bt_StopJianKong").attr({ "disabled": "disabled" });
                            if (itemConfig["id"] == "0") {
                                $("#bt_StopJianKong").attr({ "disabled": "disabled" });
                                $("#bt_StartJianKong").attr({ "disabled": "disabled" });
                                $("#ipt_cyTitle").val(itemConfig["cybt"])
                            } else {

                                $("#ipt_cyTitle").val(itemConfig["cybt"]);

                                $("#ipt_cyPic_1").val(itemConfig["cytp_1"]);
                                $("#ipt_cyPic_2").val(itemConfig["cytp_2"]);
                                $("#ipt_cyPic_3").val(itemConfig["cytp_3"]);
                                $("#ipt_cyPic_4").val(itemConfig["cytp_4"]);
                                $("#ipt_cyPic_5").val(itemConfig["cytp_5"]);
                                $("#ipt_UpdatecyPic").val(itemConfig["cytp_UpdatecyPic"]);



                                $("#ipt_jkWordMaxPrice").val(itemConfig["maxppc"]);
                                if (itemConfig["deletecy"] == "1") { $("#ck_IsUpdatecy").attr("checked", true) } else { $("#ck_IsUpdatecy").attr("checked", false) };
                                $("#ipt_jkWordTime").val(itemConfig["jkstep"]);
                                if (itemConfig["istime"] == "1") { $("#ck_IsTime").attr("checked", true) } else { $("#ck_IsTime").attr("checked", false) };
                                $("#ipt_jksTime").val(itemConfig["stime"]); $("#ipt_jkeTime").val(itemConfig["etime"]);
                                if (itemConfig["IsQAdd"] == "1") { $("#ck_IsQAdd").attr("checked", true) } else { $("#ck_IsQAdd").attr("checked", false) };
                                $("#ipt_QWait").val(itemConfig["QWait"])
                            }
                            var StepTime = 60 * 1000;
                            var jiankongDoNew = function () {
                                /*监控执行程序*/


                                var myDate = new Date();
                                //防退出
                                getServerDate();
                                //监控推广
                                if (!IsRuning) { return false; }

                                if (IsOnlineTime()) {
                                    if (IsHave()) {
                                        //推广单元存在
                                        if (fristWord['keywordId'] == "") {
                                            getFristBidWord();
                                        };
                                        if (!fristWord['FristPrice'] || fristWord['FristPrice'] == "-0.01") {
                                            getBidWordFristPrice();
                                        };
                                    } else {
                                        //推广单元不存在 添加推广
                                        saveItemSmartSolution();
                                        //刷新推广单元ID
                                        //获取首条出价
                                        window.setTimeout(function () { IsHave(); getFristBidWord(); }, 5000);

                                    };
                                } else {
                                    //不在推广时段 删除维护
                                    if (IsHave()) {
                                        //====删除宝贝======
                                        IsUpdateCy = $('#ck_IsUpdatecy').prop('checked');
                                        if (IsUpdateCy) {
                                            updateCreative(adGroupId);
                                            var dateStart = new Date(),
                                                dateEnd;
                                            while (((dateEnd = new Date()) - dateStart) <= 5000) {
                                            };
                                        };
                                        deleteAdGroup(adGroupId);
                                    };
                                };

                                $("#jk_LastTime").text(myDate.toLocaleString() + ' NewAdGroupId:' + adGroupId);
                            };// new Function(getcfService("heiche-gaoji/get-heiche-jian-kong-do-new-js", User));
                            jiankongDoNew();
                            timeId = window.setInterval(jiankongDoNew, StepTime);
                        };// new Function(getcfService("heiche-gaoji/get-heiche-jian-kong-mian-js", User)); JianKongMian()
                    },
                    cancel: function (index, layero) {
                        var jiankongStop = function () {
                            layer.msg("停止监控！");
                            $("#bt_StartJianKong").text("开始监控");
                            $("#bt_StartJianKong").removeAttr("disabled");//将按钮可用
                            $("#bt_StopJianKong").attr({ "disabled": "disabled" });
                            IsRuning = false;
                            window.clearInterval(timeId2);
                        };// new Function(getcfService("heiche-gaoji/get-heiche-stop-js", User));
                        jiankongStop(); layer.close(index)
                    }
                });
                $("#bt_StartJianKong").click(function () {
                    var jiankongAdgroup = function () {
                        if (Version == 'test') {
                            jiankongAdgroup();
                            return;
                        };
                        var itemConfig = new Object('id', '1');
                        if (itemConfig["id"] == "0") {
                            layer.msg('无人值守功能仅对指定宝贝开通！<br/>需要对当前宝贝ID（' + itemConfig["itemId"] + '）授权！<br/> 请联系交流群管理授权！');
                            return;
                        };
                        IsOnlineTime = function () {
                            var isonline = true;
                            var obj = document.getElementById("ck_IsTime");//
                            if (obj.checked) { isonline = false; } else { isonline = true; };
                            if (!isonline) {
                                var st = $("#ipt_jksTime").val();
                                var et = $("#ipt_jkeTime").val();
                                var ar = [st, et];
                                isonline = checkTime(ar);
                            };
                            return isonline;
                        };// new Function(getcfService("heiche-gaoji/get-heiche-is-online-time-js", User));
                        IsHave = function () {
                            var haveing = false;
                            var cam_id = $("#ipt_campaignId").val();
                            var item_id = $("#ipt_itemId").val();
                            var url = 'https://subway.simba.taobao.com/adgroup/adGroupList.htm?queryVO={"pageNumber":1,"pageSize":"200","queryTitle":"","queryState":"","campaignId":"' + cam_id + '"}';
                            var postdata = "sla=json&isAjaxRequest=true&token=" + User.token;
                            $.ajax({
                                type: 'POST',
                                url: url,
                                data: postdata,
                                async: false,
                                success: function (data) {
                                    var items = data.result.items;
                                    for (var idx in items) {
                                        if (items[idx].adGroupDTO.outsideItemNumId == item_id) {
                                            haveing = true;
                                            itemPicUrl = items[idx].adGroupDTO.imgUrl;
                                            adGroupId = items[idx].adGroupDTO.adGroupId;
                                        };
                                    };
                                },
                                error: function () { }
                            });
                            return haveing;
                        };// new Function(getcfService("heiche-gaoji/get-heiche-is-have-js", User));
                        saveItemSmartSolution = function () {
                            /*添加创意*/
                            var cam_id = $("#ipt_campaignId").val();
                            var item_id = $("#ipt_itemId").val();
                            var cat_id = $("#ipt_CatID").val();


                            var cyTile = $("#ipt_cyTitle").val();
                            //创意图片
                            var arr_pic = [];
                            for (var i = 1; i <= 5; i++) {
                                if ($.trim($('#ipt_cyPic_' + i).val()) == '') { continue; }
                                arr_pic.push($.trim($('#ipt_cyPic_' + i).val()));
                            }


                            creativePicNum = creativePicNum + 1 > arr_pic.length ? 0 : creativePicNum;
                            cyPic = arr_pic[creativePicNum];
                            ++creativePicNum;


                            if (arr_pic.length < 1) {
                                layer.alert('请设置创意图');
                                return false;
                            }



                            cf_getYunData(item_id);
                            if (BDData['code'] == 1) {
                                layer.alert('关键词备份数据获取失败，不能操作');
                                return false;
                            }
                            if (RQData['code'] == 1) {
                                layer.alert('人群备份数据获取失败，不能操作');
                                return false;
                            }


                            var addWords = BDData.BidWordData;
                            if (addWords != '' && addWords != null) { addWords = addWords.replace(/maxPrice/g, 'bidPrice').replace(/maxMobilePrice/g, 'mobileBidPrice'); }


                            if (addWords == '' || addWords == null) {
                                layer.alert('关键词没有备份，不能操作');
                                return;
                            }

                            var addCrowds = '[]';
                            if (typeof RQData.CrowdData == 'undefined' || typeof RQData.CrowdData == undefined || RQData.CrowdData == '') {
                                addCrowds = '[]';
                            } else {
                                var targetArr = RQData.CrowdData.split("#");
                                var targetings = new Array();
                                var e = 0;
                                for (var i = 0; i < targetArr.length; i++) {
                                    var tag = targetArr[i].split('$');
                                    var tagName = tag[0].split(',');
                                    var discount = tag[1];
                                    var onlineStatus = tag[2];
                                    var tagList = new Array();
                                    var templateId;
                                    if (typeof TargetTags[tagName[0]] == 'undefined' || TargetTags[tagName[0]] == '' || TargetTags[tagName[0]] == null) { continue; }

                                    for (var j = 0; j < tagName.length; j++) {
                                        tagList.push(TargetTags[tagName[j]].tagCode);
                                        templateId = TargetTags[tagName[j]].templateId;
                                    };
                                    targetings.push('{"crowdDTO":{"templateId":"' + templateId
                                        + '","name":"' + tag[0]
                                        + '","tagList":[' + tagList.join(',') + ']}'
                                        + ',"discount":' + discount + ',"targetingType":1}');
                                }
                                addCrowds = '[' + targetings.join(',') + ']';
                            }




                            cyPic = cyPic.replace(/https:/, '');
                            cyPic = cyPic.replace(/http:/, '');
                            cyPic = cyPic.replace(/\/\/img./, '//gd1.');

                            /* var postData = 'itemADGroupVO={"campaignId":"' + cam_id + '","itemNumId":"' + item_id + '","sortId":"' + cat_id + '","creativeElementList":[{"cname":"TITLE","cvalue":"' + cyTile + '"},{"cname":"IMGURL","cvalue":"' + cyPic + '"},{"cname":"SUBTITLE","cvalue":""},{"cname":"DESCRIPTION","cvalue":""},{"cname":"LINKURL","cvalue":"http://item.taobao.com/item.htm?id=' + item_id + '"},{"cname":"DISPLAYURL","cvalue":""},{"cname":"NPXSCORE","cvalue":""},{"cname":"MINISTORY","cvalue":""},{"cname":"DOCUMENTS","cvalue":""}],"elementTId":"1","creativeImgUrl":"' + cyPic + '","creativeTitle":"' + cyTile + '","qualityflag":0,"defaultPrice":"10","autoMatchState":1,"nonSearchState":1,"logsBidwordStr":""}'
                                 + '&addWords=' + addWords
                                 + (addCrowds == '' ? '' : '&addCrowds=' + addCrowds)
                                 + '&analyseTraceId=ac1dc00514974263452964085e'
                                 + '&sla=json&isAjaxRequest=true&token=' + User.token; //无效的赋值 */
                            var postData = {
                                itemADGroupVO: '{"campaignId":"' + cam_id + '","itemNumId":"' + item_id + '","sortId":"' + cat_id + '","creativeElementList":[{"cname":"TITLE","cvalue":"' + cyTile + '"},{"cname":"IMGURL","cvalue":"' + cyPic + '"},{"cname":"SUBTITLE","cvalue":""},{"cname":"DESCRIPTION","cvalue":""},{"cname":"LINKURL","cvalue":"http://item.taobao.com/item.htm?id=' + item_id + '"},{"cname":"DISPLAYURL","cvalue":""},{"cname":"NPXSCORE","cvalue":""},{"cname":"MINISTORY","cvalue":""},{"cname":"DOCUMENTS","cvalue":""}],"elementTId":"1","creativeImgUrl":"' + cyPic + '","creativeTitle":"' + cyTile + '","qualityflag":0,"defaultPrice":"10","autoMatchState":1,"nonSearchState":1,"logsBidwordStr":""}',
                                addWords: addWords,
                                analyseTraceId: 'ac1dc00514974263452964085e',
                                sla: 'json',
                                isAjaxRequest: true,
                                token: User.token
                            };
                            if (addCrowds != '') {
                                postData['addCrowds'] = addCrowds
                            }
                            $.ajax({
                                type: "POST",
                                url: "https://subway.simba.taobao.com/smartsolution2/saveItemSmartSolution.htm",
                                data: postData,
                                async: false,
                                success: function (data) {
                                    var ret = data;
                                    var myDate = new Date();
                                    $("#lb_jkInfomsg").prepend(myDate.toLocaleString() + ':添加推广单元图(' + (creativePicNum) + ')<br>');
                                    var infoHtml = $("#lb_jkInfomsg").html();
                                    var pos = infoHtml.indexOf("<br>", 500);
                                    if (pos > 0) {
                                        $("#lb_jkInfomsg").html(infoHtml.substring(0, pos));
                                    };
                                },
                                error: function () {
                                    alert('error:saveItemSmartSolution');
                                }
                            });
                        };// new Function(getcfService("heiche-gaoji/get-save-item-smart-solution-js", User));
                        updateCreative = function (adgid) {
                            /*
    *
    *
    *updateCreative创意
    @adgid
    */
                            var creativeId;
                            $.ajax({
                                type: 'POST',
                                url: 'https://subway.simba.taobao.com/creative/list.htm?adGroupId=' + adgid,
                                data: 'sla=json&isAjaxRequest=true&token=' + User.token,
                                async: false,
                                success: function (data) {
                                    if (data.code == 200) {
                                        if (data.result.length > 0) { creativeId = data.result[0].creativeId; }
                                    };
                                },
                            });
                            if (!creativeId) {
                                return;
                            };

                            var cyTile = $("#ipt_cyTitle").val();
                            var item_id = $("#ipt_itemId").val();
                            if ($.trim($('#ipt_UpdatecyPic').val()) != '') {
                                itemPicUrl = $('#ipt_UpdatecyPic').val();
                            }
                            if (typeof itemPicUrl == 'undefined' || itemPicUrl == '') { itemPicUrl = $('#ipt_cyPic').val(); }
                            if (itemPicUrl == '') { return; }


                            itemPicUrl = itemPicUrl.replace(/https:/, '');
                            itemPicUrl = itemPicUrl.replace(/http:/, '');
                            itemPicUrl = itemPicUrl.replace(/\/\/img./, '//gd1.');





                            var postdata = 'creative={"creativeElementList":[{"cname":"TITLE","cvalue":"' + cyTile + '"},{"cname":"IMGURL","cvalue":"' + itemPicUrl + '"},{"cname":"SUBTITLE","cvalue":""},{"cname":"DESCRIPTION","cvalue":""},{"cname":"LINKURL","cvalue":"http://item.taobao.com/item.htm?id=' + item_id + '"},{"cname":"DISPLAYURL","cvalue":""},{"cname":"NPXSCORE","cvalue":""},{"cname":"MINISTORY","cvalue":""},{"cname":"DOCUMENTS","cvalue":""}],"campaignId":"' + campaignId + '","adGroupId":"' + adgid + '","creativeId":"' + creativeId + '","elementTId":"1","qualityflag":0,"creativeAdvancedSettingDTO":{"channel":{"pc":"1","wireless":"1"}},"templateData":null,"creativeCenterTemplateId":null,"sailingType":null}'
                                + '&sla=json&isAjaxRequest=true&token=' + User.token;

                            //修改创意
                            $.ajax({
                                type: "POST",
                                url: 'https://subway.simba.taobao.com/creative/updateCreative.htm',
                                data: postdata,
                                async: false,
                                success: function (data) {
                                    var ret = data.code;
                                },
                                error: function () { }
                            });
                        };// new Function("adgid", getcfService("heiche-gaoji/get-heiche-update-creative-js", User));
                        deleteAdGroup = function (adgid) {
                            $.ajax({
                                type: "POST",
                                url: "https://subway.simba.taobao.com/adgroup/deleteAdGroup.htm",
                                data: 'campaignId=' + campaignId + '&adGroupIds=["' + adgid + '"]&sla=json&isAjaxRequest=true&token=' + User.token,
                                async: false,
                                success: function (data) {
                                    var ret = data.code;
                                    fristWord['keywordId'] = "";
                                    var myDate = new Date();
                                    $("#lb_jkInfomsg").prepend(myDate.toLocaleString() + ':删除推广单元(' + adgid + ')--当前首条出价:' + fristWord['FristPrice'] + '元<br>');
                                    adGroupId = "";
                                },
                                error: function () { }
                            });
                        };// new Function("adgid", getcfService("heiche-gaoji/get-heiche-delete-ad-group-js", User));

                        creativePicNum = 0;/*图片顺序*/

                        ws_youlanqi = null;
                        ws_youlanqi = new WebSocket("ws://127.0.0.1:88");
                        ws_youlanqi.onopen = function (msg) {
                            console.log('ws连接成功');

                        };
                        ws_youlanqi.onclose = function () {
                            console.log('webSocket closed');
                        };
                        ws_youlanqi.onerror = function (error) {
                            console.log('error :' + error.name + error.number);
                        };
                        ws_youlanqi.onmessage = function (message) {
                            console.log('receive message : ' + message.data);
                            var res = $.parseJSON(message.data);

                            switch (res['type']) {
                                case 'creativePic':
                                    if (res['flag'] == 1) {
                                        var dateStart = new Date(), dateEnd;
                                        while (((dateEnd = new Date()) - dateStart) <= 5000) { };
                                        deleteAdGroup(adGroupId);
                                        //极速添加宝贝
                                        if (IsQAdd) {
                                            var dt = QWait * 1000;
                                            var dateStart = new Date(), dateEnd;
                                            while (((dateEnd = new Date()) - dateStart) <= dt) { };
                                            saveItemSmartSolution();
                                        };
                                    }

                            }
                        };
                        IsFnCreative = function (adgid) {
                            var creativeId;
                            $.ajax({
                                type: 'POST',
                                url: 'https://subway.simba.taobao.com/creative/list.htm?adGroupId=' + adgid,
                                data: 'sla=json&isAjaxRequest=true&token=' + User.token,
                                async: false,
                                success: function (data) {
                                    if (data.code == 200) {
                                        if (data.result.length > 0) { creativeId = data.result[0].creativeId; }
                                    };
                                },
                            });
                            if (!creativeId) {
                                return false;
                            };
                            return creativeId;
                        }

                        layer.msg("监控程序打开！");
                        var maxPrice = $("#ipt_jkWordMaxPrice").val();
                        fristWord['MaxPrice'] = maxPrice;
                        var dit = parseInt($("#ipt_jkWordTime").val());
                        $("#bt_StartJianKong").text("监控中...");
                        $("#bt_StartJianKong").attr({ "disabled": "disabled" });
                        $("#bt_StopJianKong").removeAttr("disabled");//将按钮可用
                        var obj = document.getElementById("ck_IsUpdatecy");//
                        if (obj.checked) { IsUpdateCy = true; } else { IsUpdateCy = false; };
                        var obj1 = document.getElementById("ck_IsQAdd");//
                        if (obj1.checked) { IsQAdd = true; } else { IsQAdd = false; };
                        QWait = $("#ipt_QWait").val();
                        IsRuning = true;
                        var runingAdgroup = function () {
                            if (!IsOnlineTime()) return;
                            if (adGroupId == "") return;


                            //监控执行
                            var maxPrice = $("#ipt_jkWordMaxPrice").val();
                            fristWord['MaxPrice'] = maxPrice;
                            getBidWordFristPrice();
                            //if (parseFloat(fristWord['FristPrice']) >= parseFloat(fristWord['MaxPrice'])) {
                            if (1) {
                                if ($('input[name="caozuo_heiche"]:checked').size() == 0 || $('input[name="caozuo_heiche"]:checked').val() == 1) {
                                    //默认 直接删除创意
                                    //执行删除推广单元和创建推广单元
                                    IsUpdateCy = $('#ck_IsUpdatecy').prop('checked');
                                    if (IsUpdateCy) {

                                        if (!$('#ck_IsWs').prop('checked')) {
                                            //不使用ws
                                            updateCreative(adGroupId);
                                            var dateStart = new Date(), dateEnd;
                                            while (((dateEnd = new Date()) - dateStart) <= 5000) { };
                                            deleteAdGroup(adGroupId);
                                            //极速添加宝贝
                                            if (IsQAdd) {
                                                var dt = QWait * 1000;
                                                var dateStart = new Date(), dateEnd;
                                                while (((dateEnd = new Date()) - dateStart) <= dt) { };
                                                saveItemSmartSolution();
                                            };
                                        } else {
                                            var creativeId;
                                            $.ajax({
                                                type: 'POST',
                                                url: 'https://subway.simba.taobao.com/creative/list.htm?adGroupId=' + adGroupId,
                                                data: 'sla=json&isAjaxRequest=true&token=' + User.token,
                                                async: false,
                                                success: function (data) {
                                                    if (data.code == 200) {
                                                        if (data.result.length > 0) { creativeId = data.result[0].creativeId; }
                                                    };
                                                },
                                            });
                                            if (!creativeId) {
                                                return;
                                            };
                                            var item_id = $("#ipt_itemId").val();
                                            var cat_id = $('#ipt_CatID').val();
                                            cat_id = cat_id.split(' ');
                                            cat_id = cat_id[1];
                                            try {
                                                ws_youlanqi.send(JSON.stringify({ type: 'creativePic', url: 'https://upload.taobao.com/auction/container/publish.htm?catId=' + cat_id + '&itemId=' + item_id }));
                                            }
                                            catch (err) {
                                                layer.msg('重新启动辅助工具');
                                            }
                                        }

                                    } else {
                                        deleteAdGroup(adGroupId);
                                        //极速添加宝贝
                                        if (IsQAdd) {
                                            var dt = QWait * 1000;
                                            var dateStart = new Date(), dateEnd;
                                            while (((dateEnd = new Date()) - dateStart) <= dt) { };
                                            saveItemSmartSolution();
                                        };
                                    }
                                }
                                if ($('input[name="caozuo_heiche"]:checked').size() == 1 && $('input[name="caozuo_heiche"]:checked').val() == 2) {
                                    //只删除关键词和恢复关键词
                                    var creativeId = IsFnCreative(adGroupId);
                                    if (!creativeId) {
                                        //不存在 直接创建
                                        saveItemSmartSolution();
                                        return true;
                                    }
                                    //获取关键词表
                                    var keywordIds = [];
                                    var retCode = 1;
                                    $.ajax({
                                        type: "POST",
                                        url: "https://subway.simba.taobao.com/bidword/list.htm",
                                        data: "campaignId=" + campaignId + "&adGroupId=" + adGroupId + "&queryWord=&queryType=0&sla=json&isAjaxRequest=true&token=" + User.token,
                                        datatype: "json",
                                        async: false,
                                        success: function (data) {
                                            retCode = data.code;
                                            if (data.code == 200) {
                                                var bidWordList = data.result;
                                                if (bidWordList.length > 0) {
                                                    for (var i in bidWordList) {
                                                        keywordIds.push(bidWordList[i]['keywordId']);
                                                    }
                                                };
                                            };
                                        },
                                    });
                                    if (retCode != 200) {
                                        layer.msg("获取关键词列表失败，等待下一轮！");
                                        return false;
                                    }
                                    if (keywordIds.length > 0) {
                                        //删除关键词
                                        $.ajax({
                                            type: "POST",
                                            url: "https://subway.simba.taobao.com/bidword/delete.htm",
                                            data: "campaignId=" + campaignId + "&keywordIds=[" + keywordIds.join(",") + "]&sla=json&isAjaxRequest=true&token=" + User.token,
                                            datatype: "json",
                                            async: false,
                                            success: function (data) {
                                                if (data.code == 200) {
                                                    var bidWordList = data.result;
                                                    var myDate = new Date();
                                                    $("#lb_jkInfomsg").prepend(myDate.toLocaleString() + ':删除推广单元关键词<br>');
                                                    var infoHtml = $("#lb_jkInfomsg").html();
                                                    var pos = infoHtml.indexOf("<br>", 500);
                                                    if (pos > 0) {
                                                        $("#lb_jkInfomsg").html(infoHtml.substring(0, pos));
                                                    };
                                                };
                                            },
                                        });
                                    }
                                    var item_id = $("#ipt_itemId").val();
                                    var postdata = { itemId: item_id };
                                    $.extend(postdata, User);
                                    $.ajax({
                                        type: "post",
                                        //url: "https://zhitongche.yiyoushi.net/index.php?r=heiche-gaoji/get-bid-word-yun-word-data",
                                        url: server_url + '/taobao/api?r=heiche-gaoji/get-bid-word-yun-word-data',
                                        contentType: 'application/json',
                                        data: JSON.stringify(postdata),
                                        async: false,
                                        dataType: "json",
                                        success: function (data, status) {
                                            if (data['code'] != 200) {
                                                layer.alert(data.msg)
                                                return false;

                                            }

                                            if (data.result.length < 1) {
                                                layer.msg("没有备份关键词！");
                                                return;
                                            }
                                            var keywords = data.result[0]['BidWordData'];
                                            if (keywords.length > 0) {
                                                if (IsQAdd) {
                                                    var dt = QWait * 1000;
                                                    var dateStart = new Date(), dateEnd;
                                                    while (((dateEnd = new Date()) - dateStart) <= dt) { };
                                                };

                                                //添加关键词
                                                $.ajax({
                                                    type: "post",
                                                    url: "https://subway.simba.taobao.com/bidword/add.htm",
                                                    //data: 'logsBidwordStr=""&adGroupId=' + adGroupId + '&keywords='+keywords+'&sla=json&isAjaxRequest=true&token=' + User.token,
                                                    data: {
                                                        logsBidwordStr: '',
                                                        adGroupId: adGroupId,
                                                        keywords: keywords,
                                                        sla: 'json',
                                                        isAjaxRequest: true,
                                                        token: User.token
                                                    },
                                                    async: false,
                                                    success: function (data) {
                                                        var myDate = new Date();
                                                        $("#lb_jkInfomsg").prepend(myDate.toLocaleString() + ':添加推广单元关键词<br>');
                                                        var infoHtml = $("#lb_jkInfomsg").html();
                                                        var pos = infoHtml.indexOf("<br>", 500);
                                                        if (pos > 0) {
                                                            $("#lb_jkInfomsg").html(infoHtml.substring(0, pos));
                                                        };
                                                    }
                                                });
                                            }
                                        }
                                    });






                                }
                                if ($('input[name="caozuo_heiche"]:checked').size() == 1 && $('input[name="caozuo_heiche"]:checked').val() == 3) {
                                    //只更新创意图:先删除创意再添加创意
                                    var creativeId = IsFnCreative(adGroupId);
                                    if (!creativeId) {
                                        //不存在 直接创建
                                        saveItemSmartSolution();
                                        return true;
                                    }

                                    var cyTile = $("#ipt_cyTitle").val();
                                    var item_id = $("#ipt_itemId").val();
                                    var arr_pic = [];
                                    for (var i = 1; i <= 5; i++) {
                                        if ($.trim($('#ipt_cyPic_' + i).val()) == '') { continue; }
                                        arr_pic.push($.trim($('#ipt_cyPic_' + i).val()));
                                    }
                                    if (arr_pic.length < 1) {
                                        layer.alert('请设置创意图');
                                        return;
                                    }





                                    creativePicNum = creativePicNum + 1 > arr_pic.length ? 0 : creativePicNum;
                                    itemPicUrl = arr_pic[creativePicNum];
                                    ++creativePicNum;


                                    itemPicUrl = itemPicUrl.replace(/https:/, '');
                                    itemPicUrl = itemPicUrl.replace(/http:/, '');
                                    itemPicUrl = itemPicUrl.replace(/\/\/img./, '//gd1.');


                                    //添加创意
                                    var ret = { code: 1 };

                                    $.ajax({
                                        type: "POST",
                                        url: 'https://subway.simba.taobao.com/creative/addCreative.htm',
                                        data: {
                                            creative: '{"creativeElementList":[{"cname":"TITLE","cvalue":"' + cyTile + '"},{"cname":"IMGURL","cvalue":"' + itemPicUrl + '"},{"cname":"SUBTITLE","cvalue":""},{"cname":"DESCRIPTION","cvalue":""},{"cname":"LINKURL","cvalue":"http://item.taobao.com/item.htm?id=' + item_id + '"},{"cname":"DISPLAYURL","cvalue":""},{"cname":"NPXSCORE","cvalue":""},{"cname":"MINISTORY","cvalue":""},{"cname":"DOCUMENTS","cvalue":""}],"campaignId":"' + campaignId + '","adGroupId":"' + adGroupId + '","elementTId":"1","qualityflag":0,"expTraffic":null,"expTime":null,"creativeAdvancedSettingDTO":{"channel":{"pc":"1","wireless":"1"}}}',
                                            sla: 'json',
                                            isAjaxRequest: true,
                                            token: User.token,
                                            _referer: '/campaigns/standards/adgroups/items/creative/add?adGroupId=' + adGroupId + '&campaignId=' + campaignId
                                        },
                                        dataType: "json",
                                        async: false,
                                        success: function (data) {
                                            if (data.code == 200) {
                                                ret.code = 200;
                                                var myDate = new Date();
                                                $("#lb_jkInfomsg").prepend(myDate.toLocaleString() + ':添加创意图片:(' + (creativePicNum) + ')<br>');
                                                var infoHtml = $("#lb_jkInfomsg").html();
                                                var pos = infoHtml.indexOf("<br>", 500);
                                                if (pos > 0) { $("#lb_jkInfomsg").html(infoHtml.substring(0, pos)); };
                                            } else {
                                                layer.msg($.isArray(data.msg) ? data.msg[0] : data.msg);
                                            }

                                        }
                                    });
                                    if (ret.code != 200) {
                                        ;
                                        return false;
                                    }

                                    if (IsQAdd) {
                                        var dt = QWait * 1000;
                                        var dateStart = new Date(), dateEnd;
                                        while (((dateEnd = new Date()) - dateStart) <= dt) { };
                                    };

                                    //删除创意

                                    var postdata = 'sla=json&isAjaxRequest=true&token=' + User.token;
                                    $.ajax({
                                        type: "POST",
                                        url: 'https://subway.simba.taobao.com/creative/delete.htm?creativeId=' + creativeId,

                                        data: postdata,
                                        dataType: "json",
                                        async: false,
                                        success: function (data) {

                                            if (data.code == 200) {
                                                var myDate = new Date();
                                                $("#lb_jkInfomsg").prepend(myDate.toLocaleString() + ':删除创意图片<br>');
                                                var infoHtml = $("#lb_jkInfomsg").html();
                                                var pos = infoHtml.indexOf("<br>", 500);
                                                if (pos > 0) {
                                                    $("#lb_jkInfomsg").html(infoHtml.substring(0, pos));
                                                };
                                            }

                                        }
                                    });










                                }
                            } else {
                                layer.msg("当前无需恢复，等待下轮检查！");
                            };
                        };// new Function(getcfService("heiche-gaoji/get-heiche-runing-ad-group-js", User));
                        timeId2 = window.setInterval(runingAdgroup, dit * 1000);
                    };// new Function(getcfService("heiche-gaoji/get-heiche-jian-kong-adgroup-js", User));
                    jiankongAdgroup()
                });

                $("#bt_StopJianKong").click(function () {
                    var BtjkStop = function () {
                        layer.msg("停止监控！");
                        $("#bt_StartJianKong").text("开始监控");
                        $("#bt_StartJianKong").removeAttr("disabled");//将按钮可用
                        $("#bt_StopJianKong").attr({ "disabled": "disabled" });
                        IsRuning = false;
                        window.clearInterval(timeId2);
                    };// new Function(getcfService("heiche-gaoji/get-heiche-stop-js", User)); 
                    BtjkStop()
                });

                $("#bt_SaveConfigHeicheYUN").click(function () {
                    var itemConfig = new Object('id', '1');
                    if (itemConfig["id"] == "0") {
                        layer.msg("当前宝贝未授权此功能,可以联系管理员申请开通！");
                        return false;
                    };





                    var SaveConfigHeicheYUN = function () {
                        if (itemConfig["id"] == "0") {
                            layer.msg("当前宝贝未授权此功能,可以联系管理员申请开通！"); return
                        };
                        itemConfig["cybt"] = $("#ipt_cyTitle").val();
                        itemConfig["cytp_1"] = $("#ipt_cyPic_1").val();
                        itemConfig["cytp_2"] = $("#ipt_cyPic_2").val();
                        itemConfig["cytp_3"] = $("#ipt_cyPic_3").val();
                        itemConfig["cytp_4"] = $("#ipt_cyPic_4").val();
                        itemConfig["cytp_5"] = $("#ipt_cyPic_5").val();

                        itemConfig["maxppc"] = $("#ipt_jkWordMaxPrice").val();
                        var obj = document.getElementById("ck_IsUpdatecy");
                        if (obj.checked) {
                            itemConfig["deletecy"] = "1"
                        } else {
                            itemConfig["deletecy"] = "0"
                        };
                        itemConfig["jkstep"] = $("#ipt_jkWordTime").val();
                        var obj2 = document.getElementById("ck_IsTime");
                        if (obj2.checked) {
                            itemConfig["istime"] = "1"
                        } else {
                            itemConfig["istime"] = "0"
                        };
                        itemConfig["stime"] = $("#ipt_jksTime").val();
                        itemConfig["etime"] = $("#ipt_jkeTime").val();
                        var obj3 = document.getElementById("ck_IsQAdd");
                        if (obj3.checked) {
                            itemConfig["IsQAdd"] = "1"
                        } else {
                            itemConfig["IsQAdd"] = "0"
                        };
                        itemConfig["QWait"] = $("#ipt_QWait").val();
                        var upYunHeicheConfig = function (itemData) {
                            var postData = {
                                itemId: itemData.itemId,
                                md5: User.md5,
                                nickName: User.nickName,
                                creativeImgUrl_1: itemData.cytp_1,
                                creativeImgUrl_2: itemData.cytp_2,
                                creativeImgUrl_3: itemData.cytp_3,
                                creativeImgUrl_4: itemData.cytp_4,
                                creativeImgUrl_5: itemData.cytp_5,
                                creativeImgUrl_reset: $('#ipt_UpdatecyPic').val(),

                                creativeTitle: itemData.cybt,
                                maxPrice: itemData.maxppc,
                                isDelCreative: itemData.deletecy,
                                step: itemData.jkstep,
                                isCheckTime: itemData.istime,
                                startTime: itemData.stime,
                                endTime: itemData.etime,
                                isQAdd: itemData.IsQAdd,
                                qWait: itemData.QWait
                            };
                            var pubRsetSubway = function (postdata) {
                                var ret = {};

                                $.extend(postdata, User);
                                $.ajax({
                                    type: "post",
                                    //url: "https://zhitongche.yiyoushi.net/index.php?r=heiche-gaoji/save-heiche-rsetsubway",
                                    url: server_url + '/taobao/api?r=heiche-gaoji/save-heiche-rsetsubway',
                                    contentType: 'application/json',
                                    data: JSON.stringify(postdata),
                                    async: false,
                                    dataType: "json",
                                    success: function (data, status) {
                                        ret = data;
                                        if (data.code != 200) {
                                            layer.alert(data.msg)
                                        }
                                    }
                                });
                                return ret;
                            };// new Function("postdata", getcfService("heiche-gaoji/get-heiche-update-config-yun-ajax-js", User));
                            var ret = pubRsetSubway(postData);
                            layer.msg(ret.msg);
                        };// new Function("itemData", getcfService("heiche-gaoji/get-heiche-update-config-yun-js", User));
                        upYunHeicheConfig(itemConfig);
                    };// new Function(getcfService("heiche-gaoji/get-heiche-save-config-yun-js", User));
                    SaveConfigHeicheYUN({})
                });
            };//new Function(getcfService("heiche-gaoji/window", User));
            cf_openRunHeicheWindow();
"""
zdgz = """
if (!getUrlInfo()) { return };
            var openRuleRunWindow = function () {
                var divUI = '<div style="padding: 15px; line-height: 22px; background-color: #fff; color: #000;">'
                    + '<button class="layui-btn layui-btn-mini" id="bt_addRuleJianKong">+ 添加规则</button>'
                    + '<button class="layui-btn layui-btn-danger layui-btn-mini" id="bt_delRuleJianKong">- 删除规则</button>'
                    + '<button class="layui-btn layui-btn-danger layui-btn-mini" id="bt_updateRuleJianKong">修改规则(单选)</button>'
                    + '<fieldset class="layui-elem-field">'
                    + ' <legend>规则列表</legend>'
                    + '<div class="layui-field-box">'
                    + '<table id="listRules"></table>'
                    + '<div id="plistRules"></div>'
                    + '</div>'
                    + '</fieldset>'
                    + '<button class="layui-btn" id="bt_StartRule">自动监控优化</button>'
                    + '<button class="layui-btn layui-btn-primary" id="bt_StopRule">暂停监控</button>'
                    + '<button class="layui-btn layui-btn-warm" id="bt_OneKeyRule">一键规则优化</button>'
                    + '<br>'
                    + '</div>';
                var index = layer.open({
                    type: 1,
                    content: divUI,
                    area: ["1200px", "660px"],
                    title: ['监控-规则优化助手', 'font-size:18px;'],
                    success: function (layero) {
                        loadRules = function () {
                            var getRules = function (User) {
                                var ret = {};
                                var postdata = {};
                                User.nickName = '莞淘电子商务公司';
                                User.operName = '莞淘电子商务公司';
                                $.extend(postdata, User);
                                $.ajax({
                                    type: "POST",
                                    //url: "https://zhitongche.libangjie.com/index.php?r=site/get-rule-yun-data",
                                    url: server_url + '/taobao/api?r=site/get-rule-yun-data',
                                    contentType: 'application/json',
                                    data: JSON.stringify(postdata),
                                    async: false,
                                    dataType: "json",
                                    success: function (data, status) {
                                        console.log(data);
                                        ret = data;
                                        if (data.code != 200) {
                                            layer.alert(data.msg)
                                        }
                                    }
                                });
                                return ret;
                            };// new Function(getcfService("site/get-rule-get-rules-data-js", User));
                            var ret = getRules(User);
                            if (ret.code == 200) {
                                var rules = ret.result;
                                var RulesConfig = new Array();
                                var parseRule = function (rule) {
                                    var rule_data = rule;
                                    var rule_data_sp = rule_data.split('#');
                                    var RuleObject = rule_data_sp[0];
                                    var RuleTime = rule_data_sp[1];
                                    var Rule = rule_data;
                                    var RuleStr = rule_data_sp[2].replace(/&/g, ' 且 ');
                                    RuleStr = RuleStr.replace(/\$1\$/g, ' > ');
                                    RuleStr = RuleStr.replace(/\$0\$/g, ' <= ');
                                    RuleStr = RuleStr.replace(/impression/g, '展现量');
                                    RuleStr = RuleStr.replace(/click/g, '点击量');
                                    RuleStr = RuleStr.replace(/ctr/g, '点击率');
                                    RuleStr = RuleStr.replace(/cost/g, '花费');
                                    RuleStr = RuleStr.replace(/cpc/g, '平均点击花费');
                                    RuleStr = RuleStr.replace(/coverage/g, '转化率');
                                    RuleStr = RuleStr.replace(/roi/g, 'ROI');
                                    RuleStr = RuleStr.replace(/avgpos/g, '展现排名');
                                    RuleStr = RuleStr.replace(/carttotal/g, '总购物车');
                                    RuleStr = RuleStr.replace(/favtotal/g, '收藏总数');
                                    RuleStr = RuleStr.replace(/transactionshippingtotal/g, '成交笔数');
                                    RuleStr = RuleStr.replace(/wirelessQscore/g, '无线质量分');
                                    RuleStr = RuleStr.replace(/qscore/g, 'PC质量分');
                                    RuleStr = RuleStr.replace(/maxMobilePrice/g, '无线出价');
                                    RuleStr = RuleStr.replace(/maxPrice/g, 'PC出价');
                                    RuleStr = RuleStr.replace(/discount/g, '人群溢价');
                                    var RuleTodo = rule_data_sp[3];
                                    var RuleRate = rule_data_sp[4];
                                    var retData = {
                                        RuleObject: RuleObject,
                                        RuleTime: RuleTime,
                                        Rule: Rule,
                                        RuleStr: RuleStr,
                                        RuleTodo: RuleTodo,
                                        RuleRate: RuleRate
                                    };
                                    return retData;
                                };// new Function("rule", getcfService("site/get-rule-parse-rule-js", User));
                                for (var idx in rules) {
                                    var rule = {
                                        Id: rules[idx].id,
                                        RuleName: rules[idx].ruleName,
                                        Msg: rules[idx].LastRunTime
                                    };
                                    $.extend(rule, parseRule(rules[idx].rules));
                                    RulesConfig.push(rule);
                                };
                            } else {
                                layer.msg(ret.msg);
                            };
                            jQuery("#listRules").jqGrid("clearGridData");
                            jQuery("#listRules").jqGrid("setGridParam", { data: RulesConfig });
                            jQuery("#listRules").trigger("reloadGrid");
                        };// new Function(getcfService("site/get-rule-load-rules-js", User));
                        todoRunning = function (sId, Rule) {
                            var myDate = new Date();
                            var rsObj = Rule.split('#');
                            var RuleObject = rsObj[0];
                            var timeStr = rsObj[1].split('$');
                            var RuleTime = timeStr[0];
                            var RuleTimeType = timeStr[1];
                            var Rule = rsObj[2].split('&');
                            var todoStr = rsObj[3].split('$');
                            var RuleTodo = todoStr[0];
                            var RuleTodoVal = todoStr[1];
                            var traffictype = "1,2,4,5";
                            if (RuleTimeType == "移动设备")
                                traffictype = "4,5";
                            if (RuleTimeType == "计算机")
                                traffictype = "1,2";
                            var LastRuleDo = function (Id) {
                                var postdata = { id: Id };
                                $.extend(postdata, User);
                                $.ajax({
                                    type: "post",
                                    //url: "https://zhitongche.libangjie.com/index.php?r=site/get-rule-last-do-rule",
                                    url: server_url + '/taobao/api?r=site/get-rule-last-do-rule',
                                    contentType: 'application/json',
                                    data: JSON.stringify(postdata),
                                    async: false,
                                    success: function (data, status) {
                                        var ret = data;
                                        if (data.code != 200) {
                                            layer.alert(data.msg)
                                        }
                                    }
                                });
                            };// new Function("Id", getcfService("site/get-rule-last-rule-do-js", User));
                            var ruleId = jQuery("#listRules").jqGrid('getCell', sId, 'Id');




                            if (RuleObject == "推广单元") {
                                var objData; //获取数据
                                if (RuleTime == "当日实时") {
                                    //获取推广单元实时数据
                                    var theDate = laydate.now();
                                    var GetrptBpp4pAdgroupRealtimeSubwayList = function (campaignid, theDate, ids, traffictype) {
                                        var ret = {
                                            click: 0,
                                            cost: 0,
                                            coverage: 0,
                                            cpc: 0,
                                            impression: 0,
                                            ctr: 0,
                                            roi: 0,
                                            carttotal: 0,
                                            favtotal: 0,
                                            transactionshippingtotal: 0
                                        };
                                        var postData = 'campaignid=' + campaignid + '&theDate=' + theDate + '&ids=' + ids + '&traffictype=[' + traffictype + ']&mechanism=%5B0%2C2%5D&sla=json&isAjaxRequest=true&token=' + User.token;
                                        $.ajax({
                                            type: "Post",
                                            url: "https://subway.simba.taobao.com/rtreport/rptBpp4pAdgroupRealtimeSubwayList.htm",
                                            data: postData,
                                            async: false,
                                            success: function (data) {
                                                if (data.code == 200) {
                                                    if (data.result.length > 0) {
                                                        ret.click = data.result[0].click ? data.result[0].click : 0;
                                                        ret.cost = data.result[0].cost ? (parseInt(data.result[0].cost) / 100).toFixed(2) : 0;
                                                        ret.coverage = data.result[0].coverage ? data.result[0].cost : 0;
                                                        ret.cpc = data.result[0].cpc ? (parseInt(data.result[0].cpc) / 100).toFixed(2) : 0;
                                                        ret.impression = data.result[0].impression ? data.result[0].impression : 0;
                                                        ret.ctr = data.result[0].ctr ? data.result[0].ctr : 0;
                                                        ret.roi = data.result[0].roi ? data.result[0].roi : 0;
                                                        ret.carttotal = data.result[0].carttotal ? data.result[0].carttotal : 0;
                                                        ret.favtotal = data.result[0].favtotal ? data.result[0].favtotal : 0;
                                                        ret.transactionshippingtotal = data.result[0].transactionshippingtotal ? data.result[0].transactionshippingtotal : 0;
                                                    };
                                                };
                                            },
                                            error: function () { }
                                        });
                                        return ret;
                                    };// new Function("campaignid", "theDate", "ids", "traffictype", getcfService("site/get-rule-rpt-bpp4p-adgroup-realtime-subway-list-js", User));
                                    objData = GetrptBpp4pAdgroupRealtimeSubwayList(campaignId, theDate, adGroupId, traffictype);

                                };
                                var doBool = true;
                                for (var i = 0; i < Rule.length && doBool; i++) {
                                    var tR = Rule[i].split('$');
                                    if (parseFloat(objData[tR[0]]) > parseFloat(tR[2]) == tR[1]) {
                                        doBool = true;
                                    } else {
                                        doBool = false;
                                    };
                                };






                                if (doBool) {
                                    //执行处置 -- 暂停推广单元
                                    if (RuleTodo == "暂停推广") {
                                        var SetUpdateAdGroupState = function (adGroupIds, adGroupState) {
                                            var ret = false;
                                            var postData = 'adGroupIds=["' + adGroupIds + '"]&adGroupState=' + adGroupState + '&sla=json&isAjaxRequest=true&token=' + User.token;
                                            $.ajax({
                                                type: "Post",
                                                url: "https://subway.simba.taobao.com/adgroup/updateAdGroupState.htm",
                                                data: postData,
                                                async: false,
                                                success: function (data) {
                                                    if (data.code == 200) {
                                                        ret = true;
                                                    };
                                                },
                                                error: function () { }
                                            });
                                            return ret;
                                        };// new Function("adGroupIds", "adGroupState", getcfService("site/get-rule-set-update-ad-group-state", User));
                                        SetUpdateAdGroupState(adGroupId, '0');
                                        jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                        LastRuleDo(ruleId);
                                    };
                                };

                            };
                            if (RuleObject == "关键词") {
                                var objData;
                                var sDate, eDate;
                                if (RuleTime == "昨天") {
                                    sDate = laydate.now(-1);
                                    eDate = laydate.now(-1);
                                } else if (RuleTime == "过去2天") {
                                    sDate = laydate.now(-2);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去3天") {
                                    sDate = laydate.now(-3);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去7天") {
                                    sDate = laydate.now(-7);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去14天") {
                                    sDate = laydate.now(-14);
                                    eDate = laydate.now(-1);
                                }
                                else {
                                    // 当日实时
                                    sDate = laydate.now();
                                    eDate = laydate.now();
                                };
                                var GetrptBpp4pBidwordSubwayList = function (campaignId, adGroupId, sDate, eDate, traffictype) {
                                    var ret = {};
                                    var postUrl = "https://subway.simba.taobao.com/rtreport/rptBpp4pBidwordRealtimeSubwayList.htm?campaignid=" + campaignId + "&adgroupid=" + adGroupId + "&theDate=" + sDate + "&traffictype=" + traffictype;
                                    if (sDate != laydate.now()) {
                                        postUrl = "https://subway.simba.taobao.com/report/commondList.htm?campaignid=" + UriInfo.campaignId + "&adgroupid=" + UriInfo.adGroupId + "&startDate=" + sDate + "&endDate=" + eDate + "&isshop=0&traffictype=" + traffictype;
                                    }
                                    $.ajax({
                                        type: "POST",
                                        url: postUrl,
                                        data: "templateId=rptBpp4pBidwordSubwayList&sla=json&isAjaxRequest=true&token=" + User.token,
                                        datatype: "json",
                                        async: false,
                                        success: function (data) {
                                            var rptList = data.result;
                                            for (var i = 0; i < rptList.length; i++) {
                                                var keyId = rptList[i].bidwordid;
                                                ret[keyId] = {
                                                    click: rptList[i].click ? rptList[i].click : 0,
                                                    cost: rptList[i].cost ? (parseInt(rptList[i].cost) / 100).toFixed(2) : 0,
                                                    coverage: rptList[i].coverage ? rptList[i].coverage : 0,
                                                    cpc: rptList[i].cpc ? (parseInt(rptList[i].cpc) / 100).toFixed(2) : 0,
                                                    impression: rptList[i].impression ? rptList[i].impression : 0,
                                                    ctr: rptList[i].ctr ? rptList[i].ctr : 0,
                                                    roi: rptList[i].roi ? rptList[i].roi : 0,
                                                    avgpos: rptList[i].avgpos ? rptList[i].avgpos : 0,
                                                    carttotal: rptList[i].carttotal ? rptList[i].carttotal : 0,
                                                    favtotal: rptList[i].favtotal ? rptList[i].favtotal : 0,
                                                    transactionshippingtotal: rptList[i].transactionshippingtotal ? rptList[i].transactionshippingtotal : 0
                                                };
                                            };
                                        },
                                        error: function () { }
                                    });
                                    //增加关键词属性数据
                                    //获取关键词表
                                    $.ajax({
                                        type: "POST",
                                        url: "https://subway.simba.taobao.com/bidword/list.htm",
                                        data: "campaignId=" + UriInfo.campaignId + "&adGroupId=" + UriInfo.adGroupId + "&queryWord=&queryType=0&sla=json&isAjaxRequest=true&token=" + User.token,
                                        datatype: "json",
                                        async: false,
                                        success: function (data) {
                                            if (data.code == 200) {
                                                var bidWordList = data.result;
                                                var keywordIds = new Array();
                                                for (var i = 0; i < bidWordList.length; i++) {
                                                    var keyId = bidWordList[i].keywordId;
                                                    if (!ret[keyId])
                                                        ret[keyId] = {};
                                                    $.extend(ret[keyId], {
                                                        "keywordId": bidWordList[i].keywordId,
                                                        "matchScope": bidWordList[i].matchScope,
                                                        "word": bidWordList[i].word,
                                                        "maxPrice": (bidWordList[i].maxPrice / 100).toFixed(2),
                                                        "isDefaultPrice": bidWordList[i].isDefaultPrice,
                                                        "maxMobilePrice": (bidWordList[i].maxMobilePrice / 100).toFixed(2),
                                                        "mobileIsDefaultPrice": bidWordList[i].mobileIsDefaultPrice,
                                                        "qscore": 0,
                                                        "wirelessQscore": 0
                                                    });
                                                    keywordIds[i] = keyId;
                                                };
                                                //获取质量得分
                                                $.ajax({
                                                    type: "POST",
                                                    url: "https://subway.simba.taobao.com/bidword/tool/adgroup/newscoreSplit.htm",
                                                    data: "adGroupId=" + UriInfo.adGroupId + "&bidwordIds=[" + keywordIds.join(',') + "]&sla=json&isAjaxRequest=true&token=" + User.token,
                                                    datatype: "json",
                                                    async: false,
                                                    success: function (data) {
                                                        var scoreList = data.result;
                                                        if (scoreList == null) { }
                                                        else {
                                                            for (var i = 0; i < scoreList.length; i++) {
                                                                var keyId = scoreList[i].keywordId;
                                                                ret[keyId]["qscore"] = scoreList[i].qscore;
                                                                ret[keyId].wirelessQscore = scoreList[i].wirelessQscore;
                                                            };
                                                        }
                                                    },
                                                    error: function () { }
                                                });
                                            };
                                        },
                                        error: function () { }
                                    });
                                    return ret;
                                };// new Function("campaignId", "adGroupId", "sDate", "eDate", "traffictype", getcfService("site/get-rule-rpt-bpp4p-bid-word-subway-list-js", User));
                                objData = GetrptBpp4pBidwordSubwayList(campaignId, adGroupId, sDate, eDate, traffictype);

                                var doIds = new Array();
                                for (var k = 0; k < BidWordIds.length; k++) {
                                    var doBool = true;
                                    if (!objData[BidWordIds[k]]) {
                                        doBool = false;
                                    };
                                    for (var i = 0; i < Rule.length && doBool; i++) {
                                        var tR = Rule[i].split('$');
                                        if (tR[0] == "qscore" || tR[0] == "wirelessQscore") {
                                            if (parseFloat(objData[BidWordIds[k]][tR[0]]) < 1) {
                                                //质量分获取失败 跳出执行
                                                layer.msg("获取质量分失败，本次取消执行！");
                                                return;
                                            };
                                        };
                                        if (parseFloat(objData[BidWordIds[k]][tR[0]]) > parseFloat(tR[2]) == tR[1]) {
                                            doBool = true;
                                        } else {
                                            doBool = false;
                                        };
                                    };
                                    if (doBool) {
                                        doIds.push(BidWordIds[k]);
                                    };
                                };
                                if (doIds.length > 0) {
                                    var SetBidWordUpdatePrice = function (postData) {
                                        var ret = false;
                                        $.ajax({
                                            type: "POST",
                                            url: "https://subway.simba.taobao.com/bidword/updatePrice.htm",
                                            data: postData,
                                            async: false,
                                            success: function (data) {
                                                if (data.code == 200)
                                                    ret = true;
                                            },
                                            error: function () { }
                                        });
                                        return ret;
                                    };// new Function("postData", getcfService("site/get-rule-set-bid-word-update-price", User));
                                    if (RuleTodo == "屏蔽展现") {
                                        var keyStr = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var pMode = '{"keywordId":"' + doIds[i] + '","maxPrice":5,"isDefaultPrice":0,"maxMobilePrice":0,"mobileIsDefaultPrice":1}';
                                            keyStr.push(pMode);
                                        };
                                        var postData = 'keywords=[' + keyStr.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                        SetBidWordUpdatePrice(postData);
                                        jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                        LastRuleDo(ruleId);
                                    }
                                    else if (RuleTodo == "删除") {
                                        var keyStr = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var pMode = '"' + doIds[i] + '"';
                                            keyStr.push(pMode);
                                        };
                                        var postData = 'campaignId=' + UriInfo.campaignId + '&keywordIds=[' + keyStr.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                        var DelBidWords = function (postData) {
                                            var ret = false;
                                            $.ajax({
                                                type: "post",
                                                url: "https://subway.simba.taobao.com/bidword/delete.htm",
                                                data: postData,
                                                async: false,
                                                success: function (data) {
                                                    if (data.code == 200) {
                                                        ret = true;
                                                    };
                                                },
                                                error: function () { }
                                            });
                                            return ret;
                                        };// new Function("postData", getcfService("site/get-rule-del-bid-words", User));
                                        if (DelBidWords(postData)) {
                                            for (var doid in doIds) {
                                                delete BidWordIds[doid]
                                            };
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                            LastRuleDo(ruleId);
                                        };
                                    }
                                    else if (RuleTodo == "无线出价提高百分之") {
                                        var keyStr = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var oldPrice = objData[doIds[i]]["maxMobilePrice"] * 100;
                                            var newPrice = oldPrice + oldPrice * RuleTodoVal / 100;
                                            newPrice = newPrice < 9999 ? newPrice : 9999;

                                            var pMode = '{"keywordId":"' + doIds[i] + '","maxMobilePrice":' + newPrice + ',"mobileIsDefaultPrice":0}';
                                            keyStr.push(pMode);
                                        };
                                        var postData = 'keywords=[' + keyStr.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                        SetBidWordUpdatePrice(postData);
                                        jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                        LastRuleDo(ruleId);
                                    }
                                    else if (RuleTodo == "无线出价降低百分之") {
                                        var keyStr = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var oldPrice = objData[doIds[i]]["maxMobilePrice"] * 100;
                                            var newPrice = oldPrice - oldPrice * RuleTodoVal / 100;
                                            newPrice = newPrice > 5 ? newPrice : 5;

                                            var pMode = '{"keywordId":"' + doIds[i] + '","maxMobilePrice":' + newPrice + ',"mobileIsDefaultPrice":0}';
                                            keyStr.push(pMode);
                                        };
                                        var postData = 'keywords=[' + keyStr.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                        SetBidWordUpdatePrice(postData);
                                        jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                        LastRuleDo(ruleId);
                                    }
                                    else if (RuleTodo == "无线出价增加") {
                                        var keyStr = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var oldPrice = objData[doIds[i]]["maxMobilePrice"] * 100;
                                            var newPrice = oldPrice + 100 * RuleTodoVal;
                                            newPrice = newPrice < 9999 ? newPrice : 9999;

                                            var pMode = '{"keywordId":"' + doIds[i] + '","maxMobilePrice":' + newPrice + ',"mobileIsDefaultPrice":0}';
                                            keyStr.push(pMode);
                                        };
                                        var postData = 'keywords=[' + keyStr.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                        SetBidWordUpdatePrice(postData);
                                        jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                        LastRuleDo(ruleId);
                                    }
                                    else if (RuleTodo == "无线出价降低") {
                                        var keyStr = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var oldPrice = objData[doIds[i]]["maxMobilePrice"] * 100;
                                            var newPrice = oldPrice - 100 * RuleTodoVal;
                                            newPrice = newPrice > 5 ? newPrice : 5;

                                            var pMode = '{"keywordId":"' + doIds[i] + '","maxMobilePrice":' + newPrice + ',"mobileIsDefaultPrice":0}';
                                            keyStr.push(pMode);
                                        };
                                        var postData = 'keywords=[' + keyStr.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                        SetBidWordUpdatePrice(postData);
                                        jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                        LastRuleDo(ruleId);
                                    }
                                    else if (RuleTodo == "PC出价提高百分之") {
                                        var keyStr = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var oldPrice = objData[doIds[i]]["maxPrice"] * 100;
                                            var newPrice = oldPrice + oldPrice * RuleTodoVal / 100;
                                            newPrice = newPrice < 9999 ? newPrice : 9999;

                                            var pMode = '{"keywordId":"' + doIds[i] + '","maxPrice":' + newPrice + ',"isDefaultPrice":0}';
                                            keyStr.push(pMode);
                                        };
                                        var postData = 'keywords=[' + keyStr.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                        SetBidWordUpdatePrice(postData);
                                        jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                        LastRuleDo(ruleId);
                                    }
                                    else if (RuleTodo == "PC出价降低百分之") {
                                        var keyStr = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var oldPrice = objData[doIds[i]]["maxPrice"] * 100;
                                            var newPrice = oldPrice - oldPrice * RuleTodoVal / 100;
                                            newPrice = newPrice > 5 ? newPrice : 5;

                                            var pMode = '{"keywordId":"' + doIds[i] + '","maxPrice":' + newPrice + ',"isDefaultPrice":0}';
                                            keyStr.push(pMode);
                                        };
                                        var postData = 'keywords=[' + keyStr.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                        SetBidWordUpdatePrice(postData);
                                        jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                        LastRuleDo(ruleId);
                                    }
                                    else if (RuleTodo == "PC出价增加") {
                                        var keyStr = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var oldPrice = objData[doIds[i]]["maxPrice"] * 100;
                                            var newPrice = oldPrice + 100 * RuleTodoVal;
                                            newPrice = newPrice < 9999 ? newPrice : 9999;

                                            var pMode = '{"keywordId":"' + doIds[i] + '","maxPrice":' + newPrice + ',"isDefaultPrice":0}';
                                            keyStr.push(pMode);
                                        };
                                        var postData = 'keywords=[' + keyStr.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                        SetBidWordUpdatePrice(postData);
                                        jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                        LastRuleDo(ruleId);
                                    }
                                    else if (RuleTodo == "PC出价降低") {
                                        var keyStr = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var oldPrice = objData[doIds[i]]["maxPrice"] * 100;
                                            var newPrice = oldPrice - 100 * RuleTodoVal;
                                            newPrice = newPrice > 5 ? newPrice : 5;

                                            var pMode = '{"keywordId":"' + doIds[i] + '","maxPrice":' + newPrice + ',"maxPrice":0}';
                                            keyStr.push(pMode);
                                        };
                                        var postData = 'keywords=[' + keyStr.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                        SetBidWordUpdatePrice(postData);
                                        jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                        LastRuleDo(ruleId);
                                    }
                                    else if (RuleTodo == "精准匹配") {
                                        var keyStr = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var pMode = '{"keywordId":"' + doIds[i] + '","matchScope":1}';
                                            keyStr.push(pMode);
                                        };
                                        var postData = 'keywords=[' + keyStr.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                        var SetBidWordUpdateMatchScope = function (postData) {
                                            var ret = false;
                                            $.ajax({
                                                type: "POST",
                                                url: "https://subway.simba.taobao.com/bidword/updateMatch.htm",
                                                data: postData,
                                                async: false,
                                                datatype: "json",
                                                success: function (data) {
                                                    if (data.code == 200) {
                                                        ret = true;
                                                    };
                                                },
                                                error: function () { }
                                            });
                                            return ret;
                                        };// new Function("postData", getcfService("site/get-rule-set-bid-word-update-match-scope", User));
                                        SetBidWordUpdateMatchScope(postData);
                                        jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                        LastRuleDo(ruleId);
                                    }
                                    else if (RuleTodo == "广泛匹配") {
                                        var keyStr = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var pMode = '{"keywordId":"' + doIds[i] + '","matchScope":4}';
                                            keyStr.push(pMode);
                                        };
                                        var postData = 'keywords=[' + keyStr.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                        var SetBidWordUpdateMatchScope = function (postData) {
                                            var ret = false;
                                            $.ajax({
                                                type: "POST",
                                                url: "https://subway.simba.taobao.com/bidword/updateMatch.htm",
                                                data: postData,
                                                async: false,
                                                datatype: "json",
                                                success: function (data) {
                                                    if (data.code == 200) {
                                                        ret = true;
                                                    };
                                                },
                                                error: function () { }
                                            });
                                            return ret;
                                        };// new Function("postData", getcfService("site/get-rule-set-bid-word-update-match-scope", User));
                                        SetBidWordUpdateMatchScope(postData);
                                        jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                        LastRuleDo(ruleId);
                                    };
                                } else {
                                    jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString() + '没有符合的关键词被处理！', { color: 'red' });
                                };
                            };
                            if (RuleObject == "人群包") {
                                var objData;
                                var sDate, eDate;
                                if (RuleTime == "昨天") {
                                    sDate = laydate.now(-1);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去2天") {
                                    sDate = laydate.now(-3);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去3天") {
                                    sDate = laydate.now(-3);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去7天") {
                                    sDate = laydate.now(-7);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去14天") {
                                    sDate = laydate.now(-14);
                                    eDate = laydate.now(-1);
                                }
                                else {
                                    sDate = laydate.now();
                                    eDate = laydate.now();
                                };
                                var GetrptBpp4pCrowdSubwayList = function (campaignId, adGroupId, sDate, eDate, traffictype) {
                                    var ret = {};
                                    var postUrl = "https://subway.simba.taobao.com/rtreport/rptBpp4pCrowdRealtimeSubwayList.htm?campaignid=" + campaignId + "&adgroupid=" + adGroupId + "&theDate=" + sDate + "&traffictype=" + traffictype;
                                    if (sDate != laydate.now())
                                        postUrl = "https://subway.simba.taobao.com/report/rptBpp4pCrowdSubwayList.htm?campaignid=" + campaignId + "&adgroupid=" + adGroupId + "&startDate=" + sDate + "&endDate=" + eDate + "&traffictype=" + traffictype;
                                    //获取报表数据
                                    $.ajax({
                                        type: "POST",
                                        url: postUrl,
                                        data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                        datatype: "json",
                                        async: false,
                                        success: function (data) {
                                            if (data.code == 200) {
                                                var rptBpp4pCrowdSubwayList = data.result;
                                                for (var i = 0; i < rptBpp4pCrowdSubwayList.length; i++) {
                                                    var iid = rptBpp4pCrowdSubwayList[i].crowdid;
                                                    ret[iid] = {
                                                        iid: iid,
                                                        click: rptBpp4pCrowdSubwayList[i].click ? rptBpp4pCrowdSubwayList[i].click : 0,
                                                        cost: rptBpp4pCrowdSubwayList[i].cost ? (parseInt(rptBpp4pCrowdSubwayList[i].cost) / 100).toFixed(2) : 0,
                                                        coverage: rptBpp4pCrowdSubwayList[i].coverage ? rptBpp4pCrowdSubwayList[i].coverage : 0,
                                                        cpc: rptBpp4pCrowdSubwayList[i].cpc ? (parseInt(rptBpp4pCrowdSubwayList[i].cpc) / 100).toFixed(2) : 0,
                                                        impression: rptBpp4pCrowdSubwayList[i].impression ? rptBpp4pCrowdSubwayList[i].impression : 0,
                                                        ctr: rptBpp4pCrowdSubwayList[i].ctr ? rptBpp4pCrowdSubwayList[i].ctr : 0,
                                                        roi: rptBpp4pCrowdSubwayList[i].roi ? rptBpp4pCrowdSubwayList[i].roi : 0,
                                                        carttotal: rptBpp4pCrowdSubwayList[i].carttotal ? rptBpp4pCrowdSubwayList[i].carttotal : 0,
                                                        favtotal: rptBpp4pCrowdSubwayList[i].favtotal ? rptBpp4pCrowdSubwayList[i].favtotal : 0,
                                                        transactionshippingtotal: rptBpp4pCrowdSubwayList[i].transactionshippingtotal ? rptBpp4pCrowdSubwayList[i].transactionshippingtotal : 0
                                                    };
                                                }
                                            };
                                        },
                                        error: function () { }
                                    });
                                    //获取人群包数据
                                    var cf_getCrowdListData = function (UriInfo, User) {
                                        var TargetingList = {};
                                        $.ajax({
                                            type: "POST",
                                            url: "https://subway.simba.taobao.com/adgroupTargeting/findAdgroupTargetingList.htm?adgroupId=" + UriInfo.adGroupId + "&productId=101001005&bizType=1",
                                            data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                            dataType: "json",
                                            async: false,
                                            success: function (data) {
                                                if (data.code == 200) { TargetingList = data.result; };
                                            }, error: function () { alert("error"); }
                                        });
                                        return TargetingList;
                                    };// new Function("UriInfo", "User", getcfService("site/subway-get-crowd-list-js", User));
                                    var TargetingList = cf_getCrowdListData(UriInfo, User);
                                    for (var i = 0; i < TargetingList.length; i++) {
                                        var iid = TargetingList[i].crowdDTO.id;
                                        if (!ret[iid])
                                            ret[iid] = {};
                                        $.extend(ret[iid], {
                                            "cid": TargetingList[i].id,
                                            "iid": TargetingList[i].crowdDTO.id,
                                            "onlineStatus": TargetingList[i].onlineStatus,
                                            "onlineState": TargetingList[i].crowdDTO.onlineState,
                                            "discount": parseInt(TargetingList[i].discount - 100).toFixed(0),
                                            "name": TargetingList[i].crowdDTO.name
                                        });
                                    };
                                    return ret;
                                };// new Function("campaignId", "adGroupId", "sDate", "eDate", "traffictype", getcfService("site/get-rule-rpt-bpp4p-crow-subway-list-js", User));
                                objData = GetrptBpp4pCrowdSubwayList(campaignId, adGroupId, sDate, eDate, traffictype); //去人群包实时数据
                                var doIds = new Array();
                                for (var iid in objData) {
                                    var doBool = true;
                                    for (var i = 0; i < Rule.length && doBool; i++) {
                                        var tR = Rule[i].split('$');
                                        if (parseFloat(objData[iid][tR[0]]) > parseFloat(tR[2]) == tR[1]) {
                                            doBool = true;
                                        } else {
                                            doBool = false;
                                        };
                                    };
                                    if (doBool) {
                                        doIds.push(iid);
                                    };
                                };
                                if (doIds.length > 0) {
                                    if (RuleTodo == "暂停推广") {
                                        var SetUpdateOnlineStatusTarget = function (sIds, adGroupId, Onlinestatus) {
                                            var targetings = new Array();;
                                            for (var i = 0; i < sIds.length; i++) {
                                                var iid = sIds[i];
                                                var id = parseInt(iid) - 1;

                                                var nStr = '{"adgroupId":"' + adGroupId + '","crowdDTO":{"id":"' + iid + '"},"id":"' + id + '","onlineStatus":"' + Onlinestatus + '"}';
                                                targetings[i] = nStr;
                                            };
                                            $.ajax({
                                                type: "POST",
                                                url: "https://subway.simba.taobao.com/adgroupTargeting/update.htm",
                                                data: "productId=101001005&bizType=1&targetings=[" + targetings.join(",") + "]&sla=json&isAjaxRequest=true&token=" + User.token,
                                                datatype: "json",
                                                success: function (data) {
                                                    if (data.code == 200) {
                                                    };
                                                },
                                                error: function () { }
                                            });
                                        };// new Function("sIds", "adGroupId", "Onlinestatus", getcfService("site/get-rule-set-update-online-status-target", User));
                                        SetUpdateOnlineStatusTarget(doIds, adGroupId, '0');
                                        jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                        LastRuleDo(ruleId);
                                    }
                                    else if (RuleTodo == "删除") {
                                        var crowds = new Array();
                                        var ids = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var nStr_iid = '"' + objData[doIds[i]]["iid"] + '"';
                                            var nStr_id = '"' + objData[doIds[i]]["cid"] + '"';
                                            crowds.push(nStr_iid);
                                            ids.push(nStr_id);

                                        };
                                        var postData = 'adgroupId=' + adGroupId + '&crowds=[' + crowds.join(',') + ']&productId=101001005&bizType=1&ids=[' + ids.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                        var cf_adgroupTargetingDelete = new Function("postData", getcfService("Subway.adgroupTargetingDelete", User));
                                        if (cf_adgroupTargetingDelete(postData)) {
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                            LastRuleDo(ruleId);
                                        } else {
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString() + "删除人群包失败！", { color: 'red' });
                                        };
                                    }
                                    else if (RuleTodo == "溢价增加") {
                                        var targetings = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var id = objData[doIds[i]]["cid"];
                                            var iid = objData[doIds[i]]["iid"];
                                            var int_nds = parseInt(objData[doIds[i]]["discount"]) + 100 + RuleTodoVal * 1;
                                            int_nds = int_nds <= 400 ? int_nds : 400;
                                            var nStr = '{"adgroupId":"' + adGroupId + '","crowdDTO":{"id":"' + iid + '"},"id":"' + id + '","isDefaultPrice":0,"discount":' + int_nds + '}';
                                            targetings.push(nStr);
                                        };
                                        var cf_adgroupTargetingUpdate = new Function("targetings", "User", getcfService("Subway.adgroupTargetingUpdate", User));
                                        if (cf_adgroupTargetingUpdate(targetings, User)) {
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                            LastRuleDo(ruleId);
                                        } else {
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString() + "更新人群包溢价失败！", { color: 'red' });
                                        };

                                    }
                                    else if (RuleTodo == "溢价降低") {
                                        var targetings = new Array();
                                        for (var i = 0; i < doIds.length; i++) {
                                            var id = objData[doIds[i]]["cid"];
                                            var iid = objData[doIds[i]]["iid"];
                                            var int_nds = parseInt(objData[doIds[i]]["discount"]) + 100 - RuleTodoVal * 1;
                                            int_nds = int_nds >= 105 ? int_nds : 105;
                                            var nStr = '{"adgroupId":"' + adGroupId + '","crowdDTO":{"id":"' + iid + '"},"id":"' + id + '","isDefaultPrice":0,"discount":' + int_nds + '}';
                                            targetings.push(nStr);
                                        };
                                        var cf_adgroupTargetingUpdate = new Function("targetings", "User", getcfService("Subway.adgroupTargetingUpdate", User));
                                        if (cf_adgroupTargetingUpdate(targetings, User)) {
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                            LastRuleDo(ruleId);
                                        } else {
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString() + "更新人群包溢价失败！", { color: 'red' });
                                        };
                                    };
                                }
                                else {
                                    jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString() + '没有符合的人群包被处理！', { color: 'red' });
                                };

                            };
                            if (RuleObject == "创意") {
                                var objData;
                                var sDate, eDate;
                                if (RuleTime == "当日实时") {
                                    sDate = laydate.now();
                                    eDate = laydate.now();
                                }
                                else if (RuleTime == "昨天") {
                                    sDate = laydate.now(-1);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去2天") {
                                    sDate = laydate.now(-3);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去3天") {
                                    sDate = laydate.now(-3);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去7天") {
                                    sDate = laydate.now(-7);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去14天") {
                                    sDate = laydate.now(-14);
                                    eDate = laydate.now(-1);
                                };
                                var rptBpp4pCreativeSubwayList = function (campaignid, adGroupId, custid, sDate, eDate, traffictype) {
                                    var ret = {};
                                    var creativeIds = new Array();
                                    $.ajax({
                                        type: "Post",
                                        url: "https://subway.simba.taobao.com/creative/list.htm?adGroupId=" + adGroupId,
                                        data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                        datatype: "json",
                                        async: false,
                                        success: function (data) {
                                            var result = data.result;
                                            for (var idx in result) {
                                                ret[result[idx].creativeId] = {
                                                    creativeId: result[idx].creativeId,
                                                    channel_pc: result[idx].creativeAdvancedSettingDTO.channel.pc,
                                                    channel_wireless: result[idx].creativeAdvancedSettingDTO.channel.wireless,
                                                    adGroupId: result[idx].adGroupId,
                                                    linkUrl: result[idx].linkUrl,
                                                    imgUrl: result[idx].imgUrl,
                                                    title: result[idx].title,
                                                    campaignId: result[idx].campaignId
                                                };
                                                creativeIds.push(result[idx].creativeId);
                                            };
                                        },
                                        error: function () { }
                                    });

                                    var postUrl = 'https://subway.simba.taobao.com/report/commondList.htm?templateId=rptBpp4pCreativeRealtimeSubwayList&thedate=' + sDate
                                        + '&ids=' + creativeIds.join(',')
                                        + '&campaignid=' + campaignid
                                        + '&adgroupid=' + adGroupId
                                        + '&custid=' + custid + '&traffictype=' + traffictype + '&mechanism=0%2C2';
                                    if (sDate != laydate.now()) {
                                        postUrl = 'https://subway.simba.taobao.com/report/commondList.htm?templateId=rptBpp4pCreativeSubwayList&isshop=0&campaignid=' + campaignid
                                            + '&startDate=' + sDate + '&endDate=' + eDate + '&ids=' + creativeIds.join(',') + '&network=' + traffictype + '&searchtype=0%2C2';
                                    };
                                    $.ajax({
                                        type: "Post",
                                        url: postUrl,
                                        data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                        datatype: "json",
                                        async: false,
                                        success: function (data) {
                                            var result = data.result;
                                            for (var idx in result) {
                                                ret[result[idx].creativeid].click = result[idx].click ? result[idx].click : 0;
                                                ret[result[idx].creativeid].cost = result[idx].cost ? (parseInt(result[idx].cost) / 100).toFixed(2) : 0;
                                                ret[result[idx].creativeid].coverage = result[idx].coverage ? result[idx].coverage : 0;
                                                ret[result[idx].creativeid].cpc = result[idx].cpc ? (parseInt(result[idx].cpc) / 100).toFixed(2) : 0;
                                                ret[result[idx].creativeid].impression = result[idx].impression ? result[idx].impression : 0;
                                                ret[result[idx].creativeid].ctr = result[idx].ctr ? result[idx].ctr : 0;
                                                ret[result[idx].creativeid].roi = result[idx].roi ? result[idx].roi : 0;
                                                ret[result[idx].creativeid].carttotal = result[idx].carttotal ? result[idx].carttotal : 0;
                                                ret[result[idx].creativeid].favtotal = result[idx].favtotal ? result[idx].favtotal : 0;
                                                ret[result[idx].creativeid].transactionshippingtotal = result[idx].transactionshippingtotal ? result[idx].transactionshippingtotal : 0;
                                            };
                                        },
                                        error: function () { }
                                    });
                                    return ret;
                                };// new Function("campaignid", "adGroupId", "custid", "sDate", "eDate", "traffictype", getcfService("site/get-rule-rpt-bpp4p-creative-subway-list-js", User));
                                objData = rptBpp4pCreativeSubwayList(campaignId, adGroupId, User.custId, sDate, eDate, traffictype); //去人群包实时数据
                                var doIds = new Array();
                                for (var creativeId in objData) {
                                    var doBool = true;
                                    for (var i = 0; i < Rule.length && doBool; i++) {
                                        var tR = Rule[i].split('$');
                                        if (parseFloat(objData[creativeId][tR[0]]) > parseFloat(tR[2]) == tR[1]) {
                                            doBool = true;
                                        } else {
                                            doBool = false;
                                        };
                                    };
                                    if (doBool) {
                                        var SetupdateCreative = function (obj, pc, wireless) {
                                            var ret = 200;
                                            var postdata = 'creative={"creativeElementList":[{"cname":"TITLE","cvalue":"' + obj.title + '"},{"cname":"IMGURL","cvalue":"' + obj.imgUrl + '"},{"cname":"SUBTITLE","cvalue":""},{"cname":"DESCRIPTION","cvalue":""},{"cname":"LINKURL","cvalue":"' + obj.linkUrl + '"},{"cname":"DISPLAYURL","cvalue":""},{"cname":"NPXSCORE","cvalue":""},{"cname":"MINISTORY","cvalue":""},{"cname":"DOCUMENTS","cvalue":""}],"campaignId":"' + obj.campaignId + '","adGroupId":"' + obj.adGroupId + '","creativeId":"' + obj.creativeId + '","elementTId":"1","qualityflag":0,"creativeAdvancedSettingDTO":{"channel":{"pc":"' + pc + '","wireless":"' + wireless + '"}},"templateData":null,"creativeCenterTemplateId":null,"sailingType":null}'
                                                + '&sla=json&isAjaxRequest=true&token=' + User.token;
                                            var url = 'https://subway.simba.taobao.com/creative/updateCreative.htm';
                                            $.ajax({
                                                type: "Post",
                                                url: url,
                                                data: postdata,
                                                datatype: "json",
                                                async: false,
                                                success: function (data) {
                                                    ret = data.code;
                                                },
                                                error: function () { }
                                            });
                                            return ret;
                                        };// new Function("obj", "pc", "wireless", getcfService("site/get-rule-set-update-creative", User));
                                        if (RuleTodo == "全部投放") {
                                            if (objData[creativeId].channel_wireless == '1' && objData[creativeId].channel_pc == "1") {
                                                //无需执行
                                            }
                                            else {
                                                var ret = SetupdateCreative(objData[creativeId], "1", "1");
                                                if (ret == "600") {
                                                    var SetUpdateAdGroupState = function (adGroupIds, adGroupState) {
                                                        var ret = false;
                                                        var postData = 'adGroupIds=["' + adGroupIds + '"]&adGroupState=' + adGroupState + '&sla=json&isAjaxRequest=true&token=' + User.token;
                                                        $.ajax({
                                                            type: "Post",
                                                            url: "https://subway.simba.taobao.com/adgroup/updateAdGroupState.htm",
                                                            data: postData,
                                                            async: false,
                                                            success: function (data) {
                                                                if (data.code == 200) {
                                                                    ret = true;
                                                                };
                                                            },
                                                            error: function () { }
                                                        });
                                                        return ret;
                                                    };// new Function("adGroupIds", "adGroupState", getcfService("site/get-rule-set-update-ad-group-state", User));
                                                    SetUpdateAdGroupState(objData[creativeId].adGroupId, '0');
                                                };
                                                jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                                LastRuleDo(ruleId);
                                            };
                                        }
                                        else if (RuleTodo == "只投PC") {
                                            if (objData[creativeId].channel_wireless == '0' && objData[creativeId].channel_pc == "1") {
                                                //无需执行
                                            }
                                            else {
                                                var ret = SetupdateCreative(objData[creativeId], "1", "0");
                                                if (ret == "600") {
                                                    var SetUpdateAdGroupState = function (adGroupIds, adGroupState) {
                                                        var ret = false;
                                                        var postData = 'adGroupIds=["' + adGroupIds + '"]&adGroupState=' + adGroupState + '&sla=json&isAjaxRequest=true&token=' + User.token;
                                                        $.ajax({
                                                            type: "Post",
                                                            url: "https://subway.simba.taobao.com/adgroup/updateAdGroupState.htm",
                                                            data: postData,
                                                            async: false,
                                                            success: function (data) {
                                                                if (data.code == 200) {
                                                                    ret = true;
                                                                };
                                                            },
                                                            error: function () { }
                                                        });
                                                        return ret;
                                                    };// new Function("adGroupIds", "adGroupState", getcfService("site/get-rule-set-update-ad-group-state", User));
                                                    SetUpdateAdGroupState(objData[creativeId].adGroupId, '0');
                                                };
                                            };
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                            LastRuleDo(ruleId);
                                        }
                                        else if (RuleTodo == "只投无线") {
                                            if (objData[creativeId].channel_wireless == '1' && objData[creativeId].channel_pc == "0") {
                                                //无需执行
                                            }
                                            else {
                                                var ret = SetupdateCreative(objData[creativeId], "0", "1");
                                                if (ret == "600") {
                                                    var SetUpdateAdGroupState = function (adGroupIds, adGroupState) {
                                                        var ret = false;
                                                        var postData = 'adGroupIds=["' + adGroupIds + '"]&adGroupState=' + adGroupState + '&sla=json&isAjaxRequest=true&token=' + User.token;
                                                        $.ajax({
                                                            type: "Post",
                                                            url: "https://subway.simba.taobao.com/adgroup/updateAdGroupState.htm",
                                                            data: postData,
                                                            async: false,
                                                            success: function (data) {
                                                                if (data.code == 200) {
                                                                    ret = true;
                                                                };
                                                            },
                                                            error: function () { }
                                                        });
                                                        return ret;
                                                    };// new Function("adGroupIds", "adGroupState", getcfService("site/get-rule-set-update-ad-group-state", User));
                                                    SetUpdateAdGroupState(objData[creativeId].adGroupId, '0');
                                                };
                                            };
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                            LastRuleDo(ruleId);
                                        }
                                        else if (RuleTodo == "删除") {
                                            var DeleteCreative = function (creativeId) {
                                                var ret = false;
                                                var postData = 'sla=json&isAjaxRequest=true&token=' + User.token;
                                                $.ajax({
                                                    type: "Post",
                                                    url: "https://subway.simba.taobao.com/creative/delete.htm?creativeId=" + creativeId,
                                                    data: postData,
                                                    async: false,
                                                    success: function (data) {
                                                        if (data.code == 200) {
                                                            ret = true;
                                                        };
                                                    },
                                                    error: function () { }
                                                });
                                                return ret;
                                            };// new Function("creativeId", getcfService("site/get-rule-delete-creative", User));
                                            if (DeleteCreative(objData[creativeId].creativeId)) {
                                                jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString() + '删除创意【' + objData[creativeId] + '】！', { color: 'green' });
                                                LastRuleDo(ruleId);
                                            } else {
                                                var SetUpdateAdGroupState = function (adGroupIds, adGroupState) {
                                                    var ret = false;
                                                    var postData = 'adGroupIds=["' + adGroupIds + '"]&adGroupState=' + adGroupState + '&sla=json&isAjaxRequest=true&token=' + User.token;
                                                    $.ajax({
                                                        type: "Post",
                                                        url: "https://subway.simba.taobao.com/adgroup/updateAdGroupState.htm",
                                                        data: postData,
                                                        async: false,
                                                        success: function (data) {
                                                            if (data.code == 200) {
                                                                ret = true;
                                                            };
                                                        },
                                                        error: function () { }
                                                    });
                                                    return ret;
                                                };// new Function("adGroupIds", "adGroupState", getcfService("site/get-rule-set-update-ad-group-state", User));
                                                SetUpdateAdGroupState(objData[creativeId].adGroupId, '0');
                                                jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString() + '创意删除失败，暂停推广宝贝！', { color: 'red' });
                                            };
                                        };
                                    };
                                };
                            };
                            if (RuleObject == "地域") {
                                var objData;
                                var sDate, eDate;
                                if (RuleTime == "昨天") {
                                    sDate = laydate.now(-1);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去2天") {
                                    sDate = laydate.now(-3);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去3天") {
                                    sDate = laydate.now(-3);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去7天") {
                                    sDate = laydate.now(-7);
                                    eDate = laydate.now(-1);
                                }
                                else if (RuleTime == "过去14天") {
                                    sDate = laydate.now(-14);
                                    eDate = laydate.now(-1);
                                };
                                var rptBpp4pAreaList = new Function("campaignid", "adgroupid", "sDate", "eDate", getcfService("site/get-rule-rpt-bpp4p-area-list-js", User));
                                objData = rptBpp4pAreaList(campaignId, adGroupId, sDate, eDate);
                                var doIds = new Array();
                                for (var iid in objData) {
                                    var doBool = true;
                                    for (var i = 0; i < Rule.length && doBool; i++) {
                                        var tR = Rule[i].split('$');
                                        if (parseFloat(objData[iid][tR[0]]) > parseFloat(tR[2]) == tR[1]) {
                                            doBool = true;
                                        } else {
                                            doBool = false;
                                        };
                                    };
                                    if (doBool) {
                                        doIds.push(iid);
                                    };
                                };
                                if (doIds.length > 0) {
                                    var AreaUpdate = new Function("campaignId", "areaState", getcfService("Comm.Subway.AreaUpdate", User));
                                    var AreaGet = new Function("campaignId", getcfService("Comm.Subway.AreaGet", User));
                                    if (RuleTodo == "增投地区") {
                                        var oldArea = AreaGet(campaignId);
                                        if (oldArea == "all")
                                            oldArea = "19,461,125,393,333,294,234,165,417,255,508,39,1,368,145,184,212,279,68,120,92,532,438,488,109,463,406,52,357,351,471,578,599,576,574";
                                        var all = oldArea.split(',');
                                        for (var id in doIds) {
                                            if ($.inArray(doIds[id], all) < 0)
                                                all.push(doIds[id]);
                                        };
                                        var eareStr = all.join(',');
                                        if (AreaUpdate(campaignId, eareStr)) {
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                            LastRuleDo(ruleId);
                                        }
                                        else {
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString() + '更改计划投放地区失败！', { color: 'red' });
                                        };
                                    }
                                    else if (RuleTodo == "减投地区") {
                                        var oldArea = AreaGet(campaignId);
                                        if (oldArea == "all")
                                            oldArea = "19,461,125,393,333,294,234,165,417,255,508,39,1,368,145,184,212,279,68,120,92,532,438,488,109,463,406,52,357,351,471,578,599,576,574";
                                        var all = oldArea.split(',');
                                        for (var id in doIds) {
                                            var at = $.inArray(doIds[id], all);
                                            if (at >= 0)
                                                all.splice(at, 1);
                                        };
                                        var eareStr = all.join(',');
                                        if (AreaUpdate(campaignId, eareStr)) {
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                            LastRuleDo(ruleId);
                                        }
                                        else {
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString() + '更改计划投放地区失败！', { color: 'red' });
                                        };
                                    }
                                    else if (RuleTodo == "只投地区") {
                                        var all = new Array();
                                        for (var id in doIds) {
                                            all.push(doIds[id]);
                                        };
                                        var eareStr = all.join(',');
                                        if (AreaUpdate(campaignId, eareStr)) {
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                            LastRuleDo(ruleId);
                                        }
                                        else {
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString() + '更改计划投放地区失败！', { color: 'red' });
                                        };

                                    }
                                    else if (RuleTodo == "不投地区") {
                                        var all = "19,461,125,393,333,294,234,165,417,255,508,39,1,368,145,184,212,279,68,120,92,532,438,488,109,463,406,52,357,351,471,578,599,576,574".split(',');
                                        for (var id in doIds) {
                                            var at = $.inArray(doIds[id], all);
                                            if (at >= 0)
                                                all.splice(at, 1);
                                        };
                                        var eareStr = all.join(',');
                                        if (AreaUpdate(campaignId, eareStr)) {
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString(), { color: 'green' });
                                            LastRuleDo(ruleId);
                                        }
                                        else {
                                            jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString() + '更改计划投放地区失败！', { color: 'red' });
                                        };
                                    };
                                } else {
                                    jQuery("#listRules").jqGrid('setCell', sId, 'Msg', myDate.toLocaleString() + '无地域更新！', { color: 'red' });
                                };
                            };
                        };// new Function("sId", "Rule", getcfService("site/get-rule-todo-running-js", User));
                        var pageInitRules = function () {
                            jQuery("#listRules").jqGrid({
                                //data: mydata,
                                datatype: "local",
                                height: '350px',
                                width: '1100px',
                                colNames: ['规则名称', '应用对象', '数据时域', '规则', '匹配规则', '处置', '频率（秒）', 'Id', '上次执行时间'], //, '匹配规则', '处置', '频率（秒）'
                                colModel: [
                                    { name: 'RuleName', index: 'RuleName', width: 120 },
                                    { name: 'RuleObject', index: 'RuleObject', width: 90 },
                                    { name: 'RuleTime', index: 'RuleTime', width: 150 },
                                    { name: 'Rule', index: 'Rule', hidden: true },
                                    { name: 'RuleStr', index: 'RuleStr', width: 410 },
                                    { name: 'RuleTodo', index: 'RuleTodo', width: 200 },
                                    { name: 'RuleRate', index: 'RuleRate', width: 70 },
                                    { name: 'Id', index: 'Id', hidden: true },
                                    { name: 'Msg', index: 'Msg', width: 140 }
                                ],
                                pager: "#plistRules",
                                multiselect: true,
                                viewrecords: true,
                                sortname: 'RuleObject',
                                grouping: true,
                                groupingView: {
                                    groupField: ['RuleObject'],
                                    groupColumnShow: [false]
                                },
                                caption: "监控.优化规则"
                            });
                            loadRules();
                        };// new Function(getcfService("site/get-rule-page-init-js", User));
                        pageInitRules();
                    },
                    cancel: function (index, layero) {
                        var StopRuningRule = function () {
                            for (var i = 0; i < rulets.length; i++) {
                                window.clearInterval(rulets[i]);
                            };

                            layer.msg("已暂停监控");
                            rulets = new Array();
                            $("#bt_StartRule").text("自动优化监控");
                            $("#bt_StartRule").removeAttr("disabled");
                            $("#bt_StopRule").attr({ "disabled": "disabled" });
                            $("#bt_OneKeyRule").removeAttr("disabled");
                        };// new Function(getcfService("site/get-rule-stop-runing-js", User));
                        StopRuningRule();
                        window.clearInterval(bTimeId);
                        layer.close(index)
                    },
                });
                $("#bt_StartRule").click(function () {
                    var StartRuningRule = function () {
                        var sIds = getjqGridSelarrrow("#listRules");
                        if (sIds.length < 1) {
                            layer.msg("未选中任何规则！");
                            return;
                        };
                        $("#bt_StartRule").text("监控中...");
                        $("#bt_StartRule").attr({ "disabled": "disabled" });
                        $("#bt_StopRule").removeAttr("disabled");//将按钮可用
                        $("#bt_OneKeyRule").attr({ "disabled": "disabled" });

                        var GetCheckedBidWrodIds = function () {
                            var id_array = new Array();
                            $('input[name="bidwords"]:checked').each(function () {
                                id_array.push($(this).val());//向数组中添加元素
                            });
                            if (id_array.length < 1) {
                                $('input[name="bidwords"]').each(function () {
                                    id_array.push($(this).val());//向数组中添加元素
                                });
                            };
                            return id_array;
                        };// new Function(getcfService("site/get-rule-checked-bid-word-ids-js", User));
                        BidWordIds = GetCheckedBidWrodIds();
                        rulets = new Array();
                        var runingDoSame = function (index, sId, Rule, at) {
                            rulets[index] = window.setInterval(function () { todoRunning(sId, Rule) }, at);
                        };// new Function("index", "sId", "Rule", "at", getcfService("site/get-rule-runing-do-same-js", User));
                        var ri = 0;
                        for (var i = 0; i < sIds.length; i++) {
                            var RuleObject = jQuery("#listRules").jqGrid('getCell', sIds[i], 'RuleObject');
                            var RuleTime = jQuery("#listRules").jqGrid('getCell', sIds[i], 'RuleTime');
                            var Rule = jQuery("#listRules").jqGrid('getCell', sIds[i], 'Rule');
                            var RuleTodo = jQuery("#listRules").jqGrid('getCell', sIds[i], 'RuleTodo');
                            var RuleRate = jQuery("#listRules").jqGrid('getCell', sIds[i], 'RuleRate');
                            if (RuleTime.indexOf("当日实时") != -1) {
                                runingDoSame(ri, sIds[i], Rule, parseInt(RuleRate) * 1000);
                                ri++;
                            };

                        };
                    };// new Function(getcfService("site/get-rule-start-runing-js", User));
                    StartRuningRule();
                });
                $("#bt_StopRule").click(function () {
                    var StopRuningRule = function () {
                        for (var i = 0; i < rulets.length; i++) {
                            window.clearInterval(rulets[i]);
                        };

                        layer.msg("已暂停监控");
                        rulets = new Array();
                        $("#bt_StartRule").text("自动优化监控");
                        $("#bt_StartRule").removeAttr("disabled");
                        $("#bt_StopRule").attr({ "disabled": "disabled" });
                        $("#bt_OneKeyRule").removeAttr("disabled");
                    };// new Function(getcfService("site/get-rule-stop-runing-js", User));
                    StopRuningRule();
                });
                $("#bt_OneKeyRule").click(function () {
                    var DoOneKeyRules = function () {
                        /*
    if (!getUserRank(8, UserRank)) {
            layer.msg('一键应用规则优化仅对黄金版以上权限，需要对当前店铺（' + User.nickName + '）授权！\\n 未授权店铺只能批量添加单一属性标签\\n如需要多项属性任意组合标签请联系交流群管理授权店铺！');
            return;
        };
    */
                        var sIds = getjqGridSelarrrow("#listRules");
                        if (sIds.length < 1) {
                            layer.msg("未选中任何规则！");
                            return;
                        };
                        var GetCheckedBidWrodIds = function () {
                            var id_array = new Array();
                            $('input[name="bidwords"]:checked').each(function () {
                                id_array.push($(this).val());//向数组中添加元素
                            });
                            if (id_array.length < 1) {
                                $('input[name="bidwords"]').each(function () {
                                    id_array.push($(this).val());//向数组中添加元素
                                });
                            };
                            return id_array;

                        };// new Function(getcfService("site/get-rule-checked-bid-word-ids-js", User));
                        BidWordIds = GetCheckedBidWrodIds();
                        rulets = new Array();
                        for (var i = 0; i < sIds.length; i++) {
                            var RuleObject = jQuery("#listRules").jqGrid('getCell', sIds[i], 'RuleObject');
                            var RuleTime = jQuery("#listRules").jqGrid('getCell', sIds[i], 'RuleTime');
                            var Rule = jQuery("#listRules").jqGrid('getCell', sIds[i], 'Rule');
                            var RuleTodo = jQuery("#listRules").jqGrid('getCell', sIds[i], 'RuleTodo');
                            var RuleRate = jQuery("#listRules").jqGrid('getCell', sIds[i], 'RuleRate');

                            todoRunning(sIds[i], Rule);
                        };
                    };// new Function(getcfService("site/get-rule-do-one-key-rules-js", User));
                    DoOneKeyRules();
                });
                $("#bt_addRuleJianKong").click(function () {
                    var OpenAddRuleBaiche = function (sId) {
                        var btName = "添加";
                        var winName = "监控程序-添加规则";
                        if (sId != -1) {
                            btName = "修改";
                            winName = "监控程序-修改规则";
                        };

                        var opt_1 = '<option value="impression" selected>展现量</option>'
                            + '<option value="click">点击量</option>'
                            + '<option value="ctr">点击率</option>'
                            + '<option value="cost">花费</option>'
                            + '<option value="cpc">平均点击花费</option>'
                            + '<option value="coverage">转化率</option>'
                            + '<option value="roi">ROI</option>'
                            + '<option value="carttotal">总购物车</option>'
                            + '<option value="favtotal">收藏总数</option>'
                            + '<option value="transactionshippingtotal">成交笔数</option>';
                        var opt_2 = '<option value="impression" selected>展现量</option>'
                            + '<option value="click">点击量</option>'
                            + '<option value="ctr">点击率</option>'
                            + '<option value="cost">花费</option>'
                            + '<option value="cpc">平均点击花费</option>'
                            + '<option value="coverage">转化率</option>'
                            + '<option value="roi">ROI</option>'
                            + '<option value="avgpos">展现排名</option>'
                            + '<option value="carttotal">总购物车</option>'
                            + '<option value="favtotal">收藏总数</option>'
                            + '<option value="transactionshippingtotal">成交笔数</option>'
                            + '<option value="wirelessQscore">无线质量分</option>'
                            + '<option value="qscore">PC质量分</option>'
                            + '<option value="maxMobilePrice">无线出价</option>'
                            + '<option value="maxPrice">PC出价</option>';
                        var opt_3 = '<option value="impression" selected>展现量</option>'
                            + '<option value="click">点击量</option>'
                            + '<option value="ctr">点击率</option>'
                            + '<option value="cost">花费</option>'
                            + '<option value="cpc">平均点击花费</option>'
                            + '<option value="coverage">转化率</option>'
                            + '<option value="roi">ROI</option>'
                            + '<option value="carttotal">总购物车</option>'
                            + '<option value="favtotal">收藏总数</option>'
                            + '<option value="transactionshippingtotal">成交笔数</option>'
                            + '<option value="discount">人群溢价</option>';
                        var dataUIOpt = {
                            "推广单元": opt_1,
                            "关键词": opt_2,
                            "人群包": opt_3,
                            "创意": opt_1,
                            "地域": opt_1
                        };
                        var dataUI = '<span class="spanData">'
                            + '<select class="input" name="rule_data" style="width:150px">'
                            + dataUIOpt["推广单元"]
                            + '</select>'
                            + '<select class="input" name="rule_opt" style="width:60px"><option value="1" selected>></option><option value="0"><=</option></select>'
                            + '<input  type="text" name="rule_val" value="0" class="input w60"/>'
                            + '<button class="layui-btn layui-btn-mini bt_deleteRuledata"> - </button>'
                            + '<br></span>';
                        var selectTodoUI = {
                            "推广单元": '<select class="input" id="s_RuleTodo" style="width:100px"><option value="暂停推广" selected>暂停推广</option></select>',
                            "关键词": '<select class="input" id="s_RuleTodo" style="width:130px"><option value="屏蔽展现" selected>屏蔽展现</option><option value="删除">删除</option><option value="无线出价提高百分之">无线出价提高百分之</option><option value="无线出价降低百分之">无线出价降低百分之</option><option value="无线出价增加">无线出价增加</option><option value="无线出价降低">无线出价降低</option><option value="PC出价提高百分之">PC出价提高百分之</option><option value="PC出价降低百分之">PC出价降低百分之</option><option value="PC出价增加">PC出价增加</option><option value="PC出价降低">PC出价降低</option><option value="精准匹配">精准匹配</option><option value="广泛匹配">广泛匹配</option></select>>><input id="ipt_Todo_val" type="text" class="input w60" value="0"/>',
                            "人群包": '<select class="input" id="s_RuleTodo" style="width:100px"><option value="暂停推广" selected>暂停推广</option><option value="删除">删除</option><option value="溢价增加">溢价增加</option><option value="溢价降低">溢价降低</option></select>>><input id="ipt_Todo_val" type="text" class="input w60" value="0"/>',
                            "创意": '<select class="input" id="s_RuleTodo" style="width:100px"><option value="全部投放" selected>全部投放</option><option value="只投PC">只投PC</option><option value="只投无线">只投无线</option><option value="删除">删除</option></select>(如果只有一个创意，处置失败则暂停推广宝贝)',
                            "地域": '<select class="input" id="s_RuleTodo" style="width:100px"><option value="增投地区">增投地区</option><option value="减投地区">减投地区</option><option value="只投地区" selected>只投地区*</option><option value="不投地区">不投地区</option></select>'
                        };
                        var selectDateUI = {
                            "推广单元": '<select class="input" id="s_RuleTime" style="width:100px"><option value="当日实时" selected>当日实时</option></select>-<select class="input" id="s_Traffictype" style="width:100px"><option value="汇总">汇总</option><option value="移动设备">移动设备</option><option value="计算机">计算机</option></select>',
                            "关键词": '<select class="input" id="s_RuleTime" style="width:100px"><option value="当日实时" selected>当日实时</option><option value="昨天">昨天</option><option value="过去2天">过去2天</option><option value="过去3天">过去3天</option><option value="过去7天">过去7天</option><option value="过去14天">过去14天</option></select>-<select class="input" id="s_Traffictype" style="width:100px"><option value="汇总">汇总</option><option value="移动设备">移动设备</option><option value="计算机">计算机</option></select>',
                            "人群包": '<select class="input" id="s_RuleTime" style="width:100px"><option value="当日实时" selected>当日实时</option><option value="昨天">昨天</option><option value="过去2天">过去2天</option><option value="过去3天">过去3天</option><option value="过去7天">过去7天</option><option value="过去14天">过去14天</option></select>-<select class="input" id="s_Traffictype" style="width:100px"><option value="汇总">汇总</option><option value="移动设备">移动设备</option><option value="计算机">计算机</option></select>',
                            "创意": '<select class="input" id="s_RuleTime" style="width:100px"><option value="当日实时" selected>当日实时</option><option value="昨天">昨天</option><option value="过去2天">过去2天</option><option value="过去3天">过去3天</option><option value="过去7天" selected>过去7天</option><option value="过去14天">过去14天</option></select>-<select class="input" id="s_Traffictype" style="width:100px"><option value="汇总">汇总</option><option value="移动设备">移动设备</option><option value="计算机">计算机</option></select>',
                            "地域": '<select class="input" id="s_RuleTime" style="width:100px"><option value="昨天">昨天</option><option value="过去2天">过去2天</option><option value="过去3天">过去3天</option><option value="过去7天" selected>过去7天</option><option value="过去14天">过去14天</option></select>-<select class="input" id="s_Traffictype" style="width:100px"><option value="汇总">汇总</option></select>'
                        };
                        var divUI = '<div style="padding: 15px; line-height: 22px; background-color: #fff; color: #000;">'
                            + '<fieldset class="layui-elem-field">'
                            + ' <legend>匹配内容</legend>'
                            + '<div class="layui-field-box">'
                            + '应用对象：<select class="input" id="s_RuleObject" style="width:100px"><option value="推广单元" selected>推广单元</option><option value="关键词">关键词</option><option value="人群包">人群包</option><option value="创意">创意</option><option value="地域">地域</option></select>'
                            + ' 数据时域：<span id="sp_DateTraffictype"></span>'
                            + '<button class="layui-btn layui-btn-danger layui-btn-mini" id="bt_addRuledata">+ 数据项</button><br>'
                            + '<div id="baseDataUI">'
                            + '</div>'
                            + '</div>'
                            + '</fieldset>'
                            + '<fieldset class="layui-elem-field">'
                            + ' <legend>处理方式</legend>'
                            + '<div class="layui-field-box">'
                            + '操作：<span id="sp_Todo"></span><br>'
                            + '频率：每隔<input id="ipt_Rule_Rate" type="text" class="input w60" value="600"/>秒检查处理！（<span style="color:red">只针对时域"当日实时"有效，用于监控！</span>）<br>'
                            + '名称：<input id="ipt_Rule_Name" type="text" class="input" style="width:250px"/>'
                            + '</div>'
                            + '</fieldset>'
                            + '</div>';
                        var index = layer.open({
                            type: 1,
                            content: divUI,
                            area: ["600px", "530px"],
                            btn: [btName, '关闭'],
                            title: [winName, 'font-size:18px;'],
                            success: function (layero) {
                                $("#s_RuleObject").change(function () {
                                    $("#sp_Todo").html(selectTodoUI[$(this).val()]);
                                    $("#sp_DateTraffictype").html(selectDateUI[$(this).val()]);
                                    $("select[name='rule_data']").each(function () {
                                        var ov = $(this).val();
                                        $(this).html(dataUIOpt[$("#s_RuleObject").val()]);
                                        $(this).val(ov);
                                    });
                                });
                                $("#bt_addRuledata").click(function () {
                                    var ui = $(dataUI);
                                    ui.find('[name=rule_data]').html(dataUIOpt[$("#s_RuleObject").val()]);
                                    $("#baseDataUI").append(ui);
                                    $(".bt_deleteRuledata:last").click(function () {
                                        $(this).parents('.spanData').remove();
                                    });
                                });
                                if (sId != -1) {
                                    var ruleData = jQuery("#listRules").jqGrid('getCell', sId, 'Rule');
                                    var RuleName = jQuery("#listRules").jqGrid('getCell', sId, 'RuleName');
                                    var rsObj = ruleData.split('#');
                                    var RuleObject = rsObj[0];
                                    var RuleTime = rsObj[1];
                                    var Rules = rsObj[2].split('&');
                                    var RuleTodo = rsObj[3];
                                    var RuleRate = rsObj[4];
                                    $("#s_RuleObject").val(RuleObject);
                                    $("#sp_DateTraffictype").html(selectDateUI[RuleObject]);
                                    var RuleTimes = RuleTime.split('$');
                                    $("#s_RuleTime").val(RuleTimes[0]);
                                    $("#s_Traffictype").val(RuleTimes[1]);
                                    for (var i = 0; i < Rules.length; i++) {
                                        var rVals = Rules[i].split('$');
                                        $("#baseDataUI").append(dataUI);
                                        if (i > 0) {
                                            $(".bt_deleteRuledata:last").click(function () {
                                                $(this).parents('.spanData').remove();
                                            });
                                        };
                                        $(".spanData:last").find('[name=rule_data]').html(dataUIOpt[RuleObject]);
                                        $(".spanData:last").find('[name=rule_data]').val(rVals[0]);
                                        $(".spanData:last").find('[name=rule_opt]').val(rVals[1]);
                                        $(".spanData:last").find('[name=rule_val]').val(rVals[2]);
                                    };
                                    $("#sp_Todo").html(selectTodoUI[RuleObject]);
                                    var RuleTodos = RuleTodo.split('$');
                                    $("#s_RuleTodo").val(RuleTodos[0]);
                                    $("#ipt_Todo_val").val(RuleTodos[1]);
                                    $("#ipt_Rule_Rate").val(RuleRate);
                                    $("#ipt_Rule_Name").val(RuleName);
                                } else {
                                    $("#sp_DateTraffictype").html(selectDateUI["推广单元"]);
                                    $("#sp_Todo").html(selectTodoUI["推广单元"]);
                                    $("#baseDataUI").append(dataUI);

                                };
                            },
                            yes: function () {
                                var ipt_Rule_Name = $("#ipt_Rule_Name").val();
                                if (ipt_Rule_Name == "") {
                                    layer.msg("请给规则取个名字吧！");
                                    return;
                                };
                                var s_RuleObject = $("#s_RuleObject").val();
                                var s_RuleTime = $("#s_RuleTime").val();
                                var s_Traffictype = $("#s_Traffictype").val();
                                if (typeof (s_Traffictype) != "undefined") {
                                    s_RuleTime = s_RuleTime + '$' + s_Traffictype;
                                };
                                var rules = new Array();
                                $(".spanData").each(function (i) {
                                    var rule_data = $(this).find('[name=rule_data]').val();
                                    var rule_opt = $(this).find('[name=rule_opt]').val();
                                    var rule_val = $(this).find('[name=rule_val]').val();
                                    var rule = rule_data + '$' + rule_opt + '$' + rule_val;
                                    rules.push(rule);
                                });
                                var s_RuleTodo = $("#s_RuleTodo").val();
                                var ipt_Todo_val = $("#ipt_Todo_val").val();
                                if (typeof (ipt_Todo_val) != "undefined") {
                                    s_RuleTodo = s_RuleTodo + '$' + ipt_Todo_val;
                                };
                                var ipt_Rule_Rate = $("#ipt_Rule_Rate").val();
                                var ruleId = "0";
                                if (sId != -1) {
                                    ruleId = jQuery("#listRules").jqGrid('getCell', sId, 'Id');
                                };
                                var ruleData = s_RuleObject + '#'
                                    + s_RuleTime + '#'
                                    + rules.join('&') + '#'
                                    + s_RuleTodo + '#'
                                    + ipt_Rule_Rate;
                                var postData = {
                                    md5: User.md5,
                                    nickName: User.nickName,
                                    ruleName: ipt_Rule_Name,
                                    ruleObject: s_RuleObject,
                                    ruleRate: ipt_Rule_Rate,
                                    rules: ruleData,
                                    ruleTime: s_RuleTime,
                                    ruleTodo: s_RuleTodo,
                                    id: ruleId
                                };
                                var addRule = function (postData) {
                                    $.extend(postData, User);
                                    var ret = {};
                                    $.ajax({
                                        type: "post",
                                        //url: "https://zhitongche.libangjie.com/index.php?r=site/get-rule-add-rule-yun-data",
                                        url: server_url + '/taobao/api' + '?r=site/get-rule-add-rule-yun-data',
                                        contentType: 'application/json',
                                        data: JSON.stringify(postData),
                                        async: false,
                                        dataType: "json",
                                        success: function (data, status) {
                                            ret = data;
                                        }
                                    });
                                    return ret;
                                };// new Function("postData", getcfService("site/get-rule-add-rule-ajax-js", User));
                                var ret = addRule(postData); //推送到云端
                                layer.msg(ret.msg);
                                if (ret.code == 200) {
                                    loadRules();
                                };
                                if (sId != -1) {
                                    layer.close(index);
                                };
                                return;
                            },
                        });
                    };// new Function("sId", getcfService("site/get-rule-add-rule-window-js", User));
                    OpenAddRuleBaiche(-1);
                });
                $("#bt_delRuleJianKong").click(function () {
                    layer.confirm('确定要删除这些优化规则?一旦删除，所有数据将无法恢复！', { icon: 3, title: '确认删除' }, function (index) {
                        var DelRulebaiche = function () {
                            var sIds = getjqGridSelarrrow("#listRules");
                            if (sIds.length < 1) {
                                layer.msg("未选中任何规则！");
                                return;
                            };
                            for (var i = 0; i < sIds.length; i++) {
                                var ruleId = jQuery("#listRules").jqGrid('getCell', sIds[i], 'Id');
                                var postdata = { id: ruleId };
                                $.extend(postdata, User);
                                $.ajax({
                                    type: "post",
                                    //url: "https://zhitongche.libangjie.com/index.php?r=site/get-rule-delete-rule-yun-data",
                                    url: server_url + '/taobao/api?r=site/get-rule-delete-rule-yun-data',
                                    contentType: 'application/json',
                                    data: JSON.stringify(postdata),
                                    async: false,
                                    success: function (data, status) {
                                        var ret = data;
                                    }
                                });
                            };
                            loadRules();
                        };// new Function(getcfService("site/get-rule-delete-rule-ajax-js", User));
                        DelRulebaiche();
                        layer.close(index);
                    });

                });
                $("#bt_updateRuleJianKong").click(function () {
                    var sIds = getjqGridSelarrrow("#listRules");
                    if (sIds.length == 1) {
                        var OpenAddRuleBaiche = function (sId) {
                            var btName = "添加";
                            var winName = "监控程序-添加规则";
                            if (sId != -1) {
                                btName = "修改";
                                winName = "监控程序-修改规则";
                            };

                            var opt_1 = '<option value="impression" selected>展现量</option>'
                                + '<option value="click">点击量</option>'
                                + '<option value="ctr">点击率</option>'
                                + '<option value="cost">花费</option>'
                                + '<option value="cpc">平均点击花费</option>'
                                + '<option value="coverage">转化率</option>'
                                + '<option value="roi">ROI</option>'
                                + '<option value="carttotal">总购物车</option>'
                                + '<option value="favtotal">收藏总数</option>'
                                + '<option value="transactionshippingtotal">成交笔数</option>';
                            var opt_2 = '<option value="impression" selected>展现量</option>'
                                + '<option value="click">点击量</option>'
                                + '<option value="ctr">点击率</option>'
                                + '<option value="cost">花费</option>'
                                + '<option value="cpc">平均点击花费</option>'
                                + '<option value="coverage">转化率</option>'
                                + '<option value="roi">ROI</option>'
                                + '<option value="avgpos">展现排名</option>'
                                + '<option value="carttotal">总购物车</option>'
                                + '<option value="favtotal">收藏总数</option>'
                                + '<option value="transactionshippingtotal">成交笔数</option>'
                                + '<option value="wirelessQscore">无线质量分</option>'
                                + '<option value="qscore">PC质量分</option>'
                                + '<option value="maxMobilePrice">无线出价</option>'
                                + '<option value="maxPrice">PC出价</option>';
                            var opt_3 = '<option value="impression" selected>展现量</option>'
                                + '<option value="click">点击量</option>'
                                + '<option value="ctr">点击率</option>'
                                + '<option value="cost">花费</option>'
                                + '<option value="cpc">平均点击花费</option>'
                                + '<option value="coverage">转化率</option>'
                                + '<option value="roi">ROI</option>'
                                + '<option value="carttotal">总购物车</option>'
                                + '<option value="favtotal">收藏总数</option>'
                                + '<option value="transactionshippingtotal">成交笔数</option>'
                                + '<option value="discount">人群溢价</option>';
                            var dataUIOpt = {
                                "推广单元": opt_1,
                                "关键词": opt_2,
                                "人群包": opt_3,
                                "创意": opt_1,
                                "地域": opt_1
                            };
                            var dataUI = '<span class="spanData">'
                                + '<select class="input" name="rule_data" style="width:150px">'
                                + dataUIOpt["推广单元"]
                                + '</select>'
                                + '<select class="input" name="rule_opt" style="width:60px"><option value="1" selected>></option><option value="0"><=</option></select>'
                                + '<input  type="text" name="rule_val" value="0" class="input w60"/>'
                                + '<button class="layui-btn layui-btn-mini bt_deleteRuledata"> - </button>'
                                + '<br></span>';
                            var selectTodoUI = {
                                "推广单元": '<select class="input" id="s_RuleTodo" style="width:100px"><option value="暂停推广" selected>暂停推广</option></select>',
                                "关键词": '<select class="input" id="s_RuleTodo" style="width:130px"><option value="屏蔽展现" selected>屏蔽展现</option><option value="删除">删除</option><option value="无线出价提高百分之">无线出价提高百分之</option><option value="无线出价降低百分之">无线出价降低百分之</option><option value="无线出价增加">无线出价增加</option><option value="无线出价降低">无线出价降低</option><option value="PC出价提高百分之">PC出价提高百分之</option><option value="PC出价降低百分之">PC出价降低百分之</option><option value="PC出价增加">PC出价增加</option><option value="PC出价降低">PC出价降低</option><option value="精准匹配">精准匹配</option><option value="广泛匹配">广泛匹配</option></select>>><input id="ipt_Todo_val" type="text" class="input w60" value="0"/>',
                                "人群包": '<select class="input" id="s_RuleTodo" style="width:100px"><option value="暂停推广" selected>暂停推广</option><option value="删除">删除</option><option value="溢价增加">溢价增加</option><option value="溢价降低">溢价降低</option></select>>><input id="ipt_Todo_val" type="text" class="input w60" value="0"/>',
                                "创意": '<select class="input" id="s_RuleTodo" style="width:100px"><option value="全部投放" selected>全部投放</option><option value="只投PC">只投PC</option><option value="只投无线">只投无线</option><option value="删除">删除</option></select>(如果只有一个创意，处置失败则暂停推广宝贝)',
                                "地域": '<select class="input" id="s_RuleTodo" style="width:100px"><option value="增投地区">增投地区</option><option value="减投地区">减投地区</option><option value="只投地区" selected>只投地区*</option><option value="不投地区">不投地区</option></select>'
                            };
                            var selectDateUI = {
                                "推广单元": '<select class="input" id="s_RuleTime" style="width:100px"><option value="当日实时" selected>当日实时</option></select>-<select class="input" id="s_Traffictype" style="width:100px"><option value="汇总">汇总</option><option value="移动设备">移动设备</option><option value="计算机">计算机</option></select>',
                                "关键词": '<select class="input" id="s_RuleTime" style="width:100px"><option value="当日实时" selected>当日实时</option><option value="昨天">昨天</option><option value="过去2天">过去2天</option><option value="过去3天">过去3天</option><option value="过去7天">过去7天</option><option value="过去14天">过去14天</option></select>-<select class="input" id="s_Traffictype" style="width:100px"><option value="汇总">汇总</option><option value="移动设备">移动设备</option><option value="计算机">计算机</option></select>',
                                "人群包": '<select class="input" id="s_RuleTime" style="width:100px"><option value="当日实时" selected>当日实时</option><option value="昨天">昨天</option><option value="过去2天">过去2天</option><option value="过去3天">过去3天</option><option value="过去7天">过去7天</option><option value="过去14天">过去14天</option></select>-<select class="input" id="s_Traffictype" style="width:100px"><option value="汇总">汇总</option><option value="移动设备">移动设备</option><option value="计算机">计算机</option></select>',
                                "创意": '<select class="input" id="s_RuleTime" style="width:100px"><option value="当日实时" selected>当日实时</option><option value="昨天">昨天</option><option value="过去2天">过去2天</option><option value="过去3天">过去3天</option><option value="过去7天" selected>过去7天</option><option value="过去14天">过去14天</option></select>-<select class="input" id="s_Traffictype" style="width:100px"><option value="汇总">汇总</option><option value="移动设备">移动设备</option><option value="计算机">计算机</option></select>',
                                "地域": '<select class="input" id="s_RuleTime" style="width:100px"><option value="昨天">昨天</option><option value="过去2天">过去2天</option><option value="过去3天">过去3天</option><option value="过去7天" selected>过去7天</option><option value="过去14天">过去14天</option></select>-<select class="input" id="s_Traffictype" style="width:100px"><option value="汇总">汇总</option></select>'
                            };
                            var divUI = '<div style="padding: 15px; line-height: 22px; background-color: #fff; color: #000;">'
                                + '<fieldset class="layui-elem-field">'
                                + ' <legend>匹配内容</legend>'
                                + '<div class="layui-field-box">'
                                + '应用对象：<select class="input" id="s_RuleObject" style="width:100px"><option value="推广单元" selected>推广单元</option><option value="关键词">关键词</option><option value="人群包">人群包</option><option value="创意">创意</option><option value="地域">地域</option></select>'
                                + ' 数据时域：<span id="sp_DateTraffictype"></span>'
                                + '<button class="layui-btn layui-btn-danger layui-btn-mini" id="bt_addRuledata">+ 数据项</button><br>'
                                + '<div id="baseDataUI">'
                                + '</div>'
                                + '</div>'
                                + '</fieldset>'
                                + '<fieldset class="layui-elem-field">'
                                + ' <legend>处理方式</legend>'
                                + '<div class="layui-field-box">'
                                + '操作：<span id="sp_Todo"></span><br>'
                                + '频率：每隔<input id="ipt_Rule_Rate" type="text" class="input w60" value="600"/>秒检查处理！（<span style="color:red">只针对时域"当日实时"有效，用于监控！</span>）<br>'
                                + '名称：<input id="ipt_Rule_Name" type="text" class="input" style="width:250px"/>'
                                + '</div>'
                                + '</fieldset>'
                                + '</div>';
                            var index = layer.open({
                                type: 1,
                                content: divUI,
                                area: ["600px", "530px"],
                                btn: [btName, '关闭'],
                                title: [winName, 'font-size:18px;'],
                                success: function (layero) {
                                    $("#s_RuleObject").change(function () {
                                        $("#sp_Todo").html(selectTodoUI[$(this).val()]);
                                        $("#sp_DateTraffictype").html(selectDateUI[$(this).val()]);
                                        $("select[name='rule_data']").each(function () {
                                            var ov = $(this).val();
                                            $(this).html(dataUIOpt[$("#s_RuleObject").val()]);
                                            $(this).val(ov);
                                        });
                                    });
                                    $("#bt_addRuledata").click(function () {
                                        var ui = $(dataUI);
                                        ui.find('[name=rule_data]').html(dataUIOpt[$("#s_RuleObject").val()]);
                                        $("#baseDataUI").append(ui);
                                        $(".bt_deleteRuledata:last").click(function () {
                                            $(this).parents('.spanData').remove();
                                        });
                                    });
                                    if (sId != -1) {
                                        var ruleData = jQuery("#listRules").jqGrid('getCell', sId, 'Rule');
                                        var RuleName = jQuery("#listRules").jqGrid('getCell', sId, 'RuleName');
                                        var rsObj = ruleData.split('#');
                                        var RuleObject = rsObj[0];
                                        var RuleTime = rsObj[1];
                                        var Rules = rsObj[2].split('&');
                                        var RuleTodo = rsObj[3];
                                        var RuleRate = rsObj[4];
                                        $("#s_RuleObject").val(RuleObject);
                                        $("#sp_DateTraffictype").html(selectDateUI[RuleObject]);
                                        var RuleTimes = RuleTime.split('$');
                                        $("#s_RuleTime").val(RuleTimes[0]);
                                        $("#s_Traffictype").val(RuleTimes[1]);
                                        for (var i = 0; i < Rules.length; i++) {
                                            var rVals = Rules[i].split('$');
                                            $("#baseDataUI").append(dataUI);
                                            if (i > 0) {
                                                $(".bt_deleteRuledata:last").click(function () {
                                                    $(this).parents('.spanData').remove();
                                                });
                                            };
                                            $(".spanData:last").find('[name=rule_data]').html(dataUIOpt[RuleObject]);
                                            $(".spanData:last").find('[name=rule_data]').val(rVals[0]);
                                            $(".spanData:last").find('[name=rule_opt]').val(rVals[1]);
                                            $(".spanData:last").find('[name=rule_val]').val(rVals[2]);
                                        };
                                        $("#sp_Todo").html(selectTodoUI[RuleObject]);
                                        var RuleTodos = RuleTodo.split('$');
                                        $("#s_RuleTodo").val(RuleTodos[0]);
                                        $("#ipt_Todo_val").val(RuleTodos[1]);
                                        $("#ipt_Rule_Rate").val(RuleRate);
                                        $("#ipt_Rule_Name").val(RuleName);
                                    } else {
                                        $("#sp_DateTraffictype").html(selectDateUI["推广单元"]);
                                        $("#sp_Todo").html(selectTodoUI["推广单元"]);
                                        $("#baseDataUI").append(dataUI);

                                    };
                                },
                                yes: function () {
                                    var ipt_Rule_Name = $("#ipt_Rule_Name").val();
                                    if (ipt_Rule_Name == "") {
                                        layer.msg("请给规则取个名字吧！");
                                        return;
                                    };
                                    var s_RuleObject = $("#s_RuleObject").val();
                                    var s_RuleTime = $("#s_RuleTime").val();
                                    var s_Traffictype = $("#s_Traffictype").val();
                                    if (typeof (s_Traffictype) != "undefined") {
                                        s_RuleTime = s_RuleTime + '$' + s_Traffictype;
                                    };
                                    var rules = new Array();
                                    $(".spanData").each(function (i) {
                                        var rule_data = $(this).find('[name=rule_data]').val();
                                        var rule_opt = $(this).find('[name=rule_opt]').val();
                                        var rule_val = $(this).find('[name=rule_val]').val();
                                        var rule = rule_data + '$' + rule_opt + '$' + rule_val;
                                        rules.push(rule);
                                    });
                                    var s_RuleTodo = $("#s_RuleTodo").val();
                                    var ipt_Todo_val = $("#ipt_Todo_val").val();
                                    if (typeof (ipt_Todo_val) != "undefined") {
                                        s_RuleTodo = s_RuleTodo + '$' + ipt_Todo_val;
                                    };
                                    var ipt_Rule_Rate = $("#ipt_Rule_Rate").val();
                                    var ruleId = "0";
                                    if (sId != -1) {
                                        ruleId = jQuery("#listRules").jqGrid('getCell', sId, 'Id');
                                    };
                                    var ruleData = s_RuleObject + '#'
                                        + s_RuleTime + '#'
                                        + rules.join('&') + '#'
                                        + s_RuleTodo + '#'
                                        + ipt_Rule_Rate;
                                    var postData = {
                                        md5: User.md5,
                                        nickName: User.nickName,
                                        ruleName: ipt_Rule_Name,
                                        ruleObject: s_RuleObject,
                                        ruleRate: ipt_Rule_Rate,
                                        rules: ruleData,
                                        ruleTime: s_RuleTime,
                                        ruleTodo: s_RuleTodo,
                                        id: ruleId
                                    };
                                    var addRule = function (postData) {
                                        $.extend(postData, User);
                                        var ret = {};
                                        $.ajax({
                                            type: "post",
                                            //url: "https://zhitongche.libangjie.com/index.php?r=site/get-rule-add-rule-yun-data",
                                            url: server_url + '/taobao/api?r=site/get-rule-add-rule-yun-data',
                                            contentType: 'application/json',
                                            data: JSON.stringify(postData),
                                            async: false,
                                            dataType: "json",
                                            success: function (data, status) {
                                                ret = data;
                                            }
                                        });
                                        return ret;
                                    };// new Function("postData", getcfService("site/get-rule-add-rule-ajax-js", User));
                                    var ret = addRule(postData); //推送到云端
                                    layer.msg(ret.msg);
                                    if (ret.code == 200) {
                                        loadRules();
                                    };
                                    if (sId != -1) {
                                        layer.close(index);
                                    };
                                    return;
                                },
                            });
                        };// new Function("sId", getcfService("site/get-rule-add-rule-window-js", User));
                        OpenAddRuleBaiche(sIds[0]);
                    } else {
                        layer.msg("修改规则只能单选一条！");
                        return;
                    };

                });
                var baicheMain = function () {
                    campaignId = getQueryString('campaignId');
                    adGroupId = getQueryString('adGroupId');
                    $("#bt_StopRule").attr({ "disabled": "disabled" });
                    var StepTime = 60 * 1000;
                    bTimeId = window.setInterval(getServerDate, StepTime);  // 防止退出***
                };//new Function(getcfService("site/get-rule-baiche-main-js", User));
                baicheMain();
            };//new Function(getcfService("site/get-rule-window-js", User));
            openRuleRunWindow();
"""
dqgl = """
var strUI = '<div style="padding: 15px; line-height: 22px; background-color: #fff; color: #000;">' + '<div id="uaList" style="height:330px">' + '<span id="ua01">' + '青色分线 <button class="layui-btn layui-btn-mini layui-btn-normal">应用到当前计划</button><button class="layui-btn layui-btn-mini layui-btn-danger">删除</button>' + '<hr class="layui-bg-cyan">' + '</span>' + '<span id="ua02">' + '青色分割线 <button class="layui-btn layui-btn-mini layui-btn-normal">应用到当前计划</button><button class="layui-btn layui-btn-mini layui-btn-danger">删除</button>' + '<hr class="layui-bg-cyan">' + '</span>' + '</div>' + '<button class="layui-btn layui-btn-small layui-btn-normal" id="BakUserAreaBt">备份当前计划地区</button>' + '</div>';
                layer.open({
                    type: 1,
                    content: strUI,
                    area: ['600px', '450px'],
                    anim: 0,
                    title: ['计划地区管理', 'font-size:18px;'],
                    success: function (layero, index) {
                        var GetUserAreaList = function (postData) {
                            var ret = new Array();
                            $.ajax({
                                type: "post",
                                //url: "https://zhitongche.libangjie.com/index.php?r=site/get-area-yun-data",
                                url: server_url + '/taobao/api?r=site/get-area-yun-data',
                                contentType: "application/json",
                                data: JSON.stringify(User),
                                async: false, dataType: "json",
                                success: function (data) {
                                    if (data.code == 200) {
                                        ret = data.result;
                                    } else {
                                        layer.msg(data.msg);
                                    };
                                }
                            });
                            return ret;
                        };// new Function("postData", getcfService("site/get-area-yun-data-js", User));
                        var aList = GetUserAreaList();
                        //var SetUserAreaList = new Function("aList", getcfService("site/set-area-yun-data-js", User));
                        app.SetUserAreaList(aList);
                    }
                });

                $("#BakUserAreaBt").click(function () {
                    var camId = getUriInfo().campaignId;
                    if (camId == null) {
                        layer.msg("进入页面以后再备份地区数据！");
                        return;
                    };
                    var AreaGet = function (campaignId) {
                        var ret = "";
                        var postUrl = "https://subway.simba.taobao.com/area/get.htm?campaignId=" + campaignId;
                        $.ajax({
                            type: "Post", url: postUrl, data: "sla=json&isAjaxRequest=true&token=" + User.token,
                            dataType: "json", async: false, success: function (data) { ret = data.result.areaState; }, error: function () { }
                        });
                        return ret;
                    };// new Function("campaignId", getcfService("site/subway-get-area-js", User));
                    var areaStr = AreaGet(camId);
                    layer.prompt({
                        formType: 0, title: '请输入备份名称'
                    }, function (value, index, elem) {
                        var aData = { "Title": value, "Cnt": areaStr };
                        $.extend(aData, User);
                        var SaveUserArea = function (postData) {
                            var ret = new Array();
                            $.ajax({
                                type: "post",
                                //url: "https://zhitongche.libangjie.com/index.php?r=site/save-area-yun-data",
                                url: server_url + '/taobao/api?r=site/save-area-yun-data',
                                contentType: "application/json",
                                data: JSON.stringify(postData),
                                async: false, dataType: "json",
                                success: function (data, status) { if (data.code == 200) { ret = data.result; }; }
                            });
                            return ret;

                        };// new Function("postData", getcfService("site/save-area-yun-data-js", User));
                        var aList = SaveUserArea(aData);
                        //var SetUserAreaList = new Function("aList", getcfService("site/set-area-yun-data-js", User));
                        app.SetUserAreaList(aList);
                        layer.close(index);
                    });
                });
"""
pltj = """
if (!getUrlInfo()) { return };
            var cf_batchAddCrowd = function () {
                var MarkText = $("li.tabs-list.current:last").text().trim();
                var templateId = '12';
                if (MarkText == '人口属性人群') {
                    templateId = '12';
                } else if (MarkText == '天气人群') {
                    templateId = '11';
                } else if (MarkText == '自定义人群') {
                    var next_name = $("span.btn.btn-size25.fl.current").text().trim();
                    if (next_name == '天气属性人群') templateId = '11';
                } else {
                    layer.msg('<b>打个酱油!</b><br/>请先打开"人口属性人群" 或 "天气人群" Tab卡，勾选所需组合标签项，再点本按钮^_^完成批量添加！', { icon: 4 });
                    return;
                };

                var cf_getCatID = function (adGroupId) {
                var categoryId;
                    $.ajax({
                        type: "POST",
                        url: "https://subway.simba.taobao.com/adgroup/getAdGroupWithCategory.htm?adGroupId=" + adGroupId,
                        data: null,
                        async: false,
                        dataType: "json",
                        success: function (data) { if (data.code == "200") { categoryId = data.result.adGroupDTO.categoryId; }; },
                        error: function () { alert("error:getCatID"); }
                    });
                    return categoryId;
                };// new Function("adGroupId", getcfService("site/subway-get-cat-ids", User));
                var fristCat = cf_getCatID(UriInfo.adGroupId).split(' ')[0];
                var groupidArrs = new Array();
                var stringArrs = new Array();
                var tagIdArrs = new Array();
                var tagNameArrs = new Array();
                var i = 0;
                $(":checked[name='crowdAddCheckbox']").each(function () {
                    groupidArrs[i] = $(this).attr('groupid');
                    tagIdArrs[i] = $(this).attr('tagId');
                    tagNameArrs[i] = $(this).attr('tagName');
                    stringArrs[i] = '{"dimId":"' + $(this).attr('dimId') + '","tagId":"' + $(this).attr('tagId') + '","tagName":"' + $(this).attr('tagName') + '","optionGroupId":"' + $(this).attr('groupid') + '"}';
                    i++;
                });
                var tags = new Array();
                var tagNames = new Array();
                var TAs = new Array();
                var thisGid = "";
                var NumGid = 0;
                var at = 0;
                for (var i = 0; i < groupidArrs.length; i++) {
                    if (i > 0 && groupidArrs[i] != groupidArrs[i - 1]) {
                        NumGid = NumGid + 1;
                        at = 0;
                    };
                    if (thisGid != groupidArrs[i]) {
                        TAs[NumGid] = new Array();
                        tagNames[NumGid] = new Array();
                        TAs[NumGid][at] = stringArrs[i];
                        tagNames[NumGid][at] = tagNameArrs[i];
                        thisGid = groupidArrs[i];
                        at++;
                    } else {
                        TAs[NumGid][at] = stringArrs[i];
                        tagNames[NumGid][at] = tagNameArrs[i];
                        at++;
                    };
                };
                if (tagNames.length < 1) {
                    layer.msg("未勾选任何人群标签！");
                    return;
                };

                var cf_getArrZuhe = function (arr) {
                    var sarr = [[]];
                    for (var i = 0; i < arr.length; i++) {
                        var tarr = []; for (var j = 0; j < sarr.length; j++)
                            for (var k = 0; k < arr[i].length; k++)
                                tarr.push(sarr[j].concat(arr[i][k]));
                        sarr = tarr;
                    };
                    return sarr;
                };// new Function("arr", getcfService("site/get-arr-zuhe-js", User));
                var Names = cf_getArrZuhe(tagNames);

                /*
                if (tagNames.length > 1) {
                    if (!getUserRank(2,UserRank)) {
                        layer.msg('批量人群多项属性组合，需要对当前店铺（' + User.nickName + '）授权！\\n 未授权店铺只能批量添加单一属性标签\\n如需要多项属性任意组合标签请联系交流群管理授权店铺！');return;
                    };
                };
                */


                var TagsCode = cf_getArrZuhe(TAs);
                var discount = 105;
                if ($("input[placeholder='5-300整数']").val() != "") {
                    discount = 100 + parseInt($("input[placeholder='5-300整数']").val());
                };
                for (var i = 0; i < Names.length; i++) {
                    var getdata = 'productId=101001005&bizType=1&adgroupId=' + UriInfo.adGroupId + '&targetings=[{"crowdDTO":{"extParam":{"firstCat":"' + fristCat + '"},"templateId":' + templateId + ',"name":"' + Names[i].join(',') + '","tagList":[' + TagsCode[i].join(',') + ']},"isDefaultPrice":0,"priceMode":1,"discount":' + discount + '}]';
                    adgroupTargetingAdd(getdata, User.token);
                };
                layer.msg('批量人群标签添加完成，请刷新网页！');
            };// new Function(getcfService("site/add-batch-add-crowd-js", User));
            cf_batchAddCrowd();
"""
yhgj = """
if (!getUrlInfo()) { return };
            outerBidWordDataUI = function () {
                if (!adBidWordListData) return;
                var bdDataTable = new Array();
                for (var keyId in adBidWordListData) {
                    //PK点击率
                    if (adBidWordListData[keyId].ctr && adBidWordListData[keyId].ctr_hwl) {
                        if (parseFloat(adBidWordListData[keyId].ctr) > parseFloat(adBidWordListData[keyId].ctr_hwl)) {
                            adBidWordListData[keyId].pk_ctr = 1;
                        } else if (parseFloat(adBidWordListData[keyId].ctr) < parseFloat(adBidWordListData[keyId].ctr_hwl)) {
                            adBidWordListData[keyId].pk_ctr = -1;
                        } else {
                            adBidWordListData[keyId].pk_ctr = 0;
                        };
                    } else {
                        adBidWordListData[keyId].pk_ctr = null;
                    };
                    //PK转化率
                    if (adBidWordListData[keyId].coverage && adBidWordListData[keyId].cvr_hwl) {
                        if (parseFloat(adBidWordListData[keyId].coverage) > parseFloat(adBidWordListData[keyId].cvr_hwl)) {
                            adBidWordListData[keyId].pk_cvr = 1;
                        } else if (parseFloat(adBidWordListData[keyId].coverage) < parseFloat(adBidWordListData[keyId].cvr_hwl)) {
                            adBidWordListData[keyId].pk_cvr = -1;
                        } else {
                            adBidWordListData[keyId].pk_cvr = 0;
                        };
                    } else {
                        adBidWordListData[keyId].pk_cvr = null;
                    };
                    //PK平均点击单价
                    if (adBidWordListData[keyId].cpc && adBidWordListData[keyId].avgPrice_hwl) {
                        if (parseFloat(adBidWordListData[keyId].cpc) > parseFloat(adBidWordListData[keyId].avgPrice_hwl)) {
                            adBidWordListData[keyId].pk_cpc = 1;
                        } else if (parseFloat(adBidWordListData[keyId].cpc) < parseFloat(adBidWordListData[keyId].avgPrice_hwl)) {
                            adBidWordListData[keyId].pk_cpc = -1;
                        } else {
                            adBidWordListData[keyId].pk_cpc = 0;
                        };
                    } else {
                        adBidWordListData[keyId].pk_cpc = null;
                    };
                    //PK UV价值
                    if (adBidWordListData[keyId].uvvalue && adBidWordListData[keyId].uvvalue_hwl) {
                        if (adBidWordListData[keyId].uvvalue == adBidWordListData[keyId].uvvalue_hwl) {
                            adBidWordListData[keyId].pk_uvvalue = 0;
                        }
                        else {
                            adBidWordListData[keyId].pk_uvvalue = parseFloat(adBidWordListData[keyId].uvvalue) > parseFloat(adBidWordListData[keyId].uvvalue_hwl) ? 1 : -1;
                        }
                    }
                    else {
                        adBidWordListData[keyId].pk_uvvalue = null;
                    }
                    //PK ROI
                    if (adBidWordListData[keyId].roi && adBidWordListData[keyId].roi_hwl) {
                        if (adBidWordListData[keyId].roi == adBidWordListData[keyId].roi_hwl) {
                            adBidWordListData[keyId].pk_roi = 0;
                        }
                        else {
                            adBidWordListData[keyId].pk_roi = parseFloat(adBidWordListData[keyId].roi) > parseFloat(adBidWordListData[keyId].roi_hwl) ? 1 : -1;
                        }
                    }
                    else {
                        adBidWordListData[keyId].pk_roi = null;
                    }
                    bdDataTable.push(adBidWordListData[keyId]);
                };
                jQuery("#BidWordlist").jqGrid("clearGridData");
                jQuery("#BidWordlist").jqGrid("setGridParam", { data: bdDataTable });
                jQuery("#BidWordlist").trigger("reloadGrid");
            };// new Function(getcfService("site/get-bid-word-window-grid-taobao-world-tianchong-data", User));
            var cf_openBidWordWindow = function () {
                var w = $(window).width() - 3 + 10;
                //scrollbar:false, 加10PX\r\n    
                var h = $(window).height() - 5 + 10;
                //scrollbar:false,\r\n    
                var openArea = [w + 'px', h + 'px'];
                var index = layer.open({
                    type: 1, content: '<div>' +
                        '<div class="layui-form-item" style="margin-bottom: 2px;">' +
                        '     <label class="layui-form-label layui-btn" id="lb_selectDate">范围选择</label>'
                        + '       <div class="layui-input-inline">'
                        + '            <input class="layui-input" placeholder="开始日" id="LAY_Bidwordrange_s">'
                        + '       </div>'
                        + '        <div class="layui-input-inline">'
                        + '            <input class="layui-input" placeholder="截止日" id="LAY_Bidwordrange_e"> '
                        + '        </div>'
                        + '        <div class="layui-input-inline">'
                        + '             <div class="layui-btn-group"><button class="layui-btn layui-btn-primary" id="bt_getbidWordRpt">读取报表</button><button class="layui-btn layui-btn-warm" id="bt_getbidWordloadcat">读取行业</button></div>'
                        + '        </div>'
                        + '             <div><div class="layui-btn-group">'
                        + '<button class="layui-btn layui-btn-normal" id="bt_BidWordPPc">修改出价</button>'
                        + '<button class="layui-btn layui-btn-normal" id="bt_BidWordRegMode">修改匹配方式</button>'
                        + '<button class="layui-btn layui-btn-normal" id="bt_BidWorddelete">删除</button>'
                        + '<button class="layui-btn layui-btn-normal" id="bt_BidWordmark">标签</button>'
                        + '<button class="layui-btn layui-btn-danger" id="bt_BidWordYunWord">云关键词</button>'
                        //+ '<button class="layui-btn layui-btn-danger" href="#" id="bt_BidWorddaochuEXCEL" >导出EXCEL</button>'
                        + '</div></div>'
                        + '    </div>'
                        + '</div>'
                        + '<table id="BidWordlist"></table>'
                        + '<div id="BidWordpager"></div>'
                        + '',
                    area: openArea,
                    offset: ['5px', '1px'],
                    //title: ['关键词优化', 'font-size:18px;'],
                    title: false,
                    scrollbar: false,
                    //禁止浏览器滚动条
                    maxmin: false
                });
                //layer.full(index);
                var start = {
                    min: laydate.now(-30),
                    //-1代表昨天，-2代表前天，以此类推
                    max: laydate.now(),
                    istoday: true,
                    choose: function (datas) {
                        end.min = datas;
                        //开始日选好后，重置结束日的最小日期
                        end.start = datas //将结束日的初始值设定为开始日
                    }
                };
                var end = {
                    min: laydate.now(-30),
                    //-1代表昨天，-2代表前天，以此类推
                    max: laydate.now(),
                    istoday: true,
                    choose: function (datas) {
                        start.max = datas; //结束日选好后，重置开始日的最大日期
                    }
                };
                $("#lb_selectDate").click(function () {
                    var strSUI = '<button class="layui-btn layui-btn-mini layui-btn-primary datebt" data=0>今天</button>'
                        + '<button class="layui-btn layui-btn-mini layui-btn-primary datebt" data=-1>昨天</button>'
                        + '<button class="layui-btn layui-btn-mini layui-btn-primary datebt" data=-2>过去2天</button>'
                        + '<button class="layui-btn layui-btn-mini layui-btn-primary datebt" data=-3>过去3天</button>'
                        + '<button class="layui-btn layui-btn-mini layui-btn-primary datebt" data=-7>过去7天</button>'
                        + '<button class="layui-btn layui-btn-mini layui-btn-primary datebt" data=-14>过去14天</button>'
                        + '<button class="layui-btn layui-btn-mini layui-btn-primary datebt" data=-30>过去30天</button>';
                    layer.tips(strSUI, '#lb_selectDate', {
                        tips: [3, "#009688"]
                    });
                    $(".datebt").click(function () {
                        var sDt = $(this).attr("data");
                        $("#LAY_Bidwordrange_s").val(laydate.now(sDt));
                        $("#LAY_Bidwordrange_e").val(laydate.now(sDt < 0 ? -1 : 0));
                    });
                });
                document.getElementById('LAY_Bidwordrange_s').onclick = function () {
                    start.elem = this;
                    laydate(start);
                }
                document.getElementById('LAY_Bidwordrange_e').onclick = function () {
                    end.elem = this;
                    laydate(end);
                };
                //获取关键词爆表数据
                $("#bt_getbidWordRpt").click(function () {
                    var cf_do = function () {
                        var startDate = $("#LAY_Bidwordrange_s").val();
                        var endDate = $("#LAY_Bidwordrange_e").val();
                        var theDate = laydate.now();
                        if (startDate == "" && endDate == "") {
                            startDate = theDate;
                            endDate = theDate;
                        };
                        if (startDate == theDate) {
                            postUrl = "https://subway.simba.taobao.com/rtreport/rptBpp4pBidwordRealtimeSubwayList.htm?campaignid=" + UriInfo.campaignId + "&adgroupid=" + UriInfo.adGroupId + "&theDate=" + theDate + "&traffictype=1%2C2%2C4%2C5";
                        } else {
                            if (startDate > endDate) {
                                layer.msg("开始日期不能大于结束日期！请重新选择！");
                                return;
                            } else {
                                if (endDate >= theDate) {
                                    layer.msg("报表数据不能于实时(今日)同时拉取！请设置截止日期早于今日！");
                                    return;
                                };
                                postUrl = "https://subway.simba.taobao.com/report/commondList.htm?campaignid=" + UriInfo.campaignId + "&adgroupid=" + UriInfo.adGroupId + "&startDate=" + startDate + "&endDate=" + endDate + "&isshop=0&traffictype=1%2C2%2C4%2C5";
                            };
                        };
                        var index = layer.load(0, { shade: false });
                        $.ajax({
                            type: "POST",
                            url: postUrl,
                            data: "templateId=rptBpp4pBidwordSubwayList&sla=json&isAjaxRequest=true&token=" + User.token,
                            datatype: "json",
                            async: true,
                            success: function (data) {
                                var rptList = data.result;
                                //清除原数据        
                                for (var keyId in adBidWordListData) {
                                    adBidWordListData[keyId].impression = null;
                                    adBidWordListData[keyId].click = null;
                                    adBidWordListData[keyId].ctr = null;
                                    adBidWordListData[keyId].cpc = null;
                                    adBidWordListData[keyId].cost = null;
                                    adBidWordListData[keyId].coverage = null;
                                    adBidWordListData[keyId].roi = null;
                                    adBidWordListData[keyId].transactiontotal = null;
                                    adBidWordListData[keyId].transactionshippingtotal = null;
                                    adBidWordListData[keyId].carttotal = null;
                                    adBidWordListData[keyId].favtotal = null;
                                    adBidWordListData[keyId].avgpos = null;
                                    adBidWordListData[keyId].uvvalue = null;
                                };
                                for (var i = 0; i < rptList.length; i++) {
                                    var keyId = rptList[i].bidwordid;
                                    if (adBidWordListData[keyId]) {
                                        adBidWordListData[keyId].impression = rptList[i].impression ? (rptList[i].impression / 1).toFixed(0) : 0;
                                        adBidWordListData[keyId].click = rptList[i].click ? (rptList[i].click / 1).toFixed(0) : 0;
                                        adBidWordListData[keyId].ctr = rptList[i].ctr ? (rptList[i].ctr / 1).toFixed(2) : "0.00";
                                        adBidWordListData[keyId].cpc = rptList[i].cpc ? (rptList[i].cpc / 100).toFixed(2) : "0.00";
                                        adBidWordListData[keyId].cost = rptList[i].cost ? (rptList[i].cost / 100).toFixed(2) : "0.00";
                                        adBidWordListData[keyId].coverage = rptList[i].coverage ? (rptList[i].coverage / 1).toFixed(2) : "0.00";
                                        adBidWordListData[keyId].roi = rptList[i].roi ? (rptList[i].roi / 1).toFixed(2) : "0.00";
                                        adBidWordListData[keyId].transactiontotal = rptList[i].transactiontotal ? (rptList[i].transactiontotal / 100).toFixed(2) : "0.00";
                                        adBidWordListData[keyId].transactionshippingtotal = rptList[i].transactionshippingtotal ? (rptList[i].transactionshippingtotal / 1).toFixed(0) : 0;
                                        adBidWordListData[keyId].carttotal = rptList[i].carttotal ? (rptList[i].carttotal / 1).toFixed(0) : 0;
                                        adBidWordListData[keyId].favtotal = rptList[i].favtotal ? (rptList[i].favtotal / 1).toFixed(0) : 0;
                                        adBidWordListData[keyId].avgpos = rptList[i].avgpos ? (rptList[i].avgpos / 1).toFixed(0) : 0;
                                        adBidWordListData[keyId].uvvalue = rptList[i].transactiontotal ? (rptList[i].transactiontotal / (rptList[i].click * 100)).toFixed(2) : "0.00";
                                    };
                                };
                                //打印数据
                                outerBidWordDataUI();
                                $("#bidRptTime").text("报表数据[" + startDate + " -- " + endDate + "]");
                                layer.close(index);
                            },
                            error: function () { }
                        });
                    };// new Function(getcfService("site/get-bid-word-window-rpt", User));
                    cf_do();
                    return;
                });
                //获取行业数据
                $("#bt_getbidWordloadcat").click(function () {
                    var index = layer.load(0, { shade: false });
                    var cf_getBidStrCatData = function (index) {
                        var startDate = $("#LAY_Bidwordrange_s").val();
                        var endDate = $("#LAY_Bidwordrange_e").val();
                        var theDate = laydate.now(-1);
                        if ((startDate == "" && endDate == "") || (startDate == laydate.now() && endDate == laydate.now())) {
                            startDate = theDate;
                            endDate = theDate;
                        };
                        if (startDate > endDate) {
                            layer.msg("开始日期不能大于结束日期！请重新选择！");
                            return;
                        };

                        var cf_getBidStrCatDataAjax = function (keyId, postUrl, countWord, index) {
                            $.ajax({
                                type: "POST",
                                url: postUrl,
                                data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                datatype: "json",
                                async: false,
                                success: function (data) {
                                    var networkList = data.result;
                                    //清除原数据
                                    adBidWordListData[keyId].impression_hwl = null;
                                    adBidWordListData[keyId].impressionRate_hwl = null;
                                    adBidWordListData[keyId].click_hwl = null;
                                    adBidWordListData[keyId].ctr_hwl = null;
                                    adBidWordListData[keyId].cvr_hwl = null;
                                    adBidWordListData[keyId].avgPrice_hwl = null;
                                    adBidWordListData[keyId].competition_hwl = null;
                                    adBidWordListData[keyId].price_hwl = null;
                                    adBidWordListData[keyId].pct_hwl = null;
                                    adBidWordListData[keyId].uvvalue_hwl = null;
                                    adBidWordListData[keyId].roi_hwl = null;
                                    for (var i = 0; i < networkList.length; i++) {
                                        if (networkList[i].network == "3") {
                                            //PC行业数据
                                            adBidWordListData[keyId].avgPrice_hpc = (networkList[i].avgPrice / 100).toFixed(2);
                                        }
                                        else if (networkList[i].network == "4") {
                                            //无线行业数据
                                            adBidWordListData[keyId].impression_hwl = networkList[i].impression;
                                            adBidWordListData[keyId].impressionRate_hwl = (networkList[i].impressionRate / 100).toFixed(2);
                                            adBidWordListData[keyId].click_hwl = networkList[i].click;
                                            adBidWordListData[keyId].ctr_hwl = (networkList[i].ctr / 100).toFixed(2);
                                            adBidWordListData[keyId].cvr_hwl = (networkList[i].cvr / 100).toFixed(2);
                                            adBidWordListData[keyId].avgPrice_hwl = (networkList[i].avgPrice / 100).toFixed(2);
                                            adBidWordListData[keyId].competition_hwl = networkList[i].competition;
                                            adBidWordListData[keyId].price_hwl = (networkList[i].price / 100).toFixed(2);
                                            adBidWordListData[keyId].pct_hwl = (networkList[i].price * 100 / (networkList[i].click * networkList[i].cvr)).toFixed(2);
                                            adBidWordListData[keyId].uvvalue_hwl = (networkList[i].price / (100 * networkList[i].click)).toFixed(2);
                                            adBidWordListData[keyId].roi_hwl = (networkList[i].price / (networkList[i].click * networkList[i].avgPrice)).toFixed(2);
                                        };
                                    };
                                    if (countWord < 1) {
                                        outerBidWordDataUI();
                                        layer.close(index);
                                    };
                                },
                                error: function () {
                                }
                            });
                        };// new Function("keyId", "postUrl", "countWord", "index", getcfService("site/get-bid-word-window-cat-data-ajax", User));


                        //var index = layer.load(0, {shade: false});
                        var countWord = 0;
                        for (var keyId in adBidWordListData) { countWord++ };

                        for (var keyId in adBidWordListData) {
                            var bidwordStr = adBidWordListData[keyId].word;
                            var postUrl = 'https://subway.simba.taobao.com/report/getNetworkPerspective.htm?bidwordstr=' + bidwordStr + '&startDate=' + startDate + '&endDate=' + endDate + '&perspectiveType=2';
                            countWord--;

                            cf_getBidStrCatDataAjax(keyId, postUrl, countWord, index);
                            var dateStart = new Date(),
                                dateEnd;
                            while (((dateEnd = new Date()) - dateStart) <= 25) { }
                        };
                        $("#bidCatTime").text("无线行业数据[" + startDate + " -- " + endDate + "]");
                    };// new Function("index", getcfService("site/get-bid-word-window-cat-data", User));
                    setTimeout(function () { cf_getBidStrCatData(index); }, 1);
                });
                //修改价格 按钮被触发
                $("#bt_BidWordPPc").click(function () {
                    var cf_do = function () {
                        var divCont = '<button class="layui-btn layui-btn-normal" id="bt_BidWordPPc_wl">移动设备</button><br>'
                            + '<button class="layui-btn layui-btn-normal" id="bt_BidWordPPc_pc">计算机</button>';
                        var tipIndex = layer.tips(divCont, '#bt_BidWordPPc', { tips: [3, '#1E9FFF'] });
                        $("#bt_BidWordPPc_pc").click(function () {
                            layer.close(tipIndex);
                            var cf_editBidWrodPrice = function (pot) {
                                var sIds = getjqGridSelarrrow("#BidWordlist");
                                if (sIds.length < 1) {
                                    layer.msg("未选中任何关键词！");
                                    return;
                                };
                                var btnName = "";
                                var defPriceTip = '';
                                var defaultPrice;
                                var displayDefaultPrice;
                                var mobileDiscount;
                                var cf_getAdgroup = function (UriInfo, User) {
                                    var ret;
                                    $.ajax({
                                        type: "POST",
                                        url: "https://subway.simba.taobao.com/adgroup/get.htm?adGroupId=" + UriInfo.adGroupId,
                                        data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                        dataType: "json",
                                        async: false,
                                        success: function (data) {
                                            ret = data.result;
                                        },
                                        error: function () {
                                            alert("error:getAdgroup");
                                        }
                                    });
                                    return ret;
                                };// new Function("UriInfo", "User", getcfService("site/get-adgroup", User));
                                var result = cf_getAdgroup(UriInfo, User);
                                defaultPrice = result.defaultPrice;
                                displayDefaultPrice = result.displayDefaultPrice;
                                mobileDiscount = result.mobileDiscount;
                                if (pot == 0) {
                                    //修改计算机价格
                                    btnName = "修改计算机出价";
                                    defPriceTip = '<label for="radio_batchPrice02"><input type="radio" id="radio_batchPrice02"  name="batchMode" value="1">默认出价:</label><input type="text" id="batchMode_1_val" value='
                                        + displayDefaultPrice + ' class="input w60"/>元<i class="iconfont tpsHelp" data="1" style="color:red;cursor:help;">Ũ</i><br>';
                                } else {
                                    //修改移动价格
                                    btnName = "修改移动出价";
                                    defPriceTip = '<label for="radio_batchPrice02"><input type="radio" id="radio_batchPrice02"  name="batchMode" value="1">默认移动折扣:</label><input type="text" id="batchMode_1_val" value='
                                        + mobileDiscount + ' class="input w60"/>%<i class="iconfont tpsHelp" data="1" style="color:red;cursor:help;">Ũ</i><br>';
                                };
                                var divPriceUi = '<div style="padding: 15px; line-height: 22px; background-color: #fff; color: #000;">'
                                    //+'<form class="layui-form" action="">'
                                    //+'<div class="layui-form-item">'
                                    + '<div class="">'
                                    + '<label for="radio_batchPrice01"><input type="radio" id="radio_batchPrice01" name="batchMode" value="0" checked="">自定义出价：</label><input id="batchMode_0_val" type="text" class="input w60"/>元<i class="iconfont tpsHelp" data="0" style="color:red;cursor:help;">Ũ</i><br>'
                                    + defPriceTip
                                    + '<label for="radio_batchPrice03"><input type="radio" id="radio_batchPrice03" name="batchMode" value="2">首条出价，最高限价：</label><input id="batchMode_2_val"  type="text" class="input w60"/>元<i class="iconfont tpsHelp" data="2" style="color:red;cursor:help;">Ũ</i><br>'
                                    + '<label for="radio_batchPrice04"><input type="radio" id="radio_batchPrice04" name="batchMode" value="3">市场均价出价，最高限价：</label><input id="batchMode_3_val"  type="text" class="input w60"/>元<i class="iconfont tpsHelp" data="3" style="color:red;cursor:help;">Ũ</i><br>'
                                    + '<label for="radio_batchPrice05"><input type="radio" id="radio_batchPrice05" name="batchMode" value="4"> + / - 出价幅度：</label><select class="input" id="batchMode_4_opt" style="width:55px"><option value=1 selected>+</option><option value=-1>-</option></select><input id="batchMode_4_val" type="text" class="input w60"/>元<i class="iconfont tpsHelp" data="4" style="color:red;cursor:help;">Ũ</i><br>'
                                    + '<label for="radio_batchPrice06"><input type="radio" id="radio_batchPrice06" name="batchMode" value="5"> + / - 出价百分比：</label><select class="input" id="batchMode_5_opt" style="width:55px"><option value=1 selected>+</option><option value=-1>-</option></select><input id="batchMode_5_val" type="text" class="input w60"/>%<i class="iconfont tpsHelp" data="5" style="color:red;cursor:help;">Ũ</i>'
                                    + '</div>'
                                    //+'</div>'
                                    //+'</form>'
                                    + '</div>';
                                layer.open({
                                    type: 1,
                                    closeBtn: false,
                                    area: '350px;',
                                    //shade: 0.8,
                                    id: 'LAY_layuipro',
                                    //设定一个id，防止重复弹出
                                    resize: false,
                                    btn: ['修改', '取消'],
                                    moveType: 1,
                                    //拖拽模式，0或者1
                                    content: divPriceUi,
                                    success: function (layero) {
                                        var btn = layero.find('.layui-layer-btn');
                                        btn.find('.layui-layer-btn0').click(function () {
                                            var batchMode = $("input[name='batchMode'][type='radio']:checked").val();
                                            var tVal = $("#batchMode_" + batchMode + "_val").val();
                                            var ptVal = 0;
                                            ptVal = parseFloat(tVal) * 100;
                                            var newPrice;
                                            var isDefaultPrice = "0";
                                            var maxPriceStr = "maxPrice";
                                            var isDefaultPriceStr = "isDefaultPrice";
                                            var type = "pc";
                                            var avgPriceStr = "avgPrice_hpc";
                                            var fp_priceStr = "pc_fp_price";
                                            if (pot == 1) {
                                                type = "mobile";
                                                maxPriceStr = "maxMobilePrice";
                                                isDefaultPriceStr = "mobileIsDefaultPrice";
                                                avgPriceStr = "avgPrice_hwl";
                                                fp_priceStr = "wireless_fp_price";
                                            };
                                            //自定义出价
                                            if (batchMode == 0) {
                                                //ptVal = parseFloat(tVal)*100;
                                                if (!tVal) {
                                                    layer.msg("请确认输入出价出价或者调价幅度！");
                                                    return;
                                                };
                                                newPrice = ptVal;
                                            };
                                            //推广单元默认出价
                                            if (batchMode == 1) {
                                                newPrice = 0;
                                                isDefaultPrice = "1";
                                                if (type == "pc" && tVal != displayDefaultPrice) {
                                                    //DefaultPrice, adgid, async修改推广单元默认出价
                                                    var cf_updateAdGroupDefaultPrice = function (DefaultPrice) {
                                                        $.ajax({
                                                            type: "post",
                                                            url: "https://subway.simba.taobao.com/adgroup/updateAdGroupDefaultPrice.htm",
                                                            data: "adGroupIds=[" + adgid + "]&defaultPrice=" + DefaultPrice + "&sla=json&isAjaxRequest=true&token=" + User.token,
                                                            async: async,
                                                            success: function (data) {
                                                                if (data.code == 200) {
                                                                    return true;
                                                                } else {
                                                                    return false;
                                                                };
                                                            },
                                                            error: function () { return false; }
                                                        });
                                                    };// new Function("DefaultPrice", "adgid", "async", getcfService("site/subway-update-ad-group-default-price", User));
                                                    cf_updateAdGroupDefaultPrice(ptVal, UriInfo.adGroupId, true);
                                                };
                                                if (type == "mobile" && tVal != mobileDiscount) {
                                                    //adGid, mobileDiscount, async设置推广单元移动折扣价1%
                                                    var cf_updateAdGroupMobileDiscount = function (adGid, mobileDiscount, async) {
                                                        var postdata = "adGroupIds=[" + adGid + "]&mobileDiscount=" + mobileDiscount + "&sla=json&isAjaxRequest=true&token=" + User.token;
                                                        $.ajax({
                                                            type: "POST",
                                                            url: "https://subway.simba.taobao.com/adgroup/updateAdGroupMobileDiscount.htm",
                                                            data: postdata,
                                                            dataType: "json",
                                                            async: async,
                                                            success: function (data) {
                                                                if (data.code == 200) { }
                                                                else { alert(data.msg[0]); }
                                                            },
                                                            error: function () {
                                                                alert("error:updateAdGroupMobileDiscount");
                                                            }
                                                        });
                                                    }; //new Function("adGid", "mobileDiscount", "async", getcfService("site/subway-update-ad-group-mobile-discount", User));
                                                    cf_updateAdGroupMobileDiscount(UriInfo.adGroupId, tVal, true);
                                                };
                                            };
                                            //市场价出价模式  验证
                                            if (batchMode == 3) {
                                                var tid = jQuery("#BidWordlist").jqGrid('getCell', sIds[0], 'keywordId');
                                                if (!adBidWordListData[tid].avgPrice_hpc) {
                                                    layer.msg("请先拉取行业数据报表！");
                                                    return;
                                                };
                                            };
                                            //根据首条出价
                                            if (batchMode == 2) {
                                                var getPriceKeyIdStr = new Array();
                                                for (var i = 0; i < sIds.length; i++) {
                                                    var keywordId = jQuery("#BidWordlist").jqGrid('getCell', sIds[i], 'keywordId');
                                                    getPriceKeyIdStr[i] = 'bidwordIds=' + keywordId;
                                                };
                                                var cf_getPriceBatchStrategy = function (adgid, bidwordIds, type, async) {
                                                    $.ajax({
                                                        type: "post",
                                                        url: "https://subway.simba.taobao.com/bidword/tool/bidword/getPriceBatchStrategy.htm",
                                                        data: "adGroupId=" + adgid + "&" + bidwordIds + "&type=" + type + "&sla=json&isAjaxRequest=true&token=" + User.token,
                                                        async: async,
                                                        success: function (data) {
                                                            if (data.code == 200) {
                                                                var res = data.result;
                                                                for (var i = 0; i < res.length; i++) {
                                                                    //pc_fp_price
                                                                    if (type == "pc") {
                                                                        adBidWordListData[res[i].bidwordid].pc_fp_price = res[i].pc_fp_price;
                                                                    };
                                                                    //wireless_fp_price
                                                                    if (type == "mobile") {
                                                                        adBidWordListData[res[i].bidwordid].wireless_fp_price = res[i].wireless_fp_price;
                                                                    };
                                                                };
                                                            };
                                                        },
                                                        error: function () { }
                                                    });
                                                };// new Function("adgid", "bidwordIds", "type", "async", getcfService("site/subway-get-price-batch-strategy", User));
                                                cf_getPriceBatchStrategy(UriInfo.adGroupId, getPriceKeyIdStr.join("&"), type, false);
                                                //return;
                                            };
                                            var isAdd = 1;
                                            //根据 现在价格提高幅度 元
                                            if (batchMode == 4) {
                                                if (!tVal) {
                                                    layer.msg("请确认输入出价出价或者调价幅度！");
                                                    return;
                                                };
                                                isAdd = parseInt($("#batchMode_4_opt").val());
                                            };
                                            //根据 现在价格提高幅度 %
                                            if (batchMode == 5) {
                                                if (!tVal) {
                                                    layer.msg("请确认输入出价出价或者调价幅度！");
                                                    return;
                                                };
                                                isAdd = parseInt($("#batchMode_5_opt").val());
                                            };
                                            var keywords = new Array();
                                            var editKeyIds = new Array();
                                            for (var i = 0; i < sIds.length; i++) {
                                                var keywordId = jQuery("#BidWordlist").jqGrid('getCell', sIds[i], 'keywordId');
                                                editKeyIds[i] = keywordId;
                                                //市场价出价模式 出价与限价
                                                if (batchMode == 3) {
                                                    var avgPrice = parseFloat(adBidWordListData[keywordId][avgPriceStr]) * 100;
                                                    if (ptVal > 5) {
                                                        newPrice = avgPrice > ptVal ? ptVal : avgPrice;
                                                    } else {
                                                        newPrice = avgPrice;
                                                    };
                                                };
                                                //首条与限价
                                                if (batchMode == 2) {
                                                    newPrice = adBidWordListData[keywordId][fp_priceStr] > 0 ? adBidWordListData[keywordId][fp_priceStr] : (adBidWordListData[keywordId][maxPriceStr] * 100);
                                                    if (ptVal > 5) {
                                                        newPrice = newPrice > ptVal ? ptVal : newPrice;
                                                    };
                                                };
                                                // 提高幅度 元
                                                if (batchMode == 4) {
                                                    newPrice = (parseFloat(adBidWordListData[keywordId][maxPriceStr]) * 100) + isAdd * ptVal;
                                                    newPrice = newPrice > 5 ? newPrice : 5;
                                                };
                                                // 提高幅度 %
                                                if (batchMode == 5) {
                                                    newPrice = (parseFloat(adBidWordListData[keywordId][maxPriceStr]) * (1 + isAdd * tVal / 100)) * 100;
                                                    newPrice = newPrice > 5 ? newPrice : 5;
                                                };
                                                var pMode = '{"keywordId":"' + keywordId + '","' + maxPriceStr + '":' + newPrice + ',"' + isDefaultPriceStr + '":' + isDefaultPrice + '}';
                                                keywords[i] = pMode;
                                                if (isDefaultPrice == "0") {
                                                    adBidWordListData[keywordId][maxPriceStr] = (newPrice / 100).toFixed(2);
                                                } else {
                                                    if (type == "pc") {
                                                        adBidWordListData[keywordId][maxPriceStr] = tVal;
                                                    } else {
                                                        adBidWordListData[keywordId][maxPriceStr] = (parseFloat(adBidWordListData[keywordId].maxPrice) * tVal / 100).toFixed(2);
                                                    };
                                                    adBidWordListData[keywordId][isDefaultPriceStr] = isDefaultPrice;
                                                };
                                            };
                                            var postData = 'keywords=[' + keywords.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                            $.ajax({
                                                type: "POST",
                                                url: "https://subway.simba.taobao.com/bidword/updatePrice.htm",
                                                data: postData, async: false,
                                                success: function (data) {
                                                    outerBidWordDataUI();
                                                },
                                                error: function () { }
                                            });
                                        });
                                        $(".tpsHelp").each(function () {
                                            $(this).click(function () {
                                                var indexd = $(this).attr("data");
                                                var tpsCnt = "";
                                                if (indexd == "0") {
                                                    tpsCnt = "出价只能是0.05到<br>99.99之间的数字！";
                                                }
                                                if (indexd == "1") {
                                                    tpsCnt = "如更改值，将会同步设置到推广单元！";
                                                };
                                                if (indexd == "2") {
                                                    tpsCnt = "留空，表示不设置最高限价;<br>设置限价，关键词最高出价不超此价！";
                                                };
                                                if (indexd == "3") {
                                                    tpsCnt = "设置前请先拉取行业数据;<br>留空，表示不设置最高限价;<br>设置限价，关键词最高出价不超此价！";
                                                };
                                                if (indexd == "4") {
                                                    tpsCnt = "如最低出价小于0.05元，<br>将按照0.05元出价";
                                                };
                                                if (indexd == "5") {
                                                    tpsCnt = "如最低出价小于0.05元，<br>将按照0.05元出价";
                                                };
                                                layer.tips(tpsCnt, this);
                                            })
                                        });
                                    },
                                    title: [btnName, 'font-size:18px;']
                                });
                            };// new Function("pot", getcfService("site/get-bid-word-window-ppc-pc", User));
                            cf_editBidWrodPrice(0);
                        });
                        $("#bt_BidWordPPc_wl").click(function () {
                            /*
                            if (!getUserRank(2,UserRank)) {
                                layer.msg('批量移动出价 需要权限黄金版以上！<br/>需要对当前店铺（' + User.nickName + '）授权！<br/> 请联系交流群管理授权！');
                                return;
                            };
                            */

                            layer.close(tipIndex);
                            var cf_editBidWrodPrice = function (pot) {
                                var sIds = getjqGridSelarrrow("#BidWordlist");
                                if (sIds.length < 1) {
                                    layer.msg("未选中任何关键词！");
                                    return;
                                };
                                var btnName = "";
                                var defPriceTip = '';
                                var defaultPrice;
                                var displayDefaultPrice;
                                var mobileDiscount;
                                var cf_getAdgroup = function (UriInfo, User) {
                                    var ret;
                                    $.ajax({
                                        type: "POST",
                                        url: "https://subway.simba.taobao.com/adgroup/get.htm?adGroupId=" + UriInfo.adGroupId,
                                        data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                        dataType: "json",
                                        async: false,
                                        success: function (data) {
                                            ret = data.result;
                                        },
                                        error: function () {
                                            alert("error:getAdgroup");
                                        }
                                    });
                                    return ret;
                                };// new Function("UriInfo", "User", getcfService("site/get-adgroup", User));
                                var result = cf_getAdgroup(UriInfo, User);
                                defaultPrice = result.defaultPrice;
                                displayDefaultPrice = result.displayDefaultPrice;
                                mobileDiscount = result.mobileDiscount;
                                if (pot == 0) {
                                    //修改计算机价格
                                    btnName = "修改计算机出价";
                                    defPriceTip = '<label for="radio_batchPrice02"><input type="radio" id="radio_batchPrice02"  name="batchMode" value="1">默认出价:</label><input type="text" id="batchMode_1_val" value='
                                        + displayDefaultPrice + ' class="input w60"/>元<i class="iconfont tpsHelp" data="1" style="color:red;cursor:help;">Ũ</i><br>';
                                } else {
                                    //修改移动价格
                                    btnName = "修改移动出价";
                                    defPriceTip = '<label for="radio_batchPrice02"><input type="radio" id="radio_batchPrice02"  name="batchMode" value="1">默认移动折扣:</label><input type="text" id="batchMode_1_val" value='
                                        + mobileDiscount + ' class="input w60"/>%<i class="iconfont tpsHelp" data="1" style="color:red;cursor:help;">Ũ</i><br>';
                                };
                                var divPriceUi = '<div style="padding: 15px; line-height: 22px; background-color: #fff; color: #000;">'
                                    //+'<form class="layui-form" action="">'
                                    //+'<div class="layui-form-item">'
                                    + '<div class="">'
                                    + '<label for="radio_batchPrice01"><input type="radio" id="radio_batchPrice01" name="batchMode" value="0" checked="">自定义出价：</label><input id="batchMode_0_val" type="text" class="input w60"/>元<i class="iconfont tpsHelp" data="0" style="color:red;cursor:help;">Ũ</i><br>'
                                    + defPriceTip
                                    + '<label for="radio_batchPrice03"><input type="radio" id="radio_batchPrice03" name="batchMode" value="2">首条出价，最高限价：</label><input id="batchMode_2_val"  type="text" class="input w60"/>元<i class="iconfont tpsHelp" data="2" style="color:red;cursor:help;">Ũ</i><br>'
                                    + '<label for="radio_batchPrice04"><input type="radio" id="radio_batchPrice04" name="batchMode" value="3">市场均价出价，最高限价：</label><input id="batchMode_3_val"  type="text" class="input w60"/>元<i class="iconfont tpsHelp" data="3" style="color:red;cursor:help;">Ũ</i><br>'
                                    + '<label for="radio_batchPrice05"><input type="radio" id="radio_batchPrice05" name="batchMode" value="4"> + / - 出价幅度：</label><select class="input" id="batchMode_4_opt" style="width:55px"><option value=1 selected>+</option><option value=-1>-</option></select><input id="batchMode_4_val" type="text" class="input w60"/>元<i class="iconfont tpsHelp" data="4" style="color:red;cursor:help;">Ũ</i><br>'
                                    + '<label for="radio_batchPrice06"><input type="radio" id="radio_batchPrice06" name="batchMode" value="5"> + / - 出价百分比：</label><select class="input" id="batchMode_5_opt" style="width:55px"><option value=1 selected>+</option><option value=-1>-</option></select><input id="batchMode_5_val" type="text" class="input w60"/>%<i class="iconfont tpsHelp" data="5" style="color:red;cursor:help;">Ũ</i>'
                                    + '</div>'
                                    //+'</div>'
                                    //+'</form>'
                                    + '</div>';
                                layer.open({
                                    type: 1,
                                    closeBtn: false,
                                    area: '350px;',
                                    //shade: 0.8,
                                    id: 'LAY_layuipro',
                                    //设定一个id，防止重复弹出
                                    resize: false,
                                    btn: ['修改', '取消'],
                                    moveType: 1,
                                    //拖拽模式，0或者1
                                    content: divPriceUi,
                                    success: function (layero) {
                                        var btn = layero.find('.layui-layer-btn');
                                        btn.find('.layui-layer-btn0').click(function () {
                                            var batchMode = $("input[name='batchMode'][type='radio']:checked").val();
                                            var tVal = $("#batchMode_" + batchMode + "_val").val();
                                            var ptVal = 0;
                                            ptVal = parseFloat(tVal) * 100;
                                            var newPrice;
                                            var isDefaultPrice = "0";
                                            var maxPriceStr = "maxPrice";
                                            var isDefaultPriceStr = "isDefaultPrice";
                                            var type = "pc";
                                            var avgPriceStr = "avgPrice_hpc";
                                            var fp_priceStr = "pc_fp_price";
                                            if (pot == 1) {
                                                type = "mobile";
                                                maxPriceStr = "maxMobilePrice";
                                                isDefaultPriceStr = "mobileIsDefaultPrice";
                                                avgPriceStr = "avgPrice_hwl";
                                                fp_priceStr = "wireless_fp_price";
                                            };
                                            //自定义出价
                                            if (batchMode == 0) {
                                                //ptVal = parseFloat(tVal)*100;
                                                if (!tVal) {
                                                    layer.msg("请确认输入出价出价或者调价幅度！");
                                                    return;
                                                };
                                                newPrice = ptVal;
                                            };
                                            //推广单元默认出价
                                            if (batchMode == 1) {
                                                newPrice = 0;
                                                isDefaultPrice = "1";
                                                if (type == "pc" && tVal != displayDefaultPrice) {
                                                    //DefaultPrice, adgid, async修改推广单元默认出价
                                                    var cf_updateAdGroupDefaultPrice = function (DefaultPrice, adgid, async) {
                                                        $.ajax({
                                                            type: "post",
                                                            url: "https://subway.simba.taobao.com/adgroup/updateAdGroupDefaultPrice.htm",
                                                            data: "adGroupIds=[" + adgid + "]&defaultPrice=" + DefaultPrice + "&sla=json&isAjaxRequest=true&token=" + User.token,
                                                            async: async,
                                                            success: function (data) {
                                                                if (data.code == 200) {
                                                                    return true;
                                                                } else {
                                                                    return false;
                                                                };
                                                            },
                                                            error: function () { return false; }
                                                        });
                                                    };// new Function("DefaultPrice", "adgid", "async", getcfService("site/subway-update-ad-group-default-price", User));
                                                    cf_updateAdGroupDefaultPrice(ptVal, UriInfo.adGroupId, true);
                                                };
                                                if (type == "mobile" && tVal != mobileDiscount) {
                                                    //adGid, mobileDiscount, async设置推广单元移动折扣价1%
                                                    var cf_updateAdGroupMobileDiscount = function (adGid, mobileDiscount, async) {
                                                        var postdata = "adGroupIds=[" + adGid + "]&mobileDiscount=" + mobileDiscount + "&sla=json&isAjaxRequest=true&token=" + User.token;
                                                        $.ajax({
                                                            type: "POST",
                                                            url: "https://subway.simba.taobao.com/adgroup/updateAdGroupMobileDiscount.htm",
                                                            data: postdata,
                                                            dataType: "json",
                                                            async: async,
                                                            success: function (data) {
                                                                if (data.code == 200) { }
                                                                else { alert(data.msg[0]); }
                                                            },
                                                            error: function () {
                                                                alert("error:updateAdGroupMobileDiscount");
                                                            }
                                                        });
                                                    };// new Function("adGid", "mobileDiscount", "async", getcfService("site/subway-update-ad-group-mobile-discount", User));
                                                    cf_updateAdGroupMobileDiscount(UriInfo.adGroupId, tVal, true);
                                                };
                                            };
                                            //市场价出价模式  验证
                                            if (batchMode == 3) {
                                                var tid = jQuery("#BidWordlist").jqGrid('getCell', sIds[0], 'keywordId');
                                                if (!adBidWordListData[tid].avgPrice_hpc) {
                                                    layer.msg("请先拉取行业数据报表！");
                                                    return;
                                                };
                                            };
                                            //根据首条出价
                                            if (batchMode == 2) {
                                                var getPriceKeyIdStr = new Array();
                                                for (var i = 0; i < sIds.length; i++) {
                                                    var keywordId = jQuery("#BidWordlist").jqGrid('getCell', sIds[i], 'keywordId');
                                                    getPriceKeyIdStr[i] = 'bidwordIds=' + keywordId;
                                                };
                                                var cf_getPriceBatchStrategy = new Function("adgid", "bidwordIds", "type", "async", getcfService("site/subway-get-price-batch-strategy", User));
                                                cf_getPriceBatchStrategy(UriInfo.adGroupId, getPriceKeyIdStr.join("&"), type, false);
                                                //return;
                                            };
                                            var isAdd = 1;
                                            //根据 现在价格提高幅度 元
                                            if (batchMode == 4) {
                                                if (!tVal) {
                                                    layer.msg("请确认输入出价出价或者调价幅度！");
                                                    return;
                                                };
                                                isAdd = parseInt($("#batchMode_4_opt").val());
                                            };
                                            //根据 现在价格提高幅度 %
                                            if (batchMode == 5) {
                                                if (!tVal) {
                                                    layer.msg("请确认输入出价出价或者调价幅度！");
                                                    return;
                                                };
                                                isAdd = parseInt($("#batchMode_5_opt").val());
                                            };
                                            var keywords = new Array();
                                            var editKeyIds = new Array();
                                            for (var i = 0; i < sIds.length; i++) {
                                                var keywordId = jQuery("#BidWordlist").jqGrid('getCell', sIds[i], 'keywordId');
                                                editKeyIds[i] = keywordId;
                                                //市场价出价模式 出价与限价
                                                if (batchMode == 3) {
                                                    var avgPrice = parseFloat(adBidWordListData[keywordId][avgPriceStr]) * 100;
                                                    if (ptVal > 5) {
                                                        newPrice = avgPrice > ptVal ? ptVal : avgPrice;
                                                    } else {
                                                        newPrice = avgPrice;
                                                    };
                                                };
                                                //首条与限价
                                                if (batchMode == 2) {
                                                    newPrice = adBidWordListData[keywordId][fp_priceStr] > 0 ? adBidWordListData[keywordId][fp_priceStr] : (adBidWordListData[keywordId][maxPriceStr] * 100);
                                                    if (ptVal > 5) {
                                                        newPrice = newPrice > ptVal ? ptVal : newPrice;
                                                    };
                                                };
                                                // 提高幅度 元
                                                if (batchMode == 4) {
                                                    newPrice = (parseFloat(adBidWordListData[keywordId][maxPriceStr]) * 100) + isAdd * ptVal;
                                                    newPrice = newPrice > 5 ? newPrice : 5;
                                                };
                                                // 提高幅度 %
                                                if (batchMode == 5) {
                                                    newPrice = (parseFloat(adBidWordListData[keywordId][maxPriceStr]) * (1 + isAdd * tVal / 100)) * 100;
                                                    newPrice = newPrice > 5 ? newPrice : 5;
                                                };
                                                var pMode = '{"keywordId":"' + keywordId + '","' + maxPriceStr + '":' + newPrice + ',"' + isDefaultPriceStr + '":' + isDefaultPrice + '}';
                                                keywords[i] = pMode;
                                                if (isDefaultPrice == "0") {
                                                    adBidWordListData[keywordId][maxPriceStr] = (newPrice / 100).toFixed(2);
                                                } else {
                                                    if (type == "pc") {
                                                        adBidWordListData[keywordId][maxPriceStr] = tVal;
                                                    } else {
                                                        adBidWordListData[keywordId][maxPriceStr] = (parseFloat(adBidWordListData[keywordId].maxPrice) * tVal / 100).toFixed(2);
                                                    };
                                                    adBidWordListData[keywordId][isDefaultPriceStr] = isDefaultPrice;
                                                };
                                            };
                                            var postData = 'keywords=[' + keywords.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                            $.ajax({
                                                type: "POST",
                                                url: "https://subway.simba.taobao.com/bidword/updatePrice.htm",
                                                data: postData, async: false,
                                                success: function (data) {
                                                    outerBidWordDataUI();
                                                },
                                                error: function () { }
                                            });
                                        });
                                        $(".tpsHelp").each(function () {
                                            $(this).click(function () {
                                                var indexd = $(this).attr("data");
                                                var tpsCnt = "";
                                                if (indexd == "0") {
                                                    tpsCnt = "出价只能是0.05到<br>99.99之间的数字！";
                                                }
                                                if (indexd == "1") {
                                                    tpsCnt = "如更改值，将会同步设置到推广单元！";
                                                };
                                                if (indexd == "2") {
                                                    tpsCnt = "留空，表示不设置最高限价;<br>设置限价，关键词最高出价不超此价！";
                                                };
                                                if (indexd == "3") {
                                                    tpsCnt = "设置前请先拉取行业数据;<br>留空，表示不设置最高限价;<br>设置限价，关键词最高出价不超此价！";
                                                };
                                                if (indexd == "4") {
                                                    tpsCnt = "如最低出价小于0.05元，<br>将按照0.05元出价";
                                                };
                                                if (indexd == "5") {
                                                    tpsCnt = "如最低出价小于0.05元，<br>将按照0.05元出价";
                                                };
                                                layer.tips(tpsCnt, this);
                                            })
                                        });
                                    },
                                    title: [btnName, 'font-size:18px;']
                                });
                            };// new Function("pot", getcfService("site/get-bid-word-window-ppc-mobile", User));
                            cf_editBidWrodPrice(1);
                        });
                    };// new Function(getcfService("site/get-bid-word-window-ppc", User));
                    cf_do();
                    return;
                });
                //修改匹配方式 按钮被触发
                $("#bt_BidWordRegMode").click(function () {
                    var cf_do = function () {
                        /*
    if (!getUserRank(2, UserRank)) {
        layer.msg('修改匹配方式 需要权限黄金版以上！<br/>需要对当前店铺（' + User.nickName + '）授权！<br/> 请联系交流群管理授权！');
        return;
    };
    */
                        var divCont = '<button class="layui-btn layui-btn-normal" id="bt_BidWordRegMode_4">广泛匹配</button><br>'
                            + '<button class="layui-btn layui-btn-normal" id="bt_BidWordRegMode_1">精准匹配</button>';
                        var tipIndex = layer.tips(divCont, '#bt_BidWordRegMode', { tips: [3, '#1E9FFF'] });
                        $("#bt_BidWordRegMode_4").click(function () {
                            var cf_updateMatch = function (matchScope) {
                                var sIds = getjqGridSelarrrow("#BidWordlist");
                                if (sIds.length < 1) {
                                    layer.msg("未选中任何关键词！");
                                    return;
                                };
                                var keywords = new Array();
                                for (var i = 0; i < sIds.length; i++) {
                                    var keywordId = jQuery("#BidWordlist").jqGrid('getCell', sIds[i], 'keywordId');
                                    var pMode = '{"keywordId":"' + keywordId + '","matchScope":' + matchScope + '}';
                                    adBidWordListData[keywordId].matchScope = matchScope;
                                    keywords[i] = pMode;
                                };
                                var postData = 'keywords=[' + keywords.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                $.ajax({
                                    type: "POST",
                                    url: "https://subway.simba.taobao.com/bidword/updateMatch.htm",
                                    data: postData,
                                    async: true,
                                    datatype: "json",
                                    success: function (data) {
                                        if (data.code == 200) {
                                            outerBidWordDataUI();
                                        };
                                    },
                                    error: function () { }
                                });

                            };// new Function("matchScope", getcfService("site/get-bid-word-reg-mode-update-js", User));
                            cf_updateMatch("4");
                            layer.close(tipIndex);
                        });
                        $("#bt_BidWordRegMode_1").click(function () {
                            var cf_updateMatch = function (matchScope) {
                                var sIds = getjqGridSelarrrow("#BidWordlist");
                                if (sIds.length < 1) {
                                    layer.msg("未选中任何关键词！");
                                    return;
                                };
                                var keywords = new Array();
                                for (var i = 0; i < sIds.length; i++) {
                                    var keywordId = jQuery("#BidWordlist").jqGrid('getCell', sIds[i], 'keywordId');
                                    var pMode = '{"keywordId":"' + keywordId + '","matchScope":' + matchScope + '}';
                                    adBidWordListData[keywordId].matchScope = matchScope;
                                    keywords[i] = pMode;
                                };
                                var postData = 'keywords=[' + keywords.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                $.ajax({
                                    type: "POST",
                                    url: "https://subway.simba.taobao.com/bidword/updateMatch.htm",
                                    data: postData,
                                    async: true,
                                    datatype: "json",
                                    success: function (data) {
                                        if (data.code == 200) {
                                            outerBidWordDataUI();
                                        };
                                    },
                                    error: function () { }
                                });
                            };// new Function("matchScope", getcfService("site/get-bid-word-reg-mode-update-js", User));
                            cf_updateMatch("1");
                            layer.close(tipIndex);
                        });
                    };// new Function(getcfService("site/get-bid-word-reg-mode-js", User));
                    cf_do();
                    return;
                });
                //删除 按钮
                $("#bt_BidWorddelete").click(function () {
                    var cf_do = function () {
                        /*
    if (!getUserRank(2,UserRank)) {
        layer.msg("批量删除关键词功能 需要权限黄金版以上！<br/>需要对当前店铺（" + User.nickName + "）授权！<br/> 请联系交流群管理授权！");
        return;
    };
    */
                        layer.confirm("确定要删除这些人关键词?一旦删除，所有数据将无法恢复！", { icon: 3, title: "确认删除" }, function (index) {
                            var cf_bidwordDelete = function () {
                                var sIds = getjqGridSelarrrow("#BidWordlist");
                                if (sIds.length < 1) {
                                    layer.msg("未选中任何关键词！");
                                    return;
                                };
                                var keywords = new Array();
                                for (var i = 0; i < sIds.length; i++) {
                                    var keywordId = jQuery("#BidWordlist").jqGrid("getCell", sIds[i], "keywordId");
                                    var pMode = keywordId;
                                    delete adBidWordListData[keywordId];
                                    keywords[i] = pMode;
                                };

                                var postData = "campaignId=" + UriInfo.campaignId + "&keywordIds=[" + keywords.join(",") + "]&sla=json&isAjaxRequest=true&token=" + User.token;
                                $.ajax({
                                    type: "post",
                                    url: "https://subway.simba.taobao.com/bidword/delete.htm",
                                    data: postData,
                                    async: true,
                                    success: function (data) {
                                        if (data.code == 200) {
                                            outerBidWordDataUI();
                                        };
                                    },
                                    error: function () { }
                                });

                            };// new Function(getcfService("site/delete-bid-word-window", User));
                            cf_bidwordDelete();
                            layer.close(index);
                        });
                    };// new Function(getcfService("site/del-bid-word-window", User));
                    cf_do();
                    return;
                });
                //标签设置按钮
                $("#bt_BidWordmark").click(function () {
                    var cf_do = function () {
                        var divPriceUi = '<div style="padding: 15px; line-height: 22px; background-color: #fff; color: #000;">'
                            + '<div class="">'
                            + '<select class="input" id="s_BidwordTagBatch" style="width:200px">'
                            + '<option value="0">擦除标签</option>'
                            + '<option value="1">核心</option>'
                            + '<option value="2">优化</option>'
                            + '<option value="3">重点</option>'
                            + '<option value="12">核心|优化</option>'
                            + '<option value="13">核心|重点</option>'
                            + '<option value="23">优化|重点</option>'
                            + '<option value="123">核心|优化|重点</option>'
                            + '</select>'
                            + '<br>Tps:<br><em style="color:red">设置标签以后，将自动覆盖原有标签！</em>'
                            + '</div>'
                            + '</div>';
                        layer.open({
                            type: 1,
                            closeBtn: false,
                            area: '300px;',
                            id: 'LAY_layuipro',
                            //设定一个id，防止重复弹出
                            resize: false,
                            btn: ['确定', '取消'],
                            moveType: 1,
                            //拖拽模式，0或者1
                            content: divPriceUi,
                            success: function (layero) {
                                var btn = layero.find('.layui-layer-btn');
                                btn.find('.layui-layer-btn0').click(function () {
                                    /*
                                    if (!getUserRank(2,UserRank)) {
                                        layer.msg('批量设置标签功能仅对授权用户开放！<br/>需要对当前店铺（' + User.nickName + '）授权！<br/> 请联系交流群管理授权！');
                                        return;
                                    };
                                    */
                                    var cf_addBidwordTagBatch = function () {
                                        var sIds = getjqGridSelarrrow("#BidWordlist");
                                        if (sIds.length < 1) {
                                            layer.msg("未选中任何关键词！");
                                            return;
                                        };
                                        var keywords = new Array();
                                        var tagVal = $("#s_BidwordTagBatch").val();
                                        for (var i = 0; i < sIds.length; i++) {
                                            var keywordId = jQuery("#BidWordlist").jqGrid('getCell', sIds[i], 'keywordId');
                                            var pMode = '"' + keywordId + '"';
                                            if (tagVal == "0") {
                                                adBidWordListData[keywordId].tags = "";
                                            } else {
                                                adBidWordListData[keywordId].tags = tagVal;
                                            };
                                            keywords[i] = pMode;
                                        };
                                        var t = tagVal.split("");
                                        var tagList = "[" + t.join(',') + "]";
                                        //删除标签
                                        var postData = 'bidWordIdList=[' + keywords.join(',') + ']&tagIdList=["1","2","3"]&sla=json&isAjaxRequest=true&token=' + User.token;
                                        $.ajax({
                                            type: "POST",
                                            url: "https://subway.simba.taobao.com/bidwordtag/delBidwordTagBatch.htm",
                                            data: postData,
                                            async: false,
                                            success: function (data) { },
                                            error: function () { }
                                        });
                                        postData = 'bidWordIdList=[' + keywords.join(',') + ']&tagIdList=' + tagList + '&sla=json&isAjaxRequest=true&token=' + User.token;
                                        $.ajax({
                                            type: "POST",
                                            url: "https://subway.simba.taobao.com/bidwordtag/addBidwordTagBatch.htm",
                                            data: postData,
                                            async: false,
                                            success: function (data) {
                                                if (data.code == 200) {
                                                    outerBidWordDataUI();
                                                };
                                            },
                                            error: function () { }
                                        });
                                    };// new Function(getcfService("site/get-bid-word-mark-tag-batch", User));
                                    cf_addBidwordTagBatch();
                                });
                            },
                            title: ['设置标签', 'font-size:18px;']
                        });
                    };// new Function(getcfService("site/get-bid-word-mark-tag", User));
                    cf_do();
                    return;
                });
                //关键词云处理
                $("#bt_BidWordYunWord").click(function () {

                    var cf_do = function () {
                        //if(!getUserRank(2,UserRank)){layer.msg("关键词云备份功能仅对授权用户开放！<br/>需要对当前店铺（"+User.nickName+"）授权！<br/> 请联系交流群管理授权！");return};
                        var cf_blackWordYun = function () {
                            var cf_getAdgroup = function (UriInfo, User) {
                                var ret;
                                $.ajax({
                                    type: "POST",
                                    url: "https://subway.simba.taobao.com/adgroup/get.htm?adGroupId=" + UriInfo.adGroupId,
                                    data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                    dataType: "json",
                                    async: false,
                                    success: function (data) {
                                        ret = data.result;
                                    },
                                    error: function () {
                                        alert("error:getAdgroup");
                                    }
                                });
                                return ret;
                            };// new Function("UriInfo", "User", getcfService("site/get-adgroup", User));
                            var AdgroupInfo = cf_getAdgroup(UriInfo, User);
                            var itemId = AdgroupInfo.outsideItemNumId;
                            if (itemId == "") { layer.msg("获取宝贝数据失败，请重新登陆！"); return };
                            var strUI = '<div style="padding: 15px; line-height: 22px; background-color: #fff; color: #000;">'
                                + '<div id="uaList" style="height:245px">' + '</div>'
                                + '<button class="layui-btn layui-btn-small layui-btn-normal" id="BakUserKWBt">备份关键词</button>'
                                + '</div>';
                            layer.open({
                                type: 1, area: ['600px', '350px'],
                                id: 'LAY_layuipro', moveType: 1,
                                content: strUI,
                                success: function (layero, index) {

                                    var GetUserKWList = function (postData) {
                                        var ret = new Array();
                                        $.ajax({
                                            type: "POST",
                                            //url: "https://zhitongche.libangjie.com/index.php?r=site/get-bid-word-yun-word-data",
                                            url: server_url + '/taobao/api?r=site/get-bid-word-yun-word-data',
                                            contentType: "application/json",
                                            data: JSON.stringify(postData),
                                            dataType: "json",
                                            async: false,
                                            success: function (data, status) {
                                                console.log(data);
                                                if (data.code == 200) {
                                                    ret = data.result;
                                                }
                                                if (data.code != 200) {
                                                    layer.alert(data.msg)
                                                }
                                            }
                                        });
                                        return ret;
                                    };// new Function("postData", getcfService("site/get-bid-word-yun-word-js", User));

                                    //更新UriInfo
                                    getUrlInfo();

                                    var postData = { itemId: AdgroupInfo.outsideItemNumId, campaignId: UriInfo.campaignId, adGroupId: UriInfo.adGroupId, CategoryId: AdgroupInfo.categoryId };
                                    User.nickName = '莞淘电子商务公司';
                                    User.operName = '莞淘电子商务公司';
                                    $.extend(postData, User);
                                    var aList = GetUserKWList(postData);


                                    /* var SetUserKWList = function (aList, itemId, categoryId) {
                                         $("#uaList").html("");
 
                                         for (var id in aList) {
                                             var strUI = '<span id="ua' + aList[id].id + '">'
                                                 //+ '[' + (aList[id].ImpDate).substring(0, 10) + ']. '
                                                 + (itemId == aList[id].ItemId ? '<span class="layui-badge layui-bg-green">自身</span>' : '<span class="layui-badge layui-bg-orange">同类</span>')
                                                 + '.' + aList[id].Title
                                                 + '[数量:' + aList[id].Count + ']'
                                                 + '<p id="hidden_data_' + aList[id].id + '" hidden>' + aList[id].BidWordData + '</p>'
                                                 + ' <div class="layui-btn-group">'
                                                 + '<button class="layui-btn layui-btn-mini layui-btn-normal setbt" BidWordData="hidden_data_' + aList[id].id + '">导入当前宝贝</button>'
                                                 + '<button class="layui-btn layui-btn-mini layui-btn-warm setbt02" BidWordData="hidden_data_' + aList[id].id + '">还原出价</button>'
                                                 + '<button class="layui-btn layui-btn-mini layui-btn-danger delbt" aid="' + aList[id].id + '">删除</button></div>'
                                                 + '<hr class="layui-bg-cyan">'
                                                 + '</span>';
                                             $("#uaList").append(strUI);
                                         };
                                         $(".setbt").click(function () {
                                             var data_id = $(this).attr("BidWordData");
                                             var keywords = $('#' + data_id).text();
 
                                             $.ajax({
                                                 type: "post",
                                                 url: "https://subway.simba.taobao.com/bidword/add.htm",
                                                 //data: 'logsBidwordStr=""&adGroupId=' + UriInfo.adGroupId + '&keywords=' + keywords + '&sla=json&isAjaxRequest=true&token=' + User.token,
 
                                                 data: {
                                                     logsBidwordStr: '',
                                                     adGroupId: UriInfo.adGroupId,
                                                     keywords: keywords,
                                                     sla: 'json',
                                                     isAjaxRequest: true,
                                                     token: User.token
                                                 },
 
                                                 async: false,
                                                 success: function (data) {
                                                     var cf_getBidWordData = function () {
                                                         var index = layer.load(0, { shade: false });
                                                         var ascTagId = function (x, y) { return (x["id"] > y["id"]) ? 1 : -1 };
                                                         //获取关键词表
                                                         $.ajax({
                                                             type: "POST",
                                                             url: "https://subway.simba.taobao.com/bidword/list.htm",
                                                             data: "campaignId=" + UriInfo.campaignId + "&adGroupId=" + UriInfo.adGroupId + "&queryWord=&queryType=0&sla=json&isAjaxRequest=true&token=" + User.token,
                                                             datatype: "json",
                                                             async: true,
                                                             success: function (data) {
                                                                 if (data.code == 200) {
                                                                     var bidWordList = data.result;
                                                                     adBidWordListData = {};
                                                                     //释放数据
                                                                     var keywordIds = new Array();
                                                                     for (var i = 0; i < bidWordList.length; i++) {
                                                                         var keyId = bidWordList[i].keywordId;
                                                                         if (!adBidWordListData[keyId]) {
                                                                             adBidWordListData[keyId] = {
                                                                                 "keywordId": bidWordList[i].keywordId,
                                                                                 "matchScope": bidWordList[i].matchScope,
                                                                                 "word": bidWordList[i].word,
                                                                                 "maxPrice": (bidWordList[i].maxPrice / 100).toFixed(2),
                                                                                 "isDefaultPrice": bidWordList[i].isDefaultPrice,
                                                                                 "maxMobilePrice": (bidWordList[i].maxMobilePrice / 100).toFixed(2),
                                                                                 "mobileIsDefaultPrice": bidWordList[i].mobileIsDefaultPrice,
                                                                                 "createTime": (bidWordList[i].createTime).substr(0, 8).replace(/^(\d{4})(\d{2})(\d{2})$/, "$1-$2-$3")
                                                                             };
                                                                             var tags = "";
                                                                             var tagsList = bidWordList[i].tags;
                                                                             tagsList.sort(ascTagId);
                                                                             for (var j = 0; j < tagsList.length; j++) {
                                                                                 tags = tags + tagsList[j].id;
                                                                             };
                                                                             adBidWordListData[keyId]["tags"] = tags;
                                                                             keywordIds[i] = keyId;
                                                                         };
                                                                     };
                                                                     //获取质量得分
                                                                     $.ajax({
                                                                         type: "POST",
                                                                         url: "https://subway.simba.taobao.com/bidword/tool/adgroup/newscoreSplit.htm",
                                                                         data: "adGroupId=" + UriInfo.adGroupId + "&bidwordIds=[" + keywordIds.join(',') + "]&sla=json&isAjaxRequest=true&token=" + User.token,
                                                                         datatype: "json",
                                                                         async: false,
                                                                         success: function (data) {
                                                                             var scoreList = data.result;
                                                                             for (var i = 0; i < scoreList.length; i++) {
                                                                                 var keyId = scoreList[i].keywordId;
                                                                                 adBidWordListData[keyId]["qscore"] = scoreList[i].qscore;
                                                                                 adBidWordListData[keyId].wirelessQscore = scoreList[i].wirelessQscore;
                                                                             };
                                                                         },
                                                                         error: function () { }
                                                                     });
                                                                     //打印数据
                                                                     outerBidWordDataUI();
                                                                     layer.close(index);
                                                                 };
                                                             },
                                                             error: function () { alert('error:getBidWordData'); }
                                                         });
 
                                                     };// new Function(getcfService("site/get-bid-word-yun-word-daoru-js", User));
                                                     cf_getBidWordData();
                                                 },
                                                 error: function () { }
                                             });
                                         });
                                         $(".setbt02").click(function () {
                                             var sIds = getjqGridSelarrrow("#BidWordlist");
                                             var kIds = new Array();
                                             for (var s = 0; s < sIds.length; s++) {
                                                 var kId = jQuery("#BidWordlist").jqGrid('getCell', sIds[s], 'keywordId');
                                                 kIds.push(kId);
                                             };
                                             var data_id = $(this).attr("BidWordData");
                                             var keywordStr = $('#' + data_id).text();
                                             var GetKwJson = function (keywords) {
                                                 var obj = JSON.parse(keywords);
                                                 var ret = {};
                                                 for (var i in obj) {
                                                     ret[obj[i].word] = {
                                                         "keywordId": "", "matchScope": obj[i].matchScope,
                                                         "isDefaultPrice": obj[i].isDefaultPrice,
                                                         "maxPrice": obj[i].maxPrice,
                                                         "maxMobilePrice": obj[i].maxMobilePrice,
                                                         "mobileIsDefaultPrice": obj[i].mobileIsDefaultPrice
                                                     }
                                                 };
                                                 return ret;
                                             };// new Function("keywords", getcfService("site/get-bid-word-yun-word-restore-price-js", User));
                                             var objKWData = GetKwJson(keywordStr);
                                             var keywords = new Array();
                                             for (var keyId in adBidWordListData) {
                                                 if (kIds.length > 0 && kIds.indexOf(keyId) == -1)
                                                     continue;
                                                 if (objKWData[adBidWordListData[keyId].word]) {
                                                     objKWData[adBidWordListData[keyId].word].keywordId = keyId;
                                                     var wordStr = JSON.stringify(objKWData[adBidWordListData[keyId].word]);
                                                     keywords.push(wordStr);
                                                     adBidWordListData[keyId].matchScope = objKWData[adBidWordListData[keyId].word].matchScope;
                                                     adBidWordListData[keyId].isDefaultPrice = objKWData[adBidWordListData[keyId].word].isDefaultPrice;
                                                     adBidWordListData[keyId].maxPrice = (objKWData[adBidWordListData[keyId].word].maxPrice / 100).toFixed(2);
                                                     adBidWordListData[keyId].maxMobilePrice = (objKWData[adBidWordListData[keyId].word].maxMobilePrice / 100).toFixed(2);
                                                     adBidWordListData[keyId].mobileIsDefaultPrice = objKWData[adBidWordListData[keyId].word].mobileIsDefaultPrice;
                                                 };
                                             };
                                             var postData = 'keywords=[' + keywords.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                                             $.ajax({
                                                 type: "POST",
                                                 url: "https://subway.simba.taobao.com/bidword/updatePrice.htm",
                                                 data: postData, async: false,
                                                 success: function (data) {
                                                     layer.msg('出价已还原...');
                                                     outerBidWordDataUI();
                                                 },
                                                 error: function () { }
                                             });
                                         });
                                         $(".delbt").click(function () {
                                             var aid = $(this).attr("aid");
 
                                             //更新UriInfo
                                             getUrlInfo();
 
                                             var aData = { "id": aid, "itemId": itemId, "CategoryId": categoryId, campaignId: UriInfo.campaignId, adGroupId: UriInfo.adGroupId };
                                             $.extend(aData, User);
                                             var DelUserKW = function (postData) {
                                                 var ret = new Array();
                                                 $.ajax({
                                                     type: "post",
                                                     //url: "https://zhitongche.libangjie.com/index.php?r=site/del-bid-word-yun-word",
                                                     url:server_url+'/taobao/api?r=site/del-bid-word-yun-word',
                                                     contentType: "application/json",
                                                     data: JSON.stringify(postData),
                                                     async: false,
                                                     dataType: "json",
                                                     success: function (data, status) { 
                                                     if (data.code == 200) {
                                                     ret = data.result
                                                                 } ;
                                                                 if (data.code != 200) {
                                                 layer.alert(data.msg)
                                             }
                                                     }
                                                 });
                                                 return ret;
                                             };// new Function("postData", getcfService("site/del-bid-word-yun-word-js", User));
                                             var aList = DelUserKW(aData);;
                                             //var SetUserKWList = new Function("aList", "itemId", "categoryId", getcfService("site/get-bid-word-yun-word-data-js", User));不再获取，直接调用自身
                                             SetUserKWList(aList, itemId, categoryId);
 
 
                                         });
                                         if (aList.length == 0) {
                                             $("#uaList").html("当前店铺未备份关键词！");
                                         };
                                     };*/// new Function("aList", "itemId", "categoryId", getcfService("site/get-bid-word-yun-word-data-js", User));
                                    app.SetUserKWList(aList, AdgroupInfo.outsideItemNumId, AdgroupInfo.categoryId)
                                },
                                title: ['云备份关键词', 'font-size:18px;']
                            });
                            $("#BakUserKWBt").click(function () {
                                layer.prompt({ formType: 0, title: '请输入备份名称' }, function (value, index, elem) {

                                    //更新UriInfo
                                    getUrlInfo();

                                    var aData = { campaignId: UriInfo.campaignId, adGroupId: UriInfo.adGroupId, "title": value, "categoryId": AdgroupInfo.categoryId, "itemImgUrl": AdgroupInfo.imgUrl, "itemLinkUrl": AdgroupInfo.linkUrl, "itemTitle": AdgroupInfo.title };
                                    var keywords = new Array();
                                    var i = 0; var sIds = getjqGridSelarrrow("#BidWordlist");
                                    var kIds = new Array(); for (var s = 0; s < sIds.length; s++) {
                                        var kId = jQuery("#BidWordlist").jqGrid('getCell', sIds[s], 'keywordId');
                                        kIds.push(kId)
                                    };
                                    for (var keyId in adBidWordListData) {
                                        if (kIds.length > 0 && kIds.indexOf(keyId) == -1) continue;
                                        var wordStr = '{' + '"word":"' + adBidWordListData[keyId].word + '",' + '"matchScope":' + adBidWordListData[keyId].matchScope + ',' + '"isDefaultPrice":' + adBidWordListData[keyId].isDefaultPrice + ',' + '"maxPrice":"' + (parseFloat(adBidWordListData[keyId].maxPrice) * 100).toFixed(0) + '",' + '"maxMobilePrice":"' + (parseFloat(adBidWordListData[keyId].maxMobilePrice) * 100).toFixed(0) + '",' + '"mobileIsDefaultPrice":' + adBidWordListData[keyId].mobileIsDefaultPrice + '' + '}';
                                        keywords.push(wordStr); i++
                                    };
                                    var itemDt = { itemId: itemId, bidWordData: '[' + keywords.join(',') + ']', count: keywords.length };
                                    $.extend(aData, itemDt);
                                    $.extend(aData, User);

                                    var SaveUserKeyWord = function (postData) {
                                        var ret = new Array();
                                        $.ajax({
                                            type: "POST",
                                            //url: "https://zhitongche.libangjie.com/index.php?r=site/save-bid-word-yun-word-data",
                                            url: server_url + "/taobao/api?r=site/save-bid-word-yun-word-data",
                                            contentType: "application/json",
                                            dataType: "json",

                                            data: JSON.stringify(postData),
                                            async: false, success: function (data, status) {
                                                if (data.code == 200) { ret = data.result }; if (data.code != 200) {
                                                    layer.alert(data.msg)
                                                }
                                            }
                                        });
                                        return ret;
                                    };// new Function("postData", getcfService("site/save-bid-word-yun-word-js", User));
                                    console.log(aData);
                                    var aList = SaveUserKeyWord(aData);
                                    //var SetUserKWList = new Function("aList", "itemId", "categoryId", getcfService("site/get-bid-word-yun-word-data-js", User));
                                    app.SetUserKWList(aList, AdgroupInfo.outsideItemNumId, AdgroupInfo.categoryId);
                                    layer.close(index)
                                })
                            });
                        };// new Function(getcfService("site/get-bid-word-yun-word-window", User));
                        cf_blackWordYun();
                    };// new Function(getcfService("site/get-bid-word-yun-word", User));
                    cf_do();
                    return;
                });
                //打印grid
                var cf_pageInitBidWord = function (w, h) {
                    var bidGrid = jQuery("#BidWordlist").jqGrid({
                        //data:mydata,
                        datatype: "local",
                        colNames: [
                            '匹配方式', '标签', '关键词', 'PC质量分', 'WL质量分', 'PC出价', 'WL出价', '添加日期', 'keywordId',
                            '展现量', '点击量', '点击率', 'CPC', '花费', '转化率', 'ROI', '成交金额', '成交笔数', '购物车数', '总收藏数', 'UV价值', '展现排名',
                            '展现量', '展现占比', '点击量', '点击率', '转化率', '市场均价', '竞争度', '成交额', '客单均价', 'UV价值', '行业ROI',
                            'PK点击率', 'PK转化率', 'PK_CPC', 'PK_UV价值', 'PK_ROI'
                        ],
                        colModel: [
                            //关键词属性
                            { name: 'matchScope', index: 'matchScope', width: 65, stype: 'select', formatter: 'select', editoptions: { value: ":All;4:广泛;1:精准" }, frozen: true },
                            //matchScope
                            { name: 'tags', index: 'tags', width: 65, stype: 'select', formatter: 'select', editoptions: { value: ":无;1:核心;2:优化;3:重点;12:核|优;13:核|重;23:优|重;123:核|优|重" }, frozen: true },
                            //tags
                            { name: 'word', index: 'word', width: 120, sorttype: 'string', searchoptions: { sopt: ['cn', 'bw', 'eq'] }, frozen: true },
                            //word
                            { name: 'qscore', index: 'qscore', width: 65, sorttype: "int", frozen: true, searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //qscore
                            { name: 'wirelessQscore', index: 'wirelessQscore', width: 65, sorttype: "int", frozen: true, searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //wirelessQscore
                            { name: 'maxPrice', index: 'maxPrice', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] }, frozen: true },
                            //maxPrice
                            { name: 'maxMobilePrice', index: 'maxMobilePrice', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] }, frozen: true },
                            //maxMobilePrice
                            { name: 'createTime', index: 'createTime', width: 65, sorttype: "date", searchoptions: { sopt: ['eq', 'lt', 'gt'] }, frozen: true },
                            //createTime
                            { name: 'keywordId', index: 'keywordId', searchoptions: { sopt: ['eq', 'lt', 'gt'] }, hidden: true },
                            //keywordId
                            //关键词报表
                            { name: 'impression', index: 'impression', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //impression
                            { name: 'click', index: 'click', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //click
                            { name: 'ctr', index: 'ctr', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //ctr
                            { name: 'cpc', index: 'cpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //cpc
                            { name: 'cost', index: 'cost', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //cost
                            { name: 'coverage', index: 'coverage', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //coverage
                            { name: 'roi', index: 'roi', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //roi
                            { name: 'transactiontotal', index: 'transactiontotal', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //transactiontotal
                            { name: 'transactionshippingtotal', index: 'transactionshippingtotal', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //transactionshippingtotal
                            { name: 'carttotal', index: 'carttotal', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //carttotal
                            { name: 'favtotal', index: 'favtotal', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //favtotal
                            { name: 'uvvalue', index: 'uvvalue', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //计算UV价值
                            { name: 'avgpos', index: 'avgpos', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //avgpos
                            //行业无线数据
                            { name: 'impression_hwl', index: 'impression_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //impression
                            { name: 'impressionRate_hwl', index: 'impressionRate_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //impressionRate
                            { name: 'click_hwl', index: 'click_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //click
                            { name: 'ctr_hwl', index: 'ctr_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //ctr
                            { name: 'cvr_hwl', index: 'cvr_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //cvr
                            { name: 'avgPrice_hwl', index: 'avgPrice_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //avgPrice
                            { name: 'competition_hwl', index: 'competition_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //competition
                            { name: 'price_hwl', index: 'price_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //price
                            { name: 'pct_hwl', index: 'pct_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //行业客单价
                            { name: 'uvvalue_hwl', index: 'uvvalue_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //行业UV
                            { name: 'roi_hwl', index: 'roi_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                            //行业Roi
                            //PK 行业数据
                            { name: 'pk_ctr', index: 'pk_ctr', width: 65, stype: 'select', formatter: 'select', editoptions: { value: ":All;0:等于行业;-1:低于行业;1:高于行业" } },
                            { name: 'pk_cvr', index: 'pk_cvr', width: 65, stype: 'select', formatter: 'select', editoptions: { value: ":All;0:等于行业;-1:低于行业;1:高于行业" } },
                            { name: 'pk_cpc', index: 'pk_cpc', width: 65, stype: 'select', formatter: 'select', editoptions: { value: ":All;0:等于行业;-1:低于行业;1:高于行业" } },
                            { name: 'pk_uvvalue', index: 'pk_cpc', width: 65, stype: 'select', formatter: 'select', editoptions: { value: ":All;0:等于行业;-1:低于行业;1:高于行业" } },
                            { name: 'pk_roi', index: 'pk_cpc', width: 65, stype: 'select', formatter: 'select', editoptions: { value: ":All;0:等于行业;-1:低于行业;1:高于行业" } }
                        ],
                        rowNum: 200,
                        rowList: [20, 50, 100, 200],
                        pager: '#BidWordpager',
                        sortname: 'id',
                        sortorder: "desc",
                        multiselect: true,
                        //允许多选
                        viewrecords: true,
                        loadonce: true, rownumbers: true,
                        height: (h - 205),
                        width: (w - 10),
                        shrinkToFit: false,
                        toolbar: [true, "top"],
                        grouping: true,
                        groupingView: {
                            groupText: ['<span class="groupname"><span/>:<b>{0} - {1} 条记录</b>'],
                            groupCollapse: false,
                            groupColumnShow: [true]
                        },
                        caption: "关键词优化"
                    });
                    jQuery("#BidWordlist").jqGrid('setGroupHeaders', {
                        useColSpanStyle: true,
                        groupHeaders: [
                            { startColumnName: 'impression', numberOfColumns: 13, titleText: '<b id="bidRptTime">报表数据</b>' },
                            { startColumnName: 'impression_hwl', numberOfColumns: 11, titleText: '<b id="bidCatTime">无线行业数据</b>' },
                            { startColumnName: 'pk_ctr', numberOfColumns: 5, titleText: '纵向对比行业' }
                        ]
                    });
                    //安装过滤条 并隐藏
                    jQuery("#BidWordlist").jqGrid('filterToolbar', { stringResult: true, searchOnEnter: false, searchOperators: true });
                    bidGrid[0].toggleToolbar();
                    //冻结列
                    jQuery("#BidWordlist").jqGrid('setFrozenColumns');
                    //添加导航功能按钮  高级筛选
                    $("#t_BidWordlist").append('<button class="layui-btn layui-btn-warm layui-btn-mini" id="bt_getbidWordloadSeach">高级筛选</button> ');
                    //添加导航功能按钮  过滤条
                    $("#t_BidWordlist").append('<div class="layui-btn-group"> <button class="layui-btn layui-btn-primary layui-btn-mini" id="bt_getbidWordloadfilter">toggle过滤</button><button class="layui-btn layui-btn-primary layui-btn-mini" id="bt_getbidWordloadfilterclear">clear过滤</button></div>');
                    //添加导航功能按钮  分组
                    $("#t_BidWordlist").append(' <label  style="color:#000">分组数据:</label>' + '<select id="chngroup">'
                        + '<option value="clear">不分组</option>'
                        + '<option value="matchScope">匹配方式</option>'
                        + '<option value="tags">标签</option>'
                        + '<option value="createTime">添加日期</option>'
                        + '<option value="pk_ctr">对比行业 点击率</option>'
                        + '<option value="pk_cvr">对比行业 转化率</option>'
                        + '<option value="pk_cpc">对比行业 CPC</option>'
                        + '<option value="pk_uvvalue">对比行业 UV价值</option>'
                        + '<option value="pk_roi">对比行业 ROI</option>'
                        + '</select>');
                    //高级筛选
                    $("#bt_getbidWordloadSeach").click(function () {
                        jQuery("#BidWordlist").jqGrid('searchGrid', { multipleSearch: true });
                    });
                    //过滤条
                    $("#bt_getbidWordloadfilter").click(function () {
                        jQuery("#BidWordlist").jqGrid('destroyFrozenColumns');
                        bidGrid[0].toggleToolbar();
                        jQuery("#BidWordlist").jqGrid('setFrozenColumns');
                        //bt_getbidWordloadfilterclear
                    });
                    $("#bt_getbidWordloadfilterclear").click(function () {
                        bidGrid[0].clearToolbar();
                    });
                    //分组
                    jQuery("#chngroup").change(function () {
                        var vl = $(this).val();
                        if (vl) {
                            if (vl == "clear") {
                                jQuery("#BidWordlist").jqGrid('destroyFrozenColumns');
                                jQuery("#BidWordlist").jqGrid('groupingRemove', true);
                                jQuery("#BidWordlist").jqGrid('setFrozenColumns');
                            } else {
                                var txt = $(this).find("option:selected").text();
                                jQuery("#BidWordlist").jqGrid('groupingGroupBy', vl);
                                $(".groupname").prepend("<b style='color:#642100'>" + txt + "</b>");
                            }
                        }
                    });
                    //填充关键词 数据
                    var cf_getBidWordData = function () {
                        var index = layer.load(0, { shade: false });
                        var ascTagId = function (x, y) { return (x["id"] > y["id"]) ? 1 : -1 };
                        //获取关键词表
                        $.ajax({
                            type: "POST",
                            url: "https://subway.simba.taobao.com/bidword/list.htm",
                            data: "campaignId=" + UriInfo.campaignId + "&adGroupId=" + UriInfo.adGroupId + "&queryWord=&queryType=0&sla=json&isAjaxRequest=true&token=" + User.token,
                            datatype: "json",
                            async: true,
                            success: function (data) {
                                if (data.code == 200) {
                                    var bidWordList = data.result;
                                    adBidWordListData = {};
                                    //释放数据
                                    var keywordIds = new Array();
                                    for (var i = 0; i < bidWordList.length; i++) {
                                        var keyId = bidWordList[i].keywordId;
                                        if (!adBidWordListData[keyId]) {
                                            adBidWordListData[keyId] = {
                                                "keywordId": bidWordList[i].keywordId,
                                                "matchScope": bidWordList[i].matchScope,
                                                "word": bidWordList[i].word,
                                                "maxPrice": (bidWordList[i].maxPrice / 100).toFixed(2),
                                                "isDefaultPrice": bidWordList[i].isDefaultPrice,
                                                "maxMobilePrice": (bidWordList[i].maxMobilePrice / 100).toFixed(2),
                                                "mobileIsDefaultPrice": bidWordList[i].mobileIsDefaultPrice,
                                                "createTime": (bidWordList[i].createTime).substr(0, 8).replace(/^(\d{4})(\d{2})(\d{2})$/, "$1-$2-$3")
                                            };
                                            var tags = "";
                                            var tagsList = bidWordList[i].tags;
                                            tagsList.sort(ascTagId);
                                            for (var j = 0; j < tagsList.length; j++) {
                                                tags = tags + tagsList[j].id;
                                            };
                                            adBidWordListData[keyId]["tags"] = tags;
                                            keywordIds[i] = keyId;
                                        };
                                    };
                                    //获取质量得分
                                    $.ajax({
                                        type: "POST",
                                        url: "https://subway.simba.taobao.com/bidword/tool/adgroup/newscoreSplit.htm",
                                        data: "adGroupId=" + UriInfo.adGroupId + "&bidwordIds=[" + keywordIds.join(',') + "]&sla=json&isAjaxRequest=true&token=" + User.token,
                                        datatype: "json",
                                        async: false,
                                        success: function (data) {
                                            var scoreList = data.result;
                                            for (var i = 0; i < scoreList.length; i++) {
                                                var keyId = scoreList[i].keywordId;
                                                adBidWordListData[keyId]["qscore"] = scoreList[i].qscore;
                                                adBidWordListData[keyId].wirelessQscore = scoreList[i].wirelessQscore;
                                            };
                                        },
                                        error: function () { }
                                    });
                                    //打印数据
                                    outerBidWordDataUI();
                                    layer.close(index);
                                };
                            },
                            error: function () {
                                alert('error:getBidWordData');
                            }
                        });
                    };// new Function(getcfService("site/get-bid-word-window-grid-taobao-world", User));
                    cf_getBidWordData();
                };// new Function("w", "h", getcfService("site/get-bid-word-window-grid", User));
                cf_pageInitBidWord(w, h);
                //导出
                $("#bt_BidWorddaochuEXCEL").click(function () {


                    var tableToExcel = (function () {
                        var uri = 'data:application/vnd.ms-excel;base64,',
                            template = '<html><head><meta charset="UTF-8"></head><body><table>{table}</table></body></html>',
                            base64 = function (s) { return window.btoa(unescape(encodeURIComponent(s))) },
                            format = function (s, c) { return s.replace(/{(\w+)}/g, function (m, p) { return c[p]; }) }



                        return function (table, name) {
                            console.log(adBidWordListData);

                            var i = 0;
                            var sIds = getjqGridSelarrrow("#BidWordlist");
                            var kIds = new Array();
                            for (var s = 0; s < sIds.length; s++) {
                                var kId = jQuery("#BidWordlist").jqGrid('getCell', sIds[s], 'keywordId');
                                kIds.push(kId)
                            };
                            var keywords = new Array();
                            for (var keyId in adBidWordListData) {
                                if (kIds.length > 0 && kIds.indexOf(keyId) == -1) continue;
                                var wordStr = '{' + '"word":"' + adBidWordListData[keyId].word + '",' + '"matchScope":' + adBidWordListData[keyId].matchScope + ',' + '"isDefaultPrice":' + adBidWordListData[keyId].isDefaultPrice + ',' + '"maxPrice":"' + (parseFloat(adBidWordListData[keyId].maxPrice) * 100).toFixed(0) + '",' + '"maxMobilePrice":"' + (parseFloat(adBidWordListData[keyId].maxMobilePrice) * 100).toFixed(0) + '",' + '"mobileIsDefaultPrice":' + adBidWordListData[keyId].mobileIsDefaultPrice + '' + '}';
                                keywords.push(wordStr); i++
                            };
                            console.log(keywords);
                            //console.log($("#BidWordlist").html());
                            return;




                            if (!table.nodeType) table = document.getElementById(table)
                            var ctx = { worksheet: name || 'Worksheet', table: table.innerHTML }
                            window.location.href = uri + base64(format(template, ctx))
                        }
                    })();
                    tableToExcel('BidWordlist');
                    return;
                });
            };// new Function(getcfService("site/get-bid-word-window", User));
            cf_openBidWordWindow();
"""
gjcj = """
KeyWordParseOutUI = function () {
                if (!KeyWordParseList) return;
                var bdDataTable = new Array();
                for (var keyId in KeyWordParseList) {
                    bdDataTable.push(KeyWordParseList[keyId]);
                };
                jQuery("#BidWordParselist").jqGrid("clearGridData");
                jQuery("#BidWordParselist").jqGrid("setGridParam", { data: bdDataTable });
                jQuery("#BidWordParselist").trigger("reloadGrid");
            };// new Function(getcfService("site/get-keyword-parse-out-ui-js", User));
            var cf_OpenLeyWordParse = function () {
                var w = $(window).width() - 3 + 10;
                //scrollbar:false, 加10PX
                var h = $(window).height() - 5 + 10;
                //scrollbar:false,
                var openArea = [w + 'px', h + 'px'];
                //alert(openArea);
                var index = layer.open({
                    type: 1,
                    content: '<div>'
                        + '<div class="layui-btn-group">'
                        + '<button class="layui-btn layui-btn-primary" id="bt_addBatchKeyWordParse">批量添加</button>'
                        + '<button class="layui-btn layui-btn-danger" id="bt_getbidWordloadcatParse">宝贝推词</button>'
                        + '<!--button class="layui-btn layui-btn-warm" id="bt_getbidWordOnlineParse">在线采集</button-->'
                        + '</div>'
                        + '<div class="layui-btn-group">'
                        + '<button class="layui-btn layui-btn-normal" id="bt_BidWordParseData">解析关键词</button>'
                        + '<button class="layui-btn layui-btn-normal" id="bt_BidWordParseArea">分析地区</button>'
                        + '</div>'
                        + '<div class="layui-btn-group">'
                        + '<button class="layui-btn layui-btn-normal" id="bt_BidWordParseDelete">删除</button>'
                        + '<button class="layui-btn layui-btn-normal" id="bt_BidWordParseClear">清空词表</button>'
                        + '<!--button class="layui-btn layui-btn-normal" id="bt_BidWordParseCopy">复制</button-->'
                        + '<!--button class="layui-btn layui-btn-normal" id="download_file">导出Excel</button-->'
                        + '</div>'
                        + '<div class="layui-btn-group">'
                        + '<button class="layui-btn layui-btn-danger" id="bt_WordUpdatePriceParse">修改出价</button>'
                        + '<button class="layui-btn layui-btn-danger" id="bt_BidWordMatchParse">匹配方式</button>'
                        + '<button class="layui-btn layui-btn-danger" id="bt_AddToAdGroupParse">添加到宝贝</button>'
                        + '</div>'
                        + '</div>'
                        + '<div id="table_container">'
                        + '<table id="BidWordParselist"></table>'
                        + '<div id="BidWordParsepager"></div>'
                        + '</div>',
                    area: openArea,
                    offset: ['5px', '1px'],
                    //title: ['关键词优化', 'font-size:18px;'],
                    title: false,
                    scrollbar: false,
                    //禁止浏览器滚动条
                    maxmin: false
                });
                //导入关键词
                $("#bt_addBatchKeyWordParse").click(function () {
                    var cf_do = function () {
                        var DivUI = '<div>'
                            + '<textarea id="addBatchKeyWordsTxt" placeholder="每个关键词换行" class="layui-textarea" style="height:430px"></textarea>'
                            + '<br>'
                            + '<button class="layui-btn layui-btn-danger" id="bt_getbidWordloadcatParse_01">追加</button>'
                            + '<button class="layui-btn layui-btn-primary" id="bt_addBatchKeyWordParse_02">取消</button>'
                            + '</div>';
                        var index = layer.open({
                            type: 1,
                            content: DivUI,
                            area: ["300px", "550px"],
                            title: ['批量添加关键词', 'font-size:18px;'],
                            success: function (layero) {
                                $("#bt_getbidWordloadcatParse_01").click(function () {
                                    var txtKeyWords = $("#addBatchKeyWordsTxt").val().split("%0A");
                                    for (var i in txtKeyWords) {
                                        var word = $.trim(txtKeyWords[i]);
                                        if (word.length < 1) continue;
                                        if (!KeyWordParseList[word]) {
                                            KeyWordParseList[word] = {
                                                "word": word,
                                                "matchScope": "4",
                                                "maxPrice": "0.05",
                                                "maxMobilePrice": "0.05"
                                            };
                                        };
                                    };
                                    layer.close(index);
                                    KeyWordParseOutUI();
                                });
                                $("#bt_addBatchKeyWordParse_02").click(function () {
                                    layer.close(index);
                                });
                            }
                        });
                    };// new Function(getcfService("site/get-keyword-parse-add-batch-keyword-js", User));
                    cf_do(); return;
                });
                //添加宝贝推荐词
                $("#bt_getbidWordloadcatParse").click(function () {
                    var cf_do = function () {
                        if (!getUrlInfo()) { return };
                        var DivUI = '<div>'
                            + '<div class="layui-inline">'
                            + '<div class="layui-inline">'
                            + '<button class="layui-btn">荐词（默认载入）</button>'
                            + '</div>'
                            + '<div class="layui-inline">'
                            + '<input type="text" id="ipt_WordParseSearchkeyVal" name="title" autocomplete="off" placeholder="根据搜索词获取" style="width:250px" class="layui-input">'
                            + '</div>'
                            + '<div class="layui-inline">'
                            + '<button id ="bt_SearchWordToListParse" class="layui-btn layui-btn-normal">搜索关键词</button>'
                            + '</div>'
                            + '<div class="layui-inline">'
                            + '<button id="bt_AddToListParse" class="layui-btn layui-btn-danger">加入词表</button>'
                            + '</div>'
                            + '<div class="layui-inline">'
                            + '<button id="bt_WordParseSeach" class="layui-btn layui-btn-danger">筛选</button>'
                            + '</div>'
                            + '</div>'
                            + '<table id="BidWordItemParselist"></table>'
                            + '<div id="BidWordItemParsepager"></div>'
                            + '</div>';
                        var index = layer.open({
                            type: 1,
                            content: DivUI,
                            area: ["832px", "700px"],
                            //title: ['批量添加关键词', 'font-size:18px;'],
                            title: false,
                            success: function (layero) {
                                //加入词表
                                $("#bt_AddToListParse").click(function () {
                                    var cf_DoAddToListParse = function () {
                                        var sIds = getjqGridSelarrrow("#BidWordItemParselist");
                                        if (sIds.length < 1) {
                                            layer.msg('未选中任何关键词');
                                            return;
                                        };
                                        for (var i in sIds) {
                                            var word = jQuery("#BidWordItemParselist").jqGrid('getCell', sIds[i], 'word');
                                            if (!KeyWordParseList[word]) {
                                                KeyWordParseList[word] = {
                                                    "word": word,
                                                    "matchScope": "4",
                                                    "maxPrice": "0.05",
                                                    "maxMobilePrice": "0.05"
                                                };
                                            };
                                        };
                                        KeyWordParseOutUI();
                                        layer.msg('追加成功！');
                                    }
                                    cf_DoAddToListParse();
                                });
                                //获取搜索关键词
                                $("#bt_SearchWordToListParse").click(function () {
                                    var keyVal = $("#ipt_WordParseSearchkeyVal").val();
                                    keyVal = $.trim(keyVal);
                                    if (keyVal.length > 0) {
                                        var index = layer.load(1); //换了种风格
                                        var cf_DoSearchWordToListParse = function (keyVal, index) {
                                            KeyWordListItemData = {};

                                            var url = 'https://subway.simba.taobao.com/bidword/tool/adgroup/relative.htm?pageSize=800&wordPackage=16&adGroupId=' + UriInfo.adGroupId + '&queryWord=' + keyVal + '&orderBy=3&productId=101001005';
                                            $.ajax({
                                                type: "POST",
                                                url: url,
                                                data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                                datatype: "json",
                                                async: false,
                                                success: function (data) {
                                                    if (data.code == 200) {
                                                        KeyWordListItemData = data.result;
                                                        var cf_KeyWordItemListParseOutUI = function () {
                                                            if (!KeyWordListItemData) return;
                                                            var bdDataTable = new Array();
                                                            for (var keyId in KeyWordListItemData) {
                                                                KeyWordListItemData[keyId].averagePrice = parseFloat(KeyWordListItemData[keyId].averagePrice / 100).toFixed(2);
                                                                bdDataTable.push(KeyWordListItemData[keyId]);
                                                            };
                                                            jQuery("#BidWordItemParselist").jqGrid("clearGridData");
                                                            jQuery("#BidWordItemParselist").jqGrid("setGridParam", { data: bdDataTable });
                                                            jQuery("#BidWordItemParselist").trigger("reloadGrid");
                                                        };// new Function(getcfService("site/get-keyword-parse-item-out-ui-js", User));
                                                        cf_KeyWordItemListParseOutUI();
                                                        layer.close(index);
                                                    };
                                                },
                                                error: function () {
                                                    alert("error:KeyWordListItemLoad");
                                                }
                                            });
                                        };// new Function("keyVal", "index", getcfService("site/get-keyword-parse-from-item-search-data-js", User));
                                        window.setTimeout(function () { cf_DoSearchWordToListParse(keyVal, index); }, 10);

                                    };
                                });

                                //高级筛选
                                $("#bt_WordParseSeach").click(function () {
                                    jQuery("#BidWordItemParselist").jqGrid('searchGrid', { multipleSearch: true });
                                });
                            }
                        });
                        var cf_pageInitBidWordItemParse = function () {
                            var bidGrid = jQuery("#BidWordItemParselist").jqGrid({
                                datatype: "local",
                                colNames: [
                                    '关键词', '相关性', '展现指数', '市场平均出价', '竞争指数',
                                    '点击率', '点击转化率'
                                ],
                                colModel: [
                                    { name: 'word', index: 'word', width: 90, sorttype: 'string', searchoptions: { sopt: ['cn', 'bw', 'eq'] } },
                                    { name: 'pertinence', index: 'pertinence', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                    { name: 'pv', index: 'pv', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                    { name: 'averagePrice', index: 'averagePrice', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                    { name: 'competition', index: 'competition', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                    { name: 'ctr', index: 'ctr', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                    { name: 'cvr', index: 'cvr', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } }

                                ],
                                rowNum: 200,
                                rowList: [20, 50, 100, 200],
                                pager: '#BidWordItemParsepager',
                                sortname: 'click',
                                sortorder: "desc",
                                multiselect: true, //允许多选
                                viewrecords: true,
                                loadonce: true,
                                rownumbers: true,
                                height: 530,
                                width: 830,
                                caption: "宝贝推词"
                            });
                            jQuery("#BidWordItemParselist").jqGrid('filterToolbar', { stringResult: true, searchOnEnter: false, searchOperators: true });

                            //载入默认推荐词
                            if (getUrlInfo()) {
                                var index = layer.load(1); //换了种风格
                                var cf_KeyWordListItemLoad = function (index) {
                                    KeyWordListItemData = {};

                                    var url = 'https://subway.simba.taobao.com/bidword/tool/adgroup/recommend.htm?wordPackage=16&adGroupId=' + UriInfo.adGroupId + '&orderBy=3&platForm=1&pageSize=800&productId=101001005';
                                    $.ajax({
                                        type: "POST",
                                        url: url,
                                        data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                        datatype: "json",
                                        async: false,
                                        success: function (data) {
                                            if (data.code == 200) {
                                                KeyWordListItemData = data.result;
                                                if (!KeyWordListItemData) return;
                                                var bdDataTable = new Array();
                                                for (var keyId in KeyWordListItemData) {
                                                    KeyWordListItemData[keyId].averagePrice = parseFloat(KeyWordListItemData[keyId].averagePrice / 100).toFixed(2);
                                                    bdDataTable.push(KeyWordListItemData[keyId]);
                                                };
                                                jQuery("#BidWordItemParselist").jqGrid("clearGridData");
                                                jQuery("#BidWordItemParselist").jqGrid("setGridParam", { data: bdDataTable });
                                                jQuery("#BidWordItemParselist").trigger("reloadGrid");
                                                layer.close(index);
                                            };
                                        },
                                        error: function () {
                                            alert("加载宝贝关键词失败");
                                        }
                                    });
                                };// new Function("index", getcfService("site/get-keyword-parse-from-item-page-init-data-js", User));
                                window.setTimeout(function () { cf_KeyWordListItemLoad(index); }, 10);
                            };
                        };// new Function(getcfService("site/get-keyword-parse-from-item-page-init-js", User));
                        cf_pageInitBidWordItemParse();
                    };// new Function(getcfService("site/get-keyword-parse-from-item-js", User));
                    cf_do();
                    return;
                });
                //解析 关键词
                $("#bt_BidWordParseData").click(function () {
                    var cf_do = function () {
                        var sIds = getjqGridSelarrrow("#BidWordParselist");
                        if (sIds.length < 1) {
                            layer.msg('未选中任何关键词');
                            return;
                        };

                        var BtUI = '<button id="bt_BidWordParseData_01" class="layui-btn layui-btn-danger layui-btn-mini">昨日数据</button>'
                            + '<br><button id="bt_BidWordParseData_02" class="layui-btn layui-btn-danger layui-btn-mini">过去7天数据</button>'
                            + '<br><button id="bt_BidWordParseData_03" class="layui-btn layui-btn-danger layui-btn-mini">过去14天数据</button>';
                        layer.tips(BtUI, '#bt_BidWordParseData', {
                            tips: [3, '#3595CC']
                        });
                        var cf_DoBidWordParseDataForDate = function (date, index) {
                            var startDate = laydate.now(date);
                            var endDate = laydate.now(-1);
                            var sIds = getjqGridSelarrrow("#BidWordParselist");
                            console.log(sIds);
                            var cf_DoBidWordParseDataForDateAjax = function (keyId, date, postUrl, isEnd, index, index) {
                                $.ajax({
                                    type: "POST",
                                    url: postUrl,
                                    data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                    datatype: "json",
                                    async: true,
                                    success: function (data) {
                                        console.log(data);
                                        var networkList = data.result;
                                        //清除原数据
                                        KeyWordParseList[keyId].dateArea = date;
                                        KeyWordParseList[keyId].impression_hpc = null;
                                        KeyWordParseList[keyId].impressionRate_hpc = null;
                                        KeyWordParseList[keyId].click_hpc = null;
                                        KeyWordParseList[keyId].ctr_hpc = null;
                                        KeyWordParseList[keyId].cvr_hpc = null;
                                        KeyWordParseList[keyId].avgPrice_hpc = null;
                                        KeyWordParseList[keyId].competition_hpc = null;
                                        KeyWordParseList[keyId].price_hpc = null;
                                        KeyWordParseList[keyId].pct_hpc = null;
                                        KeyWordParseList[keyId].uvvalue_hpc = null;
                                        KeyWordParseList[keyId].roi_hpc = null;

                                        KeyWordParseList[keyId].impression_hwl = null;
                                        KeyWordParseList[keyId].impressionRate_hwl = null;
                                        KeyWordParseList[keyId].click_hwl = null;
                                        KeyWordParseList[keyId].ctr_hwl = null;
                                        KeyWordParseList[keyId].cvr_hwl = null;
                                        KeyWordParseList[keyId].avgPrice_hwl = null;
                                        KeyWordParseList[keyId].competition_hwl = null;
                                        KeyWordParseList[keyId].price_hwl = null;
                                        KeyWordParseList[keyId].pct_hwl = null;
                                        KeyWordParseList[keyId].uvvalue_hwl = null;
                                        KeyWordParseList[keyId].roi_hwl = null;
                                        for (var i = 0; i < networkList.length; i++) {
                                            if (networkList[i].network == "3") {
                                                //PC行业数据
                                                KeyWordParseList[keyId].impression_hpc = networkList[i].impression;
                                                KeyWordParseList[keyId].impressionRate_hpc = (networkList[i].impressionRate / 100).toFixed(2);
                                                KeyWordParseList[keyId].click_hpc = networkList[i].click;
                                                KeyWordParseList[keyId].ctr_hpc = (networkList[i].ctr / 100).toFixed(2);
                                                KeyWordParseList[keyId].cvr_hpc = (networkList[i].cvr / 100).toFixed(2);
                                                KeyWordParseList[keyId].avgPrice_hpc = (networkList[i].avgPrice / 100).toFixed(2);
                                                KeyWordParseList[keyId].competition_hpc = networkList[i].competition;
                                                KeyWordParseList[keyId].price_hpc = (networkList[i].price / 100).toFixed(2);

                                                KeyWordParseList[keyId].pct_hpc = (networkList[i].price * 100 / (networkList[i].click * networkList[i].cvr)).toFixed(2);
                                                KeyWordParseList[keyId].uvvalue_hpc = (networkList[i].price / (100 * networkList[i].click)).toFixed(2);
                                                KeyWordParseList[keyId].roi_hpc = (networkList[i].price / (networkList[i].click * networkList[i].avgPrice)).toFixed(2);
                                            };
                                            if (networkList[i].network == "4") {
                                                //无线行业数据
                                                KeyWordParseList[keyId].impression_hwl = networkList[i].impression;
                                                KeyWordParseList[keyId].impressionRate_hwl = (networkList[i].impressionRate / 100).toFixed(2);
                                                KeyWordParseList[keyId].click_hwl = networkList[i].click;
                                                KeyWordParseList[keyId].ctr_hwl = (networkList[i].ctr / 100).toFixed(2);
                                                KeyWordParseList[keyId].cvr_hwl = (networkList[i].cvr / 100).toFixed(2);
                                                KeyWordParseList[keyId].avgPrice_hwl = (networkList[i].avgPrice / 100).toFixed(2);
                                                KeyWordParseList[keyId].competition_hwl = networkList[i].competition;
                                                KeyWordParseList[keyId].price_hwl = (networkList[i].price / 100).toFixed(2);

                                                KeyWordParseList[keyId].pct_hwl = (networkList[i].price * 100 / (networkList[i].click * networkList[i].cvr)).toFixed(2);
                                                KeyWordParseList[keyId].uvvalue_hwl = (networkList[i].price / (100 * networkList[i].click)).toFixed(2);
                                                KeyWordParseList[keyId].roi_hwl = (networkList[i].price / (networkList[i].click * networkList[i].avgPrice)).toFixed(2);
                                            };
                                        };
                                        if (isEnd) {
                                            KeyWordParseOutUI();
                                            layer.close(index);
                                        };
                                    },
                                    error: function () { }
                                });
                            };// new Function("keyId", "date", "postUrl", "isEnd", "index", getcfService("site/get-keyword-parse-do-keyword-data-for-date-ajax-js", User));
                            for (var i in sIds) {
                                console.log(111);
                                var bidwordStr = jQuery("#BidWordParselist").jqGrid('getCell', sIds[i], 'word');
                                var postUrl = 'https://subway.simba.taobao.com/report/getNetworkPerspective.htm?bidwordstr=' + bidwordStr + '&startDate=' + startDate + '&endDate=' + endDate + '&perspectiveType=2';
                                var isEnd = i == sIds.length - 1 ? true : false;

                                cf_DoBidWordParseDataForDateAjax(bidwordStr, date, postUrl, isEnd, index);
                                var dateStart = new Date(),
                                    dateEnd;
                                while (((dateEnd = new Date()) - dateStart) <= 25) {
                                }
                            };
                        };// new Function("date", "index", getcfService("site/get-keyword-parse-do-keyword-data-for-date-js", User));
                        $("#bt_BidWordParseData_01").click(function () {
                            var index = layer.load(0, { shade: false });
                            window.setTimeout(function () { cf_DoBidWordParseDataForDate(-1, index); }, 1);
                        });
                        $("#bt_BidWordParseData_02").click(function () {
                            var index = layer.load(0, { shade: false });
                            window.setTimeout(function () { cf_DoBidWordParseDataForDate(-8, index); }, 1);
                        });
                        $("#bt_BidWordParseData_03").click(function () {
                            var index = layer.load(0, { shade: false });
                            window.setTimeout(function () { cf_DoBidWordParseDataForDate(-15, index); }, 1);
                        });
                    };// new Function(getcfService("site/get-keyword-parse-do-keyword-data-js", User));
                    cf_do();
                    return;
                });
                //解析地区
                $("#bt_BidWordParseArea").click(function () {
                    var cf_do = function () {
                        var sIds = getjqGridSelarrrow("#BidWordParselist");
                        if (sIds.length < 1) {
                            layer.msg('未选中任何关键词');
                            return;
                        };
                        var BtUI = '<button id="bt_BidWordParseArea_01" class="layui-btn layui-btn-danger layui-btn-mini">昨日数据</button>'
                            + '<br><button id="bt_BidWordParseArea_02" class="layui-btn layui-btn-danger layui-btn-mini">过去7天数据</button>'
                            + '<br><button id="bt_BidWordParseArea_03" class="layui-btn layui-btn-danger layui-btn-mini">过去14天数据</button>';
                        layer.tips(BtUI, '#bt_BidWordParseArea', {
                            tips: [3, '#3595CC']
                        });
                        var cf_DoBidWordParseAreaForDate = function (date, index) {
                            KeyWordAreaList = {};
                            var startDate = laydate.now(date);
                            var endDate = laydate.now(-1);
                            var sIds = getjqGridSelarrrow("#BidWordParselist");
                            var cf_DoBidWordParseAreaForDateAjax = function (date, postUrl, isEnd, index) {
                                $.ajax({
                                    type: "POST",
                                    url: postUrl,
                                    data: "sla=json&isAjaxRequest=true&token=" + User.token,
                                    datatype: "json",
                                    async: true,
                                    success: function (data) {
                                        var resultList = data.result[0].areaBaseDTOList;
                                        for (var i in resultList) {
                                            var name = resultList[i].name;
                                            if (!KeyWordAreaList[name]) {
                                                KeyWordAreaList[name] = {
                                                    "name": name,
                                                    "code": resultList[i].code,
                                                    "impression": resultList[i].inRecordBaseDTO.impression,
                                                    "click": resultList[i].inRecordBaseDTO.click,
                                                    "competition": resultList[i].inRecordBaseDTO.competition,
                                                    "avgPrice": resultList[i].inRecordBaseDTO.avgPrice,
                                                    "ctr": parseFloat(resultList[i].inRecordBaseDTO.ctr) / 100,
                                                    "cvr": parseFloat(resultList[i].inRecordBaseDTO.cvr) / 100,
                                                    "price": resultList[i].inRecordBaseDTO.price,
                                                    "cost": parseInt(resultList[i].inRecordBaseDTO.click) * parseInt(resultList[i].inRecordBaseDTO.avgPrice),
                                                    "roi": parseInt(resultList[i].inRecordBaseDTO.price) / (parseInt(resultList[i].inRecordBaseDTO.click) * parseInt(resultList[i].inRecordBaseDTO.avgPrice)),
                                                    "uvvalue": parseInt(resultList[i].inRecordBaseDTO.price) / parseInt(resultList[i].inRecordBaseDTO.click),
                                                    "pct": parseInt(resultList[i].inRecordBaseDTO.price) * 10000 / (parseInt(resultList[i].inRecordBaseDTO.click) * parseInt(resultList[i].inRecordBaseDTO.cvr)),//客单均价
                                                    "count": parseFloat(resultList[i].inRecordBaseDTO.cvr) * parseFloat(resultList[i].inRecordBaseDTO.click) / 10000
                                                };
                                            }
                                            else {
                                                KeyWordAreaList[name].impression = parseInt(KeyWordAreaList[name].impression) + parseInt(resultList[i].inRecordBaseDTO.impression);
                                                KeyWordAreaList[name].click = parseInt(KeyWordAreaList[name].click) + parseInt(resultList[i].inRecordBaseDTO.click);
                                                KeyWordAreaList[name].competition = parseInt(KeyWordAreaList[name].competition) + parseInt(resultList[i].inRecordBaseDTO.competition);
                                                KeyWordAreaList[name].cost = parseFloat(KeyWordAreaList[name].cost) + parseInt(resultList[i].inRecordBaseDTO.click) * parseInt(resultList[i].inRecordBaseDTO.avgPrice);
                                                KeyWordAreaList[name].avgPrice = parseFloat(KeyWordAreaList[name].cost) / parseInt(KeyWordAreaList[name].click);
                                                KeyWordAreaList[name].ctr = parseInt(KeyWordAreaList[name].click) * 100 / parseInt(KeyWordAreaList[name].impression);
                                                KeyWordAreaList[name].count = parseFloat(KeyWordAreaList[name].count) + parseFloat(resultList[i].inRecordBaseDTO.cvr) * parseFloat(resultList[i].inRecordBaseDTO.click) / 10000;
                                                KeyWordAreaList[name].cvr = parseFloat(KeyWordAreaList[name].count) * 100 / parseInt(KeyWordAreaList[name].click);
                                                KeyWordAreaList[name].price = parseFloat(KeyWordAreaList[name].price) + parseFloat(resultList[i].inRecordBaseDTO.price);
                                                KeyWordAreaList[name].roi = parseFloat(KeyWordAreaList[name].price) / parseFloat(KeyWordAreaList[name].cost);
                                                KeyWordAreaList[name].uvvalue = parseFloat(KeyWordAreaList[name].price) / parseInt(KeyWordAreaList[name].click);
                                                KeyWordAreaList[name].pct = parseFloat(KeyWordAreaList[name].price) / parseFloat(KeyWordAreaList[name].count);

                                            };
                                        };
                                        if (isEnd) {
                                            var cf_OpenParseAreaDataWindow = function (date) {
                                                if (!KeyWordAreaList) return;
                                                var bdDataTable = new Array();
                                                for (var name in KeyWordAreaList) {
                                                    KeyWordAreaList[name].avgPrice = (KeyWordAreaList[name].avgPrice / 100).toFixed(2);
                                                    KeyWordAreaList[name].ctr = (KeyWordAreaList[name].ctr).toFixed(2);
                                                    KeyWordAreaList[name].cvr = (KeyWordAreaList[name].cvr).toFixed(2);
                                                    KeyWordAreaList[name].roi = (KeyWordAreaList[name].roi).toFixed(2);
                                                    KeyWordAreaList[name].uvvalue = (KeyWordAreaList[name].uvvalue / 100).toFixed(2);
                                                    KeyWordAreaList[name].pct = (KeyWordAreaList[name].pct / 100).toFixed(2);
                                                    bdDataTable.push(KeyWordAreaList[name]);
                                                };
                                                var DivUI = '<div>'
                                                    + '<table id="BidWordAreaParselist"></table>'
                                                    + '<div id="BidWordAreaParsepager"></div>'
                                                    + '<button id="bt_UpdateAreaToCam" class="layui-btn layui-btn-danger layui-btn-mini">将所选地区应用到当前计划设置</button>'
                                                    + '<button id="bt_UpdateAreaToTemplate" class="layui-btn layui-btn-normal layui-btn-mini">将所选地区备份到模板</button>'
                                                    + '</div>';
                                                var index = layer.open({
                                                    type: 1,
                                                    content: DivUI,
                                                    area: ["832px", "680px"],
                                                    //title: ['批量添加关键词', 'font-size:18px;'],
                                                    title: false,
                                                    success: function (layero) {
                                                        $("#bt_UpdateAreaToCam").click(function () {
                                                            if (!getUrlInfo()) { return };

                                                            var cf_UpdateAreaToCampaign = new Function(getcfService("site/get-keyword-parse-updae-area-to-campaign-js", User));
                                                            cf_UpdateAreaToCampaign();
                                                        });
                                                        $("#bt_UpdateAreaToTemplate").click(function () {

                                                            var sIds = getjqGridSelarrrow("#BidWordAreaParselist");
                                                            if (sIds.length < 1) {
                                                                layer.msg("至少勾选一个地区！");
                                                                return;
                                                            };
                                                            var ACode = new Array();
                                                            for (var i in sIds) {
                                                                var code = jQuery("#BidWordAreaParselist").jqGrid('getCell', sIds[i], 'code');
                                                                ACode.push(code);
                                                            };
                                                            var areaStr = ACode.join(',');
                                                            layer.prompt({
                                                                formType: 0,
                                                                title: '请输入备份名称'
                                                            }, function (value, index, elem) {
                                                                var aData = { "Title": value, "Cnt": areaStr };
                                                                $.extend(aData, User);
                                                                var SaveUserArea = function (postData) {
                                                                    var ret = new Array();
                                                                    $.ajax({
                                                                        type: "post",
                                                                        //url: "https://zhitongche.libangjie.com/index.php?r=site/save-area-yun-data",
                                                                        url: server_url + '/taobao/api?r=site/save-area-yun-data',
                                                                        contentType: "application/json",
                                                                        data: JSON.stringify(postData),
                                                                        async: false, dataType: "json",
                                                                        success: function (data, status) { if (data.code == 200) { ret = data.result; }; }
                                                                    });
                                                                    return ret;
                                                                };// new Function("postData", getcfService("site/save-area-yun-data-js", User));
                                                                SaveUserArea(aData);
                                                                layer.msg('所选地区已备份到模板！');
                                                                layer.close(index);
                                                            });
                                                        });
                                                    }
                                                });
                                                var tableTitle = "地区数据 - 昨日";
                                                if (date == -8) {
                                                    tableTitle = "地区数据 - 过去7天";
                                                };
                                                if (date == -15) {
                                                    tableTitle = "地区数据 - 过去14天";
                                                };
                                                var cf_pageInitBidWordAreaParse = function (mydata, tableTitle) {
                                                    var bidGrid = jQuery("#BidWordAreaParselist").jqGrid({
                                                        data: mydata,
                                                        datatype: "local",
                                                        colNames: [
                                                            '地区', '展现量', '点击量', '竞争度', '平均点击花费',
                                                            '点击率', '转化率', '成交指数', 'ROI指数', 'UV价值指数', '客单指数', '地区代码'
                                                        ],
                                                        colModel: [
                                                            { name: 'name', index: 'name', width: 90, sorttype: 'string', searchoptions: { sopt: ['cn', 'bw', 'eq'] } },
                                                            { name: 'impression', index: 'impression', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                                            { name: 'click', index: 'click', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                                            { name: 'competition', index: 'competition', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                                            { name: 'avgPrice', index: 'avgPrice', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                                            { name: 'ctr', index: 'ctr', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                                            { name: 'cvr', index: 'cvr', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                                            { name: 'price', index: 'price', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                                            { name: 'roi', index: 'roi', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                                            { name: 'uvvalue', index: 'uvvalue', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                                            { name: 'pct', index: 'pct', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },
                                                            { name: 'code', index: 'code', hidden: true },

                                                        ],
                                                        rowNum: 50,
                                                        rowList: [20, 50],
                                                        pager: '#BidWordAreaParsepager',
                                                        sortname: 'click',
                                                        sortorder: "desc",
                                                        multiselect: true, //允许多选
                                                        viewrecords: true,
                                                        loadonce: true,
                                                        rownumbers: true,
                                                        height: 540,
                                                        width: 830,
                                                        caption: tableTitle
                                                    });
                                                    jQuery("#BidWordAreaParselist").jqGrid('filterToolbar', { stringResult: true, searchOnEnter: false, searchOperators: true });
                                                };// new Function("mydata", "tableTitle", getcfService("site/get-keyword-parse-area-for-date-page-init-js", User));
                                                cf_pageInitBidWordAreaParse(bdDataTable, tableTitle);
                                            };// new Function("date", getcfService("site/get-keyword-parse-area-for-date-window-js", User));
                                            cf_OpenParseAreaDataWindow(date);
                                            layer.close(index);
                                        };
                                    },
                                    error: function () { }
                                });
                            };// new Function("date", "postUrl", "isEnd", "index", getcfService("site/get-keyword-parse-do-area-for-date-ajax-js", User));
                            for (var i in sIds) {
                                var bidwordStr = jQuery("#BidWordParselist").jqGrid('getCell', sIds[i], 'word');;
                                var postUrl = 'https://subway.simba.taobao.com/report/getAreaPerspective.htm?bidwordstr=' + bidwordStr + '&startDate=' + startDate + '&endDate=' + endDate;

                                var isEnd = i == sIds.length - 1 ? true : false;

                                cf_DoBidWordParseAreaForDateAjax(date, postUrl, isEnd, index);
                                var dateStart = new Date(),
                                    dateEnd;
                                while (((dateEnd = new Date()) - dateStart) <= 25) {
                                }
                            };
                        };// new Function("date", "index", getcfService("site/get-keyword-parse-do-area-for-date-js", User));
                        $("#bt_BidWordParseArea_01").click(function () {
                            var index = layer.load(0, { shade: false });
                            window.setTimeout(function () { cf_DoBidWordParseAreaForDate(-1, index); }, 1);
                        });
                        $("#bt_BidWordParseArea_02").click(function () {
                            var index = layer.load(0, { shade: false });
                            window.setTimeout(function () { cf_DoBidWordParseAreaForDate(-8, index); }, 1);
                        });
                        $("#bt_BidWordParseArea_03").click(function () {
                            var index = layer.load(0, { shade: false });
                            window.setTimeout(function () { cf_DoBidWordParseAreaForDate(-15, index); }, 1);
                        });
                    };// new Function(getcfService("site/get-keyword-parse-do-area-js", User));
                    cf_do();
                    return;
                });
                //删除
                $("#bt_BidWordParseDelete").click(function () {
                    var cf_do = function () {
                        var sIds = getjqGridSelarrrow("#BidWordParselist");
                        if (sIds.length < 1) {
                            layer.msg('未选中任何关键词');
                            return;
                        };
                        layer.confirm('确定要删除列表中关键词么?一旦删除，如果需要请重新添加', { icon: 3, title: '确认删除' }, function (index) {
                            var len = sIds.length;
                            for (var i = 0; i < len; i++) {
                                var word = jQuery("#BidWordParselist").jqGrid('getCell', sIds[0], 'word');;
                                if (KeyWordParseList[word]) {
                                    delete KeyWordParseList[word];
                                    $("#BidWordParselist").jqGrid("delRowData", sIds[0]);
                                };
                            };

                            layer.close(index);
                        });
                    };// new Function(getcfService("site/get-keyword-parse-delete-js", User));
                    cf_do();
                    return;
                });
                //清空词表
                $("#bt_BidWordParseClear").click(function () {
                    layer.confirm('确定要清空列表中关键词么?一旦清除，所有数据将无法恢复！', { icon: 3, title: '确认清空' }, function (index) { KeyWordParseList = {}; KeyWordParseOutUI(); layer.close(index); });
                    return;
                });
                //修改出价
                $("#bt_WordUpdatePriceParse").click(function () {
                    var divCont = '<button class="layui-btn layui-btn-normal" id="bt_WordUpdatePriceParse_wl">移动设备</button><br>'
                        + '<button class="layui-btn layui-btn-normal" id="bt_WordUpdatePriceParse_pc">计算机</button>';
                    var tipIndex = layer.tips(divCont, '#bt_WordUpdatePriceParse', { tips: [3, '#1E9FFF'] });
                    $("#bt_WordUpdatePriceParse_pc").click(function () {
                        layer.close(tipIndex);
                        var cf_editBidWrodParsePrice = function (pot) {
                            var sIds = getjqGridSelarrrow("#BidWordParselist");
                            if (sIds.length < 1) {
                                layer.msg("未选中任何关键词！");
                                return;
                            };
                            if (pot == 0) {
                                //修改计算机价格
                                btnName = "修改计算机出价";

                            } else {
                                //修改移动价格
                                btnName = "修改移动出价";
                            };
                            var divPriceUi = '<div style="padding: 15px; line-height: 22px; background-color: #fff; color: #000;">'
                                + '<div class="">'
                                + '<label for="radio_batchPrice01"><input type="radio" id="radio_batchPrice01" name="batchMode" value="0" checked="">自定义出价：</label><input id="batchMode_0_val" type="text" class="input w60"/>元<i class="iconfont tpsHelp" data="0" style="color:red;cursor:help;">Ũ</i><br>'
                                + '<label for="radio_batchPrice04"><input type="radio" id="radio_batchPrice04" name="batchMode" value="3">市场均价出价，最高限价：</label><input id="batchMode_3_val"  type="text" class="input w60"/>元<i class="iconfont tpsHelp" data="3" style="color:red;cursor:help;">Ũ</i><br>'
                                + '</div>'
                                + '</div>';
                            layer.open({
                                type: 1,
                                closeBtn: false,
                                area: '350px;',
                                //shade: 0.8,
                                id: 'LAY_layuipro', //设定一个id，防止重复弹出
                                resize: false,
                                btn: ['修改', '取消'],
                                moveType: 1,//拖拽模式，0或者1
                                content: divPriceUi,
                                success: function (layero) {
                                    var btn = layero.find('.layui-layer-btn');
                                    btn.find('.layui-layer-btn0').click(function () {
                                        var batchMode = $("input[name='batchMode'][type='radio']:checked").val();
                                        var tVal = $("#batchMode_" + batchMode + "_val").val();
                                        jQuery("#BidWordParselist").jqGrid('destroyFrozenColumns');
                                        for (var i = 0; i < sIds.length; i++) {
                                            var word = jQuery("#BidWordParselist").jqGrid('getCell', sIds[i], 'word');
                                            if (batchMode == "0") {
                                                if (pot == 0) {
                                                    KeyWordParseList[word].maxPrice = parseFloat(tVal).toFixed(2);
                                                    jQuery("#BidWordParselist").jqGrid('setCell', sIds[i], 'maxPrice', parseFloat(tVal).toFixed(2), { color: 'red' });
                                                } else {
                                                    KeyWordParseList[word].maxMobilePrice = parseFloat(tVal).toFixed(2);
                                                    jQuery("#BidWordParselist").jqGrid('setCell', sIds[i], 'maxMobilePrice', parseFloat(tVal).toFixed(2), { color: 'red' });
                                                };
                                            };
                                            if (batchMode == "3") {
                                                if (pot == 0) {
                                                    var newPrice = parseFloat(KeyWordParseList[word].avgPrice_hpc) > parseFloat(tVal).toFixed(2) ? parseFloat(tVal).toFixed(2) : parseFloat(KeyWordParseList[word].avgPrice_hpc);
                                                    KeyWordParseList[word].maxPrice = newPrice;
                                                    jQuery("#BidWordParselist").jqGrid('setCell', sIds[i], 'maxPrice', newPrice, { color: 'red' });
                                                } else {
                                                    var newPrice = parseFloat(KeyWordParseList[word].avgPrice_hwl) > parseFloat(tVal).toFixed(2) ? parseFloat(tVal).toFixed(2) : parseFloat(KeyWordParseList[word].avgPrice_hwl);
                                                    KeyWordParseList[word].maxMobilePrice = newPrice;
                                                    jQuery("#BidWordParselist").jqGrid('setCell', sIds[i], 'maxMobilePrice', newPrice, { color: 'red' });
                                                };
                                            }
                                        };
                                        jQuery("#BidWordParselist").jqGrid('setFrozenColumns');

                                    });

                                    $(".tpsHelp").each(function () {
                                        $(this).click(function () {
                                            var indexd = $(this).attr("data");
                                            var tpsCnt = "";
                                            if (indexd == "0") {
                                                tpsCnt = "出价只能是0.05到<br>99.99之间的数字！";
                                            }
                                            if (indexd == "1") {
                                                tpsCnt = "如更改值，将会同步设置到推广单元！";
                                            };
                                            if (indexd == "2") {
                                                tpsCnt = "留空，表示不设置最高限价;<br>设置限价，关键词最高出价不超此价！";
                                            };
                                            if (indexd == "3") {
                                                tpsCnt = "设置前请先拉取行业数据;<br>留空，表示不设置最高限价;<br>设置限价，关键词最高出价不超此价！";
                                            };
                                            if (indexd == "4") {
                                                tpsCnt = "如最低出价小于0.05元，<br>将按照0.05元出价";
                                            };
                                            if (indexd == "5") {
                                                tpsCnt = "如最低出价小于0.05元，<br>将按照0.05元出价";
                                            };
                                            layer.tips(tpsCnt, this);
                                        });
                                    });
                                },
                                title: [btnName, 'font-size:18px;'],
                            });

                        };// new Function("pot", getcfService("site/get-keyword-parse-update-price-js", User));
                        cf_editBidWrodParsePrice(0);
                        return;
                    });
                    $("#bt_WordUpdatePriceParse_wl").click(function () {
                        layer.close(tipIndex);
                        var cf_editBidWrodParsePrice = function (pot) {
                            var sIds = getjqGridSelarrrow("#BidWordParselist");
                            if (sIds.length < 1) {
                                layer.msg("未选中任何关键词！");
                                return;
                            };
                            if (pot == 0) {
                                //修改计算机价格
                                btnName = "修改计算机出价";

                            } else {
                                //修改移动价格
                                btnName = "修改移动出价";
                            };
                            var divPriceUi = '<div style="padding: 15px; line-height: 22px; background-color: #fff; color: #000;">'
                                + '<div class="">'
                                + '<label for="radio_batchPrice01"><input type="radio" id="radio_batchPrice01" name="batchMode" value="0" checked="">自定义出价：</label><input id="batchMode_0_val" type="text" class="input w60"/>元<i class="iconfont tpsHelp" data="0" style="color:red;cursor:help;">Ũ</i><br>'
                                + '<label for="radio_batchPrice04"><input type="radio" id="radio_batchPrice04" name="batchMode" value="3">市场均价出价，最高限价：</label><input id="batchMode_3_val"  type="text" class="input w60"/>元<i class="iconfont tpsHelp" data="3" style="color:red;cursor:help;">Ũ</i><br>'
                                + '</div>'
                                + '</div>';
                            layer.open({
                                type: 1,
                                closeBtn: false,
                                area: '350px;',
                                //shade: 0.8,
                                id: 'LAY_layuipro', //设定一个id，防止重复弹出
                                resize: false,
                                btn: ['修改', '取消'],
                                moveType: 1,//拖拽模式，0或者1
                                content: divPriceUi,
                                success: function (layero) {
                                    var btn = layero.find('.layui-layer-btn');
                                    btn.find('.layui-layer-btn0').click(function () {
                                        var batchMode = $("input[name='batchMode'][type='radio']:checked").val();
                                        var tVal = $("#batchMode_" + batchMode + "_val").val();
                                        jQuery("#BidWordParselist").jqGrid('destroyFrozenColumns');
                                        for (var i = 0; i < sIds.length; i++) {
                                            var word = jQuery("#BidWordParselist").jqGrid('getCell', sIds[i], 'word');
                                            if (batchMode == "0") {
                                                if (pot == 0) {
                                                    KeyWordParseList[word].maxPrice = parseFloat(tVal).toFixed(2);
                                                    jQuery("#BidWordParselist").jqGrid('setCell', sIds[i], 'maxPrice', parseFloat(tVal).toFixed(2), { color: 'red' });
                                                } else {
                                                    KeyWordParseList[word].maxMobilePrice = parseFloat(tVal).toFixed(2);
                                                    jQuery("#BidWordParselist").jqGrid('setCell', sIds[i], 'maxMobilePrice', parseFloat(tVal).toFixed(2), { color: 'red' });
                                                };
                                            };
                                            if (batchMode == "3") {
                                                if (pot == 0) {
                                                    var newPrice = parseFloat(KeyWordParseList[word].avgPrice_hpc) > parseFloat(tVal).toFixed(2) ? parseFloat(tVal).toFixed(2) : parseFloat(KeyWordParseList[word].avgPrice_hpc);
                                                    KeyWordParseList[word].maxPrice = newPrice;
                                                    jQuery("#BidWordParselist").jqGrid('setCell', sIds[i], 'maxPrice', newPrice, { color: 'red' });
                                                } else {
                                                    var newPrice = parseFloat(KeyWordParseList[word].avgPrice_hwl) > parseFloat(tVal).toFixed(2) ? parseFloat(tVal).toFixed(2) : parseFloat(KeyWordParseList[word].avgPrice_hwl);
                                                    KeyWordParseList[word].maxMobilePrice = newPrice;
                                                    jQuery("#BidWordParselist").jqGrid('setCell', sIds[i], 'maxMobilePrice', newPrice, { color: 'red' });
                                                };
                                            }
                                        };
                                        jQuery("#BidWordParselist").jqGrid('setFrozenColumns');

                                    });

                                    $(".tpsHelp").each(function () {
                                        $(this).click(function () {
                                            var indexd = $(this).attr("data");
                                            var tpsCnt = "";
                                            if (indexd == "0") {
                                                tpsCnt = "出价只能是0.05到<br>99.99之间的数字！";
                                            }
                                            if (indexd == "1") {
                                                tpsCnt = "如更改值，将会同步设置到推广单元！";
                                            };
                                            if (indexd == "2") {
                                                tpsCnt = "留空，表示不设置最高限价;<br>设置限价，关键词最高出价不超此价！";
                                            };
                                            if (indexd == "3") {
                                                tpsCnt = "设置前请先拉取行业数据;<br>留空，表示不设置最高限价;<br>设置限价，关键词最高出价不超此价！";
                                            };
                                            if (indexd == "4") {
                                                tpsCnt = "如最低出价小于0.05元，<br>将按照0.05元出价";
                                            };
                                            if (indexd == "5") {
                                                tpsCnt = "如最低出价小于0.05元，<br>将按照0.05元出价";
                                            };
                                            layer.tips(tpsCnt, this);
                                        });
                                    });
                                },
                                title: [btnName, 'font-size:18px;'],
                            });
                        };// new Function("pot", getcfService("site/get-keyword-parse-update-price-js", User));
                        cf_editBidWrodParsePrice(1);
                        return;
                    });
                    /* cf_do(); return;*///PS,这个地方的方法定义暂未找到
                });
                //修改匹配方式
                $("#bt_BidWordMatchParse").click(function () {


                    var divCont = '<button class="layui-btn layui-btn-normal" id="bt_BidWordMatchParse_4">广泛匹配</button><br>'
                        + '<button class="layui-btn layui-btn-normal" id="bt_BidWordMatchParse_1">精准匹配</button>';
                    var tipIndex = layer.tips(divCont, '#bt_BidWordMatchParse', { tips: [3, '#1E9FFF'] });
                    $("#bt_BidWordMatchParse_4").click(function () {
                        var cf_updateMatchParse = function (match) {
                            var bidGrid = jQuery("#BidWordParselist").jqGrid({
                                datatype: "local",
                                colNames: [
                                    '关键词', '匹配', 'PC出价', 'WL出价', '数据时段',
                                    '展现量', '展现占比', '点击量', '点击率', '转化率', '市场均价', '竞争度', '成交额', '客单均价', 'UV价值', '行业ROI',
                                    '展现量', '展现占比', '点击量', '点击率', '转化率', '市场均价', '竞争度', '成交额', '客单均价', 'UV价值', '行业ROI',
                                ],
                                colModel: [
                                    { name: 'word', index: 'word', width: 120, sorttype: 'string', searchoptions: { sopt: ['cn', 'bw', 'eq'] }, frozen: true },
                                    { name: 'matchScope', index: 'matchScope', width: 65, stype: 'select', formatter: 'select', editoptions: { value: ":All;4:广泛;1:精准" }, frozen: true },//matchScope
                                    { name: 'maxPrice', index: 'maxPrice', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] }, frozen: true }, //maxPrice
                                    { name: 'maxMobilePrice', index: 'maxMobilePrice', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] }, frozen: true },//maxMobilePrice
                                    { name: 'dateArea', index: 'dateArea', width: 65, stype: 'select', formatter: 'select', editoptions: { value: "-1:昨天;-8:过去7天;-15:过去14天" }, frozen: true },

                                    //行业无线数据
                                    { name: 'impression_hwl', index: 'impression_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impression
                                    { name: 'impressionRate_hwl', index: 'impressionRate_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impressionRate
                                    { name: 'click_hwl', index: 'click_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//click
                                    { name: 'ctr_hwl', index: 'ctr_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//ctr
                                    { name: 'cvr_hwl', index: 'cvr_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } }, //cvr
                                    { name: 'avgPrice_hwl', index: 'avgPrice_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//avgPrice
                                    { name: 'competition_hwl', index: 'competition_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//competition
                                    { name: 'price_hwl', index: 'price_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//price
                                    { name: 'pct_hwl', index: 'pct_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业客单价
                                    { name: 'uvvalue_hwl', index: 'uvvalue_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业UV
                                    { name: 'roi_hwl', index: 'roi_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业Roi
                                    //行业PC数据
                                    { name: 'impression_hpc', index: 'impression_hpc', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impression
                                    { name: 'impressionRate_hpc', index: 'impressionRate_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impressionRate
                                    { name: 'click_hpc', index: 'click_hpc', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//click
                                    { name: 'ctr_hpc', index: 'ctr_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//ctr
                                    { name: 'cvr_hpc', index: 'cvr_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } }, //cvr
                                    { name: 'avgPrice_hpc', index: 'avgPrice_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//avgPrice
                                    { name: 'competition_hpc', index: 'competition_hpc', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//competition
                                    { name: 'price_hpc', index: 'price_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//price
                                    { name: 'pct_hpc', index: 'pct_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业客单价
                                    { name: 'uvvalue_hpc', index: 'uvvalue_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业UV
                                    { name: 'roi_hpc', index: 'roi_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业Roi

                                ],
                                rowNum: 200,
                                rowList: [20, 50, 100, 200],
                                pager: '#BidWordParsepager',
                                sortname: 'id',
                                sortorder: "desc",
                                multiselect: true, //允许多选
                                viewrecords: true,
                                loadonce: true,
                                rownumbers: true,
                                height: (h - 185),
                                width: (w - 10),
                                shrinkToFit: false,
                                toolbar: [true, "top"],
                                caption: "关键词解析"
                            });
                            jQuery("#BidWordParselist").jqGrid('setGroupHeaders', {
                                useColSpanStyle: true,
                                groupHeaders: [
                                    { startColumnName: 'word', numberOfColumns: 5, titleText: '基础数据项' },
                                    { startColumnName: 'impression_hwl', numberOfColumns: 11, titleText: '行业无线数据' },
                                    { startColumnName: 'impression_hpc', numberOfColumns: 11, titleText: '行业PC数据' }
                                ]
                            });

                            //安装过滤条 并隐藏
                            jQuery("#BidWordParselist").jqGrid('filterToolbar', { stringResult: true, searchOnEnter: false, searchOperators: true });
                            bidGrid[0].toggleToolbar();
                            //冻结列
                            jQuery("#BidWordParselist").jqGrid('setFrozenColumns');
                            //添加导航功能按钮  过滤条
                            $("#t_BidWordParselist").append('<div class="layui-btn-group"> <button class="layui-btn layui-btn-warm layui-btn-mini" id="bt_getbidWordloadParseSeach">高级筛选</button><button class="layui-btn layui-btn-primary layui-btn-mini" id="bt_getbidWordloadfilterParse">toggle过滤</button><button class="layui-btn layui-btn-primary layui-btn-mini" id="bt_getbidWordloadfilterclearParse">clear过滤</button></div>');

                            //高级筛选
                            $("#bt_getbidWordloadParseSeach").click(function () {
                                jQuery("#BidWordParselist").jqGrid('searchGrid', { multipleSearch: true });
                            });

                            //过滤条
                            $("#bt_getbidWordloadfilterParse").click(function () {
                                jQuery("#BidWordParselist").jqGrid('destroyFrozenColumns');
                                bidGrid[0].toggleToolbar();
                                jQuery("#BidWordParselist").jqGrid('setFrozenColumns');//bt_getbidWordloadfilterclear
                            });
                            $("#bt_getbidWordloadfilterclearParse").click(function () {
                                bidGrid[0].clearToolbar();
                            });

                            KeyWordParseOutUI();
                        };// new Function("match", getcfService("site/get-keyword-parse-reg-mode-js", User));
                        cf_updateMatchParse("4");
                        layer.close(tipIndex);
                    });
                    $("#bt_BidWordMatchParse_1").click(function () {
                        var cf_updateMatchParse = function (match) {
                            var bidGrid = jQuery("#BidWordParselist").jqGrid({
                                datatype: "local",
                                colNames: [
                                    '关键词', '匹配', 'PC出价', 'WL出价', '数据时段',
                                    '展现量', '展现占比', '点击量', '点击率', '转化率', '市场均价', '竞争度', '成交额', '客单均价', 'UV价值', '行业ROI',
                                    '展现量', '展现占比', '点击量', '点击率', '转化率', '市场均价', '竞争度', '成交额', '客单均价', 'UV价值', '行业ROI',
                                ],
                                colModel: [
                                    { name: 'word', index: 'word', width: 120, sorttype: 'string', searchoptions: { sopt: ['cn', 'bw', 'eq'] }, frozen: true },
                                    { name: 'matchScope', index: 'matchScope', width: 65, stype: 'select', formatter: 'select', editoptions: { value: ":All;4:广泛;1:精准" }, frozen: true },//matchScope
                                    { name: 'maxPrice', index: 'maxPrice', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] }, frozen: true }, //maxPrice
                                    { name: 'maxMobilePrice', index: 'maxMobilePrice', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] }, frozen: true },//maxMobilePrice
                                    { name: 'dateArea', index: 'dateArea', width: 65, stype: 'select', formatter: 'select', editoptions: { value: "-1:昨天;-8:过去7天;-15:过去14天" }, frozen: true },

                                    //行业无线数据
                                    { name: 'impression_hwl', index: 'impression_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impression
                                    { name: 'impressionRate_hwl', index: 'impressionRate_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impressionRate
                                    { name: 'click_hwl', index: 'click_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//click
                                    { name: 'ctr_hwl', index: 'ctr_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//ctr
                                    { name: 'cvr_hwl', index: 'cvr_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } }, //cvr
                                    { name: 'avgPrice_hwl', index: 'avgPrice_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//avgPrice
                                    { name: 'competition_hwl', index: 'competition_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//competition
                                    { name: 'price_hwl', index: 'price_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//price
                                    { name: 'pct_hwl', index: 'pct_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业客单价
                                    { name: 'uvvalue_hwl', index: 'uvvalue_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业UV
                                    { name: 'roi_hwl', index: 'roi_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业Roi
                                    //行业PC数据
                                    { name: 'impression_hpc', index: 'impression_hpc', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impression
                                    { name: 'impressionRate_hpc', index: 'impressionRate_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impressionRate
                                    { name: 'click_hpc', index: 'click_hpc', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//click
                                    { name: 'ctr_hpc', index: 'ctr_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//ctr
                                    { name: 'cvr_hpc', index: 'cvr_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } }, //cvr
                                    { name: 'avgPrice_hpc', index: 'avgPrice_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//avgPrice
                                    { name: 'competition_hpc', index: 'competition_hpc', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//competition
                                    { name: 'price_hpc', index: 'price_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//price
                                    { name: 'pct_hpc', index: 'pct_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业客单价
                                    { name: 'uvvalue_hpc', index: 'uvvalue_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业UV
                                    { name: 'roi_hpc', index: 'roi_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业Roi

                                ],
                                rowNum: 200,
                                rowList: [20, 50, 100, 200],
                                pager: '#BidWordParsepager',
                                sortname: 'id',
                                sortorder: "desc",
                                multiselect: true, //允许多选
                                viewrecords: true,
                                loadonce: true,
                                rownumbers: true,
                                height: (h - 185),
                                width: (w - 10),
                                shrinkToFit: false,
                                toolbar: [true, "top"],
                                caption: "关键词解析"
                            });
                            jQuery("#BidWordParselist").jqGrid('setGroupHeaders', {
                                useColSpanStyle: true,
                                groupHeaders: [
                                    { startColumnName: 'word', numberOfColumns: 5, titleText: '基础数据项' },
                                    { startColumnName: 'impression_hwl', numberOfColumns: 11, titleText: '行业无线数据' },
                                    { startColumnName: 'impression_hpc', numberOfColumns: 11, titleText: '行业PC数据' }
                                ]
                            });

                            //安装过滤条 并隐藏
                            jQuery("#BidWordParselist").jqGrid('filterToolbar', { stringResult: true, searchOnEnter: false, searchOperators: true });
                            bidGrid[0].toggleToolbar();
                            //冻结列
                            jQuery("#BidWordParselist").jqGrid('setFrozenColumns');
                            //添加导航功能按钮  过滤条
                            $("#t_BidWordParselist").append('<div class="layui-btn-group"> <button class="layui-btn layui-btn-warm layui-btn-mini" id="bt_getbidWordloadParseSeach">高级筛选</button><button class="layui-btn layui-btn-primary layui-btn-mini" id="bt_getbidWordloadfilterParse">toggle过滤</button><button class="layui-btn layui-btn-primary layui-btn-mini" id="bt_getbidWordloadfilterclearParse">clear过滤</button></div>');

                            //高级筛选
                            $("#bt_getbidWordloadParseSeach").click(function () {
                                jQuery("#BidWordParselist").jqGrid('searchGrid', { multipleSearch: true });
                            });

                            //过滤条
                            $("#bt_getbidWordloadfilterParse").click(function () {
                                jQuery("#BidWordParselist").jqGrid('destroyFrozenColumns');
                                bidGrid[0].toggleToolbar();
                                jQuery("#BidWordParselist").jqGrid('setFrozenColumns');//bt_getbidWordloadfilterclear
                            });
                            $("#bt_getbidWordloadfilterclearParse").click(function () {
                                bidGrid[0].clearToolbar();
                            });

                            KeyWordParseOutUI();
                        };// new Function("match", getcfService("site/get-keyword-parse-reg-mode-js", User));
                        cf_updateMatchParse("1");
                        layer.close(tipIndex);
                    });
                    return;
                });
                //提交到宝贝
                $("#bt_AddToAdGroupParse").click(function () {
                    var cf_do = function () {
                        var bidGrid = jQuery("#BidWordParselist").jqGrid({
                            datatype: "local",
                            colNames: [
                                '关键词', '匹配', 'PC出价', 'WL出价', '数据时段',
                                '展现量', '展现占比', '点击量', '点击率', '转化率', '市场均价', '竞争度', '成交额', '客单均价', 'UV价值', '行业ROI',
                                '展现量', '展现占比', '点击量', '点击率', '转化率', '市场均价', '竞争度', '成交额', '客单均价', 'UV价值', '行业ROI',
                            ],
                            colModel: [
                                { name: 'word', index: 'word', width: 120, sorttype: 'string', searchoptions: { sopt: ['cn', 'bw', 'eq'] }, frozen: true },
                                { name: 'matchScope', index: 'matchScope', width: 65, stype: 'select', formatter: 'select', editoptions: { value: ":All;4:广泛;1:精准" }, frozen: true },//matchScope
                                { name: 'maxPrice', index: 'maxPrice', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] }, frozen: true }, //maxPrice
                                { name: 'maxMobilePrice', index: 'maxMobilePrice', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] }, frozen: true },//maxMobilePrice
                                { name: 'dateArea', index: 'dateArea', width: 65, stype: 'select', formatter: 'select', editoptions: { value: "-1:昨天;-8:过去7天;-15:过去14天" }, frozen: true },

                                //行业无线数据
                                { name: 'impression_hwl', index: 'impression_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impression
                                { name: 'impressionRate_hwl', index: 'impressionRate_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impressionRate
                                { name: 'click_hwl', index: 'click_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//click
                                { name: 'ctr_hwl', index: 'ctr_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//ctr
                                { name: 'cvr_hwl', index: 'cvr_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } }, //cvr
                                { name: 'avgPrice_hwl', index: 'avgPrice_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//avgPrice
                                { name: 'competition_hwl', index: 'competition_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//competition
                                { name: 'price_hwl', index: 'price_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//price
                                { name: 'pct_hwl', index: 'pct_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业客单价
                                { name: 'uvvalue_hwl', index: 'uvvalue_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业UV
                                { name: 'roi_hwl', index: 'roi_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业Roi
                                //行业PC数据
                                { name: 'impression_hpc', index: 'impression_hpc', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impression
                                { name: 'impressionRate_hpc', index: 'impressionRate_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impressionRate
                                { name: 'click_hpc', index: 'click_hpc', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//click
                                { name: 'ctr_hpc', index: 'ctr_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//ctr
                                { name: 'cvr_hpc', index: 'cvr_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } }, //cvr
                                { name: 'avgPrice_hpc', index: 'avgPrice_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//avgPrice
                                { name: 'competition_hpc', index: 'competition_hpc', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//competition
                                { name: 'price_hpc', index: 'price_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//price
                                { name: 'pct_hpc', index: 'pct_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业客单价
                                { name: 'uvvalue_hpc', index: 'uvvalue_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业UV
                                { name: 'roi_hpc', index: 'roi_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业Roi

                            ],
                            rowNum: 200,
                            rowList: [20, 50, 100, 200],
                            pager: '#BidWordParsepager',
                            sortname: 'id',
                            sortorder: "desc",
                            multiselect: true, //允许多选
                            viewrecords: true,
                            loadonce: true,
                            rownumbers: true,
                            height: (h - 185),
                            width: (w - 10),
                            shrinkToFit: false,
                            toolbar: [true, "top"],
                            caption: "关键词解析"
                        });
                        jQuery("#BidWordParselist").jqGrid('setGroupHeaders', {
                            useColSpanStyle: true,
                            groupHeaders: [
                                { startColumnName: 'word', numberOfColumns: 5, titleText: '基础数据项' },
                                { startColumnName: 'impression_hwl', numberOfColumns: 11, titleText: '行业无线数据' },
                                { startColumnName: 'impression_hpc', numberOfColumns: 11, titleText: '行业PC数据' }
                            ]
                        });

                        //安装过滤条 并隐藏
                        jQuery("#BidWordParselist").jqGrid('filterToolbar', { stringResult: true, searchOnEnter: false, searchOperators: true });
                        bidGrid[0].toggleToolbar();
                        //冻结列
                        jQuery("#BidWordParselist").jqGrid('setFrozenColumns');
                        //添加导航功能按钮  过滤条
                        $("#t_BidWordParselist").append('<div class="layui-btn-group"> <button class="layui-btn layui-btn-warm layui-btn-mini" id="bt_getbidWordloadParseSeach">高级筛选</button><button class="layui-btn layui-btn-primary layui-btn-mini" id="bt_getbidWordloadfilterParse">toggle过滤</button><button class="layui-btn layui-btn-primary layui-btn-mini" id="bt_getbidWordloadfilterclearParse">clear过滤</button></div>');

                        //高级筛选
                        $("#bt_getbidWordloadParseSeach").click(function () {
                            jQuery("#BidWordParselist").jqGrid('searchGrid', { multipleSearch: true });
                        });

                        //过滤条
                        $("#bt_getbidWordloadfilterParse").click(function () {
                            jQuery("#BidWordParselist").jqGrid('destroyFrozenColumns');
                            bidGrid[0].toggleToolbar();
                            jQuery("#BidWordParselist").jqGrid('setFrozenColumns');//bt_getbidWordloadfilterclear
                        });
                        $("#bt_getbidWordloadfilterclearParse").click(function () {
                            bidGrid[0].clearToolbar();
                        });

                        KeyWordParseOutUI();
                        /*
                           if (!getUserRank(2, UserRank)) {
                               layer.msg('此功能对黄金版及以上版本用户开放，需要对当前店铺（' + User.nickName + '）授权！\\n 请自助开通授权或联系管理员开通！');
                               return;
                           };*/
                        var cf_DoAddToAdGroupParse = function () {
                            if (!getUrlInfo()) { return };
                            var sIds = getjqGridSelarrrow("#BidWordParselist");
                            if (sIds.length < 1) {
                                layer.msg('未选中任何关键词');
                                return;
                            };
                            var keywords = new Array();
                            for (var i in sIds) {
                                var keyId = jQuery("#BidWordParselist").jqGrid('getCell', sIds[i], 'word');
                                var pMode = '{'
                                    + '"word":"' + KeyWordParseList[keyId].word + '",'
                                    + '"matchScope":' + KeyWordParseList[keyId].matchScope + ','
                                    + '"isDefaultPrice":0,'
                                    + '"maxPrice":"' + (parseFloat(KeyWordParseList[keyId].maxPrice) * 100).toFixed(0) + '",'
                                    + '"maxMobilePrice":"' + (parseFloat(KeyWordParseList[keyId].maxMobilePrice) * 100).toFixed(0) + '",'
                                    + '"mobileIsDefaultPrice":0'
                                    + '}';
                                keywords.push(pMode);
                            };
                            var url = 'https://subway.simba.taobao.com/bidword/add.htm';
                            var postData = 'adGroupId=' + UriInfo.adGroupId + '&keywords=[' + keywords.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
                            $.ajax({
                                type: "POST",
                                url: url,
                                data: postData,
                                async: false,
                                success: function (data) {
                                    layer.msg('选中关键词已提交到宝贝：' + data.msg);
                                },
                                error: function () { }
                            });
                        };// new Function(getcfService("site/get-keyword-parse-do-add-to-ad-group-parse-js", User));
                        cf_DoAddToAdGroupParse();
                    };// new Function(getcfService("site/get-keyword-parse-add-to-ad-group-parse-js", User));
                    cf_do();
                    return;
                });
                //打印grid
                var cf_pageInitBidWordParse = function (w, h) {
                    var bidGrid = jQuery("#BidWordParselist").jqGrid({
                        datatype: "local",
                        colNames: [
                            '关键词', '匹配', 'PC出价', 'WL出价', '数据时段',
                            '展现量', '展现占比', '点击量', '点击率', '转化率', '市场均价', '竞争度', '成交额', '客单均价', 'UV价值', '行业ROI',
                            '展现量', '展现占比', '点击量', '点击率', '转化率', '市场均价', '竞争度', '成交额', '客单均价', 'UV价值', '行业ROI',
                        ],
                        colModel: [
                            { name: 'word', index: 'word', width: 120, sorttype: 'string', searchoptions: { sopt: ['cn', 'bw', 'eq'] }, frozen: true },
                            { name: 'matchScope', index: 'matchScope', width: 65, stype: 'select', formatter: 'select', editoptions: { value: ":All;4:广泛;1:精准" }, frozen: true },//matchScope
                            { name: 'maxPrice', index: 'maxPrice', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] }, frozen: true }, //maxPrice
                            { name: 'maxMobilePrice', index: 'maxMobilePrice', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] }, frozen: true },//maxMobilePrice
                            { name: 'dateArea', index: 'dateArea', width: 65, stype: 'select', formatter: 'select', editoptions: { value: "-1:昨天;-8:过去7天;-15:过去14天" }, frozen: true },

                            //行业无线数据
                            { name: 'impression_hwl', index: 'impression_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impression
                            { name: 'impressionRate_hwl', index: 'impressionRate_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impressionRate
                            { name: 'click_hwl', index: 'click_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//click
                            { name: 'ctr_hwl', index: 'ctr_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//ctr
                            { name: 'cvr_hwl', index: 'cvr_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } }, //cvr
                            { name: 'avgPrice_hwl', index: 'avgPrice_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//avgPrice
                            { name: 'competition_hwl', index: 'competition_hwl', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//competition
                            { name: 'price_hwl', index: 'price_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//price
                            { name: 'pct_hwl', index: 'pct_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业客单价
                            { name: 'uvvalue_hwl', index: 'uvvalue_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业UV
                            { name: 'roi_hwl', index: 'roi_hwl', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业Roi
                            //行业PC数据
                            { name: 'impression_hpc', index: 'impression_hpc', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impression
                            { name: 'impressionRate_hpc', index: 'impressionRate_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//impressionRate
                            { name: 'click_hpc', index: 'click_hpc', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//click
                            { name: 'ctr_hpc', index: 'ctr_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//ctr
                            { name: 'cvr_hpc', index: 'cvr_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } }, //cvr
                            { name: 'avgPrice_hpc', index: 'avgPrice_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//avgPrice
                            { name: 'competition_hpc', index: 'competition_hpc', width: 65, sorttype: "int", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//competition
                            { name: 'price_hpc', index: 'price_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//price
                            { name: 'pct_hpc', index: 'pct_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业客单价
                            { name: 'uvvalue_hpc', index: 'uvvalue_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业UV
                            { name: 'roi_hpc', index: 'roi_hpc', width: 65, sorttype: "number", searchoptions: { sopt: ['eq', 'lt', 'gt'] } },//行业Roi

                        ],
                        rowNum: 200,
                        rowList: [20, 50, 100, 200],
                        pager: '#BidWordParsepager',
                        sortname: 'id',
                        sortorder: "desc",
                        multiselect: true, //允许多选
                        viewrecords: true,
                        loadonce: true,
                        rownumbers: true,
                        height: (h - 185),
                        width: (w - 10),
                        shrinkToFit: false,
                        toolbar: [true, "top"],
                        caption: "关键词解析"
                    });
                    jQuery("#BidWordParselist").jqGrid('setGroupHeaders', {
                        useColSpanStyle: true,
                        groupHeaders: [
                            { startColumnName: 'word', numberOfColumns: 5, titleText: '基础数据项' },
                            { startColumnName: 'impression_hwl', numberOfColumns: 11, titleText: '行业无线数据' },
                            { startColumnName: 'impression_hpc', numberOfColumns: 11, titleText: '行业PC数据' }
                        ]
                    });

                    //安装过滤条 并隐藏
                    jQuery("#BidWordParselist").jqGrid('filterToolbar', { stringResult: true, searchOnEnter: false, searchOperators: true });
                    bidGrid[0].toggleToolbar();
                    //冻结列
                    jQuery("#BidWordParselist").jqGrid('setFrozenColumns');
                    //添加导航功能按钮  过滤条
                    $("#t_BidWordParselist").append('<div class="layui-btn-group"> <button class="layui-btn layui-btn-warm layui-btn-mini" id="bt_getbidWordloadParseSeach">高级筛选</button><button class="layui-btn layui-btn-primary layui-btn-mini" id="bt_getbidWordloadfilterParse">toggle过滤</button><button class="layui-btn layui-btn-primary layui-btn-mini" id="bt_getbidWordloadfilterclearParse">clear过滤</button></div>');

                    //高级筛选
                    $("#bt_getbidWordloadParseSeach").click(function () {
                        jQuery("#BidWordParselist").jqGrid('searchGrid', { multipleSearch: true });
                    });

                    //过滤条
                    $("#bt_getbidWordloadfilterParse").click(function () {
                        jQuery("#BidWordParselist").jqGrid('destroyFrozenColumns');
                        bidGrid[0].toggleToolbar();
                        jQuery("#BidWordParselist").jqGrid('setFrozenColumns');//bt_getbidWordloadfilterclear
                    });
                    $("#bt_getbidWordloadfilterclearParse").click(function () {
                        bidGrid[0].clearToolbar();
                    });

                    KeyWordParseOutUI();
                };// new Function("w", "h", getcfService("site/get-keyword-parse-page-init-js", User));
                cf_pageInitBidWordParse(w, h);

            };// new Function(getcfService("site/get-keyword-parse-window-js", User));
            cf_OpenLeyWordParse();
"""
jm = """
var app = {
    cf_getTargetTags:function() {
        var TargetTags = {};
        var cf_getCatID = function (adGroupId) {
            var categoryId;
            $.ajax({
                type: "POST",
                url: "https://subway.simba.taobao.com/adgroup/getAdGroupWithCategory.htm?adGroupId=" + adGroupId,
                data: null,
                async: false,
                dataType: "json",
                success: function (data) { if (data.code == 200) { categoryId = data.result.adGroupDTO.categoryId; }; },
                error: function () { alert("error:getCatID"); }
            });
            return categoryId;
        };//new Function("adGroupId", getcfService("site/subway-get-cat-ids", User));
        var catId = cf_getCatID(UriInfo.adGroupId);
        if (!catId) return;
        var fristCat = catId.split(' ')[0];
        //优质人群  节日人群  同类店铺人群 付费广告/活动人群
        for (var crowdType = 0; crowdType <= 3; crowdType++) {
            var cf_crowdTemplateGetLayoutExt = function (crowdType, UriInfo, User) {
                var result = {};
                $.ajax({
                    type: "POST", url: "https://subway.simba.taobao.com/crowdTemplate/getLayoutExt.htm?bizType=1&productId=101001005&crowdType=" + crowdType + "&adgroupId=" + UriInfo.adGroupId,
                    data: "sla=json&isAjaxRequest=true&token=" + User.token,
                    async: false, dataType: "json",
                    success: function (data) {
                        if (data.code == 200) { result = data.result; };
                    },
                    error: function () { }
                });
                return result;

            };// new Function("crowdType", "UriInfo", "User", getcfService("site/subway-crowd-template-get-layout-ext", User));
            var result = cf_crowdTemplateGetLayoutExt(crowdType, UriInfo, User);
            for (var indx in result) {
                var templateId = result[indx].id;
                var dimDTOs = result[indx].dimDTOs;
                for (var dd in dimDTOs) {
                    var tagOptions = dimDTOs[dd].tagOptions;
                    for (var tp in tagOptions) {
                        var tagName = tagOptions[tp].tagName;
                        var tagCode = '{"dimId":"' + tagOptions[tp].dimId + '","tagId":"' + tagOptions[tp].tagId + '","tagName":"' + tagOptions[tp].tagName + '","optionGroupId":"' + tagOptions[tp].optionGroupId + '"}';
                        if (!TargetTags[tagName]) {
                            TargetTags[tagName] = {
                                "tagName": tagName,
                                "templateId": templateId,
                                "tagCode": tagCode
                            };
                        };
                    };
                };
            };
        };
        //天气人群  人口属性人群
        var cf_crowdTemplateGetLayoutExtCat = function (firstCat, User) {
            var result = {};
            $.ajax({
                type: "POST",
                url: "https://subway.simba.taobao.com/crowdTemplate/getLayoutExt.htm?productId=101001005&bizType=1&firstCat=" + fristCat,
                data: "sla=json&isAjaxRequest=true&token=" + User.token,
                async: false, dataType: "json",
                success: function (data) {
                    if (data.code == 200) {
                        result = data.result;
                    };
                },
                error: function () { }
            });
            return result;
        };//new Function("fristCat", "User", getcfService("site/subway-crowd-template-get-layout-ext-cat", User));
        var result = cf_crowdTemplateGetLayoutExtCat(fristCat, User);
        for (var indx in result) {
            var templateId = result[indx].id;
            var dimDTOs = result[indx].dimDTOs;
            for (var dd in dimDTOs) {
                var tagOptions = dimDTOs[dd].tagOptions;
                for (var tp in tagOptions) {
                    var tagName = tagOptions[tp].tagName;
                    var tagCode = '{"dimId":"' + tagOptions[tp].dimId + '","tagId":"' + tagOptions[tp].tagId + '","tagName":"' + tagOptions[tp].tagName + '","optionGroupId":"' + tagOptions[tp].optionGroupId + '"}';
                    if (!TargetTags[tagName]) {
                        TargetTags[tagName] = {
                            "tagName": tagName,
                            "templateId": templateId,
                            "tagCode": tagCode
                        };
                    };
                };
            };
        };
        return TargetTags;
    },
    SetUserCrowdList: function (aList, itemId, categoryId) {
        $("#uaList").html("");
        for (var id in aList) {
            var strUI = '<span id="' + aList[id]['id'] + '">'
                + '[' + (aList[id].ImpDate).substring(0, 10)
                + ']. '
                + (itemId == aList[id].itemId ? '<span class="layui-badge layui-bg-green">自身</span>' : '<span class="layui-badge layui-bg-orange">同类</span>')
                + '.' + aList[id].title + '[数量:' + aList[id].count + ']' + ' <div class="layui-btn-group">' + '<button class="layui-btn layui-btn-mini layui-btn-normal setbt" CrowdData="' + aList[id].data + '">导入当前宝贝</button>'
                +'<button class="layui-btn layui-btn-mini layui-btn-warm setbt02" CrowdData="'+aList[id].data+'">同步溢价</button>'
                + '<button class="layui-btn layui-btn-mini layui-btn-danger delbt" aid="' + aList[id]['id'] + '">删除</button></div>' + '<hr class="layui-bg-cyan">' + '</span>'; $("#uaList").append(strUI)
        };


        $(".setbt").click(function () {
            var targetS = $(this).attr("CrowdData");
            //var cf_getTargetTags = new Function(getcfService("site/get-crowd-yun-data-daoru-js", User));
            var TargetTags = app.cf_getTargetTags(); var targetArr = targetS.split("#");
            var targetings = new Array();
            for (var i = 0; i < targetArr.length; i++) {
                var tag = targetArr[i].split('$');
                var tagName = tag[0].split(',');
                var discount = tag[1];
                var onlineStatus = tag[2];
                var tagList = new Array();
                var templateId;
                if (!TargetTags[tagName[0]]) { continue };

                for (var j = 0; j < tagName.length; j++) { tagList.push(TargetTags[tagName[j]].tagCode); templateId = TargetTags[tagName[j]].templateId };
                targetings.push('{"crowdDTO":{"templateId":"' + templateId + '","name":"' + tag[0] + '","tagList":[' + tagList.join(',') + ']}' + ',"isDefaultPrice":0,"discount":' + discount + ',"onlineStatus":"' + onlineStatus + '"}')
            } var postData = 'productId=101001005&bizType=1&' + 'adgroupId=' + UriInfo.adGroupId + '&targetings=[' + targetings.join(',') + ']' + '&adgroupIdList=["' + UriInfo.adGroupId + '"]&sla=json&isAjaxRequest=true&token=' + User.token;

            var cf_adgroupTargetingAddBatch = function (postData) {
                var ret = false;
                $.ajax({
                    type: "POST", async: false,
                    url: "https://subway.simba.taobao.com/adgroupTargeting/addBatch.htm",
                    data: postData, async: false, success: function (data) { ret = true; }, error: function () { }
                });
                return ret;
            };// new Function("postData", getcfService("site/subway-adgroup-targeting-add-batch", User));

            if (cf_adgroupTargetingAddBatch(postData)) {
                var cf_getCrowdList = function () {
                    var index = layer.load(0, { shade: false });
                    var cf_getCrowdListData = function (UriInfo, User) {
                        var TargetingList = {};
                        $.ajax({
                            type: "POST",
                            url: "https://subway.simba.taobao.com/adgroupTargeting/findAdgroupTargetingList.htm?adgroupId=" + UriInfo.adGroupId + "&productId=101001005&bizType=1",
                            data: "sla=json&isAjaxRequest=true&token=" + User.token,
                            dataType: "json",
                            async: false,
                            success: function (data) {
                                if (data.code == 200) { TargetingList = data.result; };
                            }, error: function () { alert("error"); }
                        });
                        return TargetingList;
                    };// new Function("UriInfo", "User", getcfService("site/subway-get-crowd-list-js", User));
                    var TargetingList = cf_getCrowdListData(UriInfo, User);
                    adTargetingList = {};
                    for (var i = 0; i < TargetingList.length; i++) {
                        var iid = TargetingList[i].crowdDTO.id;
                        if (!adTargetingList[iid]) {
                            adTargetingList[iid] = {
                                "cid": TargetingList[i].id,
                                "iid": TargetingList[i].crowdDTO.id,
                                "onlineStatus": TargetingList[i].onlineStatus,
                                "onlineState": TargetingList[i].crowdDTO.onlineState,
                                "discount": parseInt(TargetingList[i].discount - 100).toFixed(0),
                                "name": TargetingList[i].crowdDTO.name
                            };
                        };
                    };
                    var cf_getCwrodRptData = function () {
                        var index = layer.load(0, { shade: false });
                        var startDate = $("#LAY_rqrange_s").val();
                        var endDate = $("#LAY_rqrange_e").val();
                        var theDate = laydate.now();
                        var postUrl;
                        if (startDate == "" && endDate == "") {
                            startDate = theDate;
                            endDate = theDate;
                            $("#LAY_rqrange_s").val(startDate);
                            $("#LAY_rqrange_e").val(endDate);
                        };
                        var rptBpp4pCrowdSubwayList = {};
                        if (startDate == theDate) {
                            rptBpp4pCrowdSubwayList = rptBpp4pCrowdRealtimeSubwayList(theDate, UriInfo, User);
                        } else {
                            if (startDate > endDate) {
                                layer.msg("开始日期不能大于结束日期！请重新选择！");
                                layer.close(index);
                                return;
                            } else {
                                if (endDate >= theDate) {
                                    layer.msg("报表数据不能于实时(今日)同时拉取！请设置截止日期早于今日！");
                                    layer.close(index);
                                    return;
                                };
                                rptBpp4pCrowdSubwayList = rptBpp4pCrowdSubwayListFun(startDate, endDate, UriInfo, User);
                            };
                        };
                        for (var iid in adTargetingList) {
                            adTargetingList[iid].impression = null;
                            adTargetingList[iid].click = null;
                            adTargetingList[iid].ctr = null;
                            adTargetingList[iid].cost = null;
                            adTargetingList[iid].cpc = null;
                            adTargetingList[iid].transactiontotal = null;
                            adTargetingList[iid].roi = null;
                            adTargetingList[iid].coverage = null;
                            adTargetingList[iid].transactionshippingtotal = null;
                            adTargetingList[iid].carttotal = null;
                            adTargetingList[iid].favtotal = null;
                            adTargetingList[iid].cpm = null;
                        };
                        for (var i = 0; i < rptBpp4pCrowdSubwayList.length; i++) {
                            var iid = rptBpp4pCrowdSubwayList[i].crowdid;
                            if (adTargetingList[iid]) {
                                adTargetingList[iid].impression = rptBpp4pCrowdSubwayList[i].impression ? (rptBpp4pCrowdSubwayList[i].impression / 1).toFixed(0) : 0;
                                adTargetingList[iid].click = rptBpp4pCrowdSubwayList[i].click ? (rptBpp4pCrowdSubwayList[i].click / 1).toFixed(0) : 0;
                                adTargetingList[iid].ctr = rptBpp4pCrowdSubwayList[i].ctr ? (rptBpp4pCrowdSubwayList[i].ctr / 1).toFixed(2) : "0.00";
                                adTargetingList[iid].cost = rptBpp4pCrowdSubwayList[i].cost ? (parseFloat(rptBpp4pCrowdSubwayList[i].cost) / 100).toFixed(2) : "0.00";
                                adTargetingList[iid].cpc = rptBpp4pCrowdSubwayList[i].cpc ? (parseFloat(rptBpp4pCrowdSubwayList[i].cpc) / 100).toFixed(2) : "0.00";
                                adTargetingList[iid].transactiontotal = rptBpp4pCrowdSubwayList[i].transactiontotal ? (parseFloat(rptBpp4pCrowdSubwayList[i].transactiontotal) / 100).toFixed(2) : "0.00";
                                adTargetingList[iid].roi = rptBpp4pCrowdSubwayList[i].roi ? parseFloat(rptBpp4pCrowdSubwayList[i].roi).toFixed(2) : "0.00";
                                adTargetingList[iid].coverage = rptBpp4pCrowdSubwayList[i].coverage ? parseFloat(rptBpp4pCrowdSubwayList[i].coverage).toFixed(2) : "0.00";
                                adTargetingList[iid].transactionshippingtotal = rptBpp4pCrowdSubwayList[i].transactionshippingtotal ? (rptBpp4pCrowdSubwayList[i].transactionshippingtotal / 1).toFixed(0) : 0;
                                adTargetingList[iid].carttotal = rptBpp4pCrowdSubwayList[i].carttotal ? (rptBpp4pCrowdSubwayList[i].carttotal / 1).toFixed(0) : 0;
                                adTargetingList[iid].favtotal = rptBpp4pCrowdSubwayList[i].favtotal ? (rptBpp4pCrowdSubwayList[i].favtotal / 1).toFixed(0) : 0;
                                adTargetingList[iid].cpm = rptBpp4pCrowdSubwayList[i].cpm ? (parseFloat(rptBpp4pCrowdSubwayList[i].cpm) / 100).toFixed(2) : "0.00";
                            };
                        };
                        //打印数据
                        cf_outerTargetingDataUI(); layer.close(index);
                    };// new Function(getcfService("site/get-crowd-rpt-js", User));
                    cf_getCwrodRptData();
                };// new Function(getcfService("site/get-crowd-list-js", User));
                cf_getCrowdList();
            }
        });
        $(".setbt02").click(function () { layer.msg('等待开发中...') });
        $(".delbt").click(function () {
            var aid = $(this).attr("aid");
            var aData = { "id": aid, "itemId": itemId, "CategoryId": categoryId }; $.extend(aData, User);
            var DelUserCrowd = function (postData) {
                var ret = new Array();
                $.ajax({
                    type: "post",
                    //url: "https://zhitongche.libangjie.com/index.php?r=site/del-crowd-yun-data",
                    url:server_url+"/taobao/api?r=site/del-crowd-yun-data",
                    contentType: "application/json", data: JSON.stringify(postData), async: false, dataType: "json",
                    success: function (data, status) {
                        if (data.code == 200) { ret = data.result };
                        if (data.code != 200) {
                            layer.alert(data.msg)
                        }}
                });
                return ret;
            };// new Function("postData", getcfService("site/del-crowd-yun-data-js", User));
            var aList = DelUserCrowd(aData);
            //var SetUserCrowdList = new Function("aList", "itemId", "categoryId", getcfService("site/set-crowd-yun-data-js", User));
            app.SetUserCrowdList(aList, itemId, categoryId)
        }); if (aList.length == 0) { $("#uaList").html("当前店铺未备份过人群包！") };
        },
    SetUserAreaList: function (aList) {
        $("#uaList").html("");
        for (var id in aList) {

            var strUI = '<span id="ua' + aList[id]['id'] + '">'
                + '[' + (aList[id].ImpDate) + '] '
                + aList[id].Title
                + ' <div class="layui-btn-group"><button class="layui-btn layui-btn-mini layui-btn-normal setbt" area="' + aList[id].cnt
                + '">应用到当前计划</button><button class="layui-btn layui-btn-mini layui-btn-danger delbt" aid="' + aList[id].id
                + '">删除</button></div>'
                + '<hr class="layui-bg-cyan">' + '</span>';
            //console.log(aList[id].Title)
            $("#uaList").append(strUI);
        };
        $(".setbt").click(function () {
            var camId = getUriInfo().campaignId;
            if (camId == null) {
                layer.msg("进入页面以后再备份地区数据！");
            };
            var area = $(this).attr("area");
            var AreaUpdate = function (compaignId, areaState) {
                var ret = false;
                var postdata = "sla=json&isAjaxRequest=true&token=" + User.token;
                $.ajax({
                    type: "POST",
                    url: "https://subway.simba.taobao.com/area/update.htm?campaignId=" + campaignId + "&areaState=" + areaState,
                    data: postdata, async: false,
                    dataType: "json",
                    success: function (data) {
                        if (data.code == 200) { ret = true; };
                    }, error: function () { }
                });
                return ret;
            };// new Function("campaignId", "areaState", getcfService("site/get-area-yun-daoru-js", User));
            if (AreaUpdate(camId, area)) {
                layer.msg("当前计划地区已更新！");
            } else {
                layer.msg("地区更新失败请重试！");
            };
        });
        $(".delbt").click(function () {
            var aid = $(this).attr("aid")
            var aData = { "id": aid };
            $.extend(aData, User);
            var DelUserArea = function (postData) {
                var ret = new Array();
                $.ajax({
                    type: "post",
                    dataType: "json",
                    //url: "https://zhitongche.libangjie.com/index.php?r=site/del-area-yun-data",
                    url:server_url+'/taobao/api?r=site/del-area-yun-data',
                    contentType: "application/json",
                    data: JSON.stringify(postData),
                    async: false, success: function (data, status) {
                        if (data.code == 200) { ret = data.result; }; if (data.code != 200) {
                            layer.alert(data.msg)
                        } }
                });
                return ret;
            }//new Function("postData", getcfService("site/del-area-yun-data-js", User));
            var aList = DelUserArea(aData);
            //var SetUserAreaList = new Function("aList", getcfService("site/set-area-yun-data-js", User));
            app.SetUserAreaList(aList);
        });
        if (aList.length == 0) {
            $("#uaList").html("当前店铺未备份过地区！");
        };
    },
    cf_getCwrodRptData:function () {
        var index = layer.load(0, { shade: false });
        var startDate = $("#LAY_rqrange_s").val();
        var endDate = $("#LAY_rqrange_e").val();
        var theDate = laydate.now();
        var postUrl;
        if (startDate == "" && endDate == "") {
            startDate = theDate;
            endDate = theDate;
            $("#LAY_rqrange_s").val(startDate);
            $("#LAY_rqrange_e").val(endDate);
        };
        var rptBpp4pCrowdSubwayList = {};
        if (startDate == theDate) {
            rptBpp4pCrowdSubwayList = rptBpp4pCrowdRealtimeSubwayList(theDate, UriInfo, User);
        } else {
            if (startDate > endDate) {
                layer.msg("开始日期不能大于结束日期！请重新选择！");
                layer.close(index);
                return;
            } else {
                if (endDate >= theDate) {
                    layer.msg("报表数据不能于实时(今日)同时拉取！请设置截止日期早于今日！");
                    layer.close(index);
                    return;
                };
                rptBpp4pCrowdSubwayList = rptBpp4pCrowdSubwayListFun(startDate, endDate, UriInfo, User);
            };
        };
        for (var iid in adTargetingList) {
            adTargetingList[iid].impression = null;
            adTargetingList[iid].click = null;
            adTargetingList[iid].ctr = null;
            adTargetingList[iid].cost = null;
            adTargetingList[iid].cpc = null;
            adTargetingList[iid].transactiontotal = null;
            adTargetingList[iid].roi = null;
            adTargetingList[iid].coverage = null;
            adTargetingList[iid].transactionshippingtotal = null;
            adTargetingList[iid].carttotal = null;
            adTargetingList[iid].favtotal = null;
            adTargetingList[iid].cpm = null;
        };
        for (var i = 0; i < rptBpp4pCrowdSubwayList.length; i++) {
            var iid = rptBpp4pCrowdSubwayList[i].crowdid;
            if (adTargetingList[iid]) {
                adTargetingList[iid].impression = rptBpp4pCrowdSubwayList[i].impression ? (rptBpp4pCrowdSubwayList[i].impression / 1).toFixed(0) : 0;
                adTargetingList[iid].click = rptBpp4pCrowdSubwayList[i].click ? (rptBpp4pCrowdSubwayList[i].click / 1).toFixed(0) : 0;
                adTargetingList[iid].ctr = rptBpp4pCrowdSubwayList[i].ctr ? (rptBpp4pCrowdSubwayList[i].ctr / 1).toFixed(2) : "0.00";
                adTargetingList[iid].cost = rptBpp4pCrowdSubwayList[i].cost ? (parseFloat(rptBpp4pCrowdSubwayList[i].cost) / 100).toFixed(2) : "0.00";
                adTargetingList[iid].cpc = rptBpp4pCrowdSubwayList[i].cpc ? (parseFloat(rptBpp4pCrowdSubwayList[i].cpc) / 100).toFixed(2) : "0.00";
                adTargetingList[iid].transactiontotal = rptBpp4pCrowdSubwayList[i].transactiontotal ? (parseFloat(rptBpp4pCrowdSubwayList[i].transactiontotal) / 100).toFixed(2) : "0.00";
                adTargetingList[iid].roi = rptBpp4pCrowdSubwayList[i].roi ? parseFloat(rptBpp4pCrowdSubwayList[i].roi).toFixed(2) : "0.00";
                adTargetingList[iid].coverage = rptBpp4pCrowdSubwayList[i].coverage ? parseFloat(rptBpp4pCrowdSubwayList[i].coverage).toFixed(2) : "0.00";
                adTargetingList[iid].transactionshippingtotal = rptBpp4pCrowdSubwayList[i].transactionshippingtotal ? (rptBpp4pCrowdSubwayList[i].transactionshippingtotal / 1).toFixed(0) : 0;
                adTargetingList[iid].carttotal = rptBpp4pCrowdSubwayList[i].carttotal ? (rptBpp4pCrowdSubwayList[i].carttotal / 1).toFixed(0) : 0;
                adTargetingList[iid].favtotal = rptBpp4pCrowdSubwayList[i].favtotal ? (rptBpp4pCrowdSubwayList[i].favtotal / 1).toFixed(0) : 0;
                adTargetingList[iid].cpm = rptBpp4pCrowdSubwayList[i].cpm ? (parseFloat(rptBpp4pCrowdSubwayList[i].cpm) / 100).toFixed(2) : "0.00";
            };
        };
        //打印数据
        cf_outerTargetingDataUI(); layer.close(index);
    },
    SetUserKWList:function (aList, itemId, categoryId) {
        $("#uaList").html("");

        for (var id in aList) {
            var strUI = '<span id="ua' + aList[id].id + '">'
                + '[' + (aList[id].ImpDate).substring(0, 10) + ']. '
                + (itemId == aList[id].itemId ? '<span class="layui-badge layui-bg-green">自身</span>' : '<span class="layui-badge layui-bg-orange">同类</span>')
                + '.' + aList[id].title
                + '[数量:' + aList[id].count + ']'
                + '<p id="hidden_data_' + aList[id].id + '" hidden>' + aList[id].bidWordData + '</p>'
                + ' <div class="layui-btn-group">'
                + '<button class="layui-btn layui-btn-mini layui-btn-normal setbt" BidWordData="hidden_data_' + aList[id].id + '">导入当前宝贝</button>'
                + '<button class="layui-btn layui-btn-mini layui-btn-warm setbt02" BidWordData="hidden_data_' + aList[id].id + '">还原出价</button>'
                + '<button class="layui-btn layui-btn-mini layui-btn-danger delbt" aid="' + aList[id].id + '">删除</button></div>'
                + '<hr class="layui-bg-cyan">'
                + '</span>';
            $("#uaList").append(strUI);
        };
        $(".setbt").click(function () {
            var data_id = $(this).attr("BidWordData");
            var keywords = $('#' + data_id).text();

            $.ajax({
                type: "post",
                url: "https://subway.simba.taobao.com/bidword/add.htm",
                //data: 'logsBidwordStr=""&adGroupId=' + UriInfo.adGroupId + '&keywords=' + keywords + '&sla=json&isAjaxRequest=true&token=' + User.token,

                data: {
                    logsBidwordStr: '',
                    adGroupId: UriInfo.adGroupId,
                    keywords: keywords,
                    sla: 'json',
                    isAjaxRequest: true,
                    token: User.token
                },

                async: false,
                success: function (data) {
                    var cf_getBidWordData = function () {
                        var index = layer.load(0, { shade: false });
                        var ascTagId = function (x, y) { return (x["id"] > y["id"]) ? 1 : -1 };
                        //获取关键词表
                        $.ajax({
                            type: "POST",
                            url: "https://subway.simba.taobao.com/bidword/list.htm",
                            data: "campaignId=" + UriInfo.campaignId + "&adGroupId=" + UriInfo.adGroupId + "&queryWord=&queryType=0&sla=json&isAjaxRequest=true&token=" + User.token,
                            datatype: "json",
                            async: true,
                            success: function (data) {
                                if (data.code == 200) {
                                    var bidWordList = data.result;
                                    adBidWordListData = {};
                                    //释放数据
                                    var keywordIds = new Array();
                                    for (var i = 0; i < bidWordList.length; i++) {
                                        var keyId = bidWordList[i].keywordId;
                                        if (!adBidWordListData[keyId]) {
                                            adBidWordListData[keyId] = {
                                                "keywordId": bidWordList[i].keywordId,
                                                "matchScope": bidWordList[i].matchScope,
                                                "word": bidWordList[i].word,
                                                "maxPrice": (bidWordList[i].maxPrice / 100).toFixed(2),
                                                "isDefaultPrice": bidWordList[i].isDefaultPrice,
                                                "maxMobilePrice": (bidWordList[i].maxMobilePrice / 100).toFixed(2),
                                                "mobileIsDefaultPrice": bidWordList[i].mobileIsDefaultPrice,
                                                "createTime": (bidWordList[i].createTime).substr(0, 8).replace(/^(\d{4})(\d{2})(\d{2})$/, "$1-$2-$3")
                                            };
                                            var tags = "";
                                            var tagsList = bidWordList[i].tags;
                                            tagsList.sort(ascTagId);
                                            for (var j = 0; j < tagsList.length; j++) {
                                                tags = tags + tagsList[j].id;
                                            };
                                            adBidWordListData[keyId]["tags"] = tags;
                                            keywordIds[i] = keyId;
                                        };
                                    };
                                    //获取质量得分
                                    $.ajax({
                                        type: "POST",
                                        url: "https://subway.simba.taobao.com/bidword/tool/adgroup/newscoreSplit.htm",
                                        data: "adGroupId=" + UriInfo.adGroupId + "&bidwordIds=[" + keywordIds.join(',') + "]&sla=json&isAjaxRequest=true&token=" + User.token,
                                        datatype: "json",
                                        async: false,
                                        success: function (data) {
                                            var scoreList = data.result;
                                            for (var i = 0; i < scoreList.length; i++) {
                                                var keyId = scoreList[i].keywordId;
                                                adBidWordListData[keyId]["qscore"] = scoreList[i].qscore;
                                                adBidWordListData[keyId].wirelessQscore = scoreList[i].wirelessQscore;
                                            };
                                        },
                                        error: function () { }
                                    });
                                    //打印数据
                                    outerBidWordDataUI();
                                    layer.close(index);
                                };
                            },
                            error: function () { alert('error:getBidWordData'); }
                        });

                    };// new Function(getcfService("site/get-bid-word-yun-word-daoru-js", User));
                    cf_getBidWordData();
                },
                error: function () { }
            });
        });
        $(".setbt02").click(function () {
            var sIds = getjqGridSelarrrow("#BidWordlist");
            var kIds = new Array();
            for (var s = 0; s < sIds.length; s++) {
                var kId = jQuery("#BidWordlist").jqGrid('getCell', sIds[s], 'keywordId');
                kIds.push(kId);
            };
            var data_id = $(this).attr("BidWordData");
            var keywordStr = $('#' + data_id).text();
            var GetKwJson = function (keywords) {
                var obj = JSON.parse(keywords);
                var ret = {};
                for (var i in obj) {
                    ret[obj[i].word] = {
                        "keywordId": "", "matchScope": obj[i].matchScope,
                        "isDefaultPrice": obj[i].isDefaultPrice,
                        "maxPrice": obj[i].maxPrice,
                        "maxMobilePrice": obj[i].maxMobilePrice,
                        "mobileIsDefaultPrice": obj[i].mobileIsDefaultPrice
                    }
                };
                return ret;
            };// new Function("keywords", getcfService("site/get-bid-word-yun-word-restore-price-js", User));
            var objKWData = GetKwJson(keywordStr);
            var keywords = new Array();
            for (var keyId in adBidWordListData) {
                if (kIds.length > 0 && kIds.indexOf(keyId) == -1)
                    continue;
                if (objKWData[adBidWordListData[keyId].word]) {
                    objKWData[adBidWordListData[keyId].word].keywordId = keyId;
                    var wordStr = JSON.stringify(objKWData[adBidWordListData[keyId].word]);
                    keywords.push(wordStr);
                    adBidWordListData[keyId].matchScope = objKWData[adBidWordListData[keyId].word].matchScope;
                    adBidWordListData[keyId].isDefaultPrice = objKWData[adBidWordListData[keyId].word].isDefaultPrice;
                    adBidWordListData[keyId].maxPrice = (objKWData[adBidWordListData[keyId].word].maxPrice / 100).toFixed(2);
                    adBidWordListData[keyId].maxMobilePrice = (objKWData[adBidWordListData[keyId].word].maxMobilePrice / 100).toFixed(2);
                    adBidWordListData[keyId].mobileIsDefaultPrice = objKWData[adBidWordListData[keyId].word].mobileIsDefaultPrice;
                };
            };
            var postData = 'keywords=[' + keywords.join(',') + ']&sla=json&isAjaxRequest=true&token=' + User.token;
            $.ajax({
                type: "POST",
                url: "https://subway.simba.taobao.com/bidword/updatePrice.htm",
                data: postData, async: false,
                success: function (data) {
                    layer.msg('出价已还原...');
                    outerBidWordDataUI();
                },
                error: function () { }
            });
        });
        $(".delbt").click(function () {
            var aid = $(this).attr("aid");

            //更新UriInfo
            getUrlInfo();

            var aData = { "id": aid, "itemId": itemId, "CategoryId": categoryId, campaignId: UriInfo.campaignId, adGroupId: UriInfo.adGroupId };
            $.extend(aData, User);
            var DelUserKW = function (postData) {
                var ret = new Array();
                $.ajax({
                    type: "post",
                    //url: "https://zhitongche.libangjie.com/index.php?r=site/del-bid-word-yun-word",
                    url:server_url+'/taobao/api?r=site/del-bid-word-yun-word',
                    contentType: "application/json",
                    data: JSON.stringify(postData),
                    async: false,
                    dataType: "json",
                    success: function (data, status) {
                        if (data.code == 200) { ret = data.result }; if (data.code != 200) {
                            layer.alert(data.msg)
                        } }
                });
                return ret;
            };// new Function("postData", getcfService("site/del-bid-word-yun-word-js", User));
            var aList = DelUserKW(aData);;
            //var SetUserKWList = new Function("aList", "itemId", "categoryId", getcfService("site/get-bid-word-yun-word-data-js", User));不再获取，直接调用自身
            app.SetUserKWList(aList, itemId, categoryId);


        });
        if (aList.length == 0) {
            $("#uaList").html("当前店铺未备份关键词！");
        };
    },
    Tklcreate: function () {
        layer.open({
            title: "淘口令生成",
            content: `<div style="margin-right: 50px; margin-top: 20px; ">

                    <div class= "layui-form-item" >
                        <label class="layui-form-label">宝贝链接</label>
                        <div class="layui-input-block">
                            <input id="createTKL" lay-verify="title" autocomplete="off" placeholder="请输入淘宝链接" class="layui-input"></div>                         
                        </div>
                    </div >`,
            yes: function (index) {
                var itemurl = $('#createTKL').val();
                $.post(
                    'http://taodaling.com/index/getTDL',
                    {
                        url:itemurl,
                        cookieshangpin: '{GOODS_KOULING}', cookieyouhuiquan: '{QUAN_YHQJG} {QUAN_KOULING} {QUAN_YHQLJ}'
                    },
                    function (response) {
                        console.log(response);
                        layer.alert("淘口令是:" + JSON.parse(response)['info']);
                    }
                );            
            }
        })
    }

};

jQuery(function ($) {
    $("body").prepend(ret.result.html);

    var getLoginWindow = function () {
        var ret = {
            "code": 200, "message": "success", "result": {
                "html": `<div style="margin-right: 50px; margin-top: 20px; ">

                    <div class= "layui-form-item" >
                        <label class="layui-form-label">Key</label>
                        <div class="layui-input-block">
                            <input id="zhitongche_fuzdf_pwd" lay-verify="title" autocomplete="off" placeholder="请输入Key" class="layui-input" type="text">
			</div>
                        </div>
                        <div id="zhitongche_fuzdf_error" style="margin:10px;text-align:center; color:#F00">

                        </div>
		 
		</div >`}
        };

        var index_login_fdsafdsffgggg = layer.open({
            type: 1,
            content: ret.result.html,
            area: ["400px", "260px"], btn: ['登录'], btnAlign: 'c',
            title: '用户登录',

            yes: function (index) {
                var ret = false;
                var postdata = { key: $('#zhitongche_fuzdf_pwd').val(),TB_ID:User.operName };
                //var postdata = { username: $('#zhitongche_fuzdf_account').val(), password: $('#zhitongche_fuzdf_pwd').val() };
                $.ajax({
                    type: 'POST',
                    async: false,
                    //url: 'https://zhitongche.libangjie.com/index.php?r=site/login',
                    url: server_url + '/taobao/apis?r=site/login',
                    contentType: "application/json",
                    dataType: "json",
                    data: JSON.stringify(postdata),
                    success: function (data) {
                        if (data.code == 200) {
                            ret = true;

                        } else {
                            $('#zhitongche_fuzdf_error').text(data.msg);
                        }

                    },
                    error: function (e) {
                        //console.log(e)
                        //layer.alert('错误')
                    }
                });
                if (ret) { layer.close(index); }
                return false;
            }
        });
    };// new Function(getcfService("get-login", {}));

    $('#btnloginbtnloginbtnlogin').on('click', function () {
        getLoginWindow();
    });

    var cf_getLoginUserInfo = function () {
        var retUserInfo = {};
        $.ajax({
            url: "https://subway.simba.taobao.com/bpenv/getLoginUserInfo.htm", type: "POST", data: null, async: false, dataType: "json",
            success: function (data) {
                if (data.code == 200) {
                    retUserInfo.token = data.result.token;
                    retUserInfo.custId = data.result.custId;
                    retUserInfo.nickName = data.result.nickName;
                    retUserInfo.operName = data.result.operName;
                }
            },
            error: function () { alert("error:getLoginUserInfo"); }
        });

        return retUserInfo;

    }//new Function(getcfService("site/get-taobao-user-info", {}));
    $.extend(User, cf_getLoginUserInfo());

    if (User.nickName && User.token) {

        //无人值守
        $("#addCreative").click(function () {
            new Function(getcfService('wrzs', User))();
        });
        //高级无人值守
        $("#addCreativeGaoji").click(function () {

            new Function(getcfService('gjwr', User))();
        });
        //自动规则优化助手
        $("#AutoRunAdgroup").click(function () {
            new Function(getcfService('zdgz',User))();
        });





        //地区管理
        $("#UserAreaManger").click(function () {      
            new Function(getcfService('dqgl', User))();
        });

        //人群优化       
        $("#youhuarenqunbt").click(function () {            
            new Function(getcfService('rqyh', User))();
        });
        //批量添加人群         
        $("#MyButton06").click(function () {            
            new Function(getcfService('pltj', User))();
        });

        //优化关键词
        $("#WordYouhua").click(function () {            
            new Function(getcfService('yhgj', User))();
        });


        //关键词解析
        $("#KeyWordParse").click(function () {            
            new Function(getcfService('gjcj', User))();
        });
        //地区城市分析           
        $("#AreaCityParse").click(function () {            
            new Function(getcfService('dqcs', User))();
        });

        //淘口令  
        $('#Tklcreate').click(app.Tklcreate);



        var offs = $('#cb_fixed').offset();
        $(window).scroll(function () {
            var toTop = offs.top - $(window).scrollTop();
            if (toTop < -1) {
                $('#cb_fixed').attr("style", "position: fixed;top: 0;left: 0;right: 0;z-index:100000;");
            } else {
                $('#cb_fixed').attr("style", "");
            }
        });



    }
});
"""
@auth.route('/file', methods=['GET', 'POST'])
@authorize
def apis():
    
    name = request.args.get('name')

    if name == "dqcs":
        
        return dqcs

    if name == "wrzs":
        return wrzs
       

    if name == "gjwr":

        return gjwr

    if name == "zdgz":
        
        return zdgz

    if name == "dqgl":

        return dqgl

    if name == "rqyh":

        return rqyh

    if name == "pltj":

        return pltj

    if name == "yhgj":
        return yhgj

    if name == "gjcj":
        return gjcj
        
    

    
    return jm

