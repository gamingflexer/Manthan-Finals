#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# banner file

# import
from lib.color import *

class Banner:
	def banner(self):
		print("\n")

	def usage(self,_exit_=False):
		self.banner()
		print ("Program runnung to find information from mail. Please be paitent")
		if _exit_: exit(0)