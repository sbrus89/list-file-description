# list-file-description
Sets extended file attributes and displays them along with 'ls' output. 

Intended to make ls more informative by supplementing it with metadata.

Example:

-rw-rw-r-- 1 sbrus sbrus 20 Sep 2 2014 test
    This comment can give some information that can help describe what the file is
 
drwxrwxr-x 3 sbrus sbrus 4.0K May 15 2015 test_dir
    This comment would give some information about what is in this directory
 
-rwxrwxr-x 1 sbrus sbrus 3.0K Jan 22 2016 lfd.py
    Program to view the extended attributes for files/sub-directories
      - combines the output of ls and getfattr

-rwxrwxr-x 1 sbrus sbrus 3.7K Jul 7 14:52 sfd.py
    Program to set extended file attributes for directories/files
