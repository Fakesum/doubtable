from .import htbuilder as h
from . import WebSiteItem

class Header(WebSiteItem):
    def __init__(self, logo_path, menu_items) -> None:
        self.logo_path = logo_path
        self.menu_items = menu_items
    
    def get_logo(self):
        return h.a(
            h.img(
                src=self.logo_path,
                width="120",
                height="100",
            ),
            href="/",
            _class="d-flex align-items-center mb-2 mb-lg-0 text-white text-decoration-none"
        )
    
    def get_menu(self):
        return h.ul(
            *[h.li(h.a(item["name"], _class="nav-link px-2 "+("text-secondary" if item == self.menu_items[0] else "text-white"), href=item["link"])) for item in self.menu_items],
            _class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0"
        )
    
    def get_search(self):
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