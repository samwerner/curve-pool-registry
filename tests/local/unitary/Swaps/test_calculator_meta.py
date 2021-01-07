import brownie
import pytest

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


@pytest.mark.params(n_coins=3, n_metacoins=2)
def test_meta_calc_get_dy_lp_dx_meta(accounts, calculatorMeta, no_call_coverage, meta_swap, alice):
    # dx is meta pool token and dy lp token
    meta_swap._set_A(10000, 0, 0, 0, 0, {"from": alice})
    assert meta_swap.A_precise() == 10000
    expected = [89743074, 100065, 37501871, 90394938, 114182]
    actual = calculatorMeta.get_dy.call(
        2,
        (2241857934, 1895960155, 0, 0, 0, 0, 0, 0),
        100,
        4000000,
        (1000000000000000000, 1000000000000000000, 0, 0, 0, 0, 0, 0),
        (10000000000, 10000000000, 0, 0, 0, 0, 0, 0),
        0,
        1,
        [89970746, 100274, 37586976, 90624569, 114419] + [0] * 95
    )
    assert actual[:5] == expected


@pytest.mark.params(n_coins=3, n_metacoins=2)
def test_meta_calc_get_dy_base_dx_base(accounts, swap, calculatorMeta, no_call_coverage, meta_swap, alice):
    # dx and dy are base pool tokens
    meta_swap._set_A(10000, 0, 0, 0, 0, {"from": alice})
    swap._set_A(10000, 0, 0, 0, 0, {"from": alice})
    assert meta_swap.A_precise() == 10000
    assert swap.A_precise() == 10000
    # virtual LP token price is 1
    assert swap.get_virtual_price() == 1e18
    expected = [302936, 302680378, 836241086, 931038, 289803381]
    # set LP token balance [1]
    meta_swap._set_balances(
        [2000000000, 6000000000, 0, 0])
    actual = calculatorMeta.get_dy.call(
        4,
        (2000000000, 1873465287, 1921830293, 2204704420, 0, 0, 0, 0),
        100,
        4000000,
        (1000000000000000000, 1000000000000000000,
         1000000000000000000, 1000000000000000000, 0, 0, 0, 0),
        (10000000000, 10000000000, 10000000000, 10000000000, 0, 0, 0, 0),
        2,
        3,
        [302654, 302829983, 839029380, 930174, 289928981] + [0] * 95,
    )
    assert actual[:5] == expected


@pytest.mark.params(n_coins=3, n_metacoins=2)
def test_meta_calc_get_dy_meta_dx_base(accounts, swap, calculatorMeta, no_call_coverage, meta_swap, alice):
    # dx is base pool token; dy is meta pool token
    pass


@pytest.mark.params(n_coins=3, n_metacoins=2)
def test_meta_calc_get_dy_base_dx_meta(accounts, swap, calculatorMeta, no_call_coverage, meta_swap, alice):
    # dx is meta pool token; dy is base pool token
    pass


@pytest.mark.params(n_coins=3, n_metacoins=2)
def test_meta_calc_invalid_pool_size(accounts, calculatorMeta, no_call_coverage):
    with brownie.reverts("Unsupported pool size"):
        calculatorMeta.get_dy.call(
            5,
            (0, 0, 0, 0, 0, 0, 0, 0),
            0,
            0,
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            0,
            1,
            [0] * 100
        )
    with brownie.reverts("Unsupported pool size"):
        calculatorMeta.get_dy.call(
            1,
            (0, 0, 0, 0, 0, 0, 0, 0),
            0,
            0,
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            0,
            1,
            [0] * 100
        )