#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
cloadapp
Alexey Blinov / @nilcolor

Uploads a file from the command line to CloudApp
Shareable link will be in your clipboard after that (I hope so...)

Example:
    >cloudapp mega-cool-image.png

To be able to post to CloudApp you need to set CloudApp credentials
in ~/.cloudapp file. Format is simple as this:
$ cat ~/.cloudapp
    email_aka_cloudapp_login
    supa_pupa_password

Dependencies:
    cloudapp (https://github.com/originell/pycloudapp)
"""
import sys
import os
import re
import json
from subprocess import call

def abort(msg):
    print(msg)
    sys.exit(1)

def fallback(urls):
    print("I can't put urls in the clipboard. But you can select and copy next line:")
    print(",".join(urls))

try:
    from cloudapp.cloud import Cloud
except Exception, e:
    abort("You need to install CloudApp API wrapper from https://github.com/originell/pycloudapp")

if not sys.argv[1:]:
    abort("You need to specify a file or two to upload. Or three... or... you got this.")

TOKEN = re.compile("\s*//.*", re.L)

if os.path.isfile("/Users/nilcolor/.cloud"):
    with open("/Users/nilcolor/.cloud", "r") as f:
        buf = f.read()
    buf = ''.join(TOKEN.split(buf))

    SETTINGS = json.loads(buf)
else:
    with open("/Users/nilcolor/.cloud", "w") as f:
        with open("./cloud-settings.json", "r") as s:
            f.write(s.read())
    abort("You need to type your email and password into ~/.cloud file")

urls = []
your_cloud = Cloud()

try:
    your_cloud.auth(SETTINGS["email"], SETTINGS["password"])
except KeyError, e:
    abort("You missed either `email` or `password` key in ~/.cloud file. Please check your settings.")
except Exception, e:
    abort("CloudApp authentication failed. Check your email/password in ~/.cloud file.")

if not your_cloud.auth_success:
    abort("CloudApp authentication failed. Check your email/password in ~/.cloud file.")

whats = {
    'source': lambda x,v:x.append(v["content_url"]),
    'view': lambda x,v:x.append(v["url"]),
}

for f in sys.argv[1:]:
    response = your_cloud.upload_file(f)
    print("Uploaded %s to %s" %(f, response['url']))
    whats[SETTINGS.get("mode", "source")](urls, response)

try:
    cmd = 'echo %s | tr -d "\\n" | pbcopy' % ','.join(urls) # this doesn't work under terminal multiplexers like tmux... pbcopy's fault
    ret = call(cmd, shell=True)
    if ret < 0:
        fallback(urls)
except OSError, e:
    fallback(urls)
