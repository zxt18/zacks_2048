from setuptools import setup, find_packages

setup(
    name="zacks_2048",
    version="1.0.0",
    author="Zack Tan",
    description="A 2048 game with AI support.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pygame",
        "numpy",
        "pytest",
    ],
    entry_points={
        "console_scripts": [
            "zacks-2048=main:main",  # assumes you have a main() in src/main.py
        ],
    },
    python_requires=">=3.8",
)