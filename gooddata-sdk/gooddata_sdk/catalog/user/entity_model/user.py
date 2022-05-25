# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import List, Optional, Type

import attr

from gooddata_metadata_client.model.json_api_user_in import JsonApiUserIn
from gooddata_metadata_client.model.json_api_user_in_document import JsonApiUserInDocument
from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.user.entity_model.user_group import CatalogUserGroup


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserDocument(Base):
    data: CatalogUser

    @staticmethod
    def client_class() -> Type[JsonApiUserInDocument]:
        return JsonApiUserInDocument

    @classmethod
    def create_user(
        cls, user_id: str, authentication_id: Optional[str] = None, user_groups: Optional[List[str]] = None
    ) -> CatalogUserDocument:
        attributes = CatalogUserAttributes(authentication_id=authentication_id)
        relationships = None
        if user_groups is not None:
            relationships = CatalogUserRelationships(
                user_groups=CatalogUserGroupsData(data=[CatalogUserGroup(id=user_group) for user_group in user_groups])
            )
        user = CatalogUser(id=user_id, attributes=attributes, relationships=relationships)
        return cls(data=user)


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUser(Base):
    id: str
    attributes: Optional[CatalogUserAttributes] = None
    relationships: Optional[CatalogUserRelationships] = None

    @staticmethod
    def client_class() -> Type[JsonApiUserIn]:
        return JsonApiUserIn

    @property
    def get_user_groups(self) -> Optional[List[str]]:
        return self.relationships.get_user_groups if self.relationships is not None else None


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserAttributes(Base):
    authentication_id: Optional[str] = None


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserRelationships(Base):
    user_groups: Optional[CatalogUserGroupsData] = None

    @property
    def get_user_groups(self) -> Optional[List[str]]:
        return self.user_groups.get_user_groups if self.user_groups is not None else None


@attr.s(auto_attribs=True, kw_only=True)
class CatalogUserGroupsData(Base):
    data: List[CatalogUserGroup]

    @property
    def get_user_groups(self) -> Optional[List[str]]:
        return [user_group.id for user_group in self.data]
