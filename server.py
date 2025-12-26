import json
import re
import time
from threading import Thread
import requests

class Server_handler_task(Thread):
    global data_collect
    global trasfer_status
    global data_part_count
    trasfer_status = "done"
    data_collect={"Request_num":[], "Data":[]}
    data_part_count = 0
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global data_collect
        global data_part_count
        while True:
            print(json.dumps(data_collect) , " len=" ,len(data_collect))
            if (len(data_collect)!= 0):
                if (self.reporting('connection_request') == 'done'):
                    data_collect={"Request_num":[], "Data":[]}
                    data_part_count=0
            time.sleep(10)
    def reporting(self, arg):
        try:
            response = requests.get("http://ip-service.net.ua/get_telemetry.php")
            if (response.status_code == 200):
                print(re.sub(r'[^!-~a-zA-Z0-9]', '', response.content.decode('utf-8')))
                return 'done'
            else:
                return response.status_code
        except:
            return 'Connection error'

    def data_transfer(self, *kwargs):
        global trasfer_status
        global data_collect
        global data_part_count
        #print(kwargs[0]['x'], " +++ ", kwargs[0]['y'])
        data_collect["Request_num"].append(data_part_count)
        data_collect["Data"].append(kwargs[0])
        data_part_count+=1
        if (len(data_collect) > 3):
            return False
        else:
            return True

