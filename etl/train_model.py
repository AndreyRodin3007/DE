import pandas as pd, os, joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def train_task(cfg):
    inpath = os.path.join(cfg['results']['dir'], cfg['results']['preproc_csv'])
    df = pd.read_csv(inpath)
    X = df.drop('diagnosis',axis=1); y = df['diagnosis']
    ts = cfg['model']['test_size']; rs=cfg['model']['random_state']
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=ts,random_state=rs)
    scaler = StandardScaler(); X_train_s=scaler.fit_transform(X_train); X_test_s = scaler.transform(X_test)
    model = LogisticRegression(max_iter=cfg['model']['max_iter']); model.fit(X_train_s,y_train)
    r = cfg['results']
    joblib.dump(model, os.path.join(r['dir'], r['model']))
    joblib.dump(scaler, os.path.join(r['dir'], r['scaler']))
    pd.concat([X_test, y_test], axis=1).to_csv(os.path.join(r['dir'], r['test_csv']), index=False)
    print("Model & scaler saved")