from flask import Flask

def login_flask_setup(app: Flask):
    with app.app_context():
        app.config['SECRET_KEY'] = 'abdc1234'

        # Configured flask mail settings
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 587  # Gmail SMTP port
        app.config['MAIL_USE_TLS'] = True  # Uses TLS for secure connection
        app.config['MAIL_USERNAME'] = 'varundivi@gmail.com'
        app.config['MAIL_PASSWORD'] = 'hunamytiijfqsmoy'
        app.config['MAIL_DEFAULT_SENDER'] = 'varundivi@gmail.com'  # Your Gmail email address