#!/usr/bin/python

import subprocess
import os
import pprint
import re

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

# object to remove ansi color codes from ls ouptut
ansi_escape = re.compile(r'\x1b[^m]*m')

# get the output of ls
cmd = "ls -lhrt --color"
ls_output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,executable='/bin/bash').communicate()[0]
ls_sp = ls_output.splitlines()

# get the extended attributes of all the files/directories in pwd
pwd = os.getcwd()
cmd = "getfattr -d --absolute-names " + pwd + "/*"
getfattr_output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,executable='/bin/bash').communicate()[0]
getfattr_sp = filter(None,getfattr_output.split("# file:")) # split the output for each file

files = {}
for i in range(0,len(getfattr_sp)): # loop though all files with extended attributes
  file_info = filter(None,getfattr_sp[i].split("\n")) # split the file information
  full_name = file_info[0]                            # first line is: # file: /path/file
  name = full_name.split("/")[-1]                     # find the name of the file at the end of the path
  files[name] = []
  
  for i in range(1,len(file_info)):  # loop through list of attribute values (begins on second line)
                                     # Just in case other attributes are set, sfd.py only uses the user.comment attribute
    ind = file_info[i].find("user.comment=")                                      
    if ind >= 0:
      ind = ind+len("user.comment=")                          # find where comment begins: "user.comment="comments"
      descrip = file_info[i].replace(file_info[i][:ind+1],"") # remove the name of the extended attribute
      comment = descrip.replace('"','').split(r"\012")        # split lines and remove quotes
      while comment[-1] == "":
        comment.pop()
      if comment[0] == "":
        comment.pop(0)
      files[name].append(comment)

    
#pprint.pprint(files)   

print " "
print "--------------------------------------------------------"
for line in ls_sp[1:]: # loop through lines of ls output
  line_sp = line.split()
  name = ansi_escape.sub("",line_sp[-1])            # remove ansi color codes before checking for dictionary key
  if line_sp[-1][0:4] == "\x1b[0m":
    line_sp[-1] = line_sp[-1].replace("\x1b[0m","") # some names won't print with underline because they begin with \x1b[0m
  line_sp[-1] = UNDERLINE + line_sp[-1] + ENDC      # add underline
  #print repr(line_sp[-1]) # print with ansi codes
  line = " ".join(line_sp)
  print line                                        # print ls output line
  if name in files: 
    for comment in files[name]:
      for text in comment:                          # print lines of each extended attribute comment
	print YELLOW + "    " + text + ENDC
  print " "
	
print "--------------------------------------------------------"	
print " "	