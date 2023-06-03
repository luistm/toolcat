import pytest
import toml

from toolcat.project import update_version_in_pyproject_toml


@pytest.fixture
def pyproject_toml_path(tmp_path):
    pyproject_toml_path = tmp_path / "pyproject.toml"
    pyproject_toml_path.touch()
    return pyproject_toml_path


def test_update_version_in_pyproject_toml_when_a_version_is_defined(
    pyproject_toml_path,
):
    sample_toml_content = """
    [build-system]
    requires = ["poetry-core>=1.0.0"]
    build-backend = "poetry.core.masonry.api"

    [tool.poetry]
    name = "your-project"
    version = "0.1.0"
    description = "Your project description."
    authors = ["Your Name <youremail@example.com>"]
    license = "MIT"

    [tool.poetry.dependencies]
    python = "^3.9"

    [tool.poetry.dev-dependencies]
    pytest = "^6.2.2"
    """

    with open(pyproject_toml_path, "w") as f:
        f.write(sample_toml_content)

    version = "1.2.3"

    update_version_in_pyproject_toml(version, pyproject_toml_path)

    pyproject_toml = toml.load(pyproject_toml_path)
    assert pyproject_toml["tool"]["poetry"]["version"] == version  # nosec
