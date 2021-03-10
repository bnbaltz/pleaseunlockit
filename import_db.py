import dbm.gnu
import sys

url_uuid = dbm.open("url_uuid.db", "c")
lines = list(set([x.strip() for x in open(sys.argv[1], "r").readlines()]))
for line in lines:
    url_uuid[line.split(":")[0].split("-q")[-1]] = line.split(":")[1]