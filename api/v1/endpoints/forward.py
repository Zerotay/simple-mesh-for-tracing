from http.client import responses

import requests
from time import time,sleep

from fastapi import APIRouter, Request

from core.config import settings
from core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

test_data = {
    "host": "a",
    "elapsed_time": "",
    "next_node": []
}

@router.api_route("/{full_path:path}", methods=["GET"])
def forward_subpath(full_path: str, request: Request):
    start_time = time()
    logger.debug(f'Reached {settings.HOST}')
    # Currently, delay is applied before sending to next.
    sleep(settings.DELAY)
    res = {
        "host": settings.HOST,
        "elapsed_time": 0,
        "next_node": []
    }
    if not full_path:
        logger.debug(f'{settings.HOST} is the final endpoint.')
        res["elapsed_time"] = time() - start_time
        return res

    i = full_path.find('/')
    if i < 0:
        targets = full_path.split('~')
        subpath = ''
    else:
        targets = full_path[:i].split('~')
        subpath = full_path[i:]
    for t in targets:
        logger.debug(f'Try to send traffic to :: {t}')
        url = "http://"+t+subpath
        try:
            response = requests.get(url=url)
            res['next_node'].append(response.json())
        except:
            logger.debug(f'unable to send to {url}')

    res["elapsed_time"] = time() - start_time
    return res