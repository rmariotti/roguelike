class GenericComponent():
    """
    Adds runtime support for the generic type of a component.

    Unlike static typing with Generic[T], this stores the concrete type
    in `generic_type` for use at runtime.
    """
    def __init__(self, generic_type: type):
        self.generic_type = generic_type
