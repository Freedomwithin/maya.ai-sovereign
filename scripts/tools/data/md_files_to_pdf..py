#!/bin/bash

# Must insert file name into it

if [ -z "$1" ]; then
  echo "Usage: $0 <file.md> [pdf|docx]"
  exit 1
fi

input="$1"
format="${2:-pdf}"

if [ "$format" = "pdf" ]; then
  pandoc "$input" -o "${input%.md}.pdf" --pdf-engine=xelatex
elif [ "$format" = "docx" ]; then
  pandoc "$input" -o "${input%.md}.docx"
else
  echo "Format must be 'pdf' or 'docx'"