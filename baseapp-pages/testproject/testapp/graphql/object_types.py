from baseapp_core.graphql import DjangoObjectType
from graphene import relay

from ..models import User


class UserNode(DjangoObjectType):
    class Meta:
        interfaces = (relay.Node,)
        model = User
        fields = ("id",)
