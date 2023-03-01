from classes import Message, Hashchain, Colour
import pytest

SECRET = b'testsecret'
BAD_SECRET = b'badsecret'
BODY = 'test message body'

x = Hashchain(SECRET)
chain = x.generate(500)
early = chain[5]
middle = chain[250]
late = chain[490]

y = Hashchain(BAD_SECRET)
chain = x.generate(500)
early = chain[5]
middle = chain[250]
late = chain[490]


def test_make_message():
    h = Hashchain(SECRET)
    m = Message(h, BODY)

def test_make_empty_message():
    h = Hashchain(SECRET)
    m = Message(h, '')    

def test_make_hashchain():
    x = Hashchain(SECRET)

def test_last_collision():
    x = Hashchain(SECRET)
    y = Hashchain(BAD_SECRET)
    assert x.last() != y.last()

def test_next_collision():
    x = Hashchain(SECRET)
    y = Hashchain(BAD_SECRET)
    assert x.last() != y.last()

def test_last_agreement():
    x = Hashchain(SECRET)
    y = Hashchain(SECRET)
    assert x.last() == y.last()

def test_next_agreement():
    x = Hashchain(SECRET)
    y = Hashchain(SECRET)
    assert x.next() == y.next()

def test_generate_N():
    x = Hashchain(SECRET)
    chain = x.generate(500)
    assert len(chain) == 500

def test_nodupes():
    x = Hashchain(SECRET)
    chain = x.generate(500)
    seen = set()
    for x in chain:
        if x in seen: raise Exception('Hash duplicates')
        seen.add(x)

def test_long_colllision():
    x = Hashchain(SECRET)
    y = Hashchain(BAD_SECRET)
    chainx = set(x.generate(500000))
    chainy = set(y.generate(500000))
    assert len(chainx.intersection(chainy)) == 0

def test_validate_valid():
    x = Hashchain(SECRET)
    chain = x.generate(500)
    early = chain[5]
    middle = chain[250]
    late = chain[490]
    assert x.validate(early) == True
    assert x.validate(middle) == True
    assert x.validate(late) == True


def test_detect_badsecret():
    pass

def test_detect_badhash():
    pass

def test_detect_oldhash():
    pass

def test_return_last():
    pass

