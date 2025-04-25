from pathlib import Path
import zipfile
import re

def check_file(filename: Path):
    print(f"Checking file if exists: {filename}...", end=' ')
    exist = filename.exists()
    if not exist:
        print("Not found")
    else:
        print("Found")
    return exist

def print_dictinfo(info: 'dict[str, str]'):
    print('=' * 32)
    for k, v in info.items():
        print(f"{k}={v}")
    print('=' * 32)

def zip_files(zipfilename: str, files: 'list[str]'):
    print(f"Zipping {len(files)} files to {zipfilename}...")
    with zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for f in files:
            zf.write(f)
    print("OK")
    
def match_and_get(regex: str, pattern: str) -> str:
    matched = re.search(regex, pattern)
    if not matched:
        raise AssertionError('Failed to match: for pattern: %s regex: %s' % pattern, regex)
    return matched.group(1)