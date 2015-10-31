from distutils.core import setup

setup(name='kao_flask_auth',
      version='0.1.1',
      description="",
      author='Chris Loew',
      author_email='cloew123@gmail.com',
      packages=['kao_flask_auth',
                'kao_flask_auth.Controllers'],
      install_requires=['itsdangerous',
                        'passlib']
     )