#!/bin/bash


while true; do
	jekyll


	find . \( -path "./_site" -o -path "./.git" -o -name "*.swp" \) -prune -o -type f -print | xargs inotifywait -e modify
done
