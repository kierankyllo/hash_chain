from classes import Message, Hashchain


''' This testing suite is executed using pytest in terminal '''


SECRET = b'testsecret'
BAD_SECRET = b'badsecret'
BODY = 'test message body'
BAD_HASH = b'a99d9cb748c6649cf44cee493349bb2a'

def test_make_message():
    ''' tests that a message can be constructed with content'''
    h = Hashchain(SECRET, 500)
    m = Message(h, BODY)

def test_make_empty_message():
    ''' tests that a message can be constructed with empty body'''
    h = Hashchain(SECRET, 500)
    m = Message(h, '')    

def test_make_hashchain():
    ''' tests the hashchain constructor'''
    x = Hashchain(SECRET, 500)

def test_next_collision():
    ''' tests that different secrets make different starting links'''
    x = Hashchain(SECRET, 500)
    y = Hashchain(BAD_SECRET, 500)
    assert x.next() != y.next()

def test_next_agreement():
    ''' tests that the same secrets make the same hash 1 '''
    x = Hashchain(SECRET, 500)
    y = Hashchain(SECRET, 500)
    assert x.next() == y.next()

def test_generate_N():
    ''' tests generation of len 500 hash chain'''
    x = Hashchain(SECRET, 500)
    chain = x.chain()
    assert len(chain) == 500

def test_nodupes():
    ''' tests that there are no duplicates within a len 500 hash chain'''
    x = Hashchain(SECRET, 500)
    chain = x.chain()
    seen = set()
    for x in chain:
        if x in seen: raise Exception('Hash duplicates')
        seen.add(x)

def test_long_colllision():
    ''' tests for hash collisions in the first 500000 hashes'''
    x = Hashchain(SECRET, 500000)
    y = Hashchain(BAD_SECRET, 500000)
    chainx = set(x.chain())
    chainy = set(y.chain())
    assert len(chainx.intersection(chainy)) == 0

def test_long_agreement():
    ''' tests for hash agreement at hash[500000]'''
    x = Hashchain(SECRET, 500000)
    y = Hashchain(SECRET, 500000)
    chainx = x.chain()
    chainy = y.chain()
    assert chainx[-1] == chainy[-1]
    

def test_detect_badsecret():
    ''' tests that hashes generated with different secrets will not validate'''
    x = Hashchain(SECRET, 500)
    y = Hashchain(BAD_SECRET, 500)
    z = y.next()
    assert x.validate(z) == False 

def test_detect_emptyhash():
    ''' tests that an empty hash will not validate'''
    x = Hashchain(SECRET, 500)
    z = b''
    assert x.validate(z) == False

def test_detect_badhash():
    ''' tests that a random bad hash will not validate'''
    x = Hashchain(SECRET, 500)
    assert x.validate(x) == False

def test_validate_valid():
    ''' tests that hashes will valdate on another chainwith same secret'''
    x = Hashchain(SECRET, 500)
    y = Hashchain(SECRET, 500)
    a = x.next()  
    assert y.validate(a) == True


def test_detect_invalid_order():
    ''' tests that chains generated with the same secret will not validate on each other in generated order'''
    x = Hashchain(SECRET, 500)
    y = Hashchain(SECRET, 500)
    chain = x.chain()
    a = chain[-3]
    b = chain[-2]
    c = chain[-1]
    assert y.validate(a) == False
    assert y.validate(b) == False
    assert y.validate(c) == True    

def test_return_last():
    ''' tests that the last hash validated successfully is returned by Hashchain.last()'''
    x = Hashchain(SECRET, 500)
    y = Hashchain(SECRET, 500)
    chain = x.chain()
    a = chain[-3]
    b = chain[-2]
    c = chain[-1]
    assert y.validate(c) == True
    assert y.validate(b) == True
    assert y.validate(a) == True
    assert y.last() == a 

def test_return_last():
    ''' tests that the last hash validated unsucessfully is not returned by Hashchain.last()'''
    x = Hashchain(SECRET, 500)
    y = Hashchain(SECRET, 500)
    chain = x.chain()
    a = chain[-3]
    b = chain[-2]
    c = chain[-1]
    assert y.validate(c) == True
    assert y.validate(a) == False
    assert y.validate(a) == False
    assert y.last() != a

def test_detect_replay():
    ''' tests that a hash just validated will not validate immediatey after'''
    x = Hashchain(SECRET, 500)
    y = Hashchain(SECRET, 500)
    a = x.next()
    assert y.validate(a) == True
    assert y.validate(a) == False


def test_detect_late_replay():
    ''' tests that a hash validated in the past will not validate later following other validations'''
    x = Hashchain(SECRET, 500)
    y = Hashchain(SECRET, 500)
    a = x.next()
    assert y.validate(a) == True
    b = x.next()
    assert y.validate(b) == True
    c = x.next()
    assert y.validate(a) == False

def test_simulate_chat():
    x = Hashchain(SECRET, 500)
    y = Hashchain(SECRET, 500)
    ''' X composes message  'a' to send to Y'''
    a = x.next()
    # print(a.hex())
    ''' Y receives message 'a' and validates it'''
    assert y.validate(a) == True
    ''' Y composes message 'b' to send to X'''
    b = y.next()
    # print(b.hex())
    ''' X recieves message 'b' and validates it '''
    assert x.validate(b) == True




