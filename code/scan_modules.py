# coding=utf-8
# Python 3.6.5

import re
import os

all_modules = [
    'keywords',
    'array_map',
    'eval_assert',
    'zendencode',
    'preg_replace',
    'packshell',
    'include_file',
    'dynamic_func',
    'ddos',
    'call_user_func',
    'customize'
]

def keywords(file_content, file_name):
    keywords = [
        'serv-u',
        'wscript.shell',
        'phpspy',
        'jspspy',
        'webshell',
        'shell.application',
        'documents and settings/all users',
        'getruntime().exec',
        '$_[+""]=\'\'','chr(99).chr(104).chr(114)',
        'chr($a[79]).chr($a[78])',
        '"ass"."ert"',
        '挂马',
        '大马'
    ]

    knownshell = [
        '%74%68%36%73%62%65%68%71%6c%61%34%63%6f%5f%73%61%64%66%70%6e%72',
        'ixcixreaixteix_ixfixuixnixctixioixn',
        'r57shell',
    ]

    rulelist = [
        '[\'"]e[\'"]\.[\'"]v[\'"]\.[\'"]a[\'"]\.[\'"]l[\'"]',
        '[\'"]a[\'"]\.[\'"]s[\'"]\.[\'"]s[\'"]\.[\'"]e[\'"]\.[\'"]r[\'"]\.[\'"]t[\'"]'
    ]

    file_content = file_content.lower()

    for key in keywords:
        if key in file_content:
            isok=1
            if isok:
                return 1

    for key in knownshell:
        if key in file_content:
            isok=1
            if isok:
                return 1

    for rule in rulelist:
        result = re.search(rule,file_content)
        try:
            if result.group():
                return 1
        except:
            pass

    if 'cmd.exe' in file_content and 'program files' in file_content:
        isok=1
        if isok:
            return 1

    if 'www.phpdp.org' in file_content:
        return 1
    if 'www.phpjm.net' in file_content:
        return 1

    return None

def array_map(file_content, file_name):
    rule = r'(array_map[\s\n]{0,20}\(.{1,5}(eval|assert|ass\\x65rt).{1,20}\$_(GET|POST|REQUEST).{0,15})'

    if 'array_map' in file_content:
        result = re.compile(rule).findall(file_content)
        if len(result)>0:
            return 1
    else:
        return None

def eval_assert(file_content, file_name):
    rule='((eval|assert)[\s|\n]{0,30}\([\s|\n]{0,30}(\\\\{0,1}\$((_(GET|POST|REQUEST|SESSION|SERVER)(\[[\'"]{0,1})[\w\(\)]{0,15}([\'"]{0,1}\]))|\w{1,10}))\s{0,5}\))'
    rule1='((eval|assert)[\s|\n]{0,30}\((gzuncompress|gzinflate\(){0,1}[\s|\n]{0,30}base64_decode.{0,100})'
    rule2='\s{0,10}=\s{0,10}([{@]{0,2}\\\\{0,1}\$_(GET|POST|REQUEST)|file_get_contents|["\']a["\']\.["\']s["\']\.|["\']e["\']\.["\']v["\']\.|["\']ass["\']\.).{0,20}'
    vararr=['$_GET','$_POST','$_REQUEST','$_SESSION','$_SERVER']

    if 'eval' in file_content or 'assert' in file_content:
        result = re.compile(rule).findall(file_content)
        if len(result)>0:
            for group in result:
                for var in vararr:
                    if var in group[2]:
                        return 1
                resultson = re.search('\\'+group[2]+rule2,file_content)
                try:
                    if len(resultson.groups())>0:
                        return 1
                except:
                    continue

        else:
            result = re.compile(rule1).findall(file_content)
            if len(result)>0:
                return 1
    return None

def zendencode(filestr,filepath):

    if filestr[:4]=='Zend':
        if os.path.getsize(filepath)==178:
            return 1

        return None

def preg_replace(filestr,filepath):

    rule1='(preg_replace[\s\n]{0,10}\([\s\n]{0,10}((["\'].{0,15}[/@\'][is]{0,2}e[is]{0,2}["\'])|\$[a-zA-Z_][\w"\'\[\]]{0,15})\s{0,5},\s{0,5}.{0,40}(\$_(GET|POST|REQUEST|SESSION|SERVER)|str_rot13|urldecode).{0,30})'

    if 'preg_replace' in filestr:
        result = re.compile(rule1).findall(filestr)
        if len(result)>0:
            return 1
    else:
        return None

def packshell(filestr,filepath):

    rule='gzdeflate|gzcompress|gzencode'

    result = re.search(rule,filestr)

    try:
        if result.group():
            if '打包' in filestr and 'unix2DosTime' in filestr:
                isok = 1
                if isok:
                    return 1
    except:
        pass
    return None

def include_file(filestr,filepath):

    rule1='([^\'"](include|require)(_once){0,1}\s{0,5}(\s{0,5}|\(\s{0,5})["\']([\.\w\,/\\\+-_]{1,60})["\']\s*\){0,1})'
    rule2='((include|require)(_once){0,1}(\s{0,5}|\s{0,5}\(\s{0,5})[\'"]{0,1}(\$(_(GET|POST|REQUEST|SERVER)(\[[\'"]{0,1})\w{0,8}([\'"]{0,1}\])|[\w]{1,15}))[\'"]{0,1})'
    rule3='\s{0,10}=\s{0,10}([{@]{0,2}\$_(GET|POST|REQUEST)|[\'"]{0,1}php://input[\'"]{0,1}|file_get_contents).{0,20}'
    vararr=['$_GET','$_POST','$_REQUEST','$_SERVER']
    Whiterule = ['.php','$','templates','.html']

    if 'include' in filestr or 'require' in filestr :
        result = re.compile(rule1).findall(filestr)
        if len(result)>0:
            resultlist=[]
            for key in result:
                isok=1
                for Whitestr in Whiterule:
                    if Whitestr in key[4].lower():
                        isok=0
                if isok==1:
                    resultlist.append(key)
            if len(resultlist)>0:
                return 1

        result = re.compile(rule2).findall(filestr)
        if len(result)>0:
            varlist=''
            for group in result:
                if group[4] in varlist:
                    continue
                else:
                    varlist+=group[4]+"--"

                for var in vararr:
                    if var in group[4]:
                        return 1

                resultson = re.search('\\'+group[4]+rule3,filestr)
                try:
                    if len(resultson.groups())>0:
                        return 1
                except:
                    continue
        return None
    else:
        return None

def dynamic_func(filestr,filepath):

    rule1='(\$_(GET|POST|REQUEST)\[.{0,15}\]\s{0,10}\(\s{0,10}\$_(GET|POST|REQUEST).{0,15})'
    rule2='((\$(_(GET|POST|REQUEST|SESSION|SERVER)(\[[\'"]{0,1})\w{1,12}([\'"]{0,1}\])|\w{1,10}))[\s\n]{0,20}\([\s\n]{0,20}(@{0,1}\$(_(GET|POST|REQUEST|SESSION|SERVER)(\[[\'"]{0,1})\w{1,12}([\'"]{0,1}\])|\w{1,10}))[\s\n]{0,5}\))'
    rule3='\s{0,10}=\s{0,10}[{@]{0,2}(\$_(GET|POST|REQUEST)|file_get_contents|str_replace|["\']a["\']\.["\']s["\']\.|["\']e["\']\.["\']v["\']\.|["\']ass["\']\.).{0,10}'
    vararr=['$_GET','$_POST','$_REQUEST','$_SESSION','$_SERVER']

    whitefilter=[
                    (['integrate.php'],['$code ($_POST[\'cfg\'])']),
                    (['Lib/Action/IntegrateAction.class.php'],['$code ($_POST[\'cfg\'])']),
                    (['phpcms/modules/template/file.php'],['$_GET[\'action\']($_GET[\'html\']'])
    ]

    result = re.compile(rule1).findall(filestr)
    if len(result)>0:
        isok=1
        for white in whitefilter:
            if white[0][0] in filepath.replace('\\','/') and white[1][0] in result[0][0]:
                isok=0
        if isok:
            return 1
    else:
        result = re.compile(rule2).findall(filestr)
        finalresult = result
        if len(result)>0:
            for group in result:
                for var in vararr:
                    if var in group[1]:
                        resultson= re.search('\\'+group[6]+rule3,filestr)
                        try:
                            if len(resultson.groups())>0:
                                isok=1
                                for white in whitefilter:
                                    if white[0][0] in filepath.replace('\\','/') and white[1][0] in result[0][0]:
                                        isok=0
                                if isok:
                                    return 1
                        except:
                            pass
                for var in vararr:
                    if var in group[6]:
                        resultson= re.search('\\'+group[1]+rule3,filestr)

                        try:
                            if len(resultson.groups())>0:
                                isok=1
                                for white in whitefilter:
                                    if white[0][0] in filepath.replace('\\','/') and white[1][0] in result[0][0]:
                                        isok=0
                                if isok:
                                    return 1
                        except:
                            pass

                result1= re.search('\\'+group[1]+rule3,filestr)
                result2= re.search('\\'+group[6]+rule3,filestr)
                try:
                    if len(result1.groups())>0 and len(result2.groups())>0:
                        isok=1
                        for white in whitefilter:
                            if white[0][0] in filepath.replace('\\','/') and white[1][0] in result[0][0]:
                                isok=0
                        if isok:
                            return 1
                except:
                    continue
                return None
        else:
            return None

def ddos(filestr,filepath):

    keywords=[
                '启动自动攻击',
                'xxddos',
                'phpddos',
                'fsockopen("udp:',
                'fsockopen("tcp:',
                '$_get["moshi"]=="udp"'
            ]

    whitefilter=[
                    (['install/svinfo.php'],['fsockopen("tcp:']),
    ]

    filestr = filestr.lower()

    for key in keywords:
        if key in filestr:
            isok=1
            for white in whitefilter:
                if white[0][0] in filepath.replace('\\','/') and white[1][0] in key:
                    isok=0
            if isok:
                return 1
    return None

def call_user_func(filestr,filepath):

    rule='(call_user_func[\s\n]{0,25}\(.{0,25}\$_(GET|POST|REQUEST).{0,15})'

    if 'call_user_func' in filestr:
        result = re.compile(rule).findall(filestr)
        if len(result)>0:
            return 1
    else:
        return None

def customize(filestr,filepath):
    user_file = open('./rule.txt')
    for i in user_file.readlines():
        result = re.compile(i).findall(filestr)
        if len(result)>0:
            return 1
