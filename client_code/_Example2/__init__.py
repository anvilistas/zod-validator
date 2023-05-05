from ._anvil_designer import _Example2Template
from anvil import *
import anvil.server
from ..Validator import Validator
from .._example_schema import user_schema
from anvil_extras import zod as z

class _Example2(_Example2Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.validator = Validator(self, user_schema)

    def submit_button_click(self, **event_args):
        try:
            anvil.server.call("add_data", self.item)
            self.validator.reset()
        except z.ParseError as e:
            self.validator.show_errors(e)