#!/usr/bin/python

import subprocess
import sys
import xattr
import os
import re
import string
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

cmd = "tree -S"
tree = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,executable='/bin/bash').communicate()[0]
cmd = "tree -C"
tree_out= subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,executable='/bin/bash').communicate()[0]
tree_color = tree_out.splitlines()

#tree = ansi_escape.sub("",tree_color)

#print tree_out
#print tree_color
tree_filter = filter(lambda x: x in string.printable, tree)
#print tree_filter

pwd = os.getcwd()

tree_ls = tree_filter.split("\n")
n = len(tree_ls)
path_ls = []
path_ls.append(pwd)

direc = pwd
for i in range(1,n-3):
  
  nsp_i = tree_ls[i].rfind(" ")
  nsp_ip1 = tree_ls[i+1].rfind(" ")
  
  if nsp_i == nsp_ip1:
    file_name = direc + "/" + tree_ls[i].strip()
    path_ls.append(file_name)    
  elif nsp_i < nsp_ip1:
    direc = direc + "/" + tree_ls[i].strip()
    path_ls.append(direc)
  elif nsp_i > nsp_ip1:
    file_name = direc + "/" + tree_ls[i].strip()
    path_ls.append(file_name)
    direc = direc.rpartition("/")[0]
    
desc_ls = []
n = len(path_ls)
for i in range(0,n):
  cmd = "getfattr -d --absolute-names " + path_ls[i]
  getfattr_output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,executable='/bin/bash').communicate()[0]

  desc_ls.append([])  
  if getfattr_output:
    file_info = filter(None,getfattr_output.split("\n")) # split the file information
    for j in range(1,len(file_info)):  # loop through list of attribute values (begins on second line)
                                     # the loop probably isn't necessary because this fcmnt.py only uses the user.comment attribute
      ind = file_info[j].find("=")  # find where comment begins: "user.comment="comments"
      descrip = file_info[j].replace(file_info[j][:ind+1],"") # remove the name of the extended attribute
      comment = descrip.replace('"','').split(r"\012") # split lines and remove quotes
      while comment[-1] == "":
        comment.pop()
      if comment[0] == "":
        comment.pop(0)
      desc_ls[i].append(comment)  

#print pprint.pprint(tree_ls)
#print pprint.pprint(path_ls)
#print pprint.pprint(desc_ls)

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