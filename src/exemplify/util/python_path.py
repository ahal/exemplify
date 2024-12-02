import inspect
import os


def import_modules(exceptions=None):
    """
    Import all Python modules in subdirectories under the calling module.

    Args:
        exceptions (list): A list of file names to exclude (caller and
            __init__.py are implicitly excluded).
    """
    frame = inspect.stack()[1]
    mod = inspect.getmodule(frame[0])
    assert mod
    assert mod.__file__

    name = os.path.basename(mod.__file__)
    excs = {"__init__.py", name}
    if exceptions:
        excs.update(exceptions)

    modpath = mod.__name__
    if not name.startswith("__init__.py"):
        modpath = modpath.rsplit(".", 1)[0]

    calldir = os.path.dirname(mod.__file__)
    for root, _, files in os.walk(calldir):
        subdir = os.path.relpath(root, calldir)
        for f in files:
            if f.endswith(".py") and f not in excs:
                __import__(f"{modpath}.{subdir.replace('/', '.')}.{f[:-3]}")
