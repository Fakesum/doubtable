'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.10.26
github: https://github.com/Fakesum/doubtables
'''

from .import htbuilder as h
from . import WebSiteItem

class Header(WebSiteItem):
    """The Header Utility Class, it will returned the rendered navbar/header

    Derived:
        WebSiteItem : Only for type hinting.
    """
    def __init__(self, logo_path, menu_items) -> None:
        """Constructor for Header Utility Class

        Args:
            logo_path (str): The url path to the logo, Should be a url path to a svg
            menu_items (list[dict[str, str]]): The list of menu items in the format, {name: ..., link: ...}
        """
        self.logo_path = logo_path
        self.menu_items = menu_items
    
    def get_logo(self):
        """Utility Function to get the logo

        Returns:
            html: Html of the logo image.
        """
        return h.a(
            ".",
            href="/",
            _class="d-flex align-items-center mb-2 mb-lg-0 text-white text-decoration-none"
        )
    
    def get_menu(self):
        """Return the html of the menu in the navbar.

        Returns:
            Html: Html of the menu in the navbar.
        """
        return h.ul(
            *[h.li(h.a(item["name"], _class="nav-link px-2 "+("text-secondary" if item == self.menu_items[0] else "text-white"), href=item["link"])) for item in self.menu_items],
            _class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0"
        )
    
    def get_search(self):
        """return the html of the search bar.

        Returns:
            html: html of the search bar(form)
        """
        #TODO: Add Parameters,
        #TODO: Get the type of question.
        return h.form(
            h.input(
                type="search",
                _class="form-control form-control-dark",
                placeholder="Search Your Doubts...",
                aria_label="Search Doubts",
                name="search"
            ),
            _class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3",
            action="/",
            method="get"
        )
    
    def render(self):
        """The Main Render function for the header navbar.

        Returns:
            html: html of the header/navbar.
        """
        return h.header(
            h.div(
                h.div(
                    self.get_logo(),
                    self.get_menu(),
                    self.get_search(),
                    _class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start"
                ),
                _class="container"
            ),
            _class="p-3 bg-dark text-white"
        )