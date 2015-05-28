#!/usr/bin/python

import subprocess
import sys
import os
import re
import string
import getopt
import pprint

# ansi codes for color terminal output
MAGENTA = '\033[35m'
WHTIE = '\033[37m'
BLUE = '\033[34m'
CYAN = '\033[36m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
UNDERLINE = '\033[4m'
ENDC = '\033[0m'
BOLD = "\033[1m"
 
level = None
try:
  opts, args = getopt.getopt(sys.argv[1:],"L:")
  for opt, arg in opts:
    if opt == "-L":
      level = arg    
except getopt.GetoptError: 
  level = None  

# get tree ouput
if level:
  cmd = "tree -S -L " + level
else:  
  cmd = "tree -S" 
tree = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,executable='/bin/bash').communicate()[0]
if level:
  cmd = "tree -C -L " + level
else:  
  cmd = "tree -C" 
tree_out= subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,executable='/bin/bash').communicate()[0]
tree_color = tree_out.splitlines()
tree_filter = filter(lambda x: x in string.printable, tree)


# build file/directory paths from tree
pwd = os.getcwd()
tree_ls = tree_filter.split("\n")
n = len(tree_ls)
path_ls = []
path_ls.append(pwd)
direc = pwd
direc_ls = []
direc_ls.append(pwd)
#direc_ls.append(" ")
pattern = re.compile('\xe2\x94\x82\xc2\xa0\xc2\xa0|\xe2\x94\x9c\xe2\x94\x80\xe2\x94\x80|\xe2\x94\x94\xe2\x94\x80\xe2\x94\x80|    ')
for i in range(1,n-3):
  
  #print repr(tree_color[i])
  
  nsp_i = len(pattern.findall(tree_color[i]))
  nsp_im1 = len(pattern.findall(tree_color[i-1]))  

  item = re.sub(" ","\ ",tree_ls[i].strip())
  
  if nsp_i == nsp_im1:
    direc_ls.pop()
    direc_ls.append(item)
    #print 'Same level'
  elif nsp_im1 < nsp_i:
    direc_ls.append(item)
    #print 'Up level'
  elif nsp_i < nsp_im1:
    #print 'Down level'
    diff = nsp_im1-nsp_i
    for i in range(0,diff+1):
      direc_ls.pop()
    direc_ls.append(item)      
      
    
  file_name = '/'.join(direc_ls) 
  path_ls.append(file_name)
    
      
    
# get extended attributes    
desc_ls = []
n = len(path_ls)
for i in range(0,n):
  cmd = "getfattr -d --absolute-names " + path_ls[i]
  getfattr_output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,executable='/bin/bash').communicate()[0]

  desc_ls.append([])  
  if getfattr_output:
    file_info = filter(None,getfattr_output.split("\n")) # split the file information
    for j in range(1,len(file_info)):  # loop through list of attribute values (begins on second line)
                                       # just in case other attributes are set, sfd.py only uses the user.comment attribute
      ind = file_info[j].find("user.comment=")
      if ind >= 0:
        ind = ind+len("user.comment=")                           # find where comment begins: "user.comment="comments"
        descrip = file_info[j].replace(file_info[j][:ind+1],"")  # remove the name of the extended attribute
        comment = descrip.replace('"','').split(r"\012")         # split lines and remove quotes
        while comment[-1] == "":
          comment.pop()
        if comment[0] == "":
          comment.pop(0)
        desc_ls[i].append(comment)  

#print pprint.pprint(tree_ls)
#print pprint.pprint(path_ls)
#print pprint.pprint(desc_ls)


# print tree output and extended attributes
print " "
print "--------------------------------------------------------"
for i in range(0,n):

  if desc_ls[i]:
    print re.sub(r"\xe2\x94\x94","\xe2\x94\x9c",tree_color[i])
    spaces = re.sub(r"\xe2\x94\x80"," ",tree_color[i].rpartition(" ")[0])
    spaces = re.sub(r"\xe2\x94\x94","\xe2\x94\x9c",spaces)    
    for ls in desc_ls[i]:
      for text in ls:
        print spaces + YELLOW + "   " + text + ENDC
    if i != n-1:    
      print re.sub(r"\xe2\x94\x9c","\xe2\x94\x82",spaces)
    
  else:  
    print tree_color[i]  
print "--------------------------------------------------------"	
print " "	        