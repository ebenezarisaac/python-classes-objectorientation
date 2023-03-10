
import functools
import inspect
from location import Location
from position import EarthPosition

guntur = Location('Guntur', EarthPosition(43, 46))
nellore = Location('Nellore', EarthPosition(46, 46))
ongole = Location('Ongole', EarthPosition(48, 46))
hyderabad = Location('Hyderabad', EarthPosition(58, 46))

# Function decorator factory
def postcondition(predicate):

    def function_decorator(f):

        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            result = f(self, *args, **kwargs)
            if not predicate(self):
                raise RuntimeError(
                    f"Post-condition {predicate.__name__} not "
                    f"maintained for {self!r}"
                )
            return result

        return wrapper
    return function_decorator

def at_least_two_locations(itinerary):
    return len(itinerary._locations) >= 2

def invariant(predicate):
    function_decorator = postcondition(predicate)

    def class_decorator(cls):
        members = list(vars(cls).items())
        for name, member in members:
            if inspect.isfunction(member):
                decorated_member = function_decorator(member)
                setattr(cls, name, decorated_member)
        return cls

    return class_decorator


@invariant(at_least_two_locations)
class Itinerary:

    @classmethod
    def from_locations(cls, *locations):
        return cls(locations)

    def __init__(self, locations):
        self._locations = list(locations)

    def __str__(self):
        return "\n".join(location.name for location in self._locations)

    @property
    def locations(self):
        return tuple(self._locations)

    @property
    def origin(self):
        return self._locations[0]

    @property
    def destination(self):
        return self._locations[-1]

    def add(self, location):
        self._locations.append(location)

    def remove(self, name):
        removal_indexes = [
            index for index, location in enumerate(self._locations)
            if location.name == name
        ]

        for index in reversed(removal_indexes):
            del self._locations[index]
 
    def truncate_at(self, name):
        stop = None
        for index, location in enumerate(self._locations):
            if location.name == name:
                stop = index + 1

        self._locations = self._locations[:stop]