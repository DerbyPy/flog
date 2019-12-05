from unittest import mock

import pytest

from flog.model import entities as ents


class TestViews:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        ents.Post.query.delete()

    def test_hello(self, client):
        resp = client.get('/hello')
        assert resp.data == b'Hello DerbyPy!'

    def test_posts(self, mixer, client):
        mixer.blend(ents.Post, title='Foo Bar')
        resp = client.get('/posts')
        assert resp.data == b'Foo Bar'

    def test_hn_form(self, client):
        resp = client.get('/hn')
        assert resp.status_code == 200
        assert b'Please enter your HackerNews username:' in resp.data

    @mock.patch('flog.libs.hackernews.User.get_json', autospec=True, spec_set=True)
    def test_hn_post(self, m_get_json, client):
        m_get_json.return_value = {'karma': 123, 'submitted': [1, 2, 3]}

        resp = client.post('/hn', data={'username': 'rsyring'})
        assert resp.status_code == 200
        assert b'HackerNews user rsyring has 3 submissions and 123 karma.' in resp.data
