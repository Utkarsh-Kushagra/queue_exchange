from setuptools import setup, find_packages

packages=find_packages()
print(packages)
setup(
    name="publisher-service",
    version="0.1.0",
    author="vEngage",
    description="Post discharge: publisher-service",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: Private",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)