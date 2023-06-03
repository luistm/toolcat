import nox


@nox.session(python=["3.10", "3.11"])
def tests(session):
    session.install("-r", "requirements.txt")
    session.run("pytest", ".")
