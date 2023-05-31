# SPDX-License-Identifier: MIT
# Copyright (c) 2021 anvilistas

from .input_helpers import get_input_value, set_input_value


class Validator:
    def __init__(
        self,
        form,
        schema,
        *,
        input_prefix="",
        input_suffix="_input",
        error_prefix="",
        error_suffix="_error",
        submit_button=None,
        toggle_submit_enabled=False,
    ):
        self.inputs = {}
        self.errors = {}
        self.form = form
        self.schema = schema
        self.submit_button = submit_button or form.submit_button
        self.toggle_enabled = toggle_submit_enabled
        if self.toggle_enabled:
            self.submit_button.enabled = False

        for key in schema.shape:
            self.inputs[key] = getattr(form, input_prefix + key + input_suffix)
            self.errors[key] = getattr(form, error_prefix + key + error_suffix)
            on_change = self.change_handler(key)
            self.inputs[key].add_event_handler("change", on_change)

    def update_error(self, key, error):
        if not error:
            self.errors[key].text = " "
        else:
            self.errors[key].text = "\n".join(error.errors(key)) or " "

    def show_errors(self, parse_error):
        for key in self.errors:
            self.update_error(key, parse_error)

    def reset(self, **event_args):
        self.form.item = {}
        for key, input in self.inputs.items():
            set_input_value(input, None)
            self.errors[key].text = " "

    def validate(self):
        result = self.schema.safe_parse(self.form.item)
        self.show_errors(result.error)
        if self.toggle_enabled:
            self.submit_button.enabled = result.success

    def change_handler(self, key):
        def change(sender, **event_args):
            self.form.item[key] = get_input_value(sender)
            result = self.schema.safe_parse(self.form.item)
            if self.toggle_enabled:
                self.submit_button.enabled = result.success
            self.update_error(key, result.error)

        return change
