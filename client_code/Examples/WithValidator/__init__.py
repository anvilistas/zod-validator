# SPDX-License-Identifier: MIT
# Copyright (c) 2021 anvilistas

import anvil.server
from anvil import *

from anvil_extras import zod as z

from ...Validator import Validator
from ..schemas import user_schema
from ._anvil_designer import WithValidatorTemplate


class WithValidator(WithValidatorTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.validator = Validator(self, user_schema)

    def submit_button_click(self, **event_args):
        try:
            anvil.server.call("add_data", self.item)
            self.validator.reset()
        except z.ParseError as e:
            self.validator.show_errors(e)
