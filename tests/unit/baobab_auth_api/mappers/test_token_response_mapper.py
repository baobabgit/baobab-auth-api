"""Tests unitaires des mappers HTTP.

:spec: BL-API-010-003
"""

from baobab_auth_core.application.results.authenticated_user import AuthenticatedUser
from baobab_auth_core.application.results.register_user_result import RegisterUserResult
from baobab_auth_core.application.results.token_pair import TokenPair
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId

from baobab_auth_api.mappers.me_response_mapper import MeResponseMapper
from baobab_auth_api.mappers.register_response_mapper import RegisterResponseMapper
from baobab_auth_api.mappers.token_response_mapper import TokenResponseMapper


class TestTokenResponseMapper:
    def test_FEAT_001_2_token_type_lowercase(self) -> None:
        tokens = TokenPair(
            access_token="a",
            refresh_token="r",
            token_type="Bearer",
            expires_in=900,
            refresh_expires_in=1200,
        )
        response = TokenResponseMapper.to_response(tokens)
        assert response.token_type == "bearer"


class TestRegisterResponseMapper:
    def test_FEAT_001_2_register_mapping(self) -> None:
        user = AuthenticatedUser(
            id=UserId("u1"),
            auth_subject=AuthSubject("sub1"),
            email=Email("a@b.com"),
            status=UserStatus.ACTIVE,
            role_names=(RoleName("USER"),),
        )
        result = RegisterUserResult(user=user)
        response = RegisterResponseMapper.to_response(result)
        assert response.id == "u1"
        assert response.auth_subject == "sub1"


class TestMeResponseMapper:
    def test_FEAT_001_2_me_mapping(self) -> None:
        user = AuthenticatedUser(
            id=UserId("u1"),
            auth_subject=AuthSubject("sub1"),
            email=Email("a@b.com"),
            status=UserStatus.ACTIVE,
            role_names=(RoleName("USER"),),
            permissions=(),
        )
        response = MeResponseMapper.to_response(user)
        assert response.roles == ["USER"]
