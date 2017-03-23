
config = {
    'app_name': 'Olli Auth',

    # contact page email settings
    'contact_sender': 'SENDER_EMAIL_HERE',
    'contact_recipient': 'RECIPIENT_EMAIL_HERE',

    # JWT Secret
    'jwt_secret': '_PUT_KEY_HERE_YOUR_SECRET_KEY_',
    'jwt_algorithms': 'HS256',
    'jwt_expire': 157784760, # in seconds (5 years)

    # webapp2 sessions
    'webapp2_extras.sessions': {'secret_key': '_PUT_KEY_HERE_YOUR_SECRET_KEY_'},

    # salt password
    'salt': '3A7UynE902'
}
