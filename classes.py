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
    def __init__(self, SECRET):
        self.__secret = SECRET
        self.__link0 = hashlib.sha256(SECRET).digest()
        self.__last_good = b''
    
    def validate(self, unk_hash):
        ''' Returns True if the provided hash is in the chain, False otherwise'''
        if self.__check_links(self.__last_good, unk_hash) == True:
            return True
        elif self.__check_links(self.__link0, unk_hash) == True:
            return True
        else:
            return False
        
    def next(self):
        ''' Returns the next hash in the chain based on the hash to return True from Hashchain.validate()'''
        return self.__make_hashlink(self.__secret, self.__last_good)

    def last(self):
        ''' Returns the last inspected hash to return True from Hashchain.validate() empty byte string if None'''
        return self.__last_good
    
    def __make_hashlink(self, secret, in_hash):
        # private function to construct an additional link from a secret and the last link
        concat = secret + in_hash
        return hashlib.sha256(concat).digest()

    def __check_links(self, in_hash, unk_hash, depth=10000):
        # private function to scan forward in the hash chain to validate an unknown hash
        while depth > 0:
            if in_hash == unk_hash:
                self.__last_good = in_hash
                return True
            else:
                in_hash = self.__make_hashlink(self.__secret, in_hash)
                depth -= 1
        return False


class Colour:
    OK = '\033[92m'
    WARN = '\033[91m'
    END = '\033[0m'