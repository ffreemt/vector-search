# first line: 77
@memory.cache
# fmt: off
def list_tokens(
        text: Union[str, List[str]],
        label: str = "",
        lang: Optional[str] = None,
        gen_para: Union[int, bool] = False,
        gen_sent: Union[int, bool] = True,
        gen_phrase: Union[int, bool] = False,
) -> List[Tuple[str, str, int, str]]:
    # fmt: on
    """List tokens with memoization."""
    return [*gen_tokens(
        text,
        label,
        lang,
        gen_para,
        gen_sent,
        gen_phrase,
    )]
