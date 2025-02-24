import subprocess

from rich.padding import Padding

from exemplify.main import console

VERBOSE = False


def print_output(proc) -> bool:
    first = True
    while True:
        assert proc.stdout
        line = proc.stdout.readline()
        if not line:
            break

        if first and VERBOSE:
            console.print("")
            first = False

        console.print(Padding(line.strip(), (0, 0, 0, 2)))

    return not first


def run(*args, **kwargs):
    if kwargs.pop("capture_output", None):
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.PIPE

    capture_stdout = kwargs.get("stdout") in (
        subprocess.PIPE,
        subprocess.DEVNULL,
    )
    if not capture_stdout:
        kwargs["stdout"] = subprocess.PIPE

    capture_stderr = kwargs.get("stderr") in (
        subprocess.PIPE,
        subprocess.DEVNULL,
        subprocess.STDOUT,
    )
    if not capture_stderr:
        kwargs["stderr"] = subprocess.STDOUT

    kwargs["text"] = True
    proc = subprocess.Popen(*args, **kwargs)

    if not capture_stdout:
        if VERBOSE:
            print_output(proc)
        else:
            with console.capture() as capture:
                print_output(proc)

            proc.wait()

            if proc.returncode != 0:
                output = capture.get().rstrip()
                if output:
                    print(f"\n{output}")

    proc.wait()
    return proc
