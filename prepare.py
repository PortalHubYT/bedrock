#/usr/bin/env python3

import os
import re
import sys

import requests
import yaml


class Config:
    def __init__(self, filepath):
        with open(filepath, 'r') as file:
            self.data = yaml.safe_load(file)
        if not self.data:
            raise ValueError("Invalid config file!")

    @property
    def images(self):
        return self.data.get('images', {})

    @property
    def jenkins_links(self):
        return self.data.get('config', {}).get('jenkins_plugins', [])

class DockerBuilder:
    def __init__(self, config: Config):
        self.config = config

    # Could almost be normalized, but sadly some plugins are not on Jenkins
    # So we have to do it manually
    def fetch_plugins(self, plugin_path='/tmp/plugins', debug=True):
        os.makedirs(plugin_path, mode=0o777, exist_ok=True)
        
        #---> Start of culprit
        COMMAND_HELPER = 'https://apps.methodscript.com/builds/commandhelperjar/'
        # Command helper fetch
        manifest = requests.get(COMMAND_HELPER).json()
        latest_build_info = max(manifest, key=lambda x: int(x['buildId'].split('-')[1]))
        dl_link = latest_build_info['fullLink']
        if debug: print(f"Downloading CommandHelper from {dl_link}")
        with open(f'{plugin_path}/commandhelper-latest.jar', 'wb') as file:
            file.write(requests.get(dl_link).content)
            if debug:
                print(f"[COMMANDHELPER] Downloaded {dl_link}, in {plugin_path}")
        #<--- End of culprit
        
        # Jenkins plugins fetch, we rewrite Jenkins class into a for loop
        for link in self.config.jenkins_links.split('\n'):
            target_build = link + "lastSuccessfulBuild/"
            api = target_build + 'api/json'
            manifest = requests.get(api).json()
            filepath = manifest["artifacts"][0]["relativePath"]
            filename = manifest["artifacts"][0]["fileName"]
            if debug: print(f"Downloading {filename} from {target_build}")
            with open(f'{plugin_path}/{filename}', 'wb') as file:
                file.write(requests.get(target_build + 'artifact/' + filepath).content)
                if debug:
                    print(f"[JENKINS] Downloaded {filename}, in {plugin_path}")
                    
    # It generates a file that's called at the end of the Dockerfile (entrypoint)
    def write_env_to_file(self, tag, debug=True):
        image_env = self.config.images.get(tag, {})
        with open('/tmp/set_env.sh', 'w') as f:
            for key, value in image_env.items():

                if isinstance(value, list):
                    value = ','.join(value)
                elif isinstance(value, bool):
                    value = 'TRUE' if value else 'FALSE'
                elif isinstance(value, str):
                    value = value.replace('"', '\\"')

                f.write(f'export {key.upper()}="{value}"\n')
                if debug:
                    f.write(f"echo 'export {key.upper()}=\"{value}\"'\n")


if __name__ == "__main__":
    img_tag = "default"
    debug = False
    
    if len(sys.argv) > 1:
        img_tag = sys.argv[1]

    if len(sys.argv) > 2:
        debug = sys.argv[2].lower() == "true"
        
    config = Config('/tmp/profile.yml')
    builder = DockerBuilder(config)
    builder.fetch_plugins("/tmp/plugins", debug=debug)
    builder.write_env_to_file(img_tag, debug=debug)