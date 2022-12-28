#!/usr/bin/env python3

import base64
import csv
import gzip
import hashlib
import os
import pathlib
import pprint
import shutil
import urllib.request


def load_manifest_data(f):
    rows = []
    with open(f, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for k in row.keys():
                if not row[k]:
                    continue
                row[k] = row[k].strip()
            if all(not x for x in row.values()):
                break
            if not row['LINK']:
                continue
            if row['LINK'].startswith('curl'):
                l = row['LINK']
                row['CMD'] = l
                row['LINK'] = l[l.find("'")+1:l.rfind("'")]
            rows.append(row)
    return rows


def to_path(l):
    assert '://' in l, l
    assert '?' in l, l
    assert '+' in l, l

    baseurl, _ = l.split('+')

    proto, p = l.split('://')
    p, qs = p.split('?')
    return pathlib.Path(p)


def report_progress(chunk_number, chunk_size, full_size):
    if (chunk_number % 10000) == 0:
        return
    downloaded = chunk_number*chunk_size
    if full_size == -1:
        print('.', end='', flush=True)
    else:
        print('\r%04.2f%%' % downloaded/full_size, end='', flush=True)


def filename(url):
    p = to_path(url)
    if p.suffix not in ('.gz',):
        return pathlib.Path(p.name)
    return pathlib.Path(p.stem)


def download(url):
    p = to_path(url)

    fn_b64 = p.name+'.b64'
    if not os.path.exists(fn_b64):
        print('Downloading', url, 'to', fn_b64, end=' ', flush=True)
        fn, headers = urllib.request.urlretrieve(url, filename=fn_b64, reporthook=report_progress)
        assert fn == fn_b64, (fn, fn_64)
        print(' Done!')

    if not os.path.exists(p.name):
        print('Decoding base64', fn_b64, 'to', p.name, '...', end=' ', flush=True)
        with open(p.name, 'wb') as f:
            f.write(base64.b64decode(open(fn_b64, 'rb').read()))
        print(' Done!')

    if p.suffix not in ('.gz',):
        return pathlib.Path(p.name)

    if not os.path.exists(p.stem):
        print('Decompressing', p.name, 'to', p.stem, '...', end=' ', flush=True)
        with gzip.open(p.name, 'rb') as f_in:
            with open(p.stem, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(' Done!')

    return pathlib.Path(p.stem)


def check(fn, h):
    print('Checking', fn, '...', end=' ', flush=True)
    m = hashlib.sha1()
    with open(fn, 'rb') as f:
        m.update(f.read())
        while True:
            break
            data = f.read(1024*1024)
            if not data:
               break
            m.update(data)
    nh = m.hexdigest()
    print('got', h, 'needed', nh, end=' ', flush=True)
    matches = (h == nh)
    if matches:
        print('MATCHES!')
    else:
        print("DOESN'T MATCH!")
    return matches


REMOVE = False


def main(args):
    for f in args:
        print()
        print(f)
        print('-'*75)
        data = load_manifest_data(f)
        for r in data:
            fn = filename(r['LINK'])
            assert fn.suffix in ('.gds', '.oas'), (fn, r)

            matches = None
            if fn.exists():
                matches = check(fn, r['SHASUM'])
                if not matches and REMOVE:
                    d = pathlib.Path()
                    for p in d.glob(fn.name+'*'):
                        print('Removing ', p)
                        p.unlink()

            if not fn.exists():
                fn = download(r['LINK'])
                matches = check(fn, r['SHASUM'])

            assert fn.exists(), (fn, r)

            assert matches is not None, (matches, r)
            r['VALID'] = matches

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
