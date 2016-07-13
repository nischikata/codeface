#!/bin/bash
# Copyright Roger Meier <roger@bufferoverflow.ch>
# SPDX-License-Identifier:	Apache-2.0 BSD-2-Clause GPL-2.0+ MIT WTFPL

echo "Providing common binaries and libraries"

sudo apt install sinntp texlive \
	mysql-client libgraphviz-dev libarchive13 libhunspell-dev \
	python-dev exuberant-ctags nodejs git subversion libxslt1-dev \
	sloccount graphviz doxygen libxml2-dev libcurl4-openssl-dev \
	libmysqlclient-dev libcairo2-dev libxt-dev libcairo2-dev libmysqlclient-dev \
	astyle xsltproc libxml2 libxml2-dev python build-essential libyaml-dev \
	gfortran python-setuptools python-pkg-resources python-numpy python-matplotlib \
	python-libxml2 python-lxml python-lxml gcc python-pip \
	libxml2-dev libcurl4-openssl-dev xorg-dev libx11-dev libgles2-mesa-dev \
	libglu1-mesa-dev libxt-dev libpoppler-dev libpoppler-glib-dev python-mock \
	libapparmor-dev libpoppler-cpp-dev \
	wordnet wget

sudo apt install --no-install-recommends default-jdk
