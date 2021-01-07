import brownie
import pytest

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


@pytest.mark.params(n_coins=3, n_metacoins=2)
def test_meta_calc_get_dy_lp_dx_meta(accounts, calculatorMeta, meta_swap, alice):
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
def test_meta_calc_get_dy_base_dx_base(accounts, swap, calculatorMeta, meta_swap, alice):
    # dx and dy are base pool tokens
    meta_swap._set_A(10000, 0, 0, 0, 0, {"from": alice})
    swap._set_A(10000, 0, 0, 0, 0, {"from": alice})
    assert meta_swap.A_precise() == 10000
    assert swap.A_precise() == 10000
    # virtual LP token price is 1
    assert swap.get_virtual_price() == 1e18
    expected = [302936, 302680378, 836241086, 931038, 289803381]
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
def test_meta_calc_get_dy_meta_dx_base(accounts, swap, meta_lp_token, calculatorMeta, meta_swap, alice):
    # dx is base pool token; dy is meta pool token
    meta_swap._set_A(10000, 0, 0, 0, 0, {"from": alice})
    swap._set_A(10000, 0, 0, 0, 0, {"from": alice})
    meta_lp_token._mint_for_testing(ZERO_ADDRESS, 8e19)
    assert meta_lp_token.total_supply() == 8e19
    assert meta_swap.A_precise() == 10000
    assert swap.A_precise() == 10000
    assert swap.get_virtual_price() == 1e18
    expected = [1314330, 91281538, 655624, 964146705, 108630091]
    # set LP token balance for meta pool
    meta_swap._set_balances(
        [0, 6e19, 0, 0], {"from": alice})
    actual = calculatorMeta.get_dy.call(
        4,
        (2000000000, 1873465287, 1921830293, 2204704420, 0, 0, 0, 0),
        100,
        4000000,
        (1000000000000000000, 1000000000000000000,
         1000000000000000000, 1000000000000000000, 0, 0, 0, 0),
        (10000000000, 10000000000, 10000000000, 10000000000, 0, 0, 0, 0),
        1,
        0,
        [1002939, 69729839, 500290, 750000000, 83000280] + [0] * 95,
    )
    assert actual[:5] == expected


@pytest.mark.params(n_coins=3, n_metacoins=2)
def test_meta_calc_get_dy_base_dx_meta(accounts, swap, meta_lp_token, calculatorMeta, meta_swap, alice):
    # dx is meta pool token; dy is base pool token
    meta_swap._set_A(10000, 0, 0, 0, 0, {"from": alice})
    swap._set_A(10000, 0, 0, 0, 0, {"from": alice})
    meta_lp_token._mint_for_testing(ZERO_ADDRESS, 8e19)
    assert meta_lp_token.total_supply() == 8e19
    assert meta_swap.A_precise() == 10000
    assert swap.A_precise() == 10000
    assert swap.get_virtual_price() == 1e18
    expected = [292589, 6376623, 763121, 261262965, 95299]
    # set LP token balance for meta pool
    meta_swap._set_balances(
        [0, 6e19, 0, 0], {"from": alice})
    actual = calculatorMeta.get_dy.call(
        4,
        (2000000000, 1873465287, 1921830293, 2204704420, 0, 0, 0, 0),
        100,
        4000000,
        (1000000000000000000, 1000000000000000000,
         1000000000000000000, 1000000000000000000, 0, 0, 0, 0),
        (10000000000, 10000000000, 10000000000, 10000000000, 0, 0, 0, 0),
        0,
        2,
        [383785, 8364882, 1000982, 343892002, 125002] + [0] * 95,
    )
    assert actual[:5] == expected


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
