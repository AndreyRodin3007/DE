import pandas as pd, os, joblib, json
from sklearn.metrics import accuracy_score,precision_score, recall_score, f1_score

def evaluate_task(cfg):
    r=cfg['results']
    df = pd.read_csv(os.path.join(r['dir'], r['test_csv']))
    model = joblib.load(os.path.join(r['dir'], r['model']))
    scaler = joblib.load(os.path.join(r['dir'], r['scaler']))
    X = df.drop('diagnosis',axis=1); y = df['diagnosis']
    pred = model.predict(scaler.transform(X))
    metrics = {
        'accuracy': accuracy_score(y,pred),
        'precision': precision_score(y,pred),
        'recall': recall_score(y,pred),
        'f1': f1_score(y,pred)
    }
    with open(os.path.join(r['dir'],r['metrics']), 'w') as f:
        json.dump(metrics,f,indent=4)
    print("Metrics:", metrics)