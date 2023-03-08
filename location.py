import inspect
from position import EarthPosition, typename


def auto_str(cls):
    def synthesized_str(self):
        return f"This is the decorated string"
    setattr(cls, "__str__", synthesized_str)
    return cls

def auto_repr(cls):
    print(f"Decorating  {cls.__name__} with auto repr")
    members = vars(cls)
    
    if "__repr__" in members:
        raise TypeError(f"{cls.__name__} already defines __repr__")
    if "__init__" not in members:
        raise TypeError(f"{cls.__name__} doesnt  over ride __init__")


    sig = inspect.signature(cls.__init__)
    parameter_names = list(sig.parameters)[1:]
    print("__init__ parameter names: ", parameter_names)

    members_properties_checks = (
        name for name in parameter_names if not isinstance(members.get(name), property)
    )    

    # print(members_properties_checks) 
    items_with_no_props = list(members_properties_checks)
    if len(items_with_no_props) > 0:
        raise TypeError(f"Cannot apply auto_repr to {cls.__name__} because the following "
             "__init__  parameters doesn't have matching properties"
             f"{items_with_no_props}" ) 

    def synthesized_repr(self):
        return "{typename}({args})".format(
            typename=typename(self), args=", ".join(
                "{name}={value!r}".format(
                    name=name,
                    value=getattr(self, name)
                ) for name in parameter_names
            )
        )

    setattr(cls, "__repr__", synthesized_repr)

    
    return cls


@auto_repr
class Location:

    def __init__(self, name, position) -> None:
        self._name = name
        self._position = position

    @property
    def name(self):
        return self._name

    @property
    def position(self):
        return self._position

    # def __repr__(self):
    #     return f"{typename(self)}(name={self.name}, position={self.position})"

    # def __str__(self):
    #     return self.name

hong_kong = Location('Hong kong', EarthPosition(23, 44))