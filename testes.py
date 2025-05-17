import json
import pandas as pd
import requests

df = pd.read_json("cotacoes.json", orient="index")
print(df.head)