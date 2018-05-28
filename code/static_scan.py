# coding=utf-8
# Python 3.6.5

import os
import sys

from scan_modules import *

res_list = []

def scan(dir_name, file_list):
    global res_list
    for file_name in file_list:
        v = 0.5
        file_path = os.path.join(dir_name, file_name)
        for module in all_modules:
            file= open(file_path)
            file_content = file.read()
            file.close()
            result = eval(module)(file_content, file_path)
            if result != None:
                v = 0.9
                break
        res_list.append(v)
    return res_list

if __name__ == "__main__":
    dirname = 'test'
    file_list = ['1.php', '2.php', '3.php']
    res_list = scan(dirname, file_list)
    print (res_list)
