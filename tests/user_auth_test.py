"This tests the Login, Logout and Registration"
import pytest
from flask import session
from flask import g
from app.db import db

#from app.auth.forms import login_form, register_form, security_form
#from app.db.models import User

@pytest.mark.skip
def test_bad_password(client):
    response=client.post()

@pytest.mark.parametrize(
    ("username", "password", "confirm", "message"),
    (
        ("", "", "", b"Please fill out this field"),
        ("a", "", "", b"Please enter an email address"),
        ("a@a", "", "", b"Please fill out this field"),
        ("a@a", "234567", "", b"Passwords must match"),
        ("test@test", "123456", "123456", b"Already Registered"),
    ),
)
@pytest.mark.skip
def test_validate_registration(client, username, password,confirm, message):
    response = client.post(
        "/register", data={"username": username, "password": password, "confirm": confirm}
    )
    assert message in response.data


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (("a", "test", b"Incorrect username or password"), ("test", "a", b"Incorrect username or password")),
)
@pytest.mark.skip
def test_validate_login(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data
@pytest.mark.skip
def test_successful_login(client,auth):
    # test that viewing the page renders without template errors
    assert client.get("/login").status_code == 200

    #test that successful login redirects to the login page
    response = auth.login()
    assert "/dashboard" == response.headers["Location"]

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "test@test"
@pytest.mark.skip
def test_successful_registration(client,auth,application):

    # test that viewing the page renders without template errors
    assert client.get("/register").status_code == 200

    #test that successful registration redirects to the login page
    response = client.post("/register", data={"email": "abe@def", "password": "abcdef", "confirm": "abcdef"})
    assert "/login" == response.headers["Location"]

    # test that the user was inserted into the database
    with auth():
        assert (
            db().execute("SELECT * FROM user WHERE username = 'abc@def'").fetchone()
            is not None
        )



def test_dashboard_access_allowed(client):
    pass
def test_dashboard_access_denied(client):
    pass
