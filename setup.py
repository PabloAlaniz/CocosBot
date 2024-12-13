from pathlib import Path

from setuptools import setup, find_packages

# Cargar descripción larga desde README.md
long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="CocosBot",
    version="0.1.0",
    author="Pablo Alaniz",
    description="Automation for operations and API data extraction from Cocos Capital broker.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PabloAlaniz/CocosBot",
    license="MIT",
    keywords="cocos bot automation broker api",
    packages=find_packages(),
    install_requires=[
        "playwright>=1.0.0",
        "beautifulsoup4"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
