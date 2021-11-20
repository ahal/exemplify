import os
import shlex
import subprocess
import tempfile

from wellington.installables.base import Installable, register


@register("command")
class Command(Installable):
    def __init__(self, run, check=None, cwd=None, shell=False):
        self.runcmd = run
        self.checkcmd = check
        self.shell = shell

        cwd = cwd or tempfile.mkdtemp()
        self.cwd = os.path.expanduser(cwd)
        if not os.path.isdir(self.cwd):
            os.makedirs(self.cwd)

    def run(self, cmd):
        commands = cmd.split("&&")
        for command in commands:
            if "|" not in command:
                if not self.shell:
                    cmd = shlex.split(command)
                    cmd[0] = os.path.expanduser(cmd[0])
                subprocess.check_call(cmd, cwd=self.cwd, shell=self.shell)
                continue

            print(command)
            cmnds = command.split("|")
            proc = None
            for i, cmd in enumerate(cmnds):
                if not self.shell:
                    cmd = shlex.split(cmd)
                    cmd[0] = os.path.expanduser(cmd[0])

                if i == 0:
                    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=self.cwd, shell=self.shell)
                else:
                    assert proc
                    proc = subprocess.Popen(
                        cmd, stdout=subprocess.PIPE, stdin=proc.stdout, cwd=self.cwd, shell=self.shell
                    )

            assert proc
            output = proc.communicate()[0]
            print(output)
            if proc.returncode:
                raise subprocess.CalledProcessError(
                    returncode=proc.returncode, cmd=command, output=output
                )

    def exists(self):
        if not self.checkcmd:
            return False

        try:
            self.run(self.checkcmd)
            return True
        except subprocess.CalledProcessError:
            return False

    def install(self):
        self.run(self.runcmd)

    def __str__(self):
        return "RUN {} in {}".format(self.runcmd, self.cwd)


