# fetch_plugins.py
import os
import re

import requests

"""This function fetches some plugins that are not on Spigot
The logic helps pulling the latest build of the plugins"""
os.makedirs('/data/plugins', mode=0o777, exist_ok=True)

# CommandHelper
ch_build = max(re.findall(r'build-(\d+)', requests.get('https://apps.methodscript.com/builds/commandhelperjar/').text))
os.system(f'curl -o /data/plugins/commandhelper-3.3.5.jar https://apps.methodscript.com/builds/commandhelperjar/build-{ch_build}/commandhelper-3.3.5-SNAPSHOT-full.jar')

# Helper function to get jar
def get_jar(url):
    return re.search(r'\"fileName\":\"([^\"]*jar)\"', requests.get(url).text).group(1)

# FastAsyncWorldEdit and Citizens2
fa_url = 'https://ci.athion.net/job/FastAsyncWorldEdit/lastSuccessfulBuild/artifact/artifacts/' + get_jar('https://ci.athion.net/job/FastAsyncWorldEdit/lastSuccessfulBuild/api/json')
cit_url = 'https://ci.citizensnpcs.co/job/Citizens2/lastSuccessfulBuild/artifact/dist/target/' + get_jar('https://ci.citizensnpcs.co/job/Citizens2/lastSuccessfulBuild/api/json')

# Set environment variable
os.environ['PLUGINS'] = f'{fa_url},{cit_url},https://ci.dmulloy2.net/job/ProtocolLib/lastBuild/artifact/build/libs/ProtocolLib.jar'
