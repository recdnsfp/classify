#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# rf.py: implement RandomForest classifier
#
# Copyright (C) 2017 by Paweł Foremski <pjf@foremski.pl>
# Licensed under GNU GPL v3, <https://www.gnu.org/licenses/gpl-3.0.html>
#

import common
import pickle
import argparse
from sklearn.ensemble import RandomForestClassifier

def train(X, Y, store):
	cls = RandomForestClassifier(n_jobs=-1)
	cls.fit(X, Y)

	if store: pickle.dump(cls, open(store, "wb"))

	return cls

def main():
	prs = argparse.ArgumentParser(description='Train/test DNS rec. server model: Random Forest')
	common.main(prs, train, common.load, common.test)

if __name__ == "__main__": main()
