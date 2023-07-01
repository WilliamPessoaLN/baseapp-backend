import graphene
import swapper
from baseapp_core.graphql import DjangoObjectType
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language_from_request
from graphene import relay

from baseapp_pages.models import Metadata, URLPath

Page = swapper.load_model("baseapp_pages", "Page")


# class MetadataInterface(graphene.Interface):
#     meta_title = graphene.String()
#     meta_description = graphene.String(required=False)
#     meta_canonical = graphene.String(required=False)
#     meta_robots = graphene.String(required=False)
#     meta_og_type = graphene.String(required=False)
#     meta_og_image = graphene.String(required=False)


class PageInterface(relay.Node):
    url_path = graphene.Field(lambda: URLPathNode)
    url_paths = graphene.List(lambda: URLPathNode)
    metadata = graphene.Field(lambda: MetadataNode)

    # meta_title = graphene.String()
    # meta_description = graphene.String(required=False)
    # meta_canonical = graphene.String(required=False)
    # meta_robots = graphene.String(required=False)
    # meta_og_type = graphene.String(required=False)
    # meta_og_image = graphene.String(required=False)

    # # TO DO: URL alternates for SEO:
    # # https://developers.google.com/search/docs/specialty/international/localized-versions

    @classmethod
    def resolve_url_path(cls, instance, info, **kwargs):
        return URLPath.objects.filter(
            target_content_type=ContentType.objects.get_for_model(instance),
            target_object_id=instance.id,
            language=get_language_from_request(info.context),
            is_active=True,
        ).first()

    @classmethod
    def resolve_url_paths(cls, instance, info, **kwargs):
        return URLPath.objects.filter(
            target_content_type=ContentType.objects.get_for_model(instance),
            target_object_id=instance.id,
            language=get_language_from_request(info.context),
            is_active=True,
        )

    @classmethod
    def resolve_metadata(cls, instance, info, **kwargs):
        raise NotImplementedError

    # @classmethod
    # def resolve_meta_description(cls, instance, info, **kwargs):
    #     raise NotImplementedError

    # @classmethod
    # def resolve_meta_canonical(cls, instance, info, **kwargs):
    #     # TO DO: implement here in the interface

    #     # return active url path in this language the user is visiting from
    #     # we can use this to make 301 redirects?
    #     raise NotImplementedError

    # @classmethod
    # def resolve_meta_robots(cls, instance, info, **kwargs):
    #     raise NotImplementedError

    # @classmethod
    # def resolve_meta_og_type(cls, instance, info, **kwargs):
    #     raise NotImplementedError

    # @classmethod
    # def resolve_meta_og_image(cls, instance, info, **kwargs):
    #     raise NotImplementedError


class URLPathNode(DjangoObjectType):
    target = graphene.Field(PageInterface)

    class Meta:
        interfaces = (relay.Node,)
        model = URLPath
        fields = (
            "id",
            "path",
            "language",
            "is_active",
            "created",
            "modified",
            "target",
        )
        filter_fields = {
            "id": ["exact"],
        }


class PageNode(DjangoObjectType):
    metadata = graphene.Field(lambda: MetadataNode)

    class Meta:
        interfaces = (relay.Node, PageInterface)
        model = Page
        fields = "__all__"

    @classmethod
    def resolve_metadata(cls, instance, info, **kwargs):
        target_content_type = ContentType.objects.get_for_model(instance)
        metadata = Metadata.objects.filter(
            target_content_type=target_content_type,
            target_object_id=instance.id,
            language=get_language_from_request(info.context),
        ).first()
        if metadata:
            return metadata
        return MetadataNode(
            meta_title=instance.title,
        )


class MetadataNode(DjangoObjectType):
    class Meta:
        interfaces = []
        model = Metadata
        exclude = ("id",)
