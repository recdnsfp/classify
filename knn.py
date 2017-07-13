#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# knn.py: implement k-NN classifier
#
# Copyright (C) 2017 by Paweł Foremski <pjf@foremski.pl>
# Licensed under GNU GPL v3, <https://www.gnu.org/licenses/gpl-3.0.html>
#

import common
import pickle
import argparse
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# train and optionally store
def train(X, Y, store):
	cls = KNeighborsClassifier(2)
	cls.fit(X, Y)

	if store: pickle.dump(cls, open(store, "wb"))
	return cls

def load(path):
	return pickle.load(open(path, "rb"))

def test(cls, ids, X, Y):
	ok = 0
	err = 0

	labels = cls.classes_
	P = cls.predict_proba(X)
	for pid, x, proba, y in zip(ids, X, P, Y):
		i = np.argmax(proba)
		l = labels[i]

		if proba[i] < 1:
			print "probability for id %d being %d is %g" % (pid, l, proba[i])

		if l == y:
			ok += 1
		else:
			print "error: %d is %s, but was classified as %s" % (pid, y, l)
			err += 1

	return (ok, err)

def main():
	prs = argparse.ArgumentParser(description='Train/test DNS server model: k-NN')
	common.main(prs, train, load, test)

if __name__ == "__main__": main()
