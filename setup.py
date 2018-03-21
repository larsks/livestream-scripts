from setuptools import setup, find_packages


setup(
    name='pycam',
    version=0.1,
    author='Lars Kellogg-Stedman',
    author_email='lars@oddbit.com',
    url='http://github.com/larsks/livestream-scripts',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'pycam = pycam.main:main'
        ]
    }
)
