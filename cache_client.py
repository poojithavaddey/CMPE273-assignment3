import sys
import socket
import collections 
from lru_cache import lru_cache

from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE
from client_ring import NodeRing
from bloom_filter import BloomFilter

BUFFER_SIZE = 1024
item_cnt =1000000
prob = 0.05
bloomfilter = BloomFilter(item_cnt,prob)


class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
               

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()

def process(udp_clients):
    client_ring = NodeRing(udp_clients)
    hash_codes = set()
    # PUT all users.  

    @lru_cache(5)
    def get(key,data_bytes):
        if bloomfilter.is_member(key):
            response = client_ring.get_node(key).send(data_bytes)
            return response

    def put(key):
        bloomfilter.add(key)
        return True
        
    def delete(key):
        if bloomfilter.is_member(key):
            return True
    
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
        put(key)
        response = client_ring.get_node(key).send(data_bytes)
        print(response)
        hash_codes.add(str(response.decode()))

    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")

    # GET all users.
    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_GET(hc)
        get(key,data_bytes)
    
    #DELETE the user
    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_DELETE(hc)
        del_val = delete(key)
        if del_val == True:
            response = client_ring.get_node(key).send(data_bytes)
            print(response)

        

if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    process(clients)