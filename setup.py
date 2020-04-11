#!/usr/bin/env python3

import re
import setuptools

with open("fdbk_ruuvi_reporter/_version.py", "r") as f:
    try:
        version = re.search(
            r"__version__\s*=\s*[\"']([^\"']+)[\"']",f.read()).group(1)
    except:
        raise RuntimeError('Version info not available')

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="fdbk_ruuvi_reporter",
    version=version,
    author="Toni Kangas",
    description="Ruuvitag data reporter for fdbk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kangasta/fdbk_ruuvi_reporter",
    packages=setuptools.find_packages(),
    scripts=["bin/fdbk-ruuvi-reporter"],
    install_requires=[
        "fdbk==2.0a3",
        "ruuvitag-sensor>=1.0.1",
    ],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
