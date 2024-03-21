from collections import namedtuple


def as_dict(namedtuple_instance):
    """
    Convert a namedtuple instance to a dictionary.

    Args:
        namedtuple_instance: An instance of a namedtuple.

    Returns:
        dict: A dictionary containing the fields and values of the namedtuple instance.
    """
    return dict(namedtuple_instance._asdict())
