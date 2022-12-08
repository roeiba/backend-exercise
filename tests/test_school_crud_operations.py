import pytest
# test school
from random import random, randint

from tests.test_utils import get_schools, create_school, get_school, update_school, delete_school, \
    entity_is_in_collection, get_a_school
import logging
_logger = logging.getLogger(__name__)


@pytest.fixture
def a_school():
    a_school = get_a_school()
    yield a_school
    assert entity_is_in_collection(a_school, get_schools())
    delete_school(a_school.id)
    assert not entity_is_in_collection(a_school, get_schools())


def test_get_schools():
    schools = get_schools()
    _logger.info(schools)
    assert len(schools) > 0


def test_get_school(a_school):
    actual_school = get_school(school_id=a_school.id)
    assert actual_school.id == a_school.id


def test_create_school():
    i = randint(0, 10000)
    name = f"School_{i}"
    address = f"address_{i}"
    schools = get_schools()
    school = create_school(name, address)
    assert school.name == name
    assert school.address == address
    new_schools = get_schools()
    assert len(new_schools) == len(schools) + 1
    return school


def test_update_school(a_school):
    new_name = a_school.name + "_test"
    new_address = a_school.address + "_test"
    updated_school = update_school(school_id=a_school.id, name=new_name, address=new_address)
    assert new_name == updated_school.name
    assert new_address == updated_school.address
    # restore school values
    updated_school = update_school(school_id=a_school.id, name=a_school.name, address=a_school.address)
    assert updated_school.name == a_school.name
    assert updated_school.address == a_school.address
