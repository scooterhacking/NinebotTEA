import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
ABOUT = {}
with open((HERE / "ninebottea" / "version.py")) as f:
    exec(f.read(), ABOUT)

setup(
    name="ninebottea",
    version=ABOUT['__version__'],
    description="A nice library and CLI tool to handle Ninebot firmware encryption/decryption",
    long_description=README,
    long_description_content_type="text/markdown",
    author="ScooterHacking",
    author_email="hi@scooterhacking.org",
    url="https://github.com/scooterhacking/NinebotTEA",
    python_requires=">=3.8, <4",
    license="MIT",
    packages=["ninebottea"],
    keywords=["Ninebot", "NinebotTEA", "ScooterHacking", "Scooter", "Xiaomi", "XiaoTea"],
    entry_points={"console_scripts": ["ninebottea=ninebottea.__main__:main"]}
)
