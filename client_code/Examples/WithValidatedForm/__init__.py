from ._anvil_designer import WithValidatedFormTemplate
from anvil import *
import anvil.server
from ..schemas import user_schema, user_inputs, user_headings

class WithValidatedForm(WithValidatedFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.validated_form.input_schema = user_inputs
        self.validated_form.title_schema = user_headings
        self.validated_form.zod_schema = user_schema

    def validated_form_submit(self, item, **event_args):
        anvil.server.call('add_data', item)

