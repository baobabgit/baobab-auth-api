"""Tests unitaires ReentrantUnitOfWork.

:spec: BL-API-010-004
"""

from baobab_auth_core.testing.in_memory_unit_of_work import InMemoryUnitOfWork

from baobab_auth_api.infrastructure.reentrant_unit_of_work import ReentrantUnitOfWork


class TestReentrantUnitOfWork:
    def test_BL_API_010_004_nested_enter_single_commit(self) -> None:
        inner = InMemoryUnitOfWork()
        outer = ReentrantUnitOfWork(inner)
        with outer:
            with outer:
                outer.commit()
        assert inner.committed is True
