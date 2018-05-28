#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import logging
import concurrent.futures
import os.path
import re
import tornado.escape
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
import random
import static_scan
import rf
import lstm
import string

try:
    from urllib.parse import unquote
except ImportError:
    # Python 2.
    from urllib import unquote

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

upload_dir='./upload/'

# A thread pool to be used for password hashing with bcrypt.


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/upload.html",UploadHandler),
            (r"/(.*)", HomeHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            # cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        #print self.request
        #print self.get_argument
        #self.set_status(200)
        self.render("index.html")


class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        #self.set_status(200)
        #self.get_arguments
        self.render('upload.html')
    def post(self):
       # print 'post'
       # print self.set_header
        rule=''
        rule=self.get_argument('rule')
        with open('./rule.txt','a') as f:
            f.write('\n'+rule)
        weight=[1 for i in range(0,4)]
        for i in range(1,4):
            try:
                print 'w'+(str(i))
                weight[i] = int(self.get_argument('w'+(str(i))))
            except:
                weight[1]=0.8
                weight[2]=0.1
                weight[3]=0.1
        sub_dir = ''.join(random.sample(string.ascii_letters + string.digits, 32))
        os.mkdir(upload_dir+sub_dir)
        s_dir = upload_dir+sub_dir+'/'
        for field_name, files in self.request.files.items():
            for info in files:
                filename, content_type = info['filename'], info['content_type']
                body = info['body']
                file_path= s_dir+filename
                f=open(file_path,'wb')
                f.write(info['body'])
                f.close()
                logging.info('POST "%s" "%s" %d bytes',
                             filename, content_type, len(body))
          	'''
    	moudles
    	'''

        filenames=[]
        rfs=[]
        lstms=[]
        statics=[]
    	filenames,rfs=rf.start(s_dir)#[]
    	lstms=lstm.lstm_predict(s_dir,filenames)
        #print lstms
    	statics=static_scan.scan(s_dir,filenames)
        entries=[[0 for i in range(6)] for j in range(len(filenames))]
        for i in range(0,len(filenames)):
            entries[i][0]=i
            entries[i][1]=filenames[i]
        #entries=[['haha',1,1,1,1,1],['aaa',1,1,1,1,1]]
            entries[i][2]=rfs[i]
            entries[i][3]=lstms[i]
            entries[i][4]=statics[i]
            entries[i][5]=entries[i][2]*weight[1]+entries[i][3]*weight[2]+entries[i][4]*weight[3]
        self.render('result.html',items=entries,weight=weight)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
