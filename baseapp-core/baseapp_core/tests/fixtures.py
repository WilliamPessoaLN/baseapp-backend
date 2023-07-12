import json
from io import BytesIO

from django.core.files.images import ImageFile
from django.test import AsyncClient as DjangoAsyncClient, Client as DjClient

import httpretty
import pytest
from asgiref.sync import sync_to_async
from rest_framework.test import APIClient

import tests.factories as f

from ..graphql.testing import graphql_query


class Client(APIClient):
    def force_authenticate(self, user):
        self.user = user
        super().force_authenticate(user)


class DjangoClient(DjClient):
    def force_login(self, user, backend=None):
        self.user = user
        super().force_login(user, backend=backend)


class AsyncClient(DjangoAsyncClient):
    def force_authenticate(self, user):
        self.user = user


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def django_client():
    return DjangoClient()


@pytest.fixture
def outbox(mailoutbox):
    return mailoutbox


@pytest.fixture
def user_client():
    user = f.UserFactory()
    client = Client()
    client.force_authenticate(user)
    return client


@pytest.fixture
def django_user_client():
    user = f.UserFactory()
    client = DjangoClient()
    client.force_login(user)
    return client


@pytest.fixture
async def async_user_client():
    user = await sync_to_async(f.UserFactory)()
    token = await sync_to_async(f.TokenFactory)(user=user)
    client = AsyncClient()
    client.force_authenticate(user)
    client.token = token
    yield client
    await sync_to_async(token.delete)()
    await sync_to_async(user.delete)()


@pytest.fixture()
def use_httpretty():
    httpretty.enable()
    httpretty.HTTPretty.allow_net_connect = False
    yield
    httpretty.disable()
    httpretty.reset()


@pytest.fixture
def image_base64():
    return "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAMAAAAM7l6QAAAARVBMVEXPACr///8HAAIVAARnND5oABVzABcnCA6mACJHAA62ACXhztGcbXfi0dVzP0qZAB86EhqLWWPNsLZUABEjAAcaBAhbKjRAQ1vHAAAA+0lEQVQokYWTCZKEIAxFw2cTV9z6/kftsMjoiG2qVPQlAZMfEod1vfI7sHvVd+Uj5ecyWhSz43LFM0Pp9NS2k3aSHeYTHhSw6YayNZod1HDg4QO4AqPDCnyGjDnW0D/jBCrhuUKZA3PAi8V6p0Qr7MJ4hGxquNkwCuosdI2G9Laj/iGYwyV6UnC8FFeSXh0U+Zi7ig087Zgoli7eiY4m8GqCJKDN7ukSf9EtcMZHjjOOyUt03jktQ3KfKpr3FuUA+Wjpx6oWfuylLC9F5ZZsP1ry1tAHOZgshyAmeeOmiClKcX2W4l3I21nIZQxMGANzG4PXIcojyHHyMoJf+KcJUmsQs8MAAAAASUVORK5CYII="


@pytest.fixture
def image_djangofile(image_base64):
    i = BytesIO(image_base64.encode("utf-8"))
    return ImageFile(i, name="image.png")


@pytest.fixture
def deep_link_mock_success(use_httpretty):
    httpretty.register_uri(
        httpretty.POST,
        "https://api.branch.io/v1/url",
        body=json.dumps({"url": "https://example.com/128z8x81"}),
    )


@pytest.fixture
def deep_link_mock_error(use_httpretty):
    httpretty.register_uri(httpretty.POST, "https://api.branch.io/v1/url", status=400)


@pytest.fixture
def graphql_client(django_client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=django_client)

    return func


@pytest.fixture
def graphql_user_client(django_user_client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=django_user_client)

    return func
