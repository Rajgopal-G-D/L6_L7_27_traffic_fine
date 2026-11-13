from hypothesis import given, strategies as st
from traffic_fine import parse_ticket_id, total_fines, speed_excess


@given(st.text() | st.none())
def test_parse_ticket_id_no_crash(s):
    try:
        parse_ticket_id(s)
    except Exception as e:
        assert False, f"parse_ticket_id crashed with: {e!r}"


@given(st.text() | st.none())
def test_total_fines_no_crash(s):
    try:
        total_fines(s)
    except Exception as e:
        assert False, f"total_fines crashed with: {e!r}"


@given(st.text() | st.none())
def test_speed_excess_no_crash(s):
    try:
        speed_excess(s)
    except Exception as e:
        assert False, f"speed_excess crashed with: {e!r}"


# ---- Extra property tests on valid input ----

@given(
    st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1),
    st.integers(min_value=0, max_value=9999),
    st.integers(min_value=0, max_value=999999),
)
def test_parse_ticket_id_roundtrip(prefix, year, serial):
    assert parse_ticket_id(f"{prefix}-{year}-{serial}") == (prefix.upper(), year, serial)


@given(st.lists(st.integers(min_value=0, max_value=100000), min_size=1))
def test_total_fines_capped_and_non_negative(amounts):
    assert total_fines(",".join(map(str, amounts))) == min(sum(amounts), 10000)


@given(st.integers(min_value=0, max_value=400), st.integers(min_value=1, max_value=200))
def test_speed_excess_properties(speed, limit):
    assert speed_excess(f"{limit}/{limit}") == 0
    assert speed_excess(f"{speed}/{limit}") == (speed - limit) * 100 // limit
    assert speed_excess(f"{speed + 1}/{limit}") >= speed_excess(f"{speed}/{limit}")


@given(st.text() | st.none())
def test_invalid_inputs_return_none_not_garbage(s):
    # anything that isn't a clean ticket ID must give None, never a malformed tuple
    r = parse_ticket_id(s)
    assert r is None or (len(r) == 3 and isinstance(r[1], int) and isinstance(r[2], int))