import os, shutil
import boto3

def save_task(cfg):
    r=cfg['results']; c=cfg['cloud']
    src = r['dir']; arch = r['archive_dir']
    os.makedirs(arch, exist_ok=True)
    for f in os.listdir(src):
        if f.endswith(('.joblib','.json','.csv')):
            shutil.copy(os.path.join(src,f), arch)
    print("Local artifacts archived to", arch)

    if c['type']=='s3':
        s3 = boto3.client('s3')
        for f in os.listdir(src):
            path=os.path.join(src,f)
            key = os.path.join(c['s3_key_prefix'],f)
            s3.upload_file(path, c['s3_bucket'], key)
            print(f"Uploaded {f} to s3://{c['s3_bucket']}/{key}")