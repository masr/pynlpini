Pynlpini -- python中文NLP工具集
===============================================

功能介绍
-----------

1. 中文分词
1. 中文词性标注
1. 地名，人名和组织名的提取
1. 印象提取
1. 情感分析（尚不支持）
1. 语义标签和概念树的分析
1. 中文词语和短语的相关性
1. 网页版的NLP接口


安装
------------
* 本工具集只支持python2.6.x或Python2.7.x，不支持python3
* 安装pipe

        sudo pip install pipe

* 安装 numpy和scipy（如果你不需要词语或短语的相关性分析，可以忽略这一步）

        sudo yum install blas blas-devel lapack lapack-devel python-devel
        sudo pip install numpy
        sudo pip install scipy
        sudo pip install six

* 安装Flask（如果你不需要一个网页板的NLP接口，可以忽略这一步）

        sudo pip install flask

* 安装libsvm-3.18（如果你不需要情感分析的功能，可以忽略这一步）

        cd lib
        unzip libsvm-3.18.zip
        cd libsvm-3.18
        make
        cd python
        make
        cp ../libsvm.so.2 ../../../pynlpini/lib/libsvm.so.2

* 安装word2vec（如果你不需要词语或短语的相关性分析，可以忽略这一步）

        cd lib
        unzip word2vec.zip
        cd word2vec-read-only
        make

* 安装CRF++-0.54（必须安装）

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
        
* 安装redis （如果你不需要语义标签的功能可以跳过这一步）

        cd lib
        unzip redis.zip

* 下载模型，这个步骤耗时较长，取决于你的网速

        ./refresh_model.sh
    
    或者你也可以查看`http://www.dataini.com/projects/pynlpini/models/`目录下

* 加载语义标签的模型到redis，之后速度更快（如果你不需要语义标签的功能可以跳过这一步）

        python setup_redis_semantic_tag.py


* 有两种方式使用pynlpini

    1. `sudo python setup.py`  
    这一步会将pynlpini安装到系统路径下，会占用比较大的空间。然后在你的代码中可以直接`import pynlpini`.
    2. 在执行你的python代码前，先执行`export PYTHONPATH=<base-directory-of-pynlpini>`


测试
--------------

* 运行 `./test/suite.sh`
* 以上命令会用pynlpini训练数据并再`test/model`下生成model文件，然后验证模型和pynlpini代码的正确性。
  如果你自己想训练数据的话，可以借鉴上述过程。

更新模型
-----------------

* 有时，官方的模型模型会更新，请运行以下命令更新模型：

        ./refresh_model.sh  #will take long time to download
        sudo python setup.py



网页版接口
------------

* 你可以输入以下命令启动这个NLP小网站

        python -c "from pynlpini.web import web;web.run(port=7000,host='0.0.0.0')"

* 但是我建议你自己写一个脚本运行，这样可以使用调试功能

        from pynlpini.web import web
        web.run(port=7000,host='0.0.0.0',debug=True)

* 当你第一次点击进入某一个功能块时，页面可能会比较慢，因为在加载模型请耐心等待。

示例
------------

* 分词

        >>> from pynlpini import SegTagger
        >>> tagger = SegTagger()
        >>> tagger.seg_as_iter(u"巴勒斯坦和以色列") # will return a generator
        <generator object seg_as_iter at 0x155f5f0>
        >>> list(tagger.seg_as_iter(u"巴勒斯坦和以色列"))
        [u'巴勒斯坦', u'和', u'以色列']
        >>> tagger.seg_as_txt(u"巴勒斯坦和以色列")
        >>> u'巴勒斯坦 和 以色列'

* 词性标注

        >>> from pynlpini import SegTagger
        >>> from pynlpini import PosTagger
        >>> tagger = PosTagger(SegTagger())
        >>> tagger.pos_as_iter(u"巴勒斯坦和以色列") # will return a generator
        <generator object seg_as_iter at 0x155f5f0>
        >>> list(tagger.pos_as_iter(u"巴勒斯坦和以色列"))
        [(u'巴勒斯坦', 'nr'), (u'和', 'cc'), (u'以色列', 'nr')]
        
    关于nr和cc的含义请参照下表：

        [1]     AD    副词  Adverbs
        [2]     AS    语态词  --- 了
        [3]     BA    把
        [4]     CC    并列连接词（coordinating conj）
        [5]     CD    许多(many),若干（several),个把(a,few)
        [6]     CS    从属连接词（subording conj）
        [7]     DEC   从句“的”
        [8]     DEG   修饰“的”
        [9]     DER   得 in V-de-const, and V-de R
        [10]    DEV   地 before VP
        [11]    DT    限定词   各（each),全(all),某(certain/some),这(this)
        [12]    ETC   for words 等，等等
        [13]    FW    外来词 foreign words
        [14]    IJ     感叹词  interjecton
        [15]    JJ     名词修饰语
        [16]    LB    被,给   in long bei-const
        [17]    LC    方位词
        [18]    M     量词
        [19]    MSP   其他小品词（other particle） 所
        [20]    NN    口头名词、others
        [21]    NR    专有名词
        [22]    NT    时间名词  （temporal noun）
        [23]    OD    序数（ordinal numbers）
        [24]    ON    拟声法（onomatopoeia）
        [25]    P      介词   （对，由于，因为）(除了 “把”和“被”)
        [26]    PN    代词
        [27]    PU    标定符号
        [28]    SB    in short bei-const 被，给
        [29]    SP    句尾语气词
        [30]    VA    表语形容词（predicative adjective）
        [31]    VC    是
        [32]    VE    有（have，not have ,有，无，没，表示存在的词
        [33]    VV    情态动词、  动词、possess/拥有 ，rich/富有,具有

* 实体识别

        >>> from pynlpini import NerTagger
        >>> tagger = NerTagger()
        >>> list(tagger.ner_as_iter(u"尤以收录周恩来总理\n\n吊脚楼茶馆，坐落在栋梁河边的悬崖上")) #change generator to list
        [(u'周恩来', 'PER', 4), (u'栋梁河', 'LOC', 20)]
        
    PER表示人名，LOC表示地名，ORG表示组织名。
    里面的数字代表实体在原文本中的位置。
    
* 印象提取

        >>> from pynlpini import ImpressionExtractor
        >>> from pynlpini import PosTagger
        >>> from pynlpini import SegTagger
        >>> extractor = ImpressionExtractor(PosTagger(SegTagger()))
        >>> list(extractor.extract(u"参观的人不多，这家私房菜的菜式口味偏重，秘制酱汁是他家的特色，非常合我的胃口！\n做法很独特，味道也正！\n和大多数私房菜一样，食锦记也有属于自己的精致餐具。。。。从外面看还是不错的，特有感觉的一家店，这里是个装修非常精致典雅的小茶馆，感觉是个很好的饭店。"))
        [(u'人不多', u'人不多', 3), (u'口味偏重', u'口味偏重', 15), (u'做法独特', u'做法很独特', 40),
         (u'装修精致典雅', u'装修非常精致典雅', 103), (u'饭店好', u'很好的饭店', 120), (u'私房菜一样', u'私房菜一样', 56)]
        
    第一个参数是抽象过的印象，会去除一些停用词，副词，并对语序重序组织
    
    第二个参数是没有经过抽象的原文本中的印象
    
    第三个参数是该印象在原文本中的位置

* 语义标签和概念树

        from pynlpini import SemanticTagger
        analyzer = SemanticTagger()
        analyzer.get_tags(u'大卫·贝克汉姆')
        [[u'足球明星',u'英国',u'名人',u'体育',u'世界名人',u'人物',u'体育人物',u'各星座名人',u'国际足球明星',u'当代名人',u'知名人物']]

    因为叫同一个名字的事物可能有很多，那么程序无法通过仅仅参考一个名字就得出具体的事物，所以只能给出标签云的列表。
    因为这里贝克汉姆只有一个，所以标签云的个数只有一个。

        from pynlpini import SemanticHierarchyAnalyzer
        analyzer = SemanticHierarchyAnalyzer()
        analyzer.get_hierarchy_tags(u'电力')
        [u"电能", u"能源", u"技术"]

    返回上级的概念，排在越前面的概念粒度越小，并且被包含在后面一个概念中。


* 词语和短语间的相关性

        >>> from pynlpini import Word2Vector
        >>> word2vector = Word2Vector.get_word_model()
        >>> word2vector.most_similar([u"香辣蟹"])
        [(u'辣炒', 0.60607582330703735), (u'芒果螺', 0.5756109356880188), (u'香辣', 0.5698847770690918), (u'乐蟹', 0.5589337944984436), (u'椒盐', 0.55684047937393188), (u'白灼基', 0.54266512393951416), (u'石斑鱼', 0.53376764059066772), (u'龙虾粥', 0.53085452318191528), (u'濑尿虾', 0.52900636196136475), (u'富贵虾', 0.52676904201507568)]

    元组排在越前面的表示离给定的词语越相关，其中的数字表示余弦距离，1为最相关，0为不相关。

        >>> word2vector.most_similar([u"香辣蟹", u"啤酒"], topn=5)
        [(u'生啤', 0.57949370145797729), (u'白灼基', 0.57108491659164429), (u'龙虾粥', 0.54202723503112793), (u'扎啤', 0.53303158283233643), (u'蛤蜊', 0.52820837497711182)]
    
    这里还可以对词语的组合求相关性，topn指定返回多少个。
    
        >>> word2vector.doesnt_match([u"香辣蟹", u"啤酒", u"椒盐", u"地铁站"])
        u'地铁站'
        
    返回词语数组中和别的词语最不相关的，比较“另类”的词语。
    
        >>> word2vector.similarity(u"椒盐", u"香辣蟹")
        0.55684057605295545
        
    返回余弦值
        
        >>> word2vector.n_similarity([u"椒盐", u"香辣蟹"], [u"地铁站", u"出去"])
        -0.066575012129364952
    
    返回词语组合间的余弦值
    
        >>> phrase2vector = Word2Vector.get_phrase_model()
        >>> phrase2vector.most_similar([u"鼓楼大街",u"北京"])
        [(u'地安门外大街', 0.6079782247543335), (u'外大街', 0.59636682271957397), (u'前门', 0.59394305944442749), (u'西城区', 0.59110575914382935), (u'鼓楼东大街', 0.58657485246658325), (u'胡同', 0.58092218637466431), (u'烟袋斜街', 0.57343500852584839), (u'南锣鼓巷', 0.5612947940826416), (u'鼓楼', 0.5537528395652771), (u'平安大街', 0.5517389178276062)]
        
    这里可以对一个短语（词语的组合）进行相关性分析，得到的也同样是相关的短语。
        
     
TO DO
------------

* 对于中文繁体的支持
* 支持和完善情感分析
* 增加模糊智能匹配的功能
* TF-IDF


