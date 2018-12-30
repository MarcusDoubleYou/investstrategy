
from setuptools import setup, find_packages

setup(
    name='strategy',
    version='0.2.4',
    author='iMrx',
    author_email='developer@irmx.com',
    url='https://github.com/MarcusDoubleYou/investstrategy',
    packages=find_packages(),
    # package=['strategy'],
    description='evaluates and develops trading strategies',
    classifiers=['License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Topic :: Global :: Investment'],
    license='GNU',
    platforms=['any']

)
