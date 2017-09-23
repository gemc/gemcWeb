#!/bin/bash

mv components preserve_components
mv upload uploap_preserve
mv users users_preserve

export https_proxy=jprox.jlab.org:8081
export http_proxy=jprox.jlab.org:8081

git pull

rm -rf components
rm -rf upload
rm -rf users

mv preserve_components components
mv uploap_preserve upload
mv users_preserve users
