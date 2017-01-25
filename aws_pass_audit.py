#!/usr/local/bin/python 

import csv 
import os 
import subprocess
from datetime import datetime

# Create text_results.txt file
aws_cli = subprocess.check_output("aws iam get-credential-report --query 'Content' --output text | base64 -D | cut -d, -f1,4,6 > text_results.txt", shell=True)

# Open file for reading
ifile = open('text_results.txt')

# Read csv results into variable 
reader = csv.reader(ifile)

# For loop to read each value into single variables 
for row in reader: 
 name = str(row[0])
 t_f = str(row[1])
 date_s = str(row[2])

 # If password authentication is enabled begin to test age
 if t_f == 'true': 
  # strip 00:00 millisecond value off timestamp and assign to datetime object 
  date_o = datetime.strptime(date_s, '%Y-%m-%dT%H:%M:%S+00:00')

  # Subtract date password was last changed from todays date
  diff = datetime.today().date() - date_o.date()

  # assign difference in days to variable
  diff_n = diff.days
  
  # convert from datetime object to int value
  diff_int = int(diff_n)

  # Test if password is greater than 180 days old since last changed
  if diff_int > 180:
   print "Password for user", name, "is", diff_int, "days old" 

ifile.close()
os.remove("text_results.txt")
