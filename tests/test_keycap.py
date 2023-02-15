import pytest
from opk import KeyCap


@pytest.fixture
def esc_key():
    return KeyCap(legend='ESC')


@pytest.fixture
def spacebar():
    return KeyCap(unit=8, is_spacebar=True)


def test_key_cap_name_generation(esc_key, spacebar):
    assert esc_key.legend == 'ESC'
    assert esc_key.name == 'ESC_U1'
    assert spacebar.legend == ''
    assert spacebar.name == 'SPACEBAR_U8'
