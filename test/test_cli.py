from textwrap import dedent
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
            dedent(
                """
                Routine FOO ────────────────────────────────────────────────────────────────────
                COMMAND Saying hello .. ✅
                COMMAND Saying world .. ✅
                Routine BAR ────────────────────────────────────────────────────────────────────
                COMMAND Saying goodbye .. ✅
            """
            ).lstrip(),
            "",
            id="pass",
        ),
        pytest.param(
            "pass.toml",
            ["-v"],
            dedent(
                """
                Routine FOO ────────────────────────────────────────────────────────────────────
                COMMAND Saying hello ..
                  Hello                                                                         
                ✅ return code: 0
                COMMAND Saying world ..
                  world                                                                         
                ✅ return code: 0
                Routine BAR ────────────────────────────────────────────────────────────────────
                COMMAND Saying goodbye ..
                  Goodbye                                                                       
                ✅ return code: 0
            """
            ).lstrip(),
            "",
            id="verbose",
        ),
        pytest.param(
            "fail.toml",
            [],
            dedent(
                """
                Routine FOO ────────────────────────────────────────────────────────────────────
                COMMAND Saying hello .. ✅
                COMMAND Saying world ..
                  world
                ❌ return code: 1
                Routine BAR ────────────────────────────────────────────────────────────────────
                COMMAND Saying goodbye .. ✅
            """
            ).lstrip(),
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
