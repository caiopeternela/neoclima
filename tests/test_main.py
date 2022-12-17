from typer.testing import CliRunner
from neoclima.main import app

runner = CliRunner()

def test_ls_command():
    result = runner.invoke(app, "ls")
    assert result.exit_code == 0
