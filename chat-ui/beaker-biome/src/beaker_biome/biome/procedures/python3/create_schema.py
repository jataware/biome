# Define a class name
class_name = "{{ schema_name }}"

# Create the class dynamically
attributes = {"__doc__": " {{ schema_description }}"}

# Custom __repr__ to output detailed information about the class and its fields
def custom_repr(self):
    class_info = [f"{class_name}: {self.__doc__}"]
    for name, field in self.__class__.__dict__.items():
        if isinstance(field, pz.Field):
            class_info.append(f"{name}: description='{field.desc}', required={field.required}")
    return "\n".join(class_info)

# Add the custom __repr__ method to the class attributes
attributes["__repr__"] = custom_repr

for name, desc, required in zip({{ field_names }}, {{ field_descriptions }}, {{ field_required }}):
    attributes[name] = pz.Field(desc=desc, required=required)

# Create the class dynamically using type()
new_class = type(class_name, (pz.Schema,), attributes)

# Assign the dynamically created class to a variable using globals()
globals()[class_name] = new_class

new_class