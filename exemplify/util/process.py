import subprocess

from exemplify.console import console


def run(*args, **kwargs):
    capture_stdout = kwargs.get("capture_output") or kwargs.get("stdout") in (
        subprocess.PIPE,
        subprocess.DEVNULL,
    )
    if not capture_stdout:
        kwargs["stdout"] = subprocess.PIPE

    capture_stderr = kwargs.get("capture_output") or kwargs.get("stderr") in (
        subprocess.PIPE,
        subprocess.DEVNULL,
        subprocess.STDOUT,
    )
    if not capture_stderr:
        kwargs["stderr"] = subprocess.STDOUT

    kwargs["text"] = True
    proc = subprocess.run(*args, **kwargs)

    if not capture_stdout:
        console.print(proc.stdout)

    return proc
