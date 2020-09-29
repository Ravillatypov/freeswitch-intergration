from os.path import isfile

import sentry_sdk
from envparse import env

if isfile('.env'):
    env.read_envfile('.env')

ENVIRONMENT = env.str('ENVIRONMENT', default='local')

SENTRY_DSN = env.str('SENTRY_DSN', default='')
RELEASE = env.str('RELEASE', default='local')
if SENTRY_DSN:
    sentry_sdk.init(SENTRY_DSN, release=RELEASE)

DB_DSN = env.str('DB_DSN')

__dev = 'dev.' if ENVIRONMENT != 'prod' else ''
TELEPHONY_URL = f'https://telephony.{__dev}moydomonline.ru/api/v1/telephony/freeswitch/call_events/'

MQ_DSN = env.str('MQ_DSN')
MQ_EVENTS_QUEUE_NAME = env.str('MQ_EVENTS_QUEUE_NAME', default='fs_events')
MQ_CONVERTER_QUEUE_NAME = env.str('MQ_CONVERTER_QUEUE_NAME', default='convert_tasks')
MQ_UPLOADS_QUEUE_NAME = env.str('MQ_UPLOADS_QUEUE_NAME', default='upload_tasks')

S3_FOLDER_NAME = env.str('S3_FOLDER_NAME', default='audios')
S3_BUCKET_NAME = env.str('S3_BUCKET_NAME', default='mdo-appeals')

AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY', default='')
AWS_DEFAULT_REGION = env.str('AWS_DEFAULT_REGION', default='us-east-1')

DATA_PATH = env.str('DATA_PATH', default='/data')
RECORDS_PATH_PREFIX = env.str('RECORDS_PATH_PREFIX', default='/var/lib/freeswitch/recordings')

LOG_LEVEL = env.str('LOG_LEVEL', default='WARNING').upper()

EVENT_CAPTURE = env.bool('EVENT_CAPTURE', default=False)
