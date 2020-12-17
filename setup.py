from setuptools import setup

setup(name='scholaris',
      version='0.1.0',
      description='A StudentVue Grade Viewew',
      url='https://github.com/SamC302/scholaris',
      author='Kandasamy Chokkalingam',
      author_email='kck.choks@gmail.com',
      license='GNU GPL v3',
      packages=['scholaris'],
      install_requires=[
          'arrow',
          'studentvue',
          'rich'
      ],
      include_package_data=True,
      entry_points = {
          'console_scripts': ['scholaris-view=scholaris.main:main'],
      },
      zip_safe=False
      )