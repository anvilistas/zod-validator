from ._anvil_designer import _Example1Template
from anvil import *
import anvil.server
from .._example_schema import user_schema, user_inputs

class _Example1(_Example1Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.validated_form.input_schema = user_inputs
        self.validated_form.zod_schema = user_schema

    def validated_form_submit(self, item, **event_args):
        anvil.server.call('add_data', item)
