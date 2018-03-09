from app import create_app
import config

application = create_app(config)

if __name__ == '__main__':
    application.run(
        host='0.0.0.0',
        port=5000,
        # ssl_context=(config.SSL_CERT, config.SSL_KEY),
        use_reloader=True
    )
