from functools import wraps
from flask import session, redirect

def protected(signed_in=True, goto="/"):

    def wrapper_protected(func):

        @wraps(func)
        def wrapper_wrapper_protected(*args, **kwargs):
            if bool(not signed_in) ^ bool("username" in session):
                return redirect(goto)
            return func(*args, **kwargs)

        return wrapper_wrapper_protected

    return wrapper_protected