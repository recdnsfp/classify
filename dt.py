#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# dt.py: implement DecisionTree classifier
#
# Copyright (C) 2017 by Paweł Foremski <pjf@foremski.pl>
# Licensed under GNU GPL v3, <https://www.gnu.org/licenses/gpl-3.0.html>
#

import common
import pickle
import argparse
from sklearn import tree

def train(X, Y, store):
	cls = tree.DecisionTreeClassifier()
	cls.fit(X, Y)

	if store: pickle.dump(cls, open(store, "wb"))
	return cls

def main():
	prs = argparse.ArgumentParser(description='Train/test DNS rec. server model: Decision Tree')
	prs.add_argument('--viz', help='store Graphviz representation in given path')

	args, cls, names = common.main(prs, train, common.load, common.test)

	if args.viz:
		tree.export_graphviz(cls, args.viz,
			feature_names=names, class_names=["ok", "hijack"],
			filled=True, impurity=False)

if __name__ == "__main__": main()
