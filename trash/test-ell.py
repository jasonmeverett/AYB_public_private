import ell
import json
import os
from openai import OpenAI
import httpx
import json
import os

import logging
logging.basicConfig(level=logging.DEBUG)

# From the doc
OPENAI_API_KEY=json.load(open("/tmp/jwt"))["access_token"]
OPENAI_API_BASE="https://ml-cb4a4d8b-dea.env-hack.svbr-nqvp.int.cldr.work/namespaces/serving-default/endpoints/llama-3-1-70b/v1"
OPENAI_MODEL_NAME="6lbx-oajq-2ehb-irio"

http_client = httpx.Client(verify="/etc/ssl/certs/ca-certificates.crt")
client = OpenAI(
    base_url=OPENAI_API_BASE,
    api_key=OPENAI_API_KEY,
    http_client=http_client,
)
# ell.config.register_model(OPENAI_MODEL_NAME, client)

@ell.simple(model=OPENAI_MODEL_NAME, client=client)
def hello(world: str) -> str:
    return f"Say hello to {world} with a poem."

hello("zoram")
