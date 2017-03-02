#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

def renameFile(path):
    paths = os.listdir(path)
    j = 1
    for i in paths:
        jj = str(j)
        file = os.path.join(path,i)
        if os.path.isdir(file):
            continue
        newname = os.path.join(path, jj + ".jpg")
        j += 1
        os.rename(file, newname)
        print newname
    return 

if __name__ == "__main__":
    renameFile('/root/Desktop/tu2')

