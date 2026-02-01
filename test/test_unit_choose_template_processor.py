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


@pytest.mark.parametrize("label", ["envtpl", "jinjanator", "other"])
@pytest.mark.parametrize("envtpl", [True, False], ids=["envtpl", "no-envtpl"])
@pytest.mark.parametrize("jinjanator", [True, False], ids=["jinjanator", "no-jinjanator"])
def test_kind_jinjanator_envtpl(runner, yadm, envtpl, jinjanator, label):
    """Test kind: jinjanator (both jinjanator & envtpl)

    jinjanator is preferred over envtpl if available.
    """

    envtpl_avail = "true" if envtpl else "false"
    jinjanator_avail = "true" if jinjanator else "false"

    if label in ("jinjanator", "j2") and jinjanator:
        expected = "jinjanator"
    elif label in ("envtpl", "j2") and envtpl:
        expected = "envtpl"
    else:
        expected = ""

    script = f"""
        YADM_TEST=1 source {yadm}
        function envtpl_available {{ {envtpl_avail}; }}
        function jinjanator_available {{ {jinjanator_avail}; }}
        template="$(choose_template_processor "{label}")"
        echo "TEMPLATE:$template"
    """
    run = runner(command=["bash"], inp=script)
    assert run.success
    assert run.err == ""
    assert f"TEMPLATE:{expected}\n" in run.out
