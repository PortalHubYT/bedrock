#/usr/bin/env python3

import os
import re
import subprocess
from dataclasses import dataclass

import requests
import yaml

# Filenames
DOCKERFILE = "Dockerfile"
PLUGINS = './plugins'
PROFILES = 'profile.yaml'
ENV = '.env'

# API URLs & Extra plugins
COMMAND_HELPER_JAR = 'commandhelper-3.3.5-SNAPSHOT-full.jar'
COMMAND_HELPER = 'https://apps.methodscript.com/builds/commandhelperjar/'

@dataclass
class JenkinsPlugin:
    resolved: False # Will skip the rest if this is a link, case of static name
    ######### Base
    base_url: str
    artifacts: str
    api: str = base_url + 'api/json'
    ######### Parsing
    jar_regex: str = r'\"fileName\":\"([^\"]*jar)\"'
    get_json: requests.get(base_url).json()
    get_jar: re.search(jar_regex, get_json).group(1)
    ######### Final
    dl: base_url + artifacts + get_jar
    
# Jenkins specific
# FAWE = 
# CITIZENS_2 = 
# PROTOCOL_LIB = 

J_API = 'api/json'

class DockerBuilder:
    
    # Build all profile in profile.yaml
    def build_all(self):
        for tag in self.profiles.keys():
            if not tag == "config":
                self.build_image(tag)
    
    # Build a single profile
    def build_image(self, tag):
        print(f"Building image for {tag}")
        # subprocess.run(["docker", "build", "--no-cache", "--tag", tag, "-f", self.dockerfile, "."])

    def fetch_plugins(self):
        os.makedirs(PLUGINS, mode=0o777, exist_ok=True)
        self._fetch_command_helper()
        self._fetch_others()

    # Command helper is even more annoying than the other
    # extra plugins because it's URL has an encoded /
    def _fetch_command_helper(self):
        last_build = max(re.findall(r'build-(\d+)', requests.get(COMMAND_HELPER).text))
        dl_link = f'{COMMAND_HELPER}-{last_build}/{COMMAND_HELPER_JAR}'
        save_path = f'{PLUGINS}/{COMMAND_HELPER_JAR}'
        
        with open(save_path, 'wb') as file:
            file.write(requests.get(dl_link).content)

    # These are the Jenkins plugins
    def _fetch_others(self):
        jar_reg = 
        get_jar = 
        
        fawe_url = FAST_ASYNC_WORLD_EDIT + 'artifact/artifacts/' + get_jar(FAST_ASYNC_WORLD_EDIT + J_API)
        cit_url = CITIZENS_2 + 'artifact/dist/target/' + get_jar(CITIZENS_2 + J_API)
        pro_lib_url = PROTOCOL_LIB + 'artifact/build/libs/ProtocolLib.jar'
        
        os.environ['PLUGINS'] = f'{fawe_url},{cit_url},{pro_lib_url}'

    # Get the profiles from profile.yaml
    def get_profiles(self):
        with open(PROFILES, 'r') as file:
            self.profiles = yaml.safe_load(file)
            if not self.profiles: raise Exception("No profiles found!")
            
        with open(ENV, 'w') as env_file:
            sections = self.profiles.keys()
            for key, value in [profile for profile in sections]:
                if isinstance(value, dict):
                    for inner_key, inner_value in value.items():
                        env_file.write(f"{inner_key.upper()}={self._format_value(inner_value)}\n")
                else:
                    env_file.write(f"{key.upper()}={self._format_value(value)}\n")

    @staticmethod
    def _format_value(value):
        if not isinstance(value, bool):
            return value
        return 'true' if value else 'false'

if __name__ == "__main__":
    builder = DockerBuilder()
    builder.fetch_plugins()
    builder.build_all()
    builder.build_image("classic")
    # builder.build_image("flat")
    # builder.build_image("void")