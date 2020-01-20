import pytest


def test_basic_route(api):
    @api.route('/home')
    def home(req, resp):
        resp.text = 'testing 1 2 3'


def test_route_overlap(api):
    @api.route('/home')
    def home(req, resp):
        resp.text = 'testing 1 2 3'

    with pytest.raises(AssertionError):
        @api.route('/home')
        def home(req, resp):
            resp.text = 'no one will ever see this'


def test_client(api, client):
    RESPONSE_TEXT = "testing testing 123"

    @api.route("/test")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT

    assert client.get("http://testserver/test").text == RESPONSE_TEXT


def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://testserver/matthew").text == "hey matthew"
    assert client.get("http://testserver/ashley").text == "hey ashley"

def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")

    assert response.status_code == 404
    assert response.text == "Not found."
