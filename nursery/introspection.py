import importlib

def get_class(path):
    module, dot, cls = path.rpartition('.')
    m = importlib.import_module(module)
    return m.__getattribute__(cls)

