from os.path import isfile

import sentry_sdk
from envparse import env

if isfile('.env'):
    env.read_envfile('.env')

SENTRY_DSN = env.str('SENTRY_DSN', default='')
RELEASE = env.str('RELEASE', default='local')
if SENTRY_DSN:
    sentry_sdk.init(SENTRY_DSN, release=RELEASE)

DB_DSN = env.str('DB_DSN')
DEV = env.bool('DEV', default=True)
__dev = 'dev.' if DEV else ''
TELEPHONY_URL = f'https://telephony.{__dev}moydomonline.ru/api/v1/telehony/freeswitch/call_events/'

MQ_DSN = env.str('MQ_DSN')
MQ_EVENTS_QUEUE_NAME = env.str('MQ_EVENTS_QUEUE_NAME')
MQ_CONVERTER_QUEUE_NAME = env.str('MQ_CONVERTER_QUEUE_NAME')
MQ_UPLOADS_QUEUE_NAME = env.str('MQ_UPLOADS_QUEUE_NAME')

S3_FOLDER_NAME = env.str('S3_FOLDER_NAME', default='audios')
S3_BUCKET_NAME = env.str('S3_BUCKET_NAME', default='mdo-appeals')

DATA_PATH = env.str('DATA_PATH', default='/data')

LOG_LEVEL = env.str('LOG_LEVEL', default='WARNING').upper()

PASSWORD = env.str('PASSWORD', default='ClueCon')
IP = env.str('IP', default='127.0.0.1')
PORT = env.int('PORT', default=8021)
