import socketserver
import pickle
from classes import Message, Hashchain, Colour


SECRET = b'h6f28g865307gse3'
HOST = '127.0.0.1'
PORT = 9999


class MyTCPSocketHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    """
    def inspect(self):
        if self.chain.validate(self.header):
            print(Colour.OK + f'{self.client_address[0]} <VERIFIED> : '+ Colour.END + self.message)
        else:
            print(Colour.WARN + f'{self.client_address[0]} <NOT VERIFIED> : '+ Colour.END + self.message)

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024)
        self.payload = pickle.loads(self.data)
        self.header = self.payload.header
        self.message = self.payload.body
        self.chain = Hashchain(SECRET)
        self.colouring = ''

        # display the address, verification status, and the message 
        self.inspect()

        # create an acknowledgement message
        self.ack = Message(self.chain, 'ACK: '+ self.message)
        self.response = pickle.dumps(self.ack)
        
        # respond with a message object acknowledgement
        self.request.sendall(self.response)


if __name__ == "__main__":
    
    # instantiate the server, and bind to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPSocketHandler)

    # activate the server
    server.serve_forever()