from . import WebSiteItem
from .header import Header
from . import htbuilder as h

class Body(WebSiteItem):
    INFO_1 = '''This. is Doubtable. From Questions to Answers. 

The New Edtech that will help you into a better understanding of any kind of doubt that you have. 

Just enter any kind of question you have in the box and we will provide you with all the information you need and give you a quick and detailed summary about your query.'''

    INFO_2 = '''Our site ,Doubtable was made with the idea of creating a place where anyone could solve any kind of Doubts and Querys that they have <br> Doubtable helps make searching for your answers easier as you will not have to search across many sites and give you a summary on the answer you are looking for. 
 <br> Much more convenient that using a browser as you will not have to search for your answer, in doubtable will show it up front.
'''
    def __init__(self, proc_id):
        self.proc_id = proc_id
    
    def loading(self):
        return h.div(
            h.div(
                *[h.div(_class=f"pulse-bubble pulse-bubble-{i}") for i in range(1, 4)],
                _class="pulse-container"
            ),
            _class="spinner-box"
        )
    def render(self):
        return h.div(
            h.div(
                h.div(
                    h.div(
                        (h.div(self.INFO_2, id="__rbox") if self.proc_id == None else self.loading()),
                        _class="container p-3 results-container"
                    ),
                    _class="col-sm"
                ),
                h.div(
                    Header.get_search(self),
                    h.div(
                        (self.INFO_1 if self.proc_id == None else self.loading()),
                        _class="container summary-container"
                    ),
                    _class="col-sm p-3"
                ),
                _class="row"
            ),
            _class="container"
        )