from anvil_extras import zod as z
from datetime import date, timedelta
import anvil

user_schema = z.typed_dict(
    {
        "name": z.string().strip().min(3, message="Name must be atleast 3 letters").max(50).transform(str.capitalize).refine(lambda s: s != "Admin", message="You can't be an admin"),
        "email": z.string().strip().email(),
        "age": z.coerce.integer(invalid_type_error="Expected a valid age").ge(18).lt(100),
        "dob": z.date().max(date.today() - timedelta(days=365*18), "Must be older than 18"),
        "color": z.string().upper().optional().pipe(z.enum(["RED", "GREEN", "BLUE"], invalid_type_error="Must be 'red', 'green' or 'blue'")),
    }
)

#### only for example 1 ####
user_inputs = {
    "name": anvil.TextBox(),
    "email": anvil.TextBox(type="email"),
    "age": anvil.TextBox(type="number"),
    "dob": anvil.DatePicker(format="DD-MM-YYYY"),
    "color": anvil.DropDown(items=["Red", "Green", "Blue", "Orange"], include_placeholder=True)
}

user_headings = {
    "dob": "Date of Birth"
}