import hashlib


class Message:
    ''' Defines a message class containing header and body members, 
        Constructed from a chain object and a message string'''
    def __init__(self, chain, body):
        self.header = chain.next()
        self.body = body
    def __str__(self):
        return self.body


class Hashchain:
    ''' Defines a class of hashchain objects, is constructed with a byte string as a shared secret'''
    def __init__(self, SECRET, N): 
        self.__secret = SECRET            
        self.__link_0 = hashlib.sha256(SECRET).digest()
        self.__hash_chain = []
        self.__generate(N)
        self.__last = b'hhh'

    def validate(self, unk_hash):
        ''' Returns True if the provided hash is next in the chain, False otherwise'''
        if unk_hash == self.__hash_chain[-1]:
            self.__last = unk_hash
            self.__hash_chain.pop()
            return True
        else:
            return False
        
    def next(self):
        ''' Returns and pops the next hash in the chain'''
        return self.__hash_chain.pop()

    def last(self):
        ''' Returns the last inspected hash to return True from Hashchain.validate() empty byte string if None'''
        return self.__last
    
    def chain(self):
        ''' Returns a copy of the hashchain in its current state'''
        return self.__hash_chain
    
    def __generate(self, N):
        # private function to generate the hash chain
        kwn_hash = self.__link_0
        for i in range(N):
            kwn_hash = self.__make_link(self.__secret, kwn_hash)
            self.__hash_chain.append(kwn_hash)
             
    def __make_link(self, secret, in_hash):
        # private function to construct an additional link from a secret and the last link
        concat = secret + in_hash
        return hashlib.sha256(concat).digest()



class Colour:
    OK = '\033[92m'
    WARN = '\033[91m'
    END = '\033[0m'