from keras.models import load_model
import commands
import re
import os
from sklearn.feature_extraction.text import CountVectorizer

php_bin='/usr/bin/php'
max_features=5000
def load_file_opcode(file_path):
    global php_bin
    t=""
    cmd=php_bin+" -dvld.active=1 -dvld.execute=0 "+file_path
    status,output=commands.getstatusoutput(cmd)
    t=output
    tokens=re.findall(r'\s(\b[A-Z_]+\b)\s',output)
    t=" ".join(tokens)
    print "opcode count %d" % len(t)
    return t

def lstm_predict(dir,filenames):
    re = []
    files = []
    i=0
    x=[]
    ls =  load_model('lstm.mod')
    for file in filenames:
        i+=1
        print i
        print len(files)
        x.append(load_file_opcode(dir+'/'+file))
    CV = CountVectorizer(ngram_range=(2, 4), decode_error="ignore",max_features=max_features,
                                       token_pattern = r'\b\w+\b',min_df=1, max_df=1.0)
    x=CV.fit_transform(x).toarray()
    #print ls.predict(x)[0]
    lstms=[]
    for i in range(0,len(ls.predict(x))):
        lstms.append(ls.predict(x)[i][0])
    return lstms
