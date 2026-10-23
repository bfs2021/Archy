"""An unknown agent id is a typo to report, not a crash to trace back (#337).

`claude-code` is the natural guess: the docs say "Claude Code", the id is `claude`.
"""

from __future__ import annotations

import pytest
from click.testing import CliRunner

from archy.cli import main
from archy.install.registry import adapter_ids

BAD_ID = "claude-code"


@pytest.mark.parametrize(
    "args",
    [
        ["install", "--print-config", BAD_ID],
        ["install", "--target", BAD_ID, "--yes"],
        ["uninstall", "--target", BAD_ID, "--yes"],
    ],
    ids=["print-config", "install-target", "uninstall-target"],
)
def test_an_unknown_agent_id_is_a_clean_error_naming_the_known_ids(args, simulate_os):
    simulate_os("linux")
    assert BAD_ID not in adapter_ids()  # the fixture id really is unknown

    result = CliRunner().invoke(main, args)

    assert result.exit_code != 0
    assert isinstance(result.exception, SystemExit)  # click's error exit, no traceback
    assert f"Error: unknown agent '{BAD_ID}'." in result.output
    # Derived from the registry, so a new adapter shows up without a test edit.
    assert f"Known agents: {', '.join(adapter_ids())}." in result.output
