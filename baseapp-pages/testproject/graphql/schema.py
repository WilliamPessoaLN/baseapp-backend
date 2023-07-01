import graphene

from baseapp_pages.graphql.mutations import PagesMutations
from baseapp_pages.graphql.queries import PagesQuery


class Query(
    graphene.ObjectType,
    PagesQuery,
):
    pass


class Mutation(
    graphene.ObjectType,
    PagesMutations,
):
    pass


schema = graphene.Schema(query=Query)
