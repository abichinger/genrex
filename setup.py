import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'genrex',
    packages = ['genrex'],
    license='MIT',
    description = 'Genrex generates matching strings to a given regular expressions.',
    author = 'abichinger',
    author_email = 'abichinger@example.com',
    url = 'https://github.com/abichinger/genrex',
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.3',
)