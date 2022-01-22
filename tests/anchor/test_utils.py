from solmate.anchor.utils import (
    camel_to_snake,
    snake_to_camel,
    pascal_to_snake,
    snake_to_pascal,
    kebab_to_snake,
    snake_to_kebab,
)


def test_camel_to_snake():
    assert camel_to_snake("aBCD") == "a_b_c_d"
    assert camel_to_snake("marketGroup") == "market_group"


def test_snake_to_camel():
    assert snake_to_camel("a_b_c_d") == "aBCD"
    assert snake_to_camel("market_group") == "marketGroup"


def test_pascal_to_snake():
    assert pascal_to_snake("ABCD") == "a_b_c_d"
    assert pascal_to_snake("MarketGroup") == "market_group"


def test_snake_to_pascal():
    assert snake_to_pascal("a_b_c_d") == "ABCD"
    assert snake_to_pascal("market_group") == "MarketGroup"


def test_kebab_to_snake():
    assert kebab_to_snake("a-b-c-d") == "a_b_c_d"
    assert kebab_to_snake("market-group") == "market_group"


def test_snake_to_kebab():
    assert snake_to_kebab("a_b_c_d") == "a-b-c-d"
    assert snake_to_kebab("market_group") == "market-group"
