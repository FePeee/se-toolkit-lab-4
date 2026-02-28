"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_excludes_interaction_with_different_learner_id() -> None:
    """Test that filtering by item_id returns interactions with matching item_id
    even when learner_id is different."""
    interactions = [_make_log(1, 2, 1)]  # id=1, learner_id=2, item_id=1
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].item_id == 1
    assert result[0].learner_id == 2


def test_filter_with_zero_item_id() -> None:
    """Test filtering with item_id=0 as a boundary value."""
    interactions = [
        _make_log(1, 1, 0),
        _make_log(2, 2, 1),
        _make_log(3, 3, 0),
    ]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 2
    assert all(i.item_id == 0 for i in result)
    assert result[0].id == 1
    assert result[1].id == 3


def test_filter_with_very_large_item_id() -> None:
    """Test filtering with a very large item_id value (boundary test)."""
    large_item_id = 2_147_483_647  # Max 32-bit signed integer
    interactions = [
        _make_log(1, 1, large_item_id),
        _make_log(2, 2, 100),
        _make_log(3, 3, large_item_id),
    ]
    result = _filter_by_item_id(interactions, large_item_id)
    assert len(result) == 2
    assert all(i.item_id == large_item_id for i in result)
    assert result[0].id == 1
    assert result[1].id == 3


def test_filter_returns_all_matching_when_multiple_same_item_id() -> None:
    """Test that all interactions with the same item_id are returned."""
    interactions = [
        _make_log(1, 1, 5),
        _make_log(2, 2, 5),
        _make_log(3, 3, 5),
        _make_log(4, 4, 10),
    ]
    result = _filter_by_item_id(interactions, 5)
    assert len(result) == 3
    assert all(i.item_id == 5 for i in result)
    assert set(i.id for i in result) == {1, 2, 3}


def test_filter_returns_empty_when_no_matching_item_id() -> None:
    """Test filtering returns empty list when no item_id matches."""
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 2),
        _make_log(3, 3, 3),
    ]
    result = _filter_by_item_id(interactions, 999)
    assert result == []


def test_filter_with_mixed_matching_and_non_matching_item_ids() -> None:
    """Test filtering correctly selects only matching item_ids from mixed list."""
    interactions = [
        _make_log(1, 1, 10),
        _make_log(2, 2, 20),
        _make_log(3, 3, 10),
        _make_log(4, 4, 30),
        _make_log(5, 5, 10),
    ]
    result = _filter_by_item_id(interactions, 10)
    assert len(result) == 3
    assert all(i.item_id == 10 for i in result)
    assert [i.id for i in result] == [1, 3, 5]
