# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hl7tojson",
    version="0.0.2",
    author="Jerry Le",
    author_email="khanh96le@gmail.com",
    description="A simple library to convert HL7 message version 2 to JSON "
                "with human readable description",
    keywords=[
        'HL7', 'Health Level 7', 'healthcare', 'health care', 'medical record'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jerry-le/hl7tojson",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'hl7tojson': ['./data/*/*.pickle']},
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'hl7==0.3.4',
        'six==1.11.0'
    ],
)
