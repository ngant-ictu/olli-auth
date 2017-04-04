pip install -r requirements.txt -t libs/external

dev_appserver.py --enable_sendmail=yes app.yaml annotation.yaml

export GOOGLE_APPLICATION_CREDENTIALS=/olli-auth/gservice.json
