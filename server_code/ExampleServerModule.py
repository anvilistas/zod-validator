import anvil.server
from .Examples.schemas import user_schema

@anvil.server.callable
def add_data(data):
    data = user_schema.parse(data)
    print("received", data)
    ...
    return 42
