#!/bin/bash
# Copyright (C) 2013 Red Hat, Inc.
# Written by Florian Weimer <fweimer@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Reads lines from $input and displays palindromes.  This is intended
# as a performance test for process spawning, so we avoid shell
# built-ins with the "\" command prefix.

# The proper way to do this is (uses up to three cores!):
# paste "$input" <(rev "$input") | awk '{if ($1 == $2) {print $1}}'

if \test -z "$1" -o -z "$2" ; then
    echo "usage: $0 INPUT-FILE OUTPUT-FILE"
    exit 1
fi

input="$1"
output="$2"

export LC_ALL=C

while read line ; do
    if \test "$line" = "$(\printf '%s\n' "$line" | rev)" ; then
	\printf '%s\n' "$line"
    fi
done < "$input" > "$output"
