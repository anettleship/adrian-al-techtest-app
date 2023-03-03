from flask import Flask


from application.app_factory import create_app
import application.config as config

app = create_app(config.testing())


def main(app):
    app.run()


if __name__ == "__main__":
    main(app)
