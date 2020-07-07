import os

def handler(event, context):
    res = []
    
    f = open('/mnt/efs/test.txt', 'w')
    f.write("abc")
    f.close()

    for root, dirs, files in os.walk('/mnt/efs'):
        for filename in files:
            res.append(filename)

    return res
