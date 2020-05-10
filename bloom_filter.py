import math 
import mmh3 
from bitarray import bitarray 
  
class BloomFilter(object): 
    def __init__(self, n,p): 
        self.p = p 
        self.size = self.get_size(n,p) 
        self.hash_count = self.get_hash_count(self.size,n) 
        self.bit_array = bitarray(self.size) 
        self.bit_array.setall(0) 

    def add(self, ele): 
        filter_list = [] 
        for i in range(self.hash_count): 
            hash_el = mmh3.hash(ele,i) % self.size 
            filter_list.append(hash_el) 
            self.bit_array[hash_el] = True
  
    def is_member(self, ele): 
        for i in range(self.hash_count): 
            hash_el = mmh3.hash(ele,i) % self.size 
            if self.bit_array[hash_el] == False: 
                return False
        return True
  
    @classmethod
    def get_size(self,n,p): 
        m = -(n * math.log(p))/(math.log(2)**2) 
        return int(m) 
  
    @classmethod
    def get_hash_count(self, m, n): 
        k = (m/n) * math.log(2) 
        return int(k) 