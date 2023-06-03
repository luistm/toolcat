import os
import pathlib
from typing import Optional

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session as _Session
from sqlalchemy.orm import sessionmaker

Session = _Session


class Database:
    """
    Creates a database.

    The database is created in the path defined by the DATABASE environment
    variable. If the environment variable is not defined, it will create a
    database in the path defined by the `database_path` parameter.

    Optionally, it can receive a SQL file that will be executed against the
    database.
    """

    def __init__(
        self,
        database_path: Optional[pathlib.Path] = None,
        sql_file: Optional[pathlib.Path] = None,
    ) -> None:
        """
        Initializes the Database instance.

        Args:
            database_path (Optional[pathlib.Path]): Path to where the database file will be
              created.
            sql_file (Optional[pathlib.Path]): Path to the SQL file that will be executed against
              the database.

        Raises:
            KeyError: If the DATABASE environment variable is not defined and no `database_path`
              is provided.
        """
        env_path = os.environ.get("DATABASE")
        if env_path:
            database_path = pathlib.Path(env_path)

        if not database_path:
            raise KeyError("Please set the DATABASE environment variable.")

        database_path.mkdir(parents=True, exist_ok=True)
        self._database_file = database_path / "database.db"
        sqlite_url = f"sqlite:///{self._database_file}"

        engine = create_engine(sqlite_url, echo=False)
        self.engine = engine

        Session = sessionmaker(bind=engine)
        self.session = Session()

        if sql_file:
            self._run_sql_file(sql_file)

    def remove(self) -> None:
        """
        Removes the database file from the disk if it exists.
        """
        pathlib.Path(self._database_file).unlink(missing_ok=True)

    def _run_sql_file(self, sql_file_path: pathlib.Path) -> None:
        """
        Runs the SQL file against the database.

        Args:
            sql_file_path (pathlib.Path): Path to the SQL file to execute.
        """
        with open(sql_file_path) as sql_file:
            sql = sql_file.read()
            self.session.execute(text(sql))
            self.session.commit()
