"""Search vectors via faiss."""
# embed = None Path("/home/ubuntu/myapps/fastapi-s/s_embed"

from typing import (
    Callable,
    List,
    Tuple,
    Optional,
    Union,
)
from pathlib import Path
from random import choices
import warnings
from joblib import Memory
import numpy as np
import faiss
from logzero import logger

# define embd
# embed = ""
from vector_search.fetch_embed import fetch_embed

_ = Path(__file__).parent / "joblibcache"
memory = Memory(location=_, verbose=0)


@memory.cache
def faiss_flat_ip(encoded_data):
    """Faiss flatip."""
    dim = encoded_data.shape[1]
    index = faiss.IndexIDMap(faiss.IndexFlatIP(dim))
    faiss.normalize_L2(encoded_data)
    index.add_with_ids(encoded_data, np.arange(len(encoded_data)))
    return index


@memory.cache
def faiss_flat_l2(encoded_data):
    """Faiss flatl2."""
    dim = encoded_data.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(encoded_data)
    return index


@memory.cache
def embed_data(data, embed=fetch_embed):
    """Embed data."""
    if isinstance(data, str):
        data = [data]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            _ = embed(data)
        except Exception as exc:
            logger.error(exc)
            raise
    return _


# def msearch(
# pylint: disable=too-many-arguments
def vector_search(
    query_vector: Union[str, np.ndarray],
    data: List[str],
    encoded_data: Optional[np.ndarray] = None,
    embed: Optional[Callable] = None,  # embed_data
    index_: str = "",  # default to indexflatl2
    sanity_check: Union[bool, int] = False,
    topk: int = 5,
) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """Search via faiss."""

    if embed is None:
        embed = fetch_embed

    if encoded_data is None:
        encoded_data = embed(data)

    if query_vector is None:
        _ = choices(["test", "测试"])
        logger.info("generated query: %s", _)
    if isinstance(query_vector, str):
        query_vector = embed(query_vector)

    if not isinstance(query_vector, np.ndarray):
        logger.info(
            "You probably need to embed (encode) the list of str first."
            "\n\t.e.g, embed(nameof(query_vector)). Exiting"
        )
        raise SystemExit(1)
    else:
        try:
            assert query_vector.shape[1] == encoded_data[1]
        except Exception as exc:
            logger.error(exc)
            raise SystemExit(1)

    if index_.lower() in ["indexflat_ip", "flat_ip", "flatip"]:
        index = faiss_flat_ip(encoded_data)
    else:  # index_.lower() in ["indexflatl2", "flat_l2", "flatl2"]
        index = faiss_flat_l2(encoded_data)
        faiss.normalize_L2(query_vector)

    _ = index.search(query_vector, topk)
    # _ = index.search(ed, topk)

    if sanity_check:
        # query_vector = encoded_data[:10]
        top_k = index.search(encoded_data[:10], topk)
        print([np.round(top_k[0], 2), top_k[1]])
        # return None

    return _
