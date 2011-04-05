from UserDict import DictMixin
from uuid import uuid4
import threading
import math
import logging
import json


class ClientHandler(DictMixin):
    def __init__(self):
        self.active_clients = {}
    
    # DictMixin required methods
    def __getitem__(self, client_id):
        return self.active_clients[client_id]
    
    def __setitem__(self, client_id, client):
        self.active_clients[client_id] = client
        
    def __delitem__(self, client_id):
        del self.active_clients[client_id]
        
    def __contains__(self, client_id):
        return client_id in self.active_clients
        
    def keys(self):
        return self.active_clients.keys()
    # End of DictMixin required methods

class MobileClient(object):
    
    seq = 0
    seq_lock = threading.Lock()
    
    @classmethod
    def new_id(cls):
        with cls.seq_lock:
            current = cls.seq
            cls.seq += 1
            
        return "%(client_id)s-SEQ%(seq)i" % {
            "client_id": str(uuid4()),
            "seq": current
            }
    
    def __init__(self, phone_type = None, ip_addr = None):
        self.client_id = MobileClient.new_id()
        self.phone_type = phone_type
        self.ip_addr = ip_addr
        self.points = 0
        self.last_direction = None
        
        self.ax = None
        self.ay = None
        self.az = None
        self.ai = None
        self.arAlpha = None
        self.arBeta = None
        self.arGamma = None
        self.angle = None
        
        self.log = logging.getLogger("MobileClient.logger")
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s: %(name)s: %(levelname)s: %(message)s"))
        self.log.addHandler(handler)
        self.log.setLevel(logging.DEBUG)
    
    def update(self, info):
        self.ax = info["ax"]
        self.ay = info["ay"]
        self.az = info["az"]
        self.ai = info["ai"]
        self.arAlpha = info["arAlpha"]
        self.arBeta = info["arBeta"]
        self.arGamma = info["arGamma"]
        self.angle = math.atan2( float(info["ay"]), float(info["ax"]) ) * 57.29577951308232
        
        self.log.debug( "Client:%s - acceleration-data: angle=%d (ax=%s ay=%s az=%s)" % (self.client_id, self.angle, self.ax, self.ay, self.az) )
    
    def status(self):
        return {
                'ax' : self.ax,
                'ay' : self.ay,
                'az' : self.az,
                'ai' : self.ai,
                'arAlpha' : self.arAlpha,
                'arBeta' : self.arBeta,
                'arGamma' : self.arGamma,
                'angle' : self.angle
                    } 
        
    