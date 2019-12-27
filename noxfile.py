import shutil

import nox

nox.options.reuse_existing_virtualenvs = True


@nox.session
def lint(session):
    """Performs pep8 and security checks."""
    source_code = 'configuror'
    session.install('flake8', 'bandit')
    session.run('flake8', source_code)
    session.run('bandit', '-r', source_code)


@nox.session
def tests(session):
    """Runs the test suite."""
    session.install('pyyaml', 'toml', 'pytest', 'pytest-cov', 'pytest-mock')
    session.cd('tests')
    session.run('pytest')


@nox.session
def coverage(session):
    """Runs codecov command to share coverage information on codecov.io"""
    session.install('codecov')
    session.run('codecov')


@nox.session
def docs(session):
    """Builds the documentation."""
    session.install('mkdocs')
    session.run('mkdocs', 'build', '--clean')


@nox.session(python=False)
def clean(*_):
    """Since nox take a bit of memory, this command helps to clean nox environment."""
    shutil.rmtree('.nox')
