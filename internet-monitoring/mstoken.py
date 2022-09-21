import json
import os
from datetime import datetime
from dotenv import load_dotenv
from msal import PublicClientApplication
from utils import create_logger, safe_call

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')


class MsToken:
    def __init__(self, token_file):
        self.logger = create_logger('refresh_token')
        self._token_file = token_file

    @safe_call(lambda x: x.logger)
    def read(self):
        if not os.path.exists(self._token_file) or os.path.getsize(self._token_file) == 0:
            self.logger.warning(f'No token file: "{self._token_file}" or empty.')
            return None

        self.logger.info('Reading token...')
        with open(self._token_file, 'r') as fh:
            return json.load(fh)

    @safe_call(lambda x: x.logger)
    def save(self, token_to_save):
        self.logger.debug('Dumping token...')
        token_json = json.dumps(token_to_save)
        self.logger.info('Saving token...')
        with open(self._token_file, 'w') as fh:
            fh.write(token_json)

    @safe_call(lambda x: x.logger)
    def refresh(self, refresh_token):
        client_id = CLIENT_ID
        authority_url = 'https://login.microsoftonline.com/consumers/'
        scopes = ['User.Read']

        self.logger.info('Acquiring new token using a refresh_token')
        app = PublicClientApplication(client_id, authority=authority_url)
        new_token = app.acquire_token_by_refresh_token(refresh_token, scopes=scopes)
        self.logger.debug(f'New token: {new_token}')

        if 'access_token' not in new_token or 'refresh_token' not in new_token:
            self.logger.error('Access token or refresh token not present in the response')
            return None

        exp = datetime.utcfromtimestamp(int(new_token["id_token_claims"]["exp"]))
        self.logger.info(f'Got token: {new_token["access_token"][:10]}... '
                         f'Valid up to: {exp.strftime("%Y-%m-%d %H:%M:%S UTC")}')
        return new_token
