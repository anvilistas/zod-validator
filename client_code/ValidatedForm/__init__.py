# SPDX-License-Identifier: MIT
# Copyright (c) 2021 anvilistas

from anvil_extras import zod

from ._anvil_designer import ValidatedFormTemplate
from .Input import Input


class ValidatedForm(ValidatedFormTemplate):
    def __init__(self, **properties):
        self._zod_schema = zod.typed_dict({})
        self._input_schema = {}
        self._title_schema = {}
        self.inputs = {}
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

    @property
    def title_schema(self):
        return self._title_schema

    @title_schema.setter
    def title_schema(self, title_schema):
        self._title_schema = title_schema
        for key, title in title_schema.items():
            input = self.inputs.get(key)
            if input is None:
                continue
            input.title = title

    def init_inputs(self):
        self.fields_panel.clear()
        self.inputs = {}
        for key, input in self.input_schema.items():
            title = self.title_schema.get(key, key.capitalize())
            input = Input(key=key, input=input, title=title)
            input.add_event_handler("change", self.change)
            self.inputs[key] = input
            self.fields_panel.add_component(input)

    def change(self, key, value, sender, **event_args):
        self.item[key] = value
        result = self._zod_schema.safe_parse(self.item)
        self.submit_button.enabled = result.success
        sender.error = result.error

    def submit_button_click(self, **event_args):
        try:
            self.submit_button.enabled = False
            self._zod_schema.parse(self.item)
            self.raise_event("submit", item=self.item)
            for input in self.inputs.values():
                input.value = None
            self.item = {}
        except zod.ParseError as e:
            for input in self.inputs.values():
                input.error = e
