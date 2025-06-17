import pandas as pd, os

def preprocess_task(cfg):
    inp = os.path.join(cfg['results']['dir'], cfg['results']['raw_csv'])
    df = pd.read_csv(inp)
    df = df.dropna().drop(columns=['id'], errors='ignore')
    df['diagnosis'] = df['diagnosis'].map({'M':1,'B':0})
    out = os.path.join(cfg['results']['dir'], cfg['results']['preproc_csv'])
    df.to_csv(out, index=False)
    print(f"Preprocessed: {df.shape} -> {out}")