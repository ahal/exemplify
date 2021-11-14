import inspect
import os


def import_sibling_modules(exceptions=None):
    """
    Import all Python modules that are siblings of the calling module.

    Args:
        exceptions (list): A list of file names to exclude (caller and
            __init__.py are implicitly excluded).
    """
    frame = inspect.stack()[1]
    mod = inspect.getmodule(frame[0])

    name = os.path.basename(mod.__file__)
    excs = {"__init__.py", name}
    if exceptions:
        excs.update(exceptions)

    modpath = mod.__name__
    if not name.startswith("__init__.py"):
        modpath = modpath.rsplit(".", 1)[0]

    for f in os.listdir(os.path.dirname(mod.__file__)):
        if f.endswith(".py") and f not in excs:
            __import__(modpath + "." + f[:-3])
