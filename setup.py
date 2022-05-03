import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EmsiApiPy",
    version="0.0.1",
    author="Caleb Courtney",
    author_email=None,
    description="Package for connecting to the Emsi APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/calebjcourtney/EmsiApiPy",
    project_urls={
        "Bug Tracker": "https://github.com/calebjcourtney/EmsiApiPy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
)
