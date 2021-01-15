"""Init vector-search."""
from pathlib import Path
from .load_text import load_text
from .seg_text import seg_text
from .sent_tokenizer import sent_tokenizer, _sent_tokenizer
from .gen_tokens import gen_tokens, list_tokens

__version__ = "0.1.0"

# pylint: disable=invalid-name
textsdir = Path(__file__).parent.parent / "texts"
citr_en = load_text(textsdir / "catcher-in-the-rye-en.txt")
citr_shi_zh = load_text(textsdir / "catcher-in-the-rye-shixianrong-zh.txt")
citr_sun_zh = load_text(textsdir / "catcher-in-the-rye-sunzhongxu-zh.txt")

fangfang_zh = load_text(textsdir / "fangfang-zh.txt")
fangfang_en = load_text(textsdir / "fangfang-en.txt")

__all__ = (
    "load_text",
    "seg_text",
    "sent_tokenizer",
    "_sent_tokenizer",
    "gen_tokens",
    "list_tokens",
)
