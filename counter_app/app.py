from flask import Flask
import os
import functools


def create_app():
    app = Flask(__name__)

    with app.app_context():
        from .views import count_bp

        app.register_blueprint(count_bp)

        return app


def get_app_context():
    """
    Function either gets the current flask app or creates a new one.
    :return: (Flask)  A flask application instance
    """
    from flask import current_app

    if current_app:
        return current_app
    else:
        return create_app()


def with_app_context(fn):
    """
    Decorator to wrap a given function in a flask application context.
    """

    # intended for use with zappa event handler functions, making them more analagous to views

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        app = get_app_context()

        with app.app_context():
            return fn(*args, **kwargs)

    return wrapper