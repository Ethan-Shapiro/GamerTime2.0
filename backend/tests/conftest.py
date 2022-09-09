# import os

# import pytest
# from .application import create_app


# class AuthActions(object):
#     def __init__(self, client):
#         self._client = client

#     def login(self, username='test', password='test'):
#         return self._client.post(
#             '/auth/login',
#             data={'username': username, 'password': password}
#         )

#     def logout(self):
#         return self._client.get('/auth/logout')


# @pytest.fixture
# def auth(client):
#     return AuthActions(client)


# @pytest.fixture
# def client(app):
#     return app.test_client()


# @pytest.fixture
# def runner(app):
#     return app.test_cli_runner()
