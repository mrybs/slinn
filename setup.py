from setuptools import setup

def readme():
    with open('README.md', 'r') as f:
        return f.read()
    
templates = ['firstrun', 'example']


setup(name='slinn',
      version='2.2.3',
      description='A HTTPS and HTTP server framework',
      packages=['slinn', 'slinn.templates', 'slinn.guides'] + ['slinn.templates.' + template for template in templates],
      package_data={'slinn': ['default/*.*']} | {'slinn.templates.' + template: ['data/*.css', 'data/*.html', 'config.json'] for template in templates},
      author='Mark Radin',
      author_email='mrybs2@gmail.com',
      url='https://slinn.miotp.ru/',
      long_description=readme(),
      long_description_content_type='text/markdown',
      python_requires='>=3.11',
      zip_safe=True)
