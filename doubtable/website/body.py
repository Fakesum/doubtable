from . import WebSiteItem
from .header import Header
from . import htbuilder as h

class Body(WebSiteItem):
    def __init__(self, proc_id):
        self.proc_id = proc_id
    
    #TODO: Add a Description
    def render(self):
        return h.div(
            h.div(
                h.div(
                    h.div(
                        ("Info Here" if self.proc_id == None else "Loading Here"),
                        _class="container p-3 results-container"
                    ),
                    _class="col-sm"
                ),
                h.div(
                    Header.get_search(self),
                    h.div(
                        ("what is Good About doubtable" if self.proc_id == None else "Loading Here"),
                        _class="container summary-container"
                    ),
                    _class="col-sm p-3"
                ),
                _class="row"
            ),
            _class="container"
        )