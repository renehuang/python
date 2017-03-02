# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 10:33:29 2017

@author: reneh
"""

# run as python script
import sys
import argparse

parser = argparse.ArgumentParser()
# to save you a little grief, here's how you want to define
# your command line args to argparse

# required positional arg
parser.add_argument("search", type=str,
                    help="search string")

# optional arg
parser.add_argument("-t", "--totalhits", help="show total number of hits in all files",
			 action='store_true')

# optional arg
parser.add_argument("-g", "--grep", help="show matching hit lines",
			 action='store_true')

# optional arg
parser.add_argument("-f", "--filehits", help="show number of hits in files",
			 action='store_true')

# optional arg with required zippath value
parser.add_argument("-z", "--zippath", help="path of python zip file",
			 action='store')

parser.set_defaults(zippath = 'python-docs.zip')


import os
import zipfile

class phelp:
    def __init__(self, zpath):
        if not os.path.exists(zpath):
            raise FileNotFoundError('file '+ zpath + ' does not exist')
            sys.exit(1)
        if not zpath.endswith('.zip'):
            raise ValueError('file '+ zpath + ' is not a zip file')
            sys.exit(1)
        with zipfile.ZipFile(zpath, 'r') as myzip:
            self.namelist= myzip.namelist()
            count = 0
            self.dic= {}
            for name in self.namelist:
                with myzip.open(name, 'r') as myfile:
                    data = myfile.read()
                    data = data.decode('utf-8')
                    self.dic[name]=data
                    count+=1
                
#        print ('reading {} files'.format(count))
        
        
    def fileHits(self, word):
        for name, file in self.dic.items():
            found = False
            count = 0 
            for line in file.splitlines():
                if word in line:
                    found = True
                    count +=1
            if (found):
                print("{} {}".format(count, name))
        
        
    def totalHits(self, word):
        counts=0
        for name, file in self.dic.items():
            for line in file.splitlines():
                if word in line:
                    counts+=1
        print(counts)
        return None
    
    def grep(self, word):
        for name, file in self.dic.items():
            for linenum, line in enumerate(file.splitlines()):
                line = line.strip()
                if word in line:
                    print ('{}:{}:{}'.format(name, linenum, line))
        
                    
args= parser.parse_args()
p = phelp(args.zippath)
if args.filehits:
    p.fileHits(args.search)
if args.grep:
    p.grep(args.search)
if args.totalhits:
    p.totalHits(args.search)


