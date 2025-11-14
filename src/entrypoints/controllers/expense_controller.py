"""
ExpenseController: Handles expense-related HTTP requests.

This controller acts as the entry point for expense operations including
categories, purchases, and subscriptions, delegating business logic to
the application layer use cases.
"""
import logging
from uuid import UUID

from src.application.dtos import (
    CreateExpenseCategoryDTO,
    UpdateExpenseCategoryDTO,
    ExpenseCategoryResponseDTO,
    CreatePurchaseDTO,
    UpdatePurchaseDTO,
    CreateSubscriptionDTO,
    UpdateSubscriptionDTO,
    ExpenseResponseDTO,
    PaginatedResponse,
    CreatePaymentDTO,
    UpdatePaymentDTO,
    PaymentResponseDTO,
)
from src.application.use_cases.expense import (
    ExpenseCategoryCreateUseCase,
    ExpenseCategoryGetPaginatedUseCase,
    ExpenseCategoryUpdateUseCase,
    ExpenseCategoryDeleteUseCase,
    ExpenseGetPaginatedUseCase,
    PurchaseCreateUseCase,
    PurchaseUpdateUseCase,
    PurchaseDeleteUseCase,
    PurchaseGetOneUseCase,
    SubscriptionCreateUseCase,
    SubscriptionUpdateUseCase,
    SubscriptionDeleteUseCase,
    SubscriptionGetOneUseCase,
    PaymentCreateUseCase,
    PaymentUpdateUseCase,
    PaymentDeleteUseCase,
)
from src.application.ports import ExpenseCategoryRepository, ExpenseRepository, PaymentRepository
from src.entrypoints.exceptions import client_exceptions as ce
from src.entrypoints.exceptions import server_exceptions as se


logger = logging.getLogger(__name__)


class ExpenseController:
    """
    Controller for expense operations.
    
    Handles CRUD operations for expense categories, purchases, and subscriptions
    by coordinating between the presentation layer and application use cases.
    """

    def __init__(
        self,
        expense_category_repository: ExpenseCategoryRepository,
        expense_repository: ExpenseRepository,
        payment_repository: PaymentRepository,
    ):
        """Initialize the controller with repository dependencies.

        Repository dependencies are mandatory and must be provided via DI.
        """
        self._expense_category_repository: ExpenseCategoryRepository = expense_category_repository
        self._expense_repository: ExpenseRepository = expense_repository
        self._payment_repository: PaymentRepository = payment_repository

    # Expense Category methods

    def create_expense_category(self, category_data: CreateExpenseCategoryDTO) -> ExpenseCategoryResponseDTO:
        """
        Create a new expense category.

        Args:
            category_data: CreateExpenseCategoryDTO containing category information

        Returns:
            ExpenseCategoryResponseDTO with created category information

        Raises:
            ValueError: If category data is invalid
        """
        try:
            logger.info(f'Creating expense category: {category_data.name}')
            use_case = ExpenseCategoryCreateUseCase(self._expense_category_repository)
            result = use_case.execute(category_data)
            logger.info(f'Expense category created successfully with ID: {result.id}')
            return result
        except ValueError as ex:
            logger.warning(f'Failed to create expense category: {ex}')
            raise ce.BadRequest(str(ex), 'CREATE_CATEGORY_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error creating expense category: {ex}')
            raise se.InternalServerError()

    def update_expense_category(self, category_id: UUID, category_data: UpdateExpenseCategoryDTO) -> ExpenseCategoryResponseDTO:
        """
        Update an existing expense category.

        Args:
            category_id: UUID of the category to update
            category_data: UpdateExpenseCategoryDTO containing updated information

        Returns:
            ExpenseCategoryResponseDTO with updated category information

        Raises:
            ValueError: If category is not found or data is invalid
        """
        try:
            logger.info(f'Updating expense category with ID: {category_id}')
            use_case = ExpenseCategoryUpdateUseCase(self._expense_category_repository)
            result = use_case.execute(category_id, category_data)
            logger.info(f'Expense category updated successfully: {category_id}')
            return result
        except ValueError as ex:
            logger.warning(f'Failed to update expense category {category_id}: {ex}')
            raise ce.BadRequest(str(ex), 'UPDATE_CATEGORY_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error updating expense category {category_id}: {ex}')
            raise se.InternalServerError()

    def delete_expense_category(self, category_id: UUID) -> None:
        """
        Delete an expense category.

        Args:
            category_id: UUID of the category to delete

        Raises:
            ValueError: If category is not found
        """
        try:
            logger.info(f'Deleting expense category with ID: {category_id}')
            use_case = ExpenseCategoryDeleteUseCase(self._expense_category_repository)
            use_case.execute(category_id)
            logger.info(f'Expense category deleted successfully: {category_id}')
        except ValueError as ex:
            logger.warning(f'Failed to delete expense category {category_id}: {ex}')
            raise ce.NotFound(str(ex), 'CATEGORY_NOT_FOUND')
        except Exception as ex:
            logger.error(f'Unexpected error deleting expense category {category_id}: {ex}')
            raise se.InternalServerError()

    def get_paginated_expense_categories(self, filter: dict, limit: int, offset: int) -> PaginatedResponse[ExpenseCategoryResponseDTO]:
        """
        Retrieve a paginated list of expense categories.

        Args:
            filter: Dictionary with filter criteria
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            PaginatedResponse containing expense categories and pagination metadata

        Raises:
            ValueError: If filter parameters are invalid
        """
        try:
            logger.info(f'Retrieving paginated expense categories with limit={limit}, offset={offset}')
            use_case = ExpenseCategoryGetPaginatedUseCase(self._expense_category_repository)
            result = use_case.execute(filter, limit, offset)
            logger.info(f'Retrieved {len(result.items)} expense categories')
            return result
        except ValueError as ex:
            logger.warning(f'Invalid pagination parameters: {ex}')
            raise ce.BadRequest(str(ex), 'PAGINATION_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error retrieving paginated expense categories: {ex}')
            raise se.InternalServerError()

    # Purchase methods

    def create_purchase(self, purchase_data: CreatePurchaseDTO) -> ExpenseResponseDTO:
        """
        Create a new purchase.

        Args:
            purchase_data: CreatePurchaseDTO containing purchase information

        Returns:
            ExpenseResponseDTO with created purchase information

        Raises:
            ValueError: If purchase data is invalid
        """
        try:
            logger.info(f'Creating purchase: {purchase_data.title}')
            use_case = PurchaseCreateUseCase(self._expense_repository)
            result = use_case.execute(purchase_data)
            logger.info(f'Purchase created successfully with ID: {result.id}')
            return result
        except ValueError as ex:
            logger.warning(f'Failed to create purchase: {ex}')
            raise ce.BadRequest(str(ex), 'CREATE_PURCHASE_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error creating purchase: {ex}')
            raise se.InternalServerError()

    def get_purchase(self, purchase_id: UUID) -> ExpenseResponseDTO:
        """
        Retrieve a purchase by its ID.

        Args:
            purchase_id: UUID of the purchase to retrieve

        Returns:
            ExpenseResponseDTO with purchase information

        Raises:
            ValueError: If purchase is not found
        """
        try:
            logger.info(f'Retrieving purchase with ID: {purchase_id}')
            use_case = PurchaseGetOneUseCase(self._expense_repository)
            result = use_case.execute(purchase_id)
            logger.info(f'Purchase retrieved successfully: {purchase_id}')
            return result
        except ValueError as ex:
            logger.warning(f'Purchase not found: {purchase_id}')
            raise ce.NotFound(str(ex), 'PURCHASE_NOT_FOUND')
        except Exception as ex:
            logger.error(f'Unexpected error retrieving purchase {purchase_id}: {ex}')
            raise se.InternalServerError()

    def update_purchase(self, purchase_id: UUID, purchase_data: UpdatePurchaseDTO) -> ExpenseResponseDTO:
        """
        Update an existing purchase.

        Args:
            purchase_id: UUID of the purchase to update
            purchase_data: UpdatePurchaseDTO containing updated information

        Returns:
            ExpenseResponseDTO with updated purchase information

        Raises:
            ValueError: If purchase is not found or data is invalid
        """
        try:
            logger.info(f'Updating purchase with ID: {purchase_id}')
            use_case = PurchaseUpdateUseCase(self._expense_repository)
            result = use_case.execute(purchase_id, purchase_data)
            logger.info(f'Purchase updated successfully: {purchase_id}')
            return result
        except ValueError as ex:
            logger.warning(f'Failed to update purchase {purchase_id}: {ex}')
            raise ce.BadRequest(str(ex), 'UPDATE_PURCHASE_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error updating purchase {purchase_id}: {ex}')
            raise se.InternalServerError()

    def delete_purchase(self, purchase_id: UUID) -> None:
        """
        Delete a purchase.

        Args:
            purchase_id: UUID of the purchase to delete

        Raises:
            ValueError: If purchase is not found
        """
        try:
            logger.info(f'Deleting purchase with ID: {purchase_id}')
            use_case = PurchaseDeleteUseCase(self._expense_repository)
            use_case.execute(purchase_id)
            logger.info(f'Purchase deleted successfully: {purchase_id}')
        except ValueError as ex:
            logger.warning(f'Failed to delete purchase {purchase_id}: {ex}')
            raise ce.NotFound(str(ex), 'PURCHASE_NOT_FOUND')
        except Exception as ex:
            logger.error(f'Unexpected error deleting purchase {purchase_id}: {ex}')
            raise se.InternalServerError()

    # Subscription methods

    def create_subscription(self, subscription_data: CreateSubscriptionDTO) -> ExpenseResponseDTO:
        """
        Create a new subscription.

        Args:
            subscription_data: CreateSubscriptionDTO containing subscription information

        Returns:
            ExpenseResponseDTO with created subscription information

        Raises:
            ValueError: If subscription data is invalid
        """
        try:
            logger.info(f'Creating subscription: {subscription_data.title}')
            use_case = SubscriptionCreateUseCase(self._expense_repository)
            result = use_case.execute(subscription_data)
            logger.info(f'Subscription created successfully with ID: {result.id}')
            return result
        except ValueError as ex:
            logger.warning(f'Failed to create subscription: {ex}')
            raise ce.BadRequest(str(ex), 'CREATE_SUBSCRIPTION_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error creating subscription: {ex}')
            raise se.InternalServerError()

    def get_subscription(self, subscription_id: UUID) -> ExpenseResponseDTO:
        """
        Retrieve a subscription by its ID.

        Args:
            subscription_id: UUID of the subscription to retrieve

        Returns:
            ExpenseResponseDTO with subscription information

        Raises:
            ValueError: If subscription is not found
        """
        try:
            logger.info(f'Retrieving subscription with ID: {subscription_id}')
            use_case = SubscriptionGetOneUseCase(self._expense_repository)
            result = use_case.execute(subscription_id)
            logger.info(f'Subscription retrieved successfully: {subscription_id}')
            return result
        except ValueError as ex:
            logger.warning(f'Subscription not found: {subscription_id}')
            raise ce.NotFound(str(ex), 'SUBSCRIPTION_NOT_FOUND')
        except Exception as ex:
            logger.error(f'Unexpected error retrieving subscription {subscription_id}: {ex}')
            raise se.InternalServerError()

    def update_subscription(self, subscription_id: UUID, subscription_data: UpdateSubscriptionDTO) -> ExpenseResponseDTO:
        """
        Update an existing subscription.

        Args:
            subscription_id: UUID of the subscription to update
            subscription_data: UpdateSubscriptionDTO containing updated information

        Returns:
            ExpenseResponseDTO with updated subscription information

        Raises:
            ValueError: If subscription is not found or data is invalid
        """
        try:
            logger.info(f'Updating subscription with ID: {subscription_id}')
            use_case = SubscriptionUpdateUseCase(self._expense_repository)
            result = use_case.execute(subscription_id, subscription_data)
            logger.info(f'Subscription updated successfully: {subscription_id}')
            return result
        except ValueError as ex:
            logger.warning(f'Failed to update subscription {subscription_id}: {ex}')
            raise ce.BadRequest(str(ex), 'UPDATE_SUBSCRIPTION_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error updating subscription {subscription_id}: {ex}')
            raise se.InternalServerError()

    def delete_subscription(self, subscription_id: UUID) -> None:
        """
        Delete a subscription.

        Args:
            subscription_id: UUID of the subscription to delete

        Raises:
            ValueError: If subscription is not found
        """
        try:
            logger.info(f'Deleting subscription with ID: {subscription_id}')
            use_case = SubscriptionDeleteUseCase(self._expense_repository)
            use_case.execute(subscription_id)
            logger.info(f'Subscription deleted successfully: {subscription_id}')
        except ValueError as ex:
            logger.warning(f'Failed to delete subscription {subscription_id}: {ex}')
            raise ce.NotFound(str(ex), 'SUBSCRIPTION_NOT_FOUND')
        except Exception as ex:
            logger.error(f'Unexpected error deleting subscription {subscription_id}: {ex}')
            raise se.InternalServerError()

    # General expense methods

    def get_paginated_expenses(self, filter: dict, limit: int, offset: int) -> PaginatedResponse[ExpenseResponseDTO]:
        """
        Retrieve a paginated list of expenses (purchases and subscriptions).

        Args:
            filter: Dictionary with filter criteria
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            PaginatedResponse containing expenses and pagination metadata

        Raises:
            ValueError: If filter parameters are invalid
        """
        try:
            logger.info(f'Retrieving paginated expenses with limit={limit}, offset={offset}')
            use_case = ExpenseGetPaginatedUseCase(self._expense_repository)
            result = use_case.execute(filter, limit, offset)
            logger.info(f'Retrieved {len(result.items)} expenses')
            return result
        except ValueError as ex:
            logger.warning(f'Invalid pagination parameters: {ex}')
            raise ce.BadRequest(str(ex), 'PAGINATION_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error retrieving paginated expenses: {ex}')
            raise se.InternalServerError()

    # Payment methods

    def create_payment(self, payment_data: CreatePaymentDTO) -> PaymentResponseDTO:
        """
        Create a new payment for a subscription.

        Args:
            payment_data: CreatePaymentDTO containing payment information

        Returns:
            PaymentResponseDTO with created payment information

        Raises:
            ValueError: If payment data is invalid
        """
        try:
            logger.info(f'Creating payment for expense: {payment_data.expense_id}')
            use_case = PaymentCreateUseCase(self._payment_repository, self._expense_repository)
            result = use_case.execute(payment_data)
            logger.info(f'Payment created successfully with ID: {result.id}')
            return result
        except ValueError as ex:
            logger.warning(f'Failed to create payment: {ex}')
            raise ce.BadRequest(str(ex), 'CREATE_PAYMENT_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error creating payment: {ex}')
            raise se.InternalServerError()

    def update_payment(self, payment_id: UUID, payment_data: UpdatePaymentDTO) -> PaymentResponseDTO:
        """
        Update an existing payment.

        Args:
            payment_id: UUID of the payment to update
            payment_data: UpdatePaymentDTO containing updated information

        Returns:
            PaymentResponseDTO with updated payment information

        Raises:
            ValueError: If payment is not found or data is invalid
        """
        try:
            logger.info(f'Updating payment with ID: {payment_id}')
            use_case = PaymentUpdateUseCase(self._payment_repository, self._expense_repository)
            result = use_case.execute(payment_id, payment_data)
            logger.info(f'Payment updated successfully: {payment_id}')
            return result
        except ValueError as ex:
            logger.warning(f'Failed to update payment {payment_id}: {ex}')
            raise ce.BadRequest(str(ex), 'UPDATE_PAYMENT_BAD_REQUEST')
        except Exception as ex:
            logger.error(f'Unexpected error updating payment {payment_id}: {ex}')
            raise se.InternalServerError()

    def delete_payment(self, payment_id: UUID) -> None:
        """
        Delete a payment.

        Args:
            payment_id: UUID of the payment to delete

        Raises:
            ValueError: If payment is not found
        """
        try:
            logger.info(f'Deleting payment with ID: {payment_id}')
            use_case = PaymentDeleteUseCase(self._payment_repository, self._expense_repository)
            use_case.execute(payment_id)
            logger.info(f'Payment deleted successfully: {payment_id}')
        except ValueError as ex:
            logger.warning(f'Failed to delete payment {payment_id}: {ex}')
            raise ce.NotFound(str(ex), 'PAYMENT_NOT_FOUND')
        except Exception as ex:
            logger.error(f'Unexpected error deleting payment {payment_id}: {ex}')
            raise se.InternalServerError()
