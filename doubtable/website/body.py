from . import WebSiteItem
from .header import Header
from . import htbuilder as h

class Body(WebSiteItem):
    def __init__(self, results=None):
        self.results = results
    
    def render_results(self):
        if self.results == None:
            return ""
        
        return h.div(
            *[h.div(item, _class="border border-primary") for item in self.results],
            _class="container p-3"
        )
    
    def render(self):
        return h.div(
            h.div(
                h.div(
                    self.render_results(),
                    _class="col-sm"
                ),
                h.div(
                    Header.get_search(self),
                    _class="col-sm p-3"
                ),
                _class="row"
            ),
            _class="container"
        )