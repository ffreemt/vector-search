"""Test sanity."""
from vector_search import __version__


def test_version():
    """Test version sanity."""
    assert __version__[:4] == "0.1."
