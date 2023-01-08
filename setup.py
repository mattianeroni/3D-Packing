from setuptools import setup, find_packages

setup(
    name='3D-Packing',
    version='0.0.1',
    description='An algorithm for solving the Pallet Loading Problem with stability and fragility constraints.',
    author='Mattia Neroni, Ph.D, Eng.',
    author_email='mattia.neroni@ahead-research.com',
    url='https://github.com/mattianeroni/3D-Packing',
    #package_dir = {
    #    'ssa': 'ssa'
    #},
    packages=[
        'src'
    ],
    python_requires='>=3.9',
    classifiers=[
        "Development Status :: 3 - Alpha"
    ]
)