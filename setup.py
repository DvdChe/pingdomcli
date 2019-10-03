import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pingdomcli",
    version="0.0.1",
    author="David Cherriere",
    author_email="cherri.david@gmail.com",
    description="A cli tool to manage checks on Pingdom",
    long_description="This tool is still in development. It's designed to be lightweight and to use standard libs",
    long_description_content_type="text/markdown",
    url="https://github.com/DvdChe/pingdomcli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)