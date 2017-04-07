#!/usr/bin/python
# -*- coding=utf-8 -*-

import multiprocessing
import xgx_seecourse_0223
import xgx_config
import xgx_comments_0223

'''
p = multiprocessing.Pool(processes=3)
lists = '2'
try:
    print xgx_config.session
    p.map(xgx_seecourse_0223.open_period,lists)

except KeyboardInterrupt:
    print '>>quit'
'''

for i in range(5):
    p = multiprocessing.Process(target=xgx_comments_0223.comments,args=(1,))
    p.daemon = True
    print multiprocessing.current_process().name
    p.start()
    p.join(1)
    print p.is_alive()
    
