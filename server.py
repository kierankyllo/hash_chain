import socketserver
from classes import Message, Hashchain, Colour
import pickle




class TCP_Handler(socketserver.BaseRequestHandler):
    """
    Our server request handler is derived from the base class BaseRequestHandler from the sockerserver library

    """
    def inspect(self):
        '''A function to inspect the payload and provide feedback to the console'''
        if chain.validate(self.__header):
            print(Colour.OK + f'{self.client_address[0]} <VERIFIED> : '+ Colour.END + self.__message + ': ' + str(chain.last().hex()))
        else:
            print(Colour.WARN + f'{self.client_address[0]} <NOT VERIFIED> : '+ Colour.END + self.__message + ': ' + str(chain.last().hex()))


    def handle(self):
        '''This is the handler function for requests for our server'''
        
        # self.request is the TCP socket connected to the client
        self.__data = self.request.recv(1024)
        self.__payload = pickle.loads(self.__data)

        # unpack the message
        self.__header = self.__payload.header
        self.__message = self.__payload.body

        # display the address, verification status, and the message 
        self.inspect()

        # create an acknowledgement message
        self.__ack = Message(chain, 'ACK: '+ self.__message)
        self.__response = pickle.dumps(self.__ack)
        
        # respond with a message object acknowledgement
        self.request.sendall(self.__response)

SECRET = b'topsecret'
HOST = '127.0.0.1'
PORT = 9999

chain = Hashchain(SECRET, 500)

if __name__ == "__main__":    
    # instantiate the server, and bind to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), TCP_Handler)
try:
    # activate the server
    print('\n <SESSION OPENED>')
    server.serve_forever()

except KeyboardInterrupt:
    # shutdown gracefully
    print('\n <SESSION CLOSED>')
    server.server_close()