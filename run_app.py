from application.app_factory import create_app
import application.config as config

# Create app from environment variable setting. How do we best do this?

app = create_app(config.testing())


def main(app):
    app.run()


if __name__ == "__main__":
    main(app)
