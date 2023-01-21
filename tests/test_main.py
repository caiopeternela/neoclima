from typer.testing import CliRunner
from neoclima.main import app

runner = CliRunner()

def test_ls_command():
    result = runner.invoke(app, "ls")
    assert result.exit_code == 0


def test_add_command():
    result = runner.invoke(app, ["add", "nyc"], input="US\nNew York")
    outputs = [output.strip() for output in result.stdout.split(":")]
    assert outputs[0] == "Type the country name or code (ISO3166)"
    assert outputs[1] == "Type the city name"
    assert outputs[2] == "City added succesfully!"