import graphene
from baseapp_core.graphql import Node
from django.utils.translation import activate, get_language_from_request

from ..models import URLPath
from .object_types import PageNode, URLPathNode


class PagesQuery:
    url_path = graphene.Field(URLPathNode, path=graphene.String(required=True))
    page = Node.Field(PageNode)

    def resolve_url_path(self, info, path):
        language = get_language_from_request(info.context)
        activate(language)

        try:
            url_path = URLPath.objects.get(path=path, language=language)
        except URLPath.DoesNotExist:
            return None

        if not url_path.is_active:
            active_url_path = URLPath.objects.filter(
                target_content_type_id=url_path.target_content_type_id,
                target_object_id=url_path.target_object_id,
                language=language,
                is_active=True,
            ).first()
            if active_url_path:
                url_path = active_url_path

        return url_path
