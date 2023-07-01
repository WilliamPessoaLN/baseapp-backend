import pytest

from .factories import PageFactory, URLPathFactory

pytestmark = pytest.mark.django_db


def test_fallback_meta_title(django_user_client, graphql_user_client):
    page = PageFactory(user=django_user_client.user, title="Test page")
    URLPathFactory(target=page, language="en", path="/test-page/", is_active=True)

    response = graphql_user_client(
        """query { urlPath(path: \"/test-page/\") {
        target {
            id
            metadata {
                metaTitle
            }
        }
    } }"""
    )

    content = response.json()
    assert content["data"]["urlPath"]["target"]["id"] == page.relay_id
    assert content["data"]["urlPath"]["target"]["metadata"]["metaTitle"] == page.title


def test_active_url_path(django_user_client, graphql_user_client):
    page = PageFactory(user=django_user_client.user, title="Test page")
    URLPathFactory(target=page, language="en", path="/deactivated/", is_active=False)
    URLPathFactory(target=page, language="en", path="/activated/", is_active=True)

    response = graphql_user_client(
        """query { urlPath(path: \"/deactivated/\") {
        path
    } }"""
    )

    content = response.json()
    assert content["data"]["urlPath"]["path"] == "/activated/"
