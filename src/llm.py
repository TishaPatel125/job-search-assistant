import os
import logging
import instructor
from openai import OpenAI

logger = logging.getLogger(__name__)

def get_raw_client():
    api_key = os.getenv('OPENROUTER_API_KEY')
    return OpenAI(base_url='https://openrouter.ai/api/v1', api_key=api_key, max_retries=3)

def get_client():
    raw_client = get_raw_client()
    logger.debug('Creating instructor client')
    return instructor.from_openai(raw_client, mode=instructor.Mode.JSON)
