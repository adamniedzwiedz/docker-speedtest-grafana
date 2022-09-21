import os
from dotenv import load_dotenv
from mstoken import MsToken

load_dotenv()

TOKEN_FILE = os.getenv('TOKEN_FILE')

if __name__ == "__main__":
    token = MsToken(TOKEN_FILE)
    token_value = token.read()
    if token_value is not None:
        new_token_value = token.refresh(token_value['refresh_token'])
        token.save(new_token_value)
