from fastapi import APIRouter, Depends, Path

from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.credit_card_schemas_v3 import CreditCardRes, NewCreditCardReq, UpdateCreditCardReq
from app.schemas.paginated_schemas import PaginatedResponse
from app.dependencies.auth_dependencies import has_permission
from app.core.enums.role_enum import ALL_ROLES
from app.schemas.auth_schemas import DecodedJWT
from app.schemas.credit_card_schemas_v3 import CreditCardListParam
from app.controllers import CreditCardControllerV3


router = APIRouter(prefix='/credit_cards')
router.responses = {
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
    500: se.InternalServerError.dict(),
    501: se.NotImplemented.dict(),
}

credit_card_controller = CreditCardControllerV3()


@router.get(
    '',
    summary='Get a paginated list of credit cards',
    description='This endpoint returns a paginated list of all credit cards associated with the user. You can filter and sort using the query parameters.',
    response_description='A paginated list of credit cards with metadata like current page, total items, etc.',
    responses={
        400: {'description': 'Bad request, invalid query parameters or missing required parameters'},
        422: {'description': 'Unprocessable Entity, the request data does not meet validation requirements'},
    },
)
async def get_list(
    token: DecodedJWT = Depends(has_permission(ALL_ROLES)),
    params: CreditCardListParam = Depends()
) -> PaginatedResponse[CreditCardRes]:
    return await credit_card_controller.get_paginated(token, params)


@router.post(
    '',
    summary='Create a new credit card',
    description='This endpoint allows you to create a new credit card. You need to provide the necessary details in the request body.',
    response_description='Details of the newly created credit card.',
    responses={
        400: {'description': 'Bad request, invalid request data or missing required fields'},
        422: {'description': 'Unprocessable Entity, the request data does not meet validation requirements'},
    },
)
async def create(data: NewCreditCardReq) -> CreditCardRes:
    raise se.NotImplemented('This endpoint is not implemented yet', 'NOT_IMPLEMENTED')


@router.get(
    '/{credit_card_id}',
    summary='Get a credit card by ID',
    description='This endpoint returns the details of a specific credit card based on its ID.',
    response_description='Details of the credit card with the specified ID.',
    responses={
            404: {'description': 'Not Found, the credit card with the specified ID does not exist'},
            422: {'description': 'Unprocessable Entity, the request data does not meet validation requirements'},
    },
)
async def get_by_id(credit_card_id: int) -> CreditCardRes:
    raise se.NotImplemented('This endpoint is not implemented yet', 'NOT_IMPLEMENTED')


@router.patch(
    '/{credit_card_id}',
    summary='Update a credit card by ID',
    description='This endpoint allows you to update the details of a specific credit card based on its ID. You need to provide the updated details in the request body.',
    response_description='Details of the updated credit card.',
    responses={
        400: {'description': 'Bad request, invalid request data or missing required fields'},
        404: {'description': 'Not Found, the credit card with the specified ID does not exist'},
        422: {'description': 'Unprocessable Entity, the request data does not meet validation requirements'},
    },
)
async def update(credit_card_id: int, data: UpdateCreditCardReq) -> CreditCardRes:
    raise se.NotImplemented('This endpoint is not implemented yet', 'NOT_IMPLEMENTED')


@router.delete(
    '/{credit_card_id}',
    summary='Delete a credit card by ID',
    description='This endpoint allows you to delete a specific credit card based on its ID. Be cautious, as this action cannot be undone.',
    response_description='No content, the credit card has been successfully deleted.',
    status_code=204,
    responses={
        404: {'description': 'Not Found, the credit card with the specified ID does not exist'},
        422: {'description': 'Unprocessable Entity, the request data does not meet validation requirements'},
    },
)
async def delete(credit_card_id: int) -> None:
    raise se.NotImplemented('This endpoint is not implemented yet', 'NOT_IMPLEMENTED')
