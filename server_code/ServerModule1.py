import anvil.server
from ._example_schema import user_schema

@anvil.server.callable
def add_data(data):
    data = user_schema.parse(data)
    print("received", data)
    ...
    return 42
