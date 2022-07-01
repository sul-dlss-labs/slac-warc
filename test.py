import rewrite

def test_parse_cdx():
    line = "slac.stanford.edu/accel/pepii/binlist_gif/59749.gif 19950822000000 http://www.slac.stanford.edu/accel/pepii/binlist_gif/59749.gif image/gif 200 JG4BK7JIGCLZG3PIEPDK46AJ3AC2XUAG - - 36862714 SLAC_1996.warc"
    cdx = rewrite.parse_cdx_line(line)
    assert cdx["url"] == "http://www.slac.stanford.edu/accel/pepii/binlist_gif/59749.gif"
    assert cdx["datetime"] == "1995-08-22T00:00:00Z"
    assert cdx["offset"] == 36862714
    assert cdx["path"] == "data/SLAC_1996.warc"

def test_read_record():
    rec = rewrite.get_record("data/SLAC_1996.warc", 777386)
    assert rec.rec_headers["WARC-Target-URI"] == "http://www.slac.stanford.edu/archive/1996/SLACVM/www/192/rl1162/01010008.corpse"
    assert rec.rec_headers["WARC-Date"] == "2014-09-24T20:13:56Z"

def test_rewrite():
    cdx_line = "slacvm.slac.stanford.edu/find/01010008.corpse 19950105000000 http://slacvm.slac.stanford.edu/FIND/01010008.corpse text/html 200 24NCU52QG67HBV3ZVXDFDIFIXBTZ64TQ - - 777386 SLAC_1996.warc"
    cdx = rewrite.parse_cdx_line(cdx_line)
    rec = rewrite.rewrite(cdx)
    assert rec.rec_headers["WARC-Target-URI"] == "http://slacvm.slac.stanford.edu/FIND/01010008.corpse"
    assert rec.rec_headers["WARC-Date"] == "1995-01-05T00:00:00Z"
    assert rec.rec_headers["WARC-Source-URI"] == "http://www.slac.stanford.edu/archive/1996/SLACVM/www/192/rl1162/01010008.corpse"
    assert rec.rec_headers["WARC-Creation-Date"] == "2014-09-24T20:13:56Z"
    print(rec.rec_headers)
