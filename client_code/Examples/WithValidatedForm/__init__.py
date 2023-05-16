# SPDX-License-Identifier: MIT
# Copyright (c) 2021 anvilistas

import anvil.server
from anvil import *

from ..schemas import user_headings, user_inputs, user_schema
from ._anvil_designer import WithValidatedFormTemplate


class WithValidatedForm(WithValidatedFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        # self.validated_form.item = {key: None for key in user_schema.shape}
        self.validated_form.input_schema = user_inputs
        self.validated_form.title_schema = user_headings
        self.validated_form.zod_schema = user_schema

    def validated_form_submit(self, item, **event_args):
        anvil.server.call("add_data", item)
