import pytest
from click.testing import CliRunner

from serps.cli import cli


@pytest.fixture(scope="session")
def cli_runner():
    """Fixture that returns a helper function to run the serps cli."""
    runner = CliRunner()

    def cli_main(*cli_args, **cli_kwargs):
        """Run serps cli main with the given args."""
        return runner.invoke(cli, cli_args, **cli_kwargs)

    return cli_main


@pytest.fixture(params=["-V", "--version"])
def version_cli_flag(request):
    """Pytest fixture return both version invocation options."""
    return request.param


def test_cli_version(cli_runner, version_cli_flag) -> None:
    """Verify serps version output by `cookiecutter` on cli invocation."""
    result = cli_runner(version_cli_flag)
    assert result.exit_code == 0
    assert result.output.startswith("SERP")
