import importlib

def get_class(path):
    """Given a dotted path to a class, returns a class object.
    If the class doesn't exist, it variously raises ValueError or AttributeError

    TODO: Examine the use cases here, and if it's still needed, at least
    refactor it to return None if the class doesn't exist.
    """
    module, dot, cls = path.rpartition('.')
    m = importlib.import_module(module)
    return m.__getattribute__(cls)
