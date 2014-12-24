from distutils.core import setup
import sys

if sys.version_info[:2] < (2, 6) or sys.version_info[0] == 3:
    raise RuntimeError('Python version 2.6, 2.7 required. And python3 is not support.')

setup(name='pynlpini',
      version='0.10',
      description='Chinese NLP full stack toolkit',
      author='Masr',
      author_email='masrin@foxmail.com',
      packages=['pynlpini', 'pynlpini.common', 'pynlpini.impression', 'pynlpini.lib', 'pynlpini.lib.gensim',
                'pynlpini.ner', 'pynlpini.pos', 'pynlpini.seg', 'pynlpini.web', 'pynlpini.word2vec',
                "pynlpini.keyword"],
      package_data={'pynlpini': ['model/*', 'dict/*', 'web/*', 'lib/*.so.2']},
      requires=['pipe']
)
