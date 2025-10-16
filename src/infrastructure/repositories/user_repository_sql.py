import logging

from .base_repository_sql import BaseRepositorySQL
from src.infrastructure.database.models import UserModel, ProfileModel, PreferencesModel
from src.domain.auth import User as UserEntity, UserFactory

logger = logging.getLogger(__name__)


class UserRepositorySQL(BaseRepositorySQL[UserModel, UserEntity]):

    def update(self, entity: UserEntity) -> UserEntity:
        try:
            with self.session_factory() as session:
                existing_resource: UserModel | None = session.get(self.model, entity.id)
                if not existing_resource:
                    raise ValueError(f'User with id {entity.id} does not exist.')

                # Update fields
                existing_resource.username = entity.username
                existing_resource.email = entity.email
                existing_resource.password_hash = entity.encrypted_password
                existing_resource.role = entity.role.value

                # Update profile if exists
                if entity.profile:
                    if existing_resource.profile:
                        existing_resource.profile.first_name = entity.profile.first_name
                        existing_resource.profile.last_name = entity.profile.last_name
                        existing_resource.profile.birthdate = entity.profile.birthdate

                        # Update preferences if exists
                        if entity.profile.preferences and existing_resource.profile.preferences:
                            existing_resource.profile.preferences.monthly_spending_limit = entity.profile.preferences.monthly_spending_limit
                    else:
                        # Create new profile if it doesn't exist
                        preferences = PreferencesModel(
                            id=entity.profile.preferences.id,
                            monthly_spending_limit=entity.profile.preferences.monthly_spending_limit,
                            profile_id=entity.profile.id,
                        )
                        profile = ProfileModel(
                            id=entity.profile.id,
                            first_name=entity.profile.first_name,
                            last_name=entity.profile.last_name,
                            birthdate=entity.profile.birthdate,
                            user_id=entity.id,
                            preferences=preferences
                        )
                        existing_resource.profile = profile

                session.commit()
                session.refresh(existing_resource)
                return self._parse_model_to_entity(existing_resource)
        except Exception as ex:
            logger.critical(f'{self.model} - update - {ex.args} - Updated resource: {entity.to_dict()}')
            raise ex

    def _get_filter_params(self, params: dict = {}) -> dict:
        allowed_filters = ['email', 'username']
        return {k: v for k, v in params.items() if k in allowed_filters}

    def _parse_model_to_entity(self, data: UserModel) -> UserEntity:
        user = UserFactory.create(
            id=data.id,
            username=data.username,
            email=data.email,
            encrypted_password=data.password_hash,
            role=data.role,
            profile=data.profile.to_dict(include_relationships=True) if data.profile else None,
        )
        return user

    def _parse_entity_to_model(self, entity: UserEntity) -> UserModel:
        preferences = PreferencesModel(
            id=entity.profile.preferences.id,
            monthly_spending_limit=entity.profile.preferences.monthly_spending_limit,
            profile_id=entity.profile.id,
        )
        profile = ProfileModel(
            id=entity.profile.id,
            first_name=entity.profile.first_name,
            last_name=entity.profile.last_name,
            birthdate=entity.profile.birthdate,
            user_id=entity.id,
            preferences=preferences
        )

        return UserModel(
            id=entity.id,
            email=entity.email,
            username=entity.username,
            password_hash=entity.encrypted_password,
            role=entity.role.value,
            profile=profile
        )
