import os

def handler(event, context):

    for root, dirs, files in os.walk('/mnt/efs'):
        for filename in files:
            print(filename)

    return {}
