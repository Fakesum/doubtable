'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.10.26
github: https://github.com/Fakesum/doubtables
'''

from . import htbuilder as h
from . import WebSiteItem

class Footer(WebSiteItem):
    def __init__(self, social_links=["#", "#", "#", "#", "worldanvilbild@gmail.com"]) -> None:
        self.social_links = social_links
    
    def about_us(self):
        return h.div(
            h.h6(
                "About The Project",
                h.p(
                    "<Description of the project here.>"
                ),
                _class="text-uppercase mb-4 font-weight-bold"
            ),
            _class="col-md-3 col-lg-3 col-xl-3 mx-auto mt-3"
        )
    
    def render(self):
        return h.footer(
            h.div(
                h.section(
                    h.div(
                        self.about_us(),
                        _class="row"
                    )
                ),
                h.section(
                    h.div(
                        h.div(
                            h.div(
                                "© MIT License  Github Link: ",
                                h.a(
                                    "https://github.com/Fakesum/doubtable",
                                    _class="text-white",
                                    href="https://github.com/Fakesum/doubtable",
                                ),
                                _class="p-3"
                            ),
                            _class="col-md-7 col-lg-8 text-center text-md-start"
                        ),
                        _class="row d-flex align-items-center"
                    ),
                    _class="p-3 pt-0"
                ),
                _class="container p-4 pb-0"
            ),
            _class="text-center text-lg-start text-white",
            style="background-color: #45526e"
        )