import socket
import pickle
from classes import Message, Hashchain, Colour


SECRET = b'h6f28g865307gse3'
HOST = '127.0.0.1'
PORT = 9999


def inspect(payload):
    if chain.validate(payload.header):
        print(Colour.OK + f' <VERIFIED> : '+ Colour.END + payload.body)
    else:
        print(Colour.WARN + f' <NOT VERIFIED> : '+ Colour.END + payload.body)


if __name__ == "__main__":

    # Create a socket connection.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # construct the hashchain object
    chain = Hashchain(SECRET)

    # setup a prompt
    text_string = input(' <INPUT> : ')

    # compose the message object
    message = Message(chain, text_string)

    # Pickle the object and send it to the server
    data = pickle.dumps(message)
    s.send(data)
    print(' <SENT> : '+ text_string)

    # recieve the response
    ack = s.recv(1024)
    payload = pickle.loads(ack)

    # inspect the payload of the message
    inspect(payload)

    # close the connection
    s.close()
    print (' <CLOSED>')