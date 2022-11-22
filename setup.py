from setuptools import setup

setup(
    name='pwcontrol',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'pyperclip',
        'pycryptodome',
    ],
)
