import socket
import json
import threading

class UdpAsyncClient(threading.Thread):
    def __init__(self, mainLoopInstance, cbFn, port=5005, bufferSize=1024):
        self.mainLoop = mainLoopInstance
        self.parrentCb = cbFn 
        self.port = port
        self.bufferSize = bufferSize
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self.port))
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            try:
                data, _ = self.sock.recvfrom(self.bufferSize)
                message = data.decode('utf-8')
                
                try:
                    json_data = json.loads(message)
                    self.parrentCb(json_data)
                except json.JSONDecodeError as e:
                    self.parrentCb("err") 
                
            except Exception as e:
                pass
                #self.parrentCb("err") 