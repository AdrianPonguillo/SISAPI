from pysyncobj import SyncObj, SyncObjConf
from threading import Thread

class Node(Thread):
    def __init__(self, self_ip, partner_ips):
        Thread.__init__(self)
        config = SyncObjConf(autoTick=False)
        self._sync_obj = SyncObj(self_ip, partner_ips, conf=config)
        print('Creado el nodo')
        
    def run(self):
        while True:
            self._sync_obj.doTick()

    def tick(self):
        self._sync_obj.doTick()

    def is_alive(self):
        return self._sync_obj._isReady
        return self._sync_obj._isRunning

    def is_leader(self):
        return self._sync_obj._isLeader

    def get_partners(self):        
        try:
            self.xnodes = self._sync_obj.__otherNodes
            return self.xnodes
        except:
            print('No hay mas nodos')
        


