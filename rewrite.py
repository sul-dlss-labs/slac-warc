#!/usr/bin/env python3

import re
import datetime

from warcio import ArchiveIterator, WARCWriter

def main():
    fh = open("data/SLAC_rewrites.warc", "ab")
    writer = WARCWriter(fh, gzip=False)
    for cdx_line in open("data/SLAC.cdx"):
        cdx = parse_cdx_line(cdx_line)
        rec = get_record(cdx)
        new_rec = rewrite(rec, cdx)
        if new_rec:
            writer.write_record(new_rec)
    fh.close()

def rewrite(rec, cdx):
    """
    If the URL and datetime in the CDX entry are different from what is 
    found in the WARC record, rewrite the WARC record to use the new URL 
    and datetime while recording the old ones using the WARC-Creation-Date 
    and WARC-Source-URI headers. If no change is needed return None.
    """

    if rec.rec_type != "response":
        return None

    h = rec.rec_headers
    updated = False
    if cdx["datetime"] != h["WARC-Date"]:
        h["WARC-Creation-Date"] = h["WARC-Date"]
        h["WARC-Date"] = cdx["datetime"]
        updated = True

    if cdx["url"] != h["WARC-Target-URI"]:
        h["WARC-Source-URI"] = h["WARC-Target-URI"]
        h["WARC-Target-URI"] = cdx["url"]
        updated = True

    if updated:
        return rec
    else:
        return None

def parse_cdx_line(cdx_line):
    """
    Parse a CDX line into a JSON object.
    """
    cdx_line = cdx_line.strip()
    parts = cdx_line.split(' ')
    cdx = {
        "url": parts[2],
        "datetime": parse_datetime(parts[1]),
        "offset": int(parts[8]),
        "path": f"data/{parts[9]}"
    }
    return cdx

def get_record(cdx):
    """
    Get a WARC record using the CDX entry.
    """
    fh = open(cdx["path"], "rb")
    fh.seek(cdx["offset"])
    warc = ArchiveIterator(fh)
    return next(warc)

def parse_datetime(s):
    dt = datetime.datetime.strptime(s, "%Y%m%d%H%M%S")
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def write_record(rec, path):
    fh = open(path, "ab")
    writer = WARCWriter(fh, gzip=False)
    writer.write_record(rec)
    fh.close()

if __name__ == "__main__":
    main()
