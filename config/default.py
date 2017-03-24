
config = {
    'app_name': 'Olli Auth',

    # contact page email settings
    'mailgun_sender': 'Example Sender <mailgun@{}>',
    'mailgun_api_key': 'key-fbf5e71f13d5cba53cca4030cb5f8721',
    'mailgun_url': 'https://api.mailgun.net/v3/{}/messages',
    'mailgun_domain': 'sandbox1cb020983d1343209b87acea0e29dac8.mailgun.org',

    # JWT Secret
    'jwt_secret': '_PUT_KEY_HERE_YOUR_SECRET_KEY_',
    'jwt_algorithms': 'HS256',
    'jwt_expire': 157784760, # in seconds (5 years)

    # webapp2 sessions
    'webapp2_extras.sessions': {'secret_key': '_PUT_KEY_HERE_YOUR_SECRET_KEY_'},

    # salt password
    'salt': '3A7UynE902',

    # mailgun activate account expire time
    'account_activation_expire': 60 # in seconds
}
