from setuptools import setup, find_packages

setup(
    name="cherrie-saxelab-skill-challenges",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.12.0",
    ],
    python_requires=">=3.6",
    author="Cherrie Chang",
    description="Algorithms to solve the mixed design randomization challenge.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
