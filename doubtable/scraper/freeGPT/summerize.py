'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.10.26
github: https://github.com/Fakesum/doubtables
'''

from . import KeysExhausted, _make_api_call

class SummerizeKeysExhausted(KeysExhausted): pass

sumerize_from_url = lambda url, length, lang: _make_api_call(
    "https://article-extractor-and-summarizer.p.rapidapi.com/summarize",
    "article-extractor-and-summarizer.p.rapidapi.com",
    {
        "url": url,
        "length": str(length),
        "lang": lang
    },
    "summerize.keys",
    exhaustion_error=SummerizeKeysExhausted
)

sumerize_from_text = lambda text, length, lang: _make_api_call(
    "https://article-extractor-and-summarizer.p.rapidapi.com/summarize-text",
    "article-extractor-and-summarizer.p.rapidapi.com",
    {
        "text": text,
        "length": str(length),
        "lang": lang
    },
    "summerize.keys",
    type="post",
    exhaustion_error=SummerizeKeysExhausted
)