from anvil_extras import zod as z
from datetime import date, timedelta
from . import Inputs

def to_upper(x):
    try:
        return x.strip().upper()
    except Exception:
        return x

user_schema = z.typed_dict(
    {
        "name": z.string().strip().min(3, message="Name must be atleast 3 letters").max(50).transform(str.capitalize).refine(lambda s: s != "Admin", message="You can't be an admin"),
        "email": z.string().strip().email(),
        "age": z.coerce.integer(invalid_type_error="Expected a valid age").ge(18).lt(100),
        "dob": z.date().max(date.today() - timedelta(days=365*18), "Must be older than 18"),
        "color": z.not_required(z.preprocess(to_upper, z.enum(["RED", "GREEN", "BLUE"], invalid_type_error="Must be 'red', 'green' or 'blue'"))),
    }
)

input_types = {
    "name": Inputs.TEXT(),
    "email": Inputs.EMAIL(),
    "age": Inputs.NUMBER(),
    "dob": Inputs.DATE(),
    "color": Inputs.DROPDOWN(items=["RED", "GREEN", "BLUE"])
}