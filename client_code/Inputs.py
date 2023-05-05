import anvil

def _prop(attr):
    def fget(self):
        return getattr(self, attr)

    def fset(self, val):
        return setattr(self, attr, val)

    return property(fget, fset)

_value_property_map = {
    anvil.TextBox: _prop("text"),
    anvil.DatePicker: _prop("date"),
    anvil.DropDown: _prop("selected_value"),
}

def set_input_value(self, value):
    _value_property_map[type(self)].fset(self, value)

def get_input_value(self):
    return _value_property_map[type(self)].fget(self)

TEXT = anvil.TextBox

def DATE(**properties):
    properties.setdefault("format", "DD-MM-YYYY")
    return anvil.DatePicker(**properties)

def DATETIME(**properties):
    properties.setdefault("format", "DD-MM-YYYY")
    properties.setdefault("pick_time", True)
    return anvil.DatePicker(**properties)

def EMAIL(**properties):
    properties.setdefault("type","email")
    return anvil.TextBox(**properties)

def NUMBER(**properties):
    properties.setdefault("type", "number")
    return anvil.TextBox(**properties)

def DROPDOWN(**properties):
    properties.setdefault("placeholder", "Select a value")
    properties.setdefault("include_placeholder", True)
    return anvil.DropDown(**properties)