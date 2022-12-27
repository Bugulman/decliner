"""Скрипт Setup.py для проекта по упаковке."""

import json
import os

from setuptools import find_packages, setup


def read_pipenv_dependencies(fname):
    """Получаем из Pipfile.lock зависимости по умолчанию."""
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = json.load(lockfile)
        return [dependency for dependency in lockjson.get("default")]


if __name__ == "__main__":
    setup(
        name="oilyreport",
        version=os.getenv("PACKAGE_VERSION", "1.2.1"),
        # package_dir={"": "src"},
        packages=find_packages(),
        description="My package for production data analis"
        # install_requires=[
        # *read_pipenv_dependencies("Pipfile.lock"),
        # ],
    )
#
# from setuptools import find_packages, setup
#
# if __name__ == "__main__":
#     setup(
#         name="oilyreport",
#         version="1.2.1",
#         description="tNavigator additional module",
#         package_dir={"": "src"},
#         packages=find_packages("src"),
#         autor="VafinAR",
#         autor_email="reg16vp@mail.ru",
#         # py_modules=["oily_report", "dca_per_well", "DCA"],
#     )
