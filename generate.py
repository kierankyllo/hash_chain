from classes import Hashchain

SECRET = b'testsecret'
N = 500

def generate(SECRET, N):
    chain = Hashchain(SECRET, N).chain()
    with open('hash_chain.txt', 'w') as f:
        for link in chain:
            f.write(link.hex()+'\n')


if __name__ == "__main__":
   generate(SECRET, N)
