#!/bin/bash

while true; do
	jekyll
	inotifywait -e modify *.md *.html documentation/*.md css/*.css
done
