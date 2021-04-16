import setuptools

with open("README.md", "r") as f:
    long_description = f.read()
    print(long_description)

setuptools.setup(
    name="ling_features",
    version="0.0.7",
    author="Ian Gow",
    author_email="iandgow@gmail.com",
    description="Linguistic features commonly use in research.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iangow/ling_features/",
    packages=setuptools.find_packages(),
    install_requires=['nltk', 'pandas'],
    python_requires=">=3",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
