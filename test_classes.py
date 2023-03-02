from classes import Message, Hashchain

SECRET = b'testsecret'
BAD_SECRET = b'badsecret'
BODY = 'test message body'
BAD_HASH = b'a99d9cb748c6649cf44cee493349bb2a'

def test_make_message():
    ''' tests that a message can be constructed with content'''
    h = Hashchain(SECRET)
    m = Message(h, BODY)

def test_make_empty_message():
    ''' tests that a message can be constructed with empty body'''
    h = Hashchain(SECRET)
    m = Message(h, '')    

def test_make_hashchain():
    ''' tests the hashchain constructor'''
    x = Hashchain(SECRET)

def test_last_collision():
    ''' tests that different secrets make different link 0'''
    x = Hashchain(SECRET)
    y = Hashchain(BAD_SECRET)
    assert x.last() != y.last()

def test_next_collision():
    ''' tests that different secrets make differnt link 1'''
    x = Hashchain(SECRET)
    y = Hashchain(BAD_SECRET)
    assert x.next() != y.next()

def test_last_agreement():
    ''' tests that the same secrets make the same hash 0 '''
    x = Hashchain(SECRET)
    y = Hashchain(SECRET)
    assert x.last() == y.last()

def test_next_agreement():
    ''' tests that the same secrets make the same hash 1 '''
    x = Hashchain(SECRET)
    y = Hashchain(SECRET)
    assert x.next() == y.next()

def test_generate_N():
    ''' tests generation of len 500 hash chain'''
    x = Hashchain(SECRET)
    chain = x.generate(500)
    assert len(chain) == 500

def test_nodupes():
    ''' tests that there are no duplicates within a len 500 hash chain'''
    x = Hashchain(SECRET)
    chain = x.generate(500)
    seen = set()
    for x in chain:
        if x in seen: raise Exception('Hash duplicates')
        seen.add(x)

def test_long_colllision():
    ''' tests for hash collisions in the first 500000 hashes'''
    x = Hashchain(SECRET)
    y = Hashchain(BAD_SECRET)
    chainx = set(x.generate(500000))
    chainy = set(y.generate(500000))
    assert len(chainx.intersection(chainy)) == 0

def test_detect_badsecret():
    ''' tests that hashes generated with different secrets will not validate'''
    x = Hashchain(SECRET)
    y = Hashchain(BAD_SECRET)
    z = y.next()
    assert x.validate(z) == False 

def test_detect_emptyhash():
    ''' tests that an empty hash will not validate'''
    x = Hashchain(SECRET)
    z = b''
    assert x.validate(z) == False

def test_detect_badhash():
    ''' tests that a random bad hash will not validate'''
    x = Hashchain(SECRET)
    assert x.validate(BAD_HASH) == False

def test_validate_valid():
    ''' tests that successive hashes will valdate on another chain with the same secret if checked in order'''
    x = Hashchain(SECRET)
    y = Hashchain(SECRET)
    chain = x.generate(500)
    early = chain[5]
    middle = chain[250]
    late = chain[490]
    assert y.validate(early) == True
    assert y.validate(middle) == True
    assert y.validate(late) == True

def test_detect_oldhash():
    ''' tests that chains generated with the same secret will not validate on each other in reverse order'''
    x = Hashchain(SECRET)
    y = Hashchain(SECRET)
    chain = x.generate(500)
    early = chain[5]
    middle = chain[250]
    late = chain[490]
    assert y.validate(late) == True
    assert y.validate(middle) == False
    assert y.validate(early) == False    

def test_return_last():
    ''' tests that the last hash validated successfully is returned by Hashchain.last()'''
    x = Hashchain(SECRET)
    y = Hashchain(SECRET)
    chain = x.generate(500)
    early = chain[5]
    middle = chain[250]
    late = chain[490]
    assert y.validate(late) == True
    assert y.validate(middle) == False
    assert y.validate(early) == False
    assert y.last() == late 

def test_return_last():
    ''' tests that the last hash validated unsucessfully is not returned by Hashchain.last()'''
    x = Hashchain(SECRET)
    y = Hashchain(SECRET)
    chain = x.generate(500)
    early = chain[5]
    middle = chain[250]
    late = chain[490]
    assert y.validate(late) == True
    assert y.validate(early) == False
    assert y.last() != early

def test_detect_replay():
    ''' tests that a hash just validated will not validate immediatey after'''
    x = Hashchain(SECRET)
    y = Hashchain(SECRET)
    chain = x.generate(500)
    early = chain[5]
    middle = chain[250]
    late = chain[490]
    assert y.validate(early) == True
    assert y.validate(early) == False
    assert y.validate(early) == False

def test_detect_late_replay():
    ''' tests that a hash validated long ago will not validate later following other validations'''
    x = Hashchain(SECRET)
    y = Hashchain(SECRET)
    chain = x.generate(500)
    early = chain[5]
    middle = chain[250]
    late = chain[490]
    assert y.validate(early) == True
    assert y.validate(middle) == True
    assert y.validate(early) == False