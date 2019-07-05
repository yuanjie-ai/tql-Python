[<h1 align = "center">:rocket: Facets :facepunch:</h1>][1]

---
## 1. Enabling Usage in Jupyter Notebooks
```sh
git clone https://github.com/PAIR-code/facets
cd facets
jupyter nbextension install facets-dist/
```

## 2. Dive demo Jupyter notebook
```python
# Display the Dive visualization for this data
def facets_display(df):
    from IPython.core.display import display, HTML
    
    jsonstr = df.to_json(orient='records')
    HTML_TEMPLATE = """<link rel="import" href="/nbextensions/facets-dist/facets-jupyter.html">
            <facets-dive id="elem" height="600"></facets-dive>
            <script>
              var data = {jsonstr};
              document.querySelector("#elem").data = data;
            </script>"""
    html = HTML_TEMPLATE.format(jsonstr=jsonstr)
    display(HTML(html))

import pandas as pd
from sklearn.datasets import load_iris
df = pd.DataFrame(load_iris().data, columns=['a', 'b', 'c', 'd'])
```












---
[1]: https://github.com/PAIR-code/facets
