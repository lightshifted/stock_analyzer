from setuptools import setup, find_packages

setup(
    name='stock_analyzer',
    version='1.0.0',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'pandas~=2.2.3',
        'yfinance',
    ],
    author='',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)