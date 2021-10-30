from setuptools import find_packages, setup


def readme():
    with open('README.md') as f:
        return f.read()


def version():
    with open(f'src/{name}/version.py') as f:
        for line in f:
            if line.startswith(('MAJOR', 'MINOR', 'PATCH')):
                yield line.split('=')[1].strip()


pkgs = find_packages('src')

name = pkgs[0]

setup(
    author_email='tomoki.nakamaru@gmail.com',
    author='Tomoki Nakamaru',
    entry_points={'console_scripts': [f'{name}={name}.__main__:bibtefmt']},
    install_requires=['pyparsing==3.0.3'],
    license='MIT',
    long_description_content_type='text/markdown',
    long_description=readme(),
    name=name,
    package_dir={'': 'src'},
    packages=pkgs,
    version='.'.join(version())
)
