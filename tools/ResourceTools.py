import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def remove_none_values(args: dict) -> dict:
    keys_to_be_removed = []
    for key in args:
        if args[key] is None:
            keys_to_be_removed.append(key)
    for key in keys_to_be_removed:
        del args[key]
    return args


def requests_retry_session(retries=3, backoff_factor=5, status_forcelist=(500, 502, 503, 504), session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session