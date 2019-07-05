```
# _*_coding:utf-8 _*_
import logging
import time
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import fasttext
#训练模型
start=time.clock()
classifier = fasttext.supervised("news_fasttext_train_2.txt","news_fasttext.model",label_prefix="__label__")
end=time.clock()
total_time=end-start
print("总耗时:"+str(total_time))
#load训练好的模型
#classifier = fasttext.load_model('news_fasttext.model.bin', label_prefix='__label__')
#测试模型
#load训练好的模型
#import fasttext
result = classifier.test("news_fasttext_test_2.txt")
print(result.precision)
print(result.recall)
```