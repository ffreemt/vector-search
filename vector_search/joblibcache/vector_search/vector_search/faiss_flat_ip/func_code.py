# first line: 27
@memory.cache
def faiss_flat_ip(encoded_data):
    """Faiss flatip."""
    dim = encoded_data.shape[1]
    index = faiss.IndexIDMap(faiss.IndexFlatIP(dim))
    faiss.normalize_L2(encoded_data)
    index.add_with_ids(encoded_data, np.arange(len(encoded_data)))
    return index
