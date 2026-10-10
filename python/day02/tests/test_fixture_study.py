import pytest


class Fruit:
    def __init__(self, name):
        self.name = name
        self.cubed = False

    def cube(self):
        self.cubed = True


class FruitSalad:
    def __init__(self, *fruit_bowl):
        self.fruit = fruit_bowl
        self._cube_fruit()

    def _cube_fruit(self):
        for fruit in self.fruit:
            fruit.cube()


@pytest.fixture
def fruit_bowl():
    return [Fruit("apple"), Fruit("banana")]


def test_fruit_salad(fruit_bowl):
    fruit_salad = FruitSalad(*fruit_bowl)
    assert all(fruit.cubed for fruit in fruit_salad.fruit)


@pytest.fixture
def first_entry():
    return "a"


@pytest.fixture
def order(first_entry):
    return [first_entry]


def test_string(order):
    order.append("b")
    order.append("c")
    assert order == ["a", "b", "c"]


def test_int(order):
    order.append(2)
    assert order == ["a", 2]


@pytest.fixture
def second_entry():
    return 2


@pytest.fixture
def order2(first_entry, second_entry):
    return [first_entry, second_entry]


@pytest.fixture
def expected_list():
    return ["a", 2, 3.0]


def test_string2(order2, expected_list):
    order2.append(3.0)
    assert order2 == expected_list


@pytest.fixture
def order3():
    return []


@pytest.fixture
def append_first(order3, first_entry):
    return order3.append(first_entry)


def test_string_only(append_first, order3, first_entry):
    assert order3 == [first_entry]


@pytest.fixture
def order4(first_entry):
    return []


@pytest.fixture(autouse=True)
def append_fist2(order4, first_entry):
    return order4.append(first_entry)


def test_string_only2(order4, first_entry):
    assert order4 == [first_entry]


def test_string_and_int(order4, first_entry):
    order4.append(2)
    assert order4 == [first_entry, 2]
