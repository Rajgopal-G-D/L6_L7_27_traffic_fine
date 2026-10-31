import pytest
from traffic_fine import speeding_fine, license_action, total_penalty

#Example test cases:
def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0


@pytest.mark.parametrize(
    ("speed", "limit", "zone", "expected"),
    [
        (141, 100, "school", 6000),
        (121, 100, "highway", 2000),
        (120, 100, "city", 500),
        (110, 100, "city", 500),
    ],
)
def test_speeding_fine_by_zone_and_excess(speed, limit, zone, expected):
    assert speeding_fine(speed, limit, zone) == expected


def test_clean_record():
    assert license_action(2, False, False) == "none"


@pytest.mark.parametrize(
    ("points", "is_commercial", "repeat_offender", "expected"),
    [
        (12, True, False, "revoke"),
        (12, False, False, "suspend"),
        (8, False, True, "suspend"),
        (8, False, False, "warning"),
        (4, False, False, "notice"),
    ],
)
def test_license_action_by_points_and_record(
    points, is_commercial, repeat_offender, expected
):
    assert license_action(points, is_commercial, repeat_offender) == expected


def test_total_penalty_below_cap():
    assert total_penalty([100, 250, 50]) == 400


def test_total_penalty_empty_list():
    assert total_penalty([]) == 0


def test_total_penalty_is_capped():
    assert total_penalty([7000, 4000]) == 10000


def test_total_penalty_rejects_negative_fines():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([100, -1])
