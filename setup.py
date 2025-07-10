from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="vinted-api-wrapper",
    version="0.3.8",
    description="Unofficial Wrapper for Vinted API",
    author="Paweł Stawikowski",
    author_email="pawikoski@gmail.com",
    packages=find_packages(),
    url="https://github.com/Pawikoski/vinted-api-wrapper",
    python_requires=">=3.10",
    install_requires=["requests", "dacite", "beautifulsoup4"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
