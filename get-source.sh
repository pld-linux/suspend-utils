#!/bin/sh
PACKAGE=suspend-utils

set -e
set -x

if [ ! -d $PACKAGE/ ]; then
	git clone git://git.kernel.org/pub/scm/linux/kernel/git/rafael/suspend-utils.git $PACKAGE/
else
	cd $PACKAGE
	git pull --rebase
	cd ..
fi

export GIT_DIR=$PACKAGE/.git
VERSION=1.0.g$(git rev-parse --short master)
ARCHIVE=$PACKAGE-$VERSION.tar.gz

if [ -e $ARCHIVE ]; then
	echo >&2 "$ARCHIVE already exists"
	exit 0
fi
git archive master --prefix=$PACKAGE-$VERSION/ -o $ARCHIVE
