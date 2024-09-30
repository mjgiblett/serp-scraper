"""serps distutils configuration."""

from pathlib import Path

from setuptools import setup


def _get_version() -> str:
    """Read serps/VERSION.txt and return its contents."""
    path = Path("serps").resolve()
    version_file = path / "VERSION.txt"
    return version_file.read_text().strip()


def _get_requirements() -> list[str]:
    """Read requirements.txt and return its contents."""
    path = Path(__file__).parent.resolve()
    requirements_file = path / "requirements.txt"
    return requirements_file.read_text().strip().split("\n")


setup(
    name="SERP Scraper",
    version=_get_version(),
    description=(""),
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Matthew Giblett",
    url="https://github.com/mjgiblett/serp-scraper",
    packages=["serps"],
    package_dir={"serps": "serps"},
    entry_points={"console_scripts": ["serps = serps.__main__:main"]},
    python_requires=">=3.12",
    install_requires=_get_requirements(),
    license="MIT",
)
