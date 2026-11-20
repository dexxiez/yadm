"""Unit tests: choose_template_processor"""

import pytest


@pytest.mark.parametrize("label", ["", "default", "other"])
@pytest.mark.parametrize("awk", [True, False], ids=["awk", "no-awk"])
def test_kind_default(runner, yadm, awk, label):
    """Test kind: default"""

    expected = "default"
    awk_avail = "true"

    if not awk:
        awk_avail = "false"
        expected = ""

    if label == "other":
        expected = ""

    script = f"""
        YADM_TEST=1 source {yadm}
        function awk_available {{ {awk_avail}; }}
        template="$(choose_template_processor "{label}")"
        echo "TEMPLATE:$template"
    """
    run = runner(command=["bash"], inp=script)
    assert run.success
    assert run.err == ""
    assert f"TEMPLATE:{expected}\n" in run.out


@pytest.mark.parametrize("label", ["envtpl", "jinjanator", "jinja2", "j2", "other"])
@pytest.mark.parametrize("envtpl", [True, False], ids=["envtpl", "no-envtpl"])
@pytest.mark.parametrize("jinja2", [True, False], ids=["jinja2", "no-jinja2"])
@pytest.mark.parametrize("jinjanator", [True, False], ids=["jinjanator", "no-jinjanator"])
def test_kind_jinja(runner, yadm, envtpl, jinja2, jinjanator, label):
    """Test kind: jinjanator, jinja2 & envtpl

    Preference: jinjanator > built-in jinja2 > envtpl. A "jinjanator" template
    falls back to the built-in jinja2 renderer if jinjanator is broken.
    """

    envtpl_avail = "true" if envtpl else "false"
    jinja2_avail = "true" if jinja2 else "false"
    jinjanator_avail = "true" if jinjanator else "false"

    if label in ("jinjanator", "j2") and jinjanator:
        expected = "jinjanator"
    elif label in ("jinja2", "jinjanator", "j2") and jinja2:
        expected = "jinja2"
    elif label in ("envtpl", "j2") and envtpl:
        expected = "envtpl"
    else:
        expected = ""

    script = f"""
        YADM_TEST=1 source {yadm}
        function envtpl_available {{ {envtpl_avail}; }}
        function jinja2_available {{ {jinja2_avail}; }}
        function jinjanator_available {{ {jinjanator_avail}; }}
        template="$(choose_template_processor "{label}")"
        echo "TEMPLATE:$template"
    """
    run = runner(command=["bash"], inp=script)
    assert run.success
    assert run.err == ""
    assert f"TEMPLATE:{expected}\n" in run.out


@pytest.mark.parametrize("works", [True, False], ids=["healthy", "broken"])
@pytest.mark.parametrize("tool", ["jinjanator", "envtpl"])
def test_broken_python_tool_is_unavailable(runner, yadm, tmpdir, works, tool):
    """A tool on PATH whose python module is gone must not be chosen"""

    fake = tmpdir.join(tool)
    fake.write(f"#!/bin/sh\nexit {0 if works else 1}\n", ensure=True)
    fake.chmod(0o755)

    script = f"""
        YADM_TEST=1 source {yadm}
        {tool.upper()}_PROGRAM="{fake}"
        {tool}_available && echo AVAILABLE || echo UNAVAILABLE
    """
    run = runner(command=["bash"], inp=script)
    assert run.success
    assert ("AVAILABLE\n" if works else "UNAVAILABLE\n") == run.out
