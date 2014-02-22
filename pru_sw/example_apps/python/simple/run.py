#!/usr/bin/env python
# vim: ts=2:sw=2:tw=80:nowrap

from subprocess import Popen
import os
os.putenv('LD_LIBRARY_PATH',
  os.getenv('LD_LIBRARY_PATH','') + \
  ':' + os.path.join(os.path.dirname(__file__), '../../../app_loader/lib')
)

os.system('python simple.py')
