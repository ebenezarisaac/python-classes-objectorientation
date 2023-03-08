from msilib.schema import Component, Property


class Position:

    def __init__(self, lattitude, longitude):
        if not (-90 <= lattitude <= 90):
            raise ValueError(f"Latitude {lattitude} out of range")

        if not (-180 <= longitude <= 180):
            raise ValueError(f"Longitude {longitude} out of range")

        self._lattitude = lattitude
        self._longitude = longitude

    @property
    def lattitude(self):
        return self._lattitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def latitude_hemisphere(self):
        return "N" if self.lattitude  >= 0 else "S"

    @property
    def longitude_hemisphere(self):
        return "E" if self.longitude  >= 0 else "W"

    def __repr__(self):
        return f"{typename(self)}(lattittude={self.lattitude}, longitude={self.longitude})"
    
    def __str__(self):
        return format(self)

    def __format__(self, format_spec):
        component_format_spec = ".2f"
        _, dot, suffix = format_spec.partition(".")
        if dot:
            num_decimal_places = int(suffix)
            component_format_spec = f".{num_decimal_places}f"
        latitude = format(abs(self.lattitude), component_format_spec)
        longitude = format(abs(self.longitude), component_format_spec)
        return (
            f"{latitude} {self.latitude_hemisphere}, "
            f"{longitude} {self.longitude_hemisphere}"
        )
        
def typename(obj):
    return type(obj).__name__

class EarthPosition(Position):
    pass

