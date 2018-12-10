import ast
import codecs
import os
import re
from setuptools import setup, find_packages


def read_file(path):
    with codecs.open(path, 'rb', 'utf-8') as f:
        return f.read()


_version_re = re.compile(r'__version__\s+=\s+(.*)')
_source_dir = os.path.split(os.path.abspath(__file__))[0]
version = str(ast.literal_eval(_version_re.search(
    read_file(os.path.join(_source_dir, 'ivision_gridengine_client/__init__.py'))).group(1)))

requirements_list = list(filter(
    lambda v: v and not v.startswith('#'),
    (s.strip() for s in read_file(
        os.path.join(_source_dir, 'requirements.txt')).split('\n'))
))
dependency_links = [s for s in requirements_list if s.startswith('git+')]
install_requires = [s for s in requirements_list if not s.startswith('git+')]


setup(
    name='IVISION GridEngine Client',
    version=version,
    url='todo',
    author='Xiulong Yuan',
    author_email='yuanxl14@mails.tsinghua.edu.cn',
    description='The client side for IVISION GridEngine.',
    long_description=__doc__,
    packages=find_packages(
        '.', include=['ivision_gridengine_client', 'ivision_gridengine_client.*']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    setup_requires=['setuptools'],
    install_requires=install_requires,
    dependency_links=dependency_links,
    classifiers=[
        'Development Status :: 2 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points='''
        [console_scripts]
        ivision_run=ivision_gridengine_client.mlrun:mlrun
    '''
)
