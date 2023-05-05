from .input_helpers import set_input_value, get_input_value

class Validator:
    def __init__(self, form, schema, input_suffix="_input", error_suffix="_error", submit_button=None):
        self.inputs = {}
        self.errors = {}
        self.form = form
        self.schema = schema
        self.submit_button = submit_button or form.submit_button
        self.submit_button.enabled = False

        for key in schema.shape:
            self.inputs[key] = getattr(form, key + input_suffix)
            self.errors[key] = getattr(form, key + error_suffix)

        for key, input in self.inputs.items():
            change = self.change(key)
            input.add_event_handler("change", change)

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
        for input, error in zip(self.inputs.values(), self.errors.values()):
            set_input_value(input, None)
            error.text = " "

    def change(self, key):
        def change(sender, **event_args):
            self.form.item[key] = get_input_value(sender)
            result = self.schema.safe_parse(self.form.item)
            self.submit_button.enabled = result.success
            self.update_error(key, result.error)
        return change