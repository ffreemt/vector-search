"""fetch doc/para/send corr matrix from fastai server."""

from typing import List, Union

import numpy as np
import httpx
import logzero
from logzero import logger

logzero.loglevel(10)

URL = "http://127.0.0.1:8000/text/"
URL = "http://216.24.255.63:8000/text/"
URL = "http://216.24.255.63:8008/embed"


# fmt: off
def fetch_embed(
        sents1: Union[str, List[str]],
        url: str = URL,
) -> np.ndarray:
    # fmt: on
    """Fetch doc/para/send embedding from fastai server.

    >>> sents1 = ["test abc", "test abc"]
    >>> res = fetch_embed(sents1)
    >>> np.array(res).shape ==  (2, 512)
    True
    >>> res[0] == res[1]
    True
    """
    if isinstance(sents1, str):
        sents1 = [sents1]

    data = {
        "text1": sents1,
    }
    try:
        resp = httpx.post(
            url,
            json=data,
            timeout=None,
        )
        resp.raise_for_status()
    except Exception as exc:
        resp = None
        logger.error("exc: %s", exc)
        raise

    jdata = {}
    try:
        jdata = resp.json()  # type: ignore
    except Exception as exc:
        logger.error("exc: %s", exc)
        jdata.update({"embed": [[0]]})
        raise

    return np.array(jdata.get("embed")).astype("float32")
