from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name="danspeechdemo",
    version="0.0.1",
    author="Rasmus Arpe Fogh Jensen, Martin Carsten Nielsen",
    author_email="rasmus.arpe@gmail.com, mcnielsen4270@gmail.com,",
    description="Demo for the DanSpeech tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rasmusafj/danspeech",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data = True
)