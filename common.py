#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 by Paweł Foremski <pjf@foremski.pl>
# Licensed under GNU GPL v3, <https://www.gnu.org/licenses/gpl-3.0.html>
#

import ArffReader

id_field = "probe_id"
gt_field = "hijacked"

ignored_fields = [
	id_field, gt_field,
	"ping_from", "ping_asn", "ping_net",

#	"ping_min", "tr_hopcount", "tr_aslen", "tr_exit_rtt", "tr_exit_asn", "tr_exit_net",
#	"whoami2_rt", "whoami2_ip", "whoami2_asn", "whoami2_net",
]

# read samples
def read_samples(path):
	ar = ArffReader.ArffReader(open(path))
	ids = []
	X = []
	Y = []
	for row in ar:
		# append all numeric fields in current row into x
		x = []
		for field in ar.fields:
			if field in ignored_fields:
				continue
			elif ar.types[field].startswith("numeric"):
				value = float(row[field])
				x.append(int(round(value)))

		# add to X/Y database
		X.append(x)
		if gt_field in row:
			Y.append(int(row[gt_field]))

		# keep track of probe_id
		ids.append(int(row[id_field]))

	# add names
	names = []
	for field in ar.fields:
		if field in ignored_fields: continue
		elif ar.types[field].startswith("numeric"):
			names.append(field)

	print "%s: read %d samples" % (path, len(X))
	return (ids, X, Y, names)

def classify(cls, ids, X):
	L = cls.predict(X)
	for pid, l in zip(ids, L):
		print "%d is %d" % (pid, l)

def main(prs, train, load, test):
	prs.add_argument('--train', help='path to ARFF training file')
	prs.add_argument('--store', help='where to store the model')
	prs.add_argument('--load', help='where to load the model from')
	prs.add_argument('--test', help='path to ARFF testing file')
	prs.add_argument('--find', help='find hijacked probe_ids in given file')
	args = prs.parse_args()

	Xtr, Ytr = None, None
	Xte, Yte = None, None
	cls = None
	names = []

	if args.train:
		trids, Xtr, Ytr, names = read_samples(args.train)
		cls = train(Xtr, Ytr, args.store)

	if args.load:
		cls = load(args.load)

	if not cls: raise Exception("please specify --train or --load")

	if args.test:
		teids, Xte, Yte, names = read_samples(args.test)
		ok, err = test(cls, teids, Xte, Yte)
		print "test: ok=%d   err=%d" % (ok, err)

	if args.find:
		fids, Xfi, Yfi, names = read_samples(args.find)
		classify(cls, fids, Xfi)

	return args, cls, names
