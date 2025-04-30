from fastapi import APIRouter, Depends, Path

from app.dependencies.auth_dependencies import has_permission
from app.controllers.user_controller import UserController
from app.core.enums.role_enum import ALL_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.user_schemas_v1 import UserResV1
from app.schemas.auth_schemas import DecodedJWT


router = APIRouter(prefix='/users')
router.responses = {
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
    500: se.InternalServerError.dict(),
}
controller = UserController()


@router.get(
    '/{user_id}',
    responses={
        200: {'description': 'User info obtained'},
        404: {'description': 'User not found'},
    }
)
async def get_by_id(
    user_id: int = Path(ge=1),
    token: DecodedJWT = Depends(has_permission(ALL_ROLES))
) -> UserResV1:
    return controller.get_info(token, user_id)
