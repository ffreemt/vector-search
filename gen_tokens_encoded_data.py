"""Generate and save list_tokens and encoded_data."""
# pylint:

from pathlib import Path
from functools import reduce
from joblib import dump
from logzero import logger
from tqdm import tqdm

from vector_search import load_text, list_tokens


def main():
    """main"""
    repl = [('catcher-in-the-rye', 'citr'), ('sunzhongxu', 'sun'), ('shixianrong', 'shi')]
    # reduce(lambda x, y: x.replace(y[0], y[1]), repl,
    # "catcher-in-the-rye-en") -> citr-en

    files = [*Path("texts").glob("*.txt")]
    labels = [reduce(lambda x, y: x.replace(y[0], y[1]), repl, elm.stem) for elm in files]
    label_dict = dict(zip(files, labels))

    data_dir = Path("data")
    try:
        data_dir.mkdir(exist_ok=True)
    except Exception as exc:
        logger.error(exc)
        raise SystemExit(1) from exc

    for file in tqdm(files):
        _ = load_text(file)
        label = label_dict[file]
        _ = list_tokens(_.splitlines(), label)
        dump(_, (data_dir / file.stem).as_posix() + ".lzma")

        # list_tokens(load_text(files[0]).splitlines(), 'citr-en')
        # joblib.load(data_dir / file.stem).as_posix() + ".lzma")
        

if __name__ == "__main__":
    main()
