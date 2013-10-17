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

# Benchmark driver for the palindrome.sh script.  Data is appended to
# the file named in the first argument, in CSV format, with columns
# elapsed time, user time, system time, all in seconds.

stat="$1"

if test -z "$stat" ; then
    echo "usage: $0 OUTPUT-FILE-PREFIX"
    exit 1
fi
    

input="$(mktemp)"
output="$(mktemp)"

cleanup () {
    rm "$input" "$output"
}

trap cleanup 0

head -n 13000 /usr/share/dict/words > "$input"

for x in {1..30} ; do
    echo "Iteration $x"
    : > "$output"
    \time -o "$stat" -a -f "%e,%U,%S"  bash palindromes.sh "$input" "$output"
done
