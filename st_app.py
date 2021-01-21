"""Demo faiss semantic search multilingual.

Based on st-bumblebee-aligner, to be deplyed on share.streamlit.io
"""

__version__ = "0.1.0"

from typing import List

from timeit import default_timer
# import base64
# from io import BytesIO

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from polyglot.text import Detector, Text
from sentence_splitter import split_text_into_sentences

import logzero
from logzero import logger

# from bee_aligner.fetch_sent_corr import fetch_sent_corr
from vector_search.fetch_embed import fetch_embed

logzero.loglevel(20)

# use sentence_splitter if supported
LANG_S = ["ca", "cs", "da", "nl", "en", "fi", "fr", "de",
          "el", "hu", "is", "it", "lv", "lt", "no", "pl",
          "pt", "ro", "ru", "sk", "sl", "es", "sv", "tr"]


def seg_text(text: str, lang: str) -> List[str]:
    """ split text to sentences.

    use sentence_splitter if supported,
    else use polyglot.text.Text
    """
    if lang in LANG_S:
        return split_text_into_sentences(text, lang)

    return [elm.string for elm in Text(text, lang).sentences]


def split_text(text, sep='\n'):
    """Split text."""
    if isinstance(text, bytes):
        text = text.decode("utf8")
    return [elm.strip() for elm in text.split(sep) if elm.strip()]


@st.cache
def sent_embed(text1, url=None):
    """Embed sents."""
    if isinstance(text1, str):
        text1 = split_text(text1)
        logger.debug('type: %s, text[:4]: %s', type(text1), text1[:4])
    if url is None:
        return fetch_embed(text1)

    return fetch_embed(text1, url=url)


def front_cover():
    """Front."""
    # global src_fileio, op_selectbox, model_url

    st.sidebar.title(
        f"streamlit powered semantic search (multilingual) v{__version__}"
    )

    # st.sidebar.markdown("# web bumblebee aligner")
    # st.sidebar.markdown("total # of paras limited to 300")

    # branch
    _ = """
    st.sidebar.subheader("What would you like to do?")
    op_selectbox = st.sidebar.selectbox(
        "",
        ("Para/Sent Align", "Simple Sent Align")
    )
    st.success(op_selectbox)

    # st.sidebar.subheader("Select a model")
    mod_selectbox = st.sidebar.selectbox(
        "Select a model (optional)",
        ("Model 1", "Google USE")
    )
    st.success(mod_selectbox)

    # model_url
    if mod_selectbox in ["Model 1"]:
        model_url = None
        # default to preset url "http://216.24.255.63:8000/text/"
    else:
        model_url = "http://216.24.255.63:8008/text/"

    # st.markdown("## pick two files")
    st.sidebar.subheader("pick two separate files")
    # or a single dual-language file

    src_fileio = st.sidebar.file_uploader(
        "Choose a file (utf8 txt)", type=['txt',], key="src_text")
    # """


def instruction1():
    """Instructions."""
    # , or, a single file containing English and Chinese text (free format)
    st.info(
        "Pick two files first\n\nFrom the left sidebar, pick two files, "
        "for example, one contains English text, one contains Chinese text. "
        "All files should be in **utf-8 txt** format (**no pdf, docx format "
        "etc supported**). bumblebee supports many language pairs, not just "
        "English-Chinese."
    )


def back_cover():
    """Endnotes."""
    st.markdown(
        "--- \n* use the left sidebar to navigate\n* "
        f"semantic search (multilingual) v{__version__} from mu@qq41947782's "
        "keyboard in "
        "cyberspace. Join **qq group 316287378** for feedback and "
        "questions or to be kept updated. "
    )


pd.set_option('precision', 2)
pd.options.display.float_format = '{:,.2f}'.format


def main():
    """Main."""

    front_cover()

    back_cover()

    # st.write(src_fileio.name)


main()
