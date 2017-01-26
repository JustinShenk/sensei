#!/bin/sh
rm -rf build dist

pyInstaller sensei.spec

dist/sensei
