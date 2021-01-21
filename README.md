# vector-search [![Codacy Badge](https://api.codacy.com/project/badge/Grade/31c6bcb6723942a3bb12474cd7e74dac)](https://app.codacy.com/gh/ffreemt/vector-search?utm_source=github.com&utm_medium=referral&utm_content=ffreemt/vector-search&utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/vector-search.svg)](https://badge.fury.io/py/vector-search)[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/ffreemt/vector-search/st_app.py)

vector search based on faiss (currently just flatl2 and flatip)

## Special Dependencies

`vector-search` depends on polyglot that in turn depends on `libicu`

To install `libicu`
### For Linux/OSX

E.g.
*   Ubuntu: `sudo apt install libicu-dev`
*   Centos: `yum install libicu`
*   OSX: `brew install icu4c`

Then use `poetry` or `pip` to install ` PyICU pycld2 Morfessor`, e.g.
```bash
pip install PyICU pycld2 Morfessor
```
or
```python
poetry add PyICU pycld2 Morfessor
```
### For Windows

Download and install the `pyicu` and `pycld2` (possibly also `Morfessor`) whl packages for your OS/Python version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu and https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2 (possibly also Morfessor https://www.lfd.uci.edu/~gohlke/pythonlibs/)

## Final Note

The repo is for study purpose only. If you believe that your interests have been violated in any way, please let me know. I'll promptly follow it up with appropriate actions.