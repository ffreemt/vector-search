# first line: 37
@memory.cache
def faiss_flat_l2(encoded_data):
    """Faiss flatl2."""
    dim = encoded_data.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(encoded_data)
    return index
