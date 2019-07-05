# [Bert][1]

---
```python
class IMDBProcessor(DataProcessor):
    """
    IMDB data processor
    """
    def _read_csv(self, data_dir, file_name):
        with tf.gfile.Open(data_dir + file_name, "r") as f:
            reader = csv.reader(f, delimiter=",", quotechar=None)
            lines = []
            for line in reader:
                lines.append(line)

        return lines

    def get_train_examples(self, data_dir):
        lines = self._read_csv(data_dir, "trainData.csv")

        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "train-%d" % (i)
            text_a = tokenization.convert_to_unicode(line[0])
            label = tokenization.convert_to_unicode(line[1])
            examples.append(
                InputExample(guid=guid, text_a=text_a, label=label))
        return examples

    def get_dev_examples(self, data_dir):
        lines = self._read_csv(data_dir, "devData.csv")

        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "dev-%d" % (i)
            text_a = tokenization.convert_to_unicode(line[0])
            label = tokenization.convert_to_unicode(line[1])
            examples.append(
                InputExample(guid=guid, text_a=text_a, label=label))
        return examples

    def get_test_examples(self, data_dir):
        lines = self._read_csv(data_dir, "testData.csv")

        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "test-%d" % (i)
            text_a = tokenization.convert_to_unicode(line[0])
            label = tokenization.convert_to_unicode(line[1])
            examples.append(
                InputExample(guid=guid, text_a=text_a, label=label))
        return examples

    def get_labels(self):
        return ["0", "1"]
```

```python
python run_classifier.py \
  --data_dir=$MY_DATASET \
  --task_name=imdb \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --output_dir=../output/ \
  --do_train=true \
  --do_eval=true \
  --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
  --max_seq_length=200 \
  --train_batch_size=16 \
  --learning_rate=5e-5\
  --num_train_epochs=2.0
```

---
[1]: https://www.jianshu.com/p/9f32d882321b

