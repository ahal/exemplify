def test_command_basic(run_exemplify):
    result = run_exemplify(
        """
        [[test.step]]
        type = "command"
        run = "echo 'foo'" 
        """
    )
    ret, out, err = result
    assert ret == 0
    assert "COMMAND echo 'foo' .. ✅" in out
    assert err == ""


def test_command_fail(run_exemplify):
    result = run_exemplify(
        """
        [[test.step]]
        type = "command"
        run = "exit 1" 
        """
    )
    ret, out, err = result
    assert ret == 1
    assert "COMMAND exit 1 .. ❌ return code: 1" in out
    assert err == ""
