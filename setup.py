from setuptools import setup, find_packages

setup(name='relationalpandas',
      version='1.0',
      description='relationalpandas',
      author='Florian Teich',
      author_email='florianteich@gmail.com',
      url='https://github.com/FlorianTeich/RelationalPandas',
      packages=find_packages(include=['relationalpandas', 'relationalpandas.*']),
      python_requires=">=3.6",
     )