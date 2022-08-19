from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read()

setup(name='pythonping',
      version='1.1.3',
      description='A simple way to ping in Python',
      url='https://github.com/alessandromaggio/pythonping',
      author='Alessandro Maggio',
      author_email='me@alessandromaggio.com',
      license='MIT',
      packages=['pythonping'],
      keywords=['ping', 'icmp', 'network'],
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: System Administrators',
            'Natural Language :: English'
      ],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
