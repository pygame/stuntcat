from setuptools import setup, find_packages

setup(
    name='stuntcat',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: pygame',
        'Topic :: Games/Entertainment :: Arcade',
    ],
    license='LGPL',
    author='stuntcat team',
    author_email='stuntcat@pygame.org',
    maintainer='stuntcat team',
    maintainer_email='stuntcat@pygame.org',
    description='Stuntcat is the first pygame 2 community game.',
    include_package_data=True,
    long_description='stuntcat is the first pygame 2 community game.',
    package_dir={'stuntcat': 'stuntcat'},
    packages=find_packages(),
    # package_data={'stuntcat': []},
    url='https://github.com/pygame/stuntcat',
    install_requires=['pygame'],
    version='0.0.1dev',
    entry_points={
        'console_scripts': [
            'stuntcat=stuntcat.cli:main',
        ],
    },
)
