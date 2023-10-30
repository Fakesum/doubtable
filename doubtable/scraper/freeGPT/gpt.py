'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.10.26
github: https://github.com/Fakesum/doubtables
'''

from . import _make_api_call, KeysExhausted, _split_into_paragraph
from .summerize import (
    sumerize_from_url,
    sumerize_from_text
)

class GPTApiKeysExhausted(KeysExhausted): pass

def request(content):
    return _make_api_call(
        "https://chatgpt-api8.p.rapidapi.com/",
        "chatgpt-api8.p.rapidapi.com",
        content,
        "gpt.keys",
        r_type="post",
        exhaustion_error=GPTApiKeysExhausted
    )

def get_answer(query, source, itype="url", summary_length=50, lang="en"):
    """Get the answer of a question with given source to pull the answer from.

    Args:
        query (str): the question that needs to be answered
        source (str): source which the answer will be pulled from, can be a url 
        or it can be text which needs to be summerize, use the itype paramenter to specify whether a url or text is given.

        o_length (str, optional): the length of output, can be either "long" or "short" . Defaults to "short".
        itype (str, optional): the type of input can be either "url" or "text" . Defaults to "url".
        summary_length (int, optional): the no. of sentences in the summary, maximum is 50. Defaults to 50.
        lang (str, optional): the language of the output. Defaults to "en".

    """
    summary_length = min((summary_length, 50)) # length can be max 50 sentences.

    if itype == "url":
        summary = sumerize_from_url(source, summary_length, lang)["summary"].replace("\n\n", " ").replace("\n", " ")
    elif itype == "text":
        summary = sumerize_from_text(source, summary_length, lang)["summary"].replace("\n\n", " ").replace("\n", " ")
    
    res = request(
        [
            {
                "content":f"""answer from summary: '{summary}'""",
                "role": "system"
            },
            {
                "content": query,
                "role": "user"
            }
        ]
    )
    print(res)
    
    return _split_into_paragraph(res["text"])