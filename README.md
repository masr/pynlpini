Pynlpini -- the Chinese NLP full stack toolkit
===============================================

DESCRIPTION
-----------
The toolkit includes:

1. Chinese words segmentation
1. Chiense part of speech analysis
1. Location/Person Name/Organization entity detection
1. Impression extraction
1. Sentiment analysis
1. Semantic tag and semantic tree
1. Correlation between Chinese words and phrases
1. A web interface

INSTALLATION
------------
* Make sure you have python2.6.x or Python2.7.x and Python3 is not support.
* Install pipe

        sudo pip install pipe

* Install numpy and scipy (If you do not need correlation analysis, you can skip this step)

        sudo yum install blas blas-devel lapack lapack-devel python-devel
        sudo pip install numpy
        sudo pip install scipy
        sudo pip install six

* Install Flask (If you do not need a web interface, you can skip this step)

        sudo pip install flask

* Install libsvm-3.18 (If you do not need sentiment analysis, you can skip this step)

        cd lib
        unzip libsvm-3.18.zip
        cd libsvm-3.18
        make
        cd python
        make
        cp ../libsvm.so.2 ../../../pynlpini/lib/libsvm.so.2

* Install word2vec (If you do not need correlation analyze, you can skip this step)

        cd lib
        unzip word2vec.zip
        cd word2vec-read-only
        make

* Install CRF++-0.54 (For Seg, Pos, Ner and Impression, must have)

        cd lib
        gunzip CRF++-0.54.tar.gz
        tar -xvf CRF++-0.54.tar
        cd CRF++-0.54
        ./configure --prefix=/usr
        make
        sudo make install
        cd python
        python setup.py build
        sudo python setup.py install
        sudo ldconfig

* Download models, will take long time.

        ./refresh_model.sh

* There is two way to install Pynlpini

    1. `sudo python setup.py`  
    Please note that it will install scripts and models in system path like /usr/lib and will consume a little large space.
    2. You can just run locally with `export PYTHONPATH=<base-directory-of-pynlpini>` before running your python code


Test
--------------

* Run `./test/suite.sh`
* Above command will train data and generate the model in `tmp/model`, then load the model to do NLP job.
  This is useful to guide you to train model yourself.

Refresh the model
-----------------
Sometimes the official model will update with better accuracy, you can run below command :

        ./refresh_model.sh  #will take long time to download
        sudo python setup.py



Web interface
------------

* You can run below command to setup a web server with NLP function

        python -c "from pynlpini.web import web;web.run(port=7000,host='0.0.0.0')"

* But we recommend you to write a script to run the server such that debug mode can be enbled.

        from pynlpini.web import web
        web.run(port=7000,host='0.0.0.0',debug=True)

* If you first use one of the NLP function, it will be a little slow because the service will load the model at the first time.
  So, please be patient. It will be very fast after loading.

* ps: The semantic tag("语义标签") will consume a lot of memory.

