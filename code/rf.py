import os
import re
from sklearn.feature_extraction.text import CountVectorizer
import sys
import numpy as np
from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.metrics import classification_report
from sklearn import preprocessing
from sklearn.externals import joblib
import chardet

webshell_dir="../data/webshell/webshell/"
whitefile_dir="../data/webshell/normal/"

white_count=0
black_count=0
max_features=5000

def load_files_re(dir):
    files_list = []
    g = os.walk(dir)
    for path, d, filelist in g:
        #print d;
        for filename in filelist:
            if filename.endswith('.php'):
                fulepath = os.path.join(path, filename)
                print "Loading %s" % fulepath
                t = load_file(fulepath)
                files_list.append(t)
                print "Load %s successfully" % fulepath

    return files_list

def load_file(file_path):
    t=""
    encoding=''
    try:
        with open(file_path,'r') as f:
            for line in f:
                t+=line
    except:
        with open(file_path,'rb') as f1:
            buf=f1.read()
            result=chardet.detect(buf)
            encoding=result['encoding']
            print encoding
        with open(file_path,'rb') as f:
            for line in f:
                try:
                    t+=line.decode(encoding).encode('utf-8')
                except:
                    print 'erro raised by the code of your files,please encode your files by utf-8!'
    t=re_removecomment(t)
    t=t.replace('\n',' ')
    t=t.replace('\r',' ')
    return t





def re_removecomment(cod):
    result, number = re.subn('(?<!:)\\/\\/.*|\\/\\*(\\s|.)*?\\*\\/|(#.*?\n)','', cod)#comments
    return result


def get_feature_by_bag_tfidf():
    global white_count
    global black_count
    global max_features
    print "max_features=%d" % max_features
    x=[]
    y=[]

    webshell_files_list = load_files_re(webshell_dir)
    y1=[1]*len(webshell_files_list)
    black_count=len(webshell_files_list)

    wp_files_list =load_files_re(whitefile_dir)
    y2=[0]*len(wp_files_list)

    white_count=len(wp_files_list)


    x=webshell_files_list+wp_files_list
    y=y1+y2

    CV = CountVectorizer(ngram_range=(2, 4), decode_error="ignore",max_features=max_features,
                                       token_pattern = r'\b\w+\b',min_df=1, max_df=1.0)#n-gram
    x=CV.fit_transform(x).toarray()

    transformer = TfidfTransformer(smooth_idf=False)
    x_tfidf = transformer.fit_transform(x)#tf-idf  the regularilizm of a word to add the W
    x = x_tfidf.toarray()

    return x,y


def check_webshell(clf,dir):
    all_php=0
    webshell=0
    name_list = []
    files_list = []
    global max_features
    g = os.walk(dir)
    for path, d, filelist in g:
        #print d;
        for filename in filelist:
            #print os.path.join(path, filename)
            if filename.endswith('.php'):
                fulepath = os.path.join(path, filename)
                #print "Loading %s" % fulepat
                name_list.append(filename)
                t = load_file(fulepath)
                files_list.append(t)
                #print "Load %s successfully" % fulepath
    x=files_list
    CV = CountVectorizer(ngram_range=(2, 4), decode_error="ignore",max_features=max_features,
                                       token_pattern = r'\b\w+\b',min_df=1, max_df=1.0)#n-gram
    x=CV.fit_transform(x).toarray()
    transformer = TfidfTransformer(smooth_idf=False)
    x_tfidf = transformer.fit_transform(x)#tf-idf  the regularilizm of a word to add the W
    x = x_tfidf.toarray()
    y_pred = clf.predict_proba(x)
    #print y_pred
    all_php=len(x)
    y_rf=[]
    for i in range(0,all_php):
        y_rf.append(y_pred[i][1])
    #print y_rf
    #print name_list
    return name_list,y_rf

def start(dir):
    '''
    x, y = get_feature_by_bag_tfidf()
    print "load %d white %d black" % (white_count, black_count)
    print "rf and bag and removecomment 2-gram and tfidf "
    rf = RandomForestClassifier(n_estimators=50)
    rf.fit(x, y)
    joblib.dump(rf, 'rf.model')
   	'''

    rf = joblib.load('rf.model')
    return check_webshell(rf,dir)

if __name__ == '__main__':
    max_features=5000
    start('/home/leo/data/webshell/webshell/PHP/php')
