# SPDX-License-Identifier: MIT
# Copyright (c) 2021 anvilistas

import anvil.server

from ...input_helpers import get_input_value, set_input_value
from ._anvil_designer import InputTemplate


class Input(InputTemplate):
    def __init__(self, error=None, input=None, key="", title="", **properties):
        self.init_components(
            error=error, input=input, key=key, title=title, **properties
        )
        self.setup_input()

    def setup_input(self):
        self.input_panel.clear()
        self.input_panel.add_component(self.input, expand=True)
        self.input.add_event_handler("change", self.change)

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, error):
        self._error = error
        if not error:
            self.error_label.text = " "
        else:
            self.error_label.text = "\n".join(error.errors(self.key)) or " "

    @property
    def value(self):
        return get_input_value(self.input)

    @value.setter
    def value(self, value):
        set_input_value(self.input, value)

    def change(self, **event_args):
        self.raise_event("change", key=self.key, value=self.value)

    @property
    def title(self):
        return self.label.text

    @title.setter
    def title(self, value):
        self.label.text = value
