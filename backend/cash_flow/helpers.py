import re
import unicodedata
from typing import Optional


def norm_str(s: Optional[str],
                     lower: bool = True,
                     ascii: bool = True,
                     remove_punctuation: bool = False,
                     sep: str = '') -> str:
    """
    Normalize a string.

    Behavior:
    - None -> empty string
    - trims surrounding whitespace
    - collapses internal whitespace to a single `sep`
    - optionally lowercases
    - optionally converts Unicode to ASCII (removes diacritics)
    - optionally removes punctuation (keeps letters, digits, underscore and whitespace)

    Examples:
    >>> normalize_string("  Héllo,  Wörld!  ")
    'hello world'
    >>> normalize_string("Café-au-lait", remove_punctuation=True, sep='-')
    'cafe-au-lait'  # note: punctuation removed but hyphens kept only if not considered punctuation before collapse
    """
    if s is None:
        return ''

    s = str(s).strip()

    if lower:
        s = s.lower()

    if ascii:
        s = unicodedata.normalize('NFKD', s)
        s = s.encode('ascii', 'ignore').decode('ascii')

    if remove_punctuation:
        # remove characters that are not word characters or whitespace
        s = re.sub(r'[^\w\s]', '', s)

    # collapse any whitespace sequence into the given separator and trim again
    s = re.sub(r'\s+', sep, s).strip()

    return s