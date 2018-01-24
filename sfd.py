#!/usr/bin/python

import subprocess
import sys
import os
import re

editor = "nano"
#method = "fattr"
method = "file"

# check argument list
n = len(sys.argv)
if n > 2:
  print "sfd: too many arguments"
  raise SystemExit(0)
if n < 2:
  print "sfd: supply a file name"
  raise SystemExit(0)

#get object name and current directory  
argls = str(sys.argv)
file_name = sys.argv[1]
pwd = os.getcwd()
full_name = pwd+"/"+file_name

# check if object exists
if not os.path.exists(full_name):
  print "sfd: file does not exist"
  raise SystemExit(0)
  
# check if owner has write permissions
#   - This will need to be considered more carefully if used when different owners/groups are involved
cmd = "ls -ld " + full_name  
ls_output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,executable='/bin/bash').communicate()[0]

prem_mod = 0
if ls_output[2] != "w":
  try:
    #print "sfd: attempting to add write permissions..."
    cmd = "chmod u+w " + full_name        
    chmod_output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,executable='/bin/bash').communicate()[0]     
    prem_mod = 1
  except:
    print "sfd: owner does not have write permissions"  
    print ls_output
    raise SystemExit(0)
  
if method == "fattr":

  # check if object already has extended attributes  
  cmd = "getfattr -d --absolute-names " + full_name
  existing_attr = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,executable='/bin/bash').communicate()[0]

  # open dummy file for extended attribute input (overwrite if already exists)
  f = open(".descrip","w")

  # write any existing object extended attibutes to file
  if existing_attr != "":
    file_info = filter(None,existing_attr.split("\n"))  #split output lines and get rid of empty strings
    for i in range(1,len(file_info)):  # loop through list of attribute values (begins on second line)
                                     # just in case other attrubutes are set, this program only uses the user.comment attribute
      ind = file_info[i].find("user.comment=")                                 
      if ind >= 0:                                     
        ind =ind+len("user.comment=")                           # find where comment begins
        descrip = file_info[i].replace(file_info[i][:ind+1],"") # remove the name of the extended attrubute
        comment = descrip.replace('"','').split(r"\012")        # split lines and remove quotes
 
        for line in comment:    # write to file
          f.write("%s\n" % line)
      
  f.write("\n")
  f.write("\n")
  f.write("\n")
  f.write("# Enter comment for: " + file_name + "\n")
  f.write("# Full path: " + full_name + "\n")      
    
  f.close()    

  # Allow user to input comments and read them in 
  subprocess.call([editor,".descrip"])
  f = open(".descrip")
  cmnt = f.read().strip()
  f.close()

  # Process input comments
  cmnt_sp = cmnt.split("\n")
  cmnt_ls = []
  for line in cmnt_sp:
    if line and line[0] != "#": # leave out commented lines...blank lines are also skipped
      cmnt_ls.append(line)    
  cmnt = "\n".join(cmnt_ls)

  if cmnt == "":
    print "sfd: comment is empty, exiting..."
    raise SystemExit(0)


  # Add the inputed comment as an extended attribute
  cmd = 'setfattr -n user.comment -v "' + cmnt + '" ' + full_name
  subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,executable='/bin/bash').communicate()[0]

elif method == "file":
  
  # Create description file name  
  if os.path.islink(full_name):
    path = os.path.realpath(full_name)
    file_name = path.split("/")[-1]
    descrip_fname =  path + "/." + file_name
  else:
    descrip_fname = pwd + "/." + file_name    
    
  if os.path.isfile(full_name):
    extension = "-file.descrip"
  elif os.path.isdir(full_name):
    extension = "-dir.descrip"
  else:
    print "sfd: file type error..."
    raise SystemExit(0) 
  descrip_fname = descrip_fname + extension
  
  # Edit the description file
  if os.path.exists(descrip_fname):    
    subprocess.call(["chmod","+w",descrip_fname])
  subprocess.call([editor,descrip_fname])
  subprocess.call(["chmod","-w",descrip_fname])    
  
  
  
  
# remove the write permissions if they were added
if prem_mod == 1:
  cmd = "chmod u-w " + full_name        
  chmod_output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,executable='/bin/bash').communicate()[0]     