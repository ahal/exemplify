import pytest

from exemplify.cli import run


@pytest.fixture
def run_with_args():
    def inner(args):
        return run(args)

    return inner


@pytest.mark.parametrize(
    "exemplar,args,expected_stdout,expected_stderr",
    (
        pytest.param(
            "pass.toml",
            [],
            """
Routine foo succeeded! 0:00:00
  ✅ COMMAND Saying hello
  ✅ COMMAND Saying world
Routine bar succeeded! 0:00:00
  ✅ COMMAND Saying goodbye""".lstrip(),
            "",
            id="pass",
        ),
        pytest.param(
            "pass.toml",
            ["-v"],
            """
Routine foo succeeded! 0:00:00
  ✅ COMMAND Saying hello
  + echo Hello           
  Hello                  
  ✅ COMMAND Saying world
  + echo world           
  world                  
Routine bar succeeded! 0:00:00
  ✅ COMMAND Saying goodbye
  + echo Goodbye           
  Goodbye                  """.lstrip(),
            "",
            id="verbose",
        ),
        pytest.param(
            "fail.toml",
            [],
            """
Routine foo failed! 0:00:00
  ✅ COMMAND Saying hello
  ❌ COMMAND Saying world
  + echo world; exit 1   
  world                  
Routine bar succeeded! 0:00:00
  ✅ COMMAND Saying goodbye""".lstrip(),
            "",
            id="fail",
        ),
    ),
)
def test_cli(
    datadir, capfd, run_with_args, exemplar, args, expected_stdout, expected_stderr
):
    args.insert(0, str(datadir / exemplar))
    run_with_args(args)
    stdout, stderr = capfd.readouterr()
    print(stdout)
    print(stderr)

    assert stdout == expected_stdout
    assert stderr == expected_stderr
