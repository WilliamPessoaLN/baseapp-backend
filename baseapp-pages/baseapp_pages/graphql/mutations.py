import graphene
import swapper
from baseapp_core.graphql import RelayMutation, login_required
from baseapp_core.graphql.utils import get_pk_from_relay_id
from graphql_relay.node.node import from_global_id

Page = swapper.load_model("baseapp_pages", "Page")


class PageCreate(RelayMutation):
    class Input:
        url = graphene.String(required=True)
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        # published_at = DateTimeField(required=True)
        tags = graphene.String()

    page = graphene.Field(Page)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        page = Page._meta.model()
        # page = page_save(page, input, info.context)
        return PageCreate(page=page)


class PageEdit(RelayMutation):
    class Input:
        id = graphene.ID(required=True)
        url = graphene.String(required=True)
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        # published_at = DateTimeField(required=True)
        tags = graphene.String()

    page = graphene.Field(Page)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        gid_type, gid = from_global_id(input.get("id"))
        page = Page._meta.model.objects.get(document_id=gid)

        # error = has_permission(cls, info.context, page, "edit")
        # if error:
        #     return error

        # page = page_save(page, input, info.context)
        return PageEdit(page=page)


class PageDelete(RelayMutation):
    class Input:
        id = graphene.ID(required=True)

    pageDeletedID = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        relay_id = input.get("id")
        pk = get_pk_from_relay_id(relay_id)
        page = Page._meta.model.objects.get(pk=pk)

        # error = has_permission(cls, info.context, page, 'delete')
        # if error:
        #     return error

        page.delete()

        return PageDelete(pageDeletedID=relay_id)


class PagesMutations(object):
    page_create = PageCreate.Field()
    page_edit = PageEdit.Field()
    page_delete = PageDelete.Field()
