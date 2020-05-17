from flask import request,redirect,url_for,session

def login_required(func):
    def inner():
        if request.cookies.get("user") not in session:
            return redirect(url_for("login"))

        func()
    return inner

def validate_user(user,pwd):
    if(user=="liwe" and pwd=="123"):
        return True
    else:
        return False