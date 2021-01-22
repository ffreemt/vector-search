"""Demo faiss semantic search (multilingual).

Based on st-bumblebee-aligner, to be deployed on share.streamlit.io
"""
# pylint:

__version__ = "0.1.0"

from typing import (
    List,
    Optional,
    Union,
)

from pathlib import Path
from timeit import default_timer
from itertools import chain
# import base64
# from io import BytesIO

import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from joblib import load

# import seaborn as sns
# import matplotlib.pyplot as plt
from polyglot.text import Detector, Text
from sentence_splitter import split_text_into_sentences

import logzero
from logzero import logger

# from bee_aligner.fetch_sent_corr import fetch_sent_corr
from vector_search.fetch_embed import fetch_embed
from vector_search.vector_search import vector_search

logzero.loglevel(20)

# use sentence_splitter if supported
LANG_S = ["ca", "cs", "da", "nl", "en", "fi", "fr", "de",
          "el", "hu", "is", "it", "lv", "lt", "no", "pl",
          "pt", "ro", "ru", "sk", "sl", "es", "sv", "tr"]


# global
query = ""  # type: Union[str, List[str]]


def seg_text(text: str, lang: Optional[str] = None) -> List[str]:
    """split text to sentences.

    use sentence_splitter if supported,
    else use polyglot.text.Text
    """
    if lang is None:
        lang = Detector("testt 12 3").language.code

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

    img = Image.open("img/under_construction.jpg")
    st.image(img, width=200)

    # st.write("(In progress...)")
    st.warning("(In progress...)")
    st.write("repo https://github.com/ffreemt/vector-search")

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
        "--- \n* Use the left sidebar to navigate\n* "
        f"semantic search (multilingual) v{__version__} from mu@qq41947782's "
        "keyboard in "
        "cyberspace. Join **qq group 316287378** for feedback and "
        "questions or to be kept updated. "
    )


def main():
    """Main."""
    pd.set_option('precision', 2)
    pd.options.display.float_format = '{:,.2f}'.format

    front_cover()

    book_titles = [
        "The Catcher in the Rye",
        "麦田守望者（施）",
        "麦田捕手（孙）",
        "芳芳日记（英）",
        "芳芳日记",
    ]
    book_dir = Path("texts").resolve()
    book_files = [
        "catcher-in-the-rye-en.txt",
        "catcher-in-the-rye-shixianrong-zh.txt",
        "catcher-in-the-rye-sunzhongxu-zh.txt",
        "fangfang-en.txt",
        "fangfang-zh.txt",
    ]
    book_files = [*Path("texts").glob("*.txt")]
    book_dict = dict(
        zip(book_titles, book_files)
    )
    book_list = ["None", "All", ] + [*book_dict]

    #
    books_selected = st.multiselect(
        f"Select books to search from: {book_list}",
        book_list,
        default=["麦田守望者（施）", "麦田捕手（孙）",]
    )
    if books_selected:
        if "All" in books_selected[-1:]:
            books_selected = [*book_dict]
        elif "None" in books_selected[-1:]:
            books_selected = []
        st.write("You selected: ", books_selected)
    else:
        st.write("You have not selected anything. Click the dropdown")
        return None

    if not books_selected:
        return None

    st.info(books_selected)
    files_selected = [book_dict[elm] for elm in books_selected]
    files_stem = [elm.stem for elm in files_selected]
    # ['catcher-in-the-rye-shixianrong-zh', 'catcher-in-the-rye-sunzhongxu-zh']

    token_files = [Path("data") / (elm + ".lzma") for elm in files_stem]

    encoded_files = [Path("data") / (elm + "-encoded.lzma") for elm in files_stem]

    # np.all([*map(lambda x: x.is_file(), token_files)])
    # np.all([*map(lambda x: x.is_file(), encoded_files)])

    # tokens = []
    # for elm in token_files: tokens.extend(load(elm))
    tokens = [*chain.from_iterable([load(elm) for elm in token_files])]  # 1.3s
    encoded = [*chain.from_iterable([load(elm) for elm in encoded_files])]  # 9 sec

    tokens = np.array(tokens)
    encoded = np.array(encoded)


    index_ = st.radio("Select type: ", ("flat-l2 (distance)", "flat-ip (cosine)"))

    label = "Paste some sentenes here: "
    max_chars = 1000
    text = st.text_area(label, value='', height=None, max_chars=max_chars, key=None)

    try:
        sents = seg_text(text)
    except Exception as exc:
        sents = [str(exc)]

    sents

    "+".join(sents)

    st.write(text, sents)

    _ = vector_search(sents, tokens, encoded, index_=index_)
    _

    back_cover()

    # st.write(src_fileio.name)
    return None


main()
