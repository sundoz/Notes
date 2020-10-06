import pytest


@pytest.mark.parametrize('x, y, result',[
    (1,1,2),
    (1,12,13),
    (1,122,123)
])

def test_add(x, y, result):
    assert x + y == result