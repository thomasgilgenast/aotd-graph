# base image
FROM ubuntu:16.04

# add graph-tool repos to sources.list
RUN echo "deb http://downloads.skewed.de/apt/xenial xenial universe" >> /etc/apt/sources.list && \
	echo "deb-src http://downloads.skewed.de/apt/xenial xenial universe" >> /etc/apt/sources.list

# public key
RUN apt-key adv --keyserver pgp.skewed.de --recv-key 612DEFB798507F25

# install graph-tool and pip
RUN apt-get update && apt-get install --yes --no-install-recommends \
	python3-graph-tool \
	python3-pip

# set working directory and copy files
WORKDIR /aotd-graph
ADD requirements.txt /aotd-graph

# install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# set default backend in matplotlibrc
RUN echo "backend: Cairo" >> matplotlibrc
