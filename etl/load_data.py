import pandas as pd, os, yaml

def load_data_task(cfg):
    raw = cfg['data']['raw_path']
    df = pd.read_csv(raw, header=None)
    cols = ['id','diagnosis'] + [f'col{i}' for i in range(df.shape[1]-2)]
    df.columns = cols
    out = os.path.join(cfg['results']['dir'], cfg['results']['raw_csv'])
    os.makedirs(cfg['results']['dir'], exist_ok=True)
    df.to_csv(out, index=False)
    print(f"Loaded raw data: {df.shape} -> {out}")