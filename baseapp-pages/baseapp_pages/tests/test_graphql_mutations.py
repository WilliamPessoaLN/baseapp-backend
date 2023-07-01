import pytest

# from .factories import PageFactory

pytestmark = pytest.mark.django_db


# def test_user_can_notifications_mark_all_as_read(django_user_client, graphql_user_client):
#     NotificationFactory(recipient=django_user_client.user)
#     notification = NotificationFactory(recipient=django_user_client.user)
#     assert notification.unread is True

#     response = graphql_user_client(
#         "mutation { notificationsMarkAllAsRead(input: { read: true }) { recipient { notificationsUnreadCount } } }",
#     )

#     content = response.json()
#     assert (
#         content["data"]["notificationsMarkAllAsRead"]["recipient"]["notificationsUnreadCount"] == 0
#     )

#     notification.refresh_from_db()
#     assert notification.unread is False
