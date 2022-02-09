from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="syscall",
    packages=find_packages(),
    include_package_data=True,
    version="0.0.1",
    license="MIT",
    description="ctypes-based Linux syscall wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="gray",
    author_email="greyschwinger@gmail.com",
    url="https://github.com/jschwinger233/py-linux-syscall",
    platform=("linux"),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
)
