class WebSiteItem:
    def render(self):
        raise NotImplementedError

from .header import Header
from .body import Body
from .footer import Footer