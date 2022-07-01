#!/usr/bin/env python3

import datetime

from warcio import ArchiveIterator, WARCWriter

def main():
    for cdx_line in open("data/SLAC.cdx"):
        cdx = parse_cdx_line(cdx_line)
        rec = rewrite(cdx)
        new_path = cdx["path"].replace(".warc", "_2022.warc.gz")
        write_record(rec, new_path)

def rewrite(cdx):
    rec = get_record(cdx["path"], cdx["offset"])
    if rec.rec_type == "response":
        rec.rec_headers["WARC-Creation-Date"] = rec.rec_headers["WARC-Date"]
        rec.rec_headers["WARC-Source-URI"] = rec.rec_headers["WARC-Target-URI"]
        rec.rec_headers["WARC-Target-URI"] = cdx["url"]
        rec.rec_headers["WARC-Date"] = cdx["datetime"]
    return rec

def parse_cdx_line(cdx_line):
    cdx_line = cdx_line.strip()
    parts = cdx_line.split(' ')
    return {
        "url": parts[2],
        "datetime": parse_datetime(parts[1]),
        "offset": int(parts[8]),
        "path": f"data/{parts[9]}"
    }

def get_record(path, offset):
    fh = open(path, "rb")
    fh.seek(offset)
    warc = ArchiveIterator(fh)
    return next(warc)

def parse_datetime(s):
    dt = datetime.datetime.strptime(s, "%Y%m%d%H%M%S")
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def write_record(rec, path):
    fh = open(path, "ab")
    writer = WARCWriter(fh, gzip=True)
    writer.write_record(rec)
    fh.close()

if __name__ == "__main__":
    main()
