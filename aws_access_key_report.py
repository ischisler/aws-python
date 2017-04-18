#!/usr/local/bin/python 

import csv 
import os 
import subprocess
from datetime import datetime

# Create text_results.txt file
aws_cli = subprocess.check_output("aws iam get-credential-report --query 'Content' --output text | base64 -D | cut -d, -f1,4,6,8,9,10,11,14,15,16 > text_results.txt", shell=True)

# Open file for reading
ifile = open('text_results.txt', 'r')
ofile = open('user_audit.html', 'w')

header = """<html><head>Account Audit Report</head><body><table border="1"><tr><th>Username</th><th>Password Enabled</th><th>Password Age (Days)</th><th>MFA Enabled</th><th>More than one active key</th><th>Access Key 1 Active</th><th>Access Key 1 Age (Days)</th><th>Access Key 1 Last Used</th><th>Access Key 2 Active</th><th>Access Key 2 Age (Days)</th><th>Access Key 2 Last Used</th></tr>"""
close_html = """</table></body></html>"""

ofile.write(header)

# Read csv results into variable 
reader = csv.reader(ifile)

# For loop to read each value into single variables 
for row in reader: 
        name = str(row[0])
        pass_t_f = str(row[1])
        pass_date_s = str(row[2])
        mfa_active = str(row[3])
        access_key_1_active = str(row[4])
        access_key_1_last_rotated = str(row[5])
        access_key_1_last_used = str(row[6])
        access_key_2_active = str(row[7])
        access_key_2_last_rotated = str(row[8])
        access_key_2_last_used = str(row[8])

        if name == '<root_account>':
                ofile.write("""<tr><td>root_account</td><td>not_supported</td><td>not_supported</td>""")

        #user_html = """<tr><td>{user}</td></tr>""".format(user=name)
        #ofile.write(user_html)
        if name != 'user' and name != '<root_account>':
                ofile.write("""<tr><td>{user}</td>""".format(user=name))

           #     ofile.write("""<tr><td>{user}</td>""".format(user=name))

        # If password authentication is enabled begin to test age
        if pass_t_f == 'true' and name != 'user' and name != '<root_account>': 
                ofile.write("""<td>{pass_en}</td>""".format(pass_en=pass_t_f))
                # strip 00:00 millisecond value off timestamp and assign to datetime object 
                pass_date_o = datetime.strptime(pass_date_s, '%Y-%m-%dT%H:%M:%S+00:00')
                # Subtract date password was last changed from todays date
                pass_diff = datetime.today().date() - pass_date_o.date()
                # assign pass_difference in days to variable
                pass_diff_n = pass_diff.days
                # convert from datetime object to int value
                pass_diff_int = int(pass_diff_n)

                if pass_diff_int > 365:
                      ofile.write("""<td bgcolor="red">{pass_diff_int}</td>""".format(pass_diff_int=pass_diff_int))
                      print "Password for user", name, "is", pass_diff_int, "days old"
                else:
                      ofile.write("""<td bgcolor="lightgreen">{pass_diff_int}</td>""".format(pass_diff_int=pass_diff_int))
        elif name != 'user' and name != '<root_account>': 
                ofile.write("""<td>{pass_en}</td>""".format(pass_en=pass_t_f))
                ofile.write("""<td>{pass_date_s}</td>""".format(pass_date_s=pass_date_s))

        if mfa_active == 'false' and name != 'user': 
                ofile.write("""<td bgcolor="red">{mfa_active}</td>""".format(mfa_active=mfa_active))
                print "User: ", name, "does not have MFA enabled"
        elif name != 'user': 
                ofile.write("""<td bgcolor="lightgreen">{mfa_active}</td>""".format(mfa_active=mfa_active))

        if access_key_1_active == 'true' and access_key_2_active == 'true': 
                ofile.write("""<td bgcolor="red">true</td>""")
                print "User: ", name, "has two active access keys" 
        elif name != 'user': 
                ofile.write("""<td bgcolor="lightgreen">false</td>""")
        # Is access key 1 active
        if access_key_1_active == 'true' and name != 'user': 
                ofile.write("""<td>{key_1}</td>""".format(key_1=access_key_1_active))
                key_1_date_o = datetime.strptime(access_key_1_last_rotated, '%Y-%m-%dT%H:%M:%S+00:00')
                key_1_diff = datetime.today().date() - key_1_date_o.date()
                key_1_diff_days = key_1_diff.days
                key_1_diff_int = int(key_1_diff_days)
                if key_1_diff_int > 365: 
                      ofile.write("""<td bgcolor="red">{key_1_diff_int}</td>""".format(key_1_diff_int=key_1_diff_int))
                      ofile.write("""<td>{key_1_diff_int}</td>""".format(key_1_diff_int=access_key_1_last_used))
                      print "Access Key 1 for user", name, "is active and has not been rotated in", key_1_diff_int, "days"
                else: 
                      ofile.write("""<td bgcolor="lightgreen">{key_1_diff_int}</td>""".format(key_1_diff_int=key_1_diff_int))
                      ofile.write("""<td>{key_1_diff_int}</td>""".format(key_1_diff_int=access_key_1_last_used))
        elif name != 'user': 
                ofile.write("""<td>{key_1}</td>""".format(key_1=access_key_1_active))
                ofile.write("""<td>N/A</td>""")
                ofile.write("""<td>N/A</td>""")

        if access_key_2_active == 'true' and name != 'user': 
                ofile.write("""<td>{key_2}</td>""".format(key_2=access_key_2_active))
                key_2_date_o = datetime.strptime(access_key_2_last_rotated, '%Y-%m-%dT%H:%M:%S+00:00')
                key_2_diff = datetime.today().date() - key_2_date_o.date()
                key_2_diff_days = key_2_diff.days
                key_2_diff_int = int(key_2_diff_days)
                if key_2_diff_int > 365: 
                      ofile.write("""<td bgcolor="red">{key_2_diff_int}</td>""".format(key_2_diff_int=key_2_diff_int))
                      ofile.write("""<td>{key_2_diff_int}</td>""".format(key_2_diff_int=access_key_2_last_used))
                      print "Access Key 1 for user", name, "is active and has not been rotated in", key_2_diff_int, "days"
                else: 
                      ofile.write("""<td bgcolor="lightgreen">{key_2_diff_int}</td>""".format(key_2_diff_int=key_2_diff_int))
                      ofile.write("""<td>{key_2_diff_int}</td>""".format(key_2_diff_int=access_key_2_last_used))
        elif name != 'user': 
                ofile.write("""<td>{key_2}</td>""".format(key_2=access_key_2_active))
                ofile.write("""<td>N/A</td>""")
                ofile.write("""<td>N/A</td>""")

        ofile.write("""</td>""")

ofile.write(close_html)

ifile.close()
ofile.close()
os.remove("text_results.txt")
