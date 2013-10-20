zmail
=====
'z' for 'zaochny'.

The script 'send_letters_csv.py' is an utility for distant math study group.
It helps e-mail registration letters to a list of users given in a csv-file.

Usage: write in command line
'python3 send_letters_csv.py CSV-FILE SENDER PASSWORD'
CSV-FILE - file in .csv format, one row for each user. It's fields:
0. timestamp, 
1. name, 
2. birthday, 
3. form, 
4. school, 
5. city, 
6. country, 
7. district, 
8. e-mail, 
9. phone, 
10. content for receiving mail, 
11. user's comment, 
12. code, 
13. registration date, 
14. our comment
Only fields 1, 3, 4, 5, 8, 12, 14 are used by the script for now.

SENDER - sender's email
PASSWORD - sender's password for SMTP-server.



