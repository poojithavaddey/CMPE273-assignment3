import collections

def lru_cache(cap):
    l = cap
    cache = collections.OrderedDict()
    def inner_func(func):
        def inner(*args):
            key = args[0]
            if cache.get(key):
                cache.move_to_end(key,last=True)
                return cache[key]
            else:
                res = func(key,args[1])
                cache[key]= res 
                return cache[key]                      
        return inner
    return inner_func
