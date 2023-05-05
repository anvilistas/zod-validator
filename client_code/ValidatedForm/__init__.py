from ._anvil_designer import ValidatedFormTemplate
from anvil import *
from anvil_extras import zod
import anvil.server
from ..Input import Input

class ValidatedForm(ValidatedFormTemplate):
    def __init__(self, **properties):
        self._zod_schema = zod.typed_dict({})
        self._input_schema = {}
        self.inputs = []
        self.init_components(**properties)

    @property
    def zod_schema(self):
        return self._zod_schema

    @zod_schema.setter
    def zod_schema(self, schema):
        self._zod_schema = schema

    @property
    def input_schema(self):
        return self._input_schema

    @input_schema.setter
    def input_schema(self, input_schema):
        self._input_schema = input_schema
        self.init_inputs()

    def init_inputs(self):
        self.fields_panel.clear()
        self.inputs = []
        for key, input in self.input_schema.items():
            input = Input(key=key, input=input)
            input.add_event_handler("change", self.change)
            self.inputs.append(input)
            self.fields_panel.add_component(input)

    def change(self, key, value, sender, **event_args):
        self.item[key] = value
        result = self._zod_schema.safe_parse(self.item)
        self.submit_button.enabled = result.success
        sender.error = result.error

    def submit_button_click(self, **event_args):
        try:
            self.submit_button.enabled = False
            self.raise_event("submit", item=self.item)
            for input in self.inputs:
                input.value = None
            self.item = {}
        except zod.ParseError as e:
            for input in self.inputs:
                input.error = e
