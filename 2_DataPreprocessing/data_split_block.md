```python
def data_block_split(data, batch_size=128000, n_block=None):
    from tqdm import tqdm
    block_list = []
    if n_block is None:
        n_block = int(data.shape[0]/batch_size) + 1
    print('Splited to', n_block, 'blocks')
    
    for n in tqdm(range(n_block)):
        index_start = n * batch_size
        index_end = (n + 1) * batch_size
        block_list.append(data[index_start:index_end])
    return block_list
 ```
