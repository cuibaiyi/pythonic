import hashlib
file_path = 'C:\\Users\\cby\\Desktop\\dict.txt'
file_newpath = 'C:\\Users\\cby\\Desktop\\sha256.txt'
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        data = line.strip()
        data_sha = hashlib.sha256(data.encode('utf-8')).hexdigest()
        with open(file_newpath, 'a', encoding='utf-8') as w:
            w.write(data_sha.upper() + '\n')
