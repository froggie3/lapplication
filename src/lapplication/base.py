def to_dict(obj: object) -> dict:
    """Creates a dictionary from the object without magic methods."""
    return {k: v for k, v in vars(obj).items() if not k.startswith("_")}


class Base:
    """A base class that contains human readable representation of the object."""

    def __repr__(self):
        params = ", ".join(f"{k}={v!r}" for k, v in to_dict(self).items())
        return f"{self.__class__.__name__}({params})"
