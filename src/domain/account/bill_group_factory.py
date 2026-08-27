from uuid import UUID
from typing import TYPE_CHECKING

from .bill_group import BillGroup


if TYPE_CHECKING:
    from ..expense import Bill


class BillGroupFactory:
    """Factory for creating BillGroup account instances."""

    @staticmethod
    def create(
        id: UUID,
        owner_id: UUID,
        alias: str,
        is_enabled: bool = True,
        expenses: list['Bill'] | None = None,
        **kwargs,  # Ignore extra fields for flexibility
    ) -> BillGroup:
        """
        Create a new BillGroup instance.

        Args:
            id: Unique identifier for the bill group
            owner_id: User who owns this bill group
            alias: Display name (e.g., "Casa y Auto", "Trabajo", "Salud")
            is_enabled: Whether the bill group is active (default: True)
            expenses: List of Bill expenses in this group

        Returns:
            A new BillGroup instance
        """
        return BillGroup(
            id=id,
            owner_id=owner_id,
            alias=alias,
            is_enabled=is_enabled,
            expenses=expenses or [],
        )
