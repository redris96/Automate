Automate
========
A collection of scripts which automate routine stuff I do.

To install pre-requisites do:
bash install.sh

Info
====

mega.py
=======
pre-requisites:
1. Create and account on "https://forum.snahp.it/"
2. Create a file called "config.py" to hold your username and password.
The contents of the file should be:
```
username = "<your_username>"
password = "<your_password>"
```

The main source for the links is "https://forum.snahp.it/"
It gets the top x posts under Movies/"720p / 1080p" and Tv/"720p / 1080p" along with names, views and the post URL.

Usage:
```
python mega.py [<top>]
```
top: "Integer", to get top x posts. [optional, default=5]

bookmyshow.py
=============
usage: 
```
python bookmyshow.py "movie name"
```
It will check if the given movie is in theatres or not and will give you the link for booking if it is already out.
Features: Even if the movie name is typed incorrectly, it will give the closest matching result.

NOTE
---- 
If the movie name has spaces, please use "". The full movie name must be given as the first argument.

usage: python bookmyshow.py
Will show all currently showing movies along with their URLs.

Cron
-----
If you want to keep running it every x minutes, create a cronjob using:
```
crontab -e
```
And add the frequency and location of script.
For example The following runs the script every 5 minutes
```
*/5 * * * * python /home/rishith/dev/automate/bookmyshow.py Mahanoti
```

If you want the output to be mailed to you, when the movie is out, then do:
```
crontab -e
```
and add this line on top:
```
MAILTO=<you_email@domain.com>
```

And follow this tutorial to set up a working mailing system through gmail:
https://www.linode.com/docs/email/postfix/configure-postfix-to-send-mail-using-gmail-and-google-apps-on-debian-or-ubuntu/

NOTE 
----
Whenever there is an output, cron will send a mail. Even when the movie is not out, you'll get a mail. To stop this, remove (or comment) the print statements for the case when movie is not found:
i.e in file bookmyshow.py, comment lines 48-51
```
# else:
# 	print "Sorry " + movie + " is not out yet."
# 	print "Showing closest match with similarity ", max_val
# 	print_result(result)
```