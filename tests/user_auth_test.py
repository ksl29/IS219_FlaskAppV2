"This tests the Login, Logout and Registration"
import pytest
from flask import session
from flask import g
from app.db import db


#==========================
#Password Confirmation
#==========================

def test_password_confirmation(client):
    response = client.post(
        "/register", data={"username": "a@a", "password": "234567" , "confirm": ""}
    )
    assert b"Passwords must match" in response.data


#==========================
#Successful Login
#==========================
def test_successful_login(client):
    # test that viewing the page renders without template errors
    assert client.get("/login").status_code == 200

    #test that successful login redirects to the login page
    response = client.post("/login", data={"email": "test@test", "password": "123456"})
    assert "/dashboard" == response.headers["Location"]


#==========================
#Successful Registration
#========================== 
def test_successful_registration(client):

    # test that viewing the page renders without template errors
    assert client.get("/register").status_code == 200

    #test that successful registration redirects to the login page
    response = client.post("/register", data={"email": "abe@def", "password": "abcdef", "confirm": "abcdef"})
    assert "/login" == response.headers["Location"]



#==========================
#Login Validation
#==========================
@pytest.mark.skip
def test_bad_login(client):
    response = client.post(
        "/login", data={"username": "a@a", "password": "234567" }
    )
    assert "/login" == response.headers["Location"]

#==========================
#Dashboard Allowed
#==========================
@pytest.mark.skip
def test_dashboard_access_allowed(client):

    # test that viewing the page renders without template errors
    assert client.get("/register").status_code == 200

    response = client.post("/login", data={"username": "test@test", "password": "123456" })
    response = client.get("/dashboard")
    
    assert response.headers["Location"] == "/dashboard"

#==========================
#Dashboard Denied
#==========================

def test_dashboard_access_denied(client):
    response = client.get("/dashboard")
    assert response.headers["Location"] != "/dashboard"
    



