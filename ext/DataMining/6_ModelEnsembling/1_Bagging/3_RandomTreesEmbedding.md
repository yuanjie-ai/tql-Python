<h1 align = "center">:rocket: RandomTreesEmbedding :facepunch:</h1>

---
RandomTreesEmbedding实现了数据的无监督学习。其编码方式以1到k的方式，从高维数据到稀疏二进制编码。这种编码方式很有效，可以用作其他学习任务的基础。通过选择树的个数和深度可以决定该编码的大小和稀疏程度。在集成中的每个树，其编码包括了每个完整的树。编码的最大大小为n_estimators*2**max_depth，森林中树叶的最大值。邻近的数据点很可能具有相同的树叶节点，其间的转换时隐式、非参数的密度估计。
