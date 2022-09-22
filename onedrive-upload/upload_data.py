import argparse
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from mstoken import MsToken
from utils import create_logger

load_dotenv()

TOKEN_FILE = os.getenv('TOKEN_FILE')
folder_id = os.getenv('FOLDER_ID')
base_url = 'https://graph.microsoft.com/v1.0/me'


def create_parser():
    parser = argparse.ArgumentParser(description='Upload file to one drive')
    parser.add_argument('-s', '--source', dest='source', help='source file path', required=True)
    parser.add_argument('-d', '--dest', dest='dest', help='destination file name', required=True)
    return parser


if __name__ == "__main__":
    arg_parser = create_parser()
    args = arg_parser.parse_args()
    if not os.path.exists(args.source):
        arg_parser.error(f'File {arg_parser} does not exist')

    logger = create_logger('upload_data')
    token = MsToken(TOKEN_FILE)

    token_value = token.read()
    if token_value is None:
        logger.error('Empty token')
        exit(1)

    access_token = token_value['access_token']
    headers = {'Authorization': 'Bearer ' + access_token}
    request_body = {
        'item': {
            'description': f'Influx DB data backup at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            'name': args.dest
        }
    }

    url = f'{base_url}/drive/items/{folder_id}:/{args.dest}:/createUploadSession'
    logger.info('Making request to Onedrive...')
    logger.debug(f'Url: {url}, Request body: {request_body}')
    response = requests.post(
        url,
        headers=headers,
        json=request_body
    )

    logger.debug(f'Upload session: {response.json()}')
    logger.info('Uploading file to Onedrive...')
    try:
        upload_url = response.json()['uploadUrl']
        with open(args.source, 'rb') as fh:
            status = requests.put(upload_url, data=fh.read())
            logger.info(f'Status upload: {status.reason}')
    except Exception as err:
        logger.error(f'Failed to upload with error: {err}')
