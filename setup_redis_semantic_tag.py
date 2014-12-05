# coding=utf-8
import redis
import json


def arr_in_arrs(arr, arrs):
    arrstrs = [','.join(sorted(arr)) for arr in arrs]
    arr = ','.join(sorted(arr))
    return arr in arrstrs


r = redis.Redis(host='localhost', port=6499)
r.delete("pynlpini")
with open("./pynlpini/model/semantic_tag.lst") as list_file:
    for line in list_file:
        line = line.strip().decode("utf-8")
        splits = line.split(chr(127))
        name = splits[0]
        tags = splits[1:]
        if len(tags) == 0 or (len(tags) == 1 and len(tags[0]) == 0):
            continue
        data = r.hget("pynlpini", name)
        if data is None:
            data = []
        else:
            data = json.loads(data)
        if not arr_in_arrs(tags, data):
            data.append(tags)
            r.hset("pynlpini", name, json.dumps(data, ensure_ascii=False))