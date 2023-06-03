import pytest

from toolcat.database import Database, Session, text


class TestDatabase:
    def test_should_raise_a_key_error_when_environment_variable_is_not_defined(self):
        with pytest.raises(KeyError):
            _ = Database()

    def test_create_database_file_in_path_defined_by_environment_variable(self, tmpdir, monkeypatch):
        database = tmpdir / "database_file_by_env.db"
        monkeypatch.setenv("DATABASE", str(database))

        _ = Database()

        assert database.exists()  # nosec

    def test_remove_the_database_file_when_remove_is_called(self, tmp_path):
        database_file = tmp_path / "database"
        sql_file = tmp_path / "sql_file.sql"
        sql_file.write_text("CREATE TABLE test_table (id INTEGER PRIMARY KEY);")
        db = Database(database_file, sql_file=sql_file)

        db.remove()

        database_file = tmp_path / "database.db"
        assert not database_file.exists()  # nosec

    def test_create_database_given_initial_sql_file(self, tmp_path):
        sql_file = tmp_path / "sql_file.sql"
        sql_file.write_text("CREATE TABLE test_table (id INTEGER PRIMARY KEY);")

        database = Database(tmp_path, sql_file=sql_file)

        sql_stmt = "SELECT * FROM test_table;"
        with Session(database.engine) as session:
            result = session.execute(text(sql_stmt))
        assert result.fetchall() == []  # nosec
