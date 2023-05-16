# SPDX-License-Identifier: MIT
# Copyright (c) 2021 anvilistas

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
