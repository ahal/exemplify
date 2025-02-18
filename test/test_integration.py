from textwrap import dedent

import pytest


def test_command_basic(run_exemplify):
    ret, out, err = run_exemplify(
        """
        [[test.step]]
        type = "command"
        run = "echo 'foo'"
        """
    )
    assert ret == 0
    assert "COMMAND echo 'foo' .. ✅" in out
    assert err == ""


def test_command_fail(run_exemplify):
    ret, out, err = run_exemplify(
        """
        [[test.step]]
        type = "command"
        run = "exit 1"
        """
    )
    assert ret == 1
    assert "COMMAND exit 1 .. ❌ return code: 1" in out
    assert err == ""


@pytest.fixture
def pass_toml():
    return """
        [[foo.step]]
        type = "command"
        alias = "Saying hello"
        run = "echo Hello"

        [[foo.step]]
        type = "command"
        alias = "Saying world"
        run = "echo world"

        [[bar.step]]
        type = "command"
        alias = "Saying goodbye"
        run = "echo Goodbye"
    """


@pytest.fixture
def fail_toml():
    return """
        [[foo.step]]
        type = "command"
        alias = "Saying hello"
        run = "echo Hello"

        [[foo.step]]
        type = "command"
        alias = "Saying world"
        run = "echo world; exit 1"

        [[bar.step]]
        type = "command"
        alias = "Saying goodbye"
        run = "echo Goodbye"
    """


def test_legacy_cli_test_pass(pass_toml, run_exemplify):
    ret, out, err = run_exemplify(pass_toml)
    assert ret == 0
    assert (
        out
        == dedent(
            """
                Routine FOO ────────────────────────────────────────────────────────────────────
                COMMAND Saying hello .. ✅
                COMMAND Saying world .. ✅
                Routine BAR ────────────────────────────────────────────────────────────────────
                COMMAND Saying goodbye .. ✅
            """
        ).lstrip()
    )
    assert err == ""


def test_legacy_cli_test_pass_verbose(pass_toml, run_exemplify):
    ret, out, err = run_exemplify(pass_toml, verbose=True)
    assert ret == 0
    assert (
        out
        == dedent(
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
        ).lstrip()
    )
    assert err == ""


def test_legacy_cli_test_fail(fail_toml, run_exemplify):
    ret, out, err = run_exemplify(fail_toml)
    assert ret == 1
    assert (
        out
        == dedent(
            """
                Routine FOO ────────────────────────────────────────────────────────────────────
                COMMAND Saying hello .. ✅
                COMMAND Saying world ..
                  world
                ❌ return code: 1
                Routine BAR ────────────────────────────────────────────────────────────────────
                COMMAND Saying goodbye .. ✅
            """
        ).lstrip()
    )
    assert err == ""
