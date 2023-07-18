import configparser

class Config:
    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def get(self, section, option):
        value = self.config.get(section, option)
        if ',' in value:
            return [int(i) for i in value.split(',')]
        return value

    def get_all_nodes(self):
        nodes = {}
        for section in self.config.sections():
            node_data = {}
            for key in self.config[section]:
                node_data[key] = self.get(section, key)
            nodes[section] = node_data
        print (nodes)
        return nodes

    def get_nodes(self):
        nodes = {}
        for section in self.config.sections():
            ip = self.config[section]['ip']
            port_in = self.config[section]['puertos_entrada']
            nodes[section] = f"{ip}:{port_in}"
        return nodes
    
    def get_ips(self):
        nodes = {}
        for section in self.config.sections():
            ip = self.config[section]['ip']
            #port_in = self.config[section]['puertos_entrada']
            nodes[section] = f"{ip}"
        return nodes