from pathlib import Path

import toml


def update_version_in_pyproject_toml(version: str, pyproject_path: str) -> None:
    """
    Updates the version of the project in the pyproject.toml file.

    Args:
        version (str): The new version string to update.
        pyproject_path (str): The path to the pyproject.toml file.

    Returns:
        None
    """
    pyproject_toml_path = Path(pyproject_path)
    pyproject_toml = toml.load(pyproject_toml_path)
    pyproject_toml["tool"]["poetry"]["version"] = version

    with open(pyproject_toml_path, "w") as f:
        toml.dump(pyproject_toml, f)
