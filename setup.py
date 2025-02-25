from setuptools import find_packages, setup

setup(
    name="flipbook",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=3.0.0",
        "Werkzeug>=3.0.1",
        "Pillow>=10.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-cov>=4.1.0",
            "pytest-flask>=1.3.0",
            "black>=23.12.1",
            "flake8>=7.0.0",
            "isort>=5.13.2",
        ],
    },
    author="aurlro",
    description="Un visualisateur de flipbook interactif avec interface web",
    python_requires=">=3.8",
)
