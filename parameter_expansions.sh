#!/bin/bash
echo start
echo "$# parameters"
test() {
        echo "$# parameters: "
        echo "$*"
        echo "$@"
        for arg1 in "$*"
                do echo "[$arg1]"  #the expansion of "$*" is indeed a single word.
        done
        echo "\$@"
        for arg2 in "$@"
                do echo "[$arg2]"
        done
        exit 1;
}
test "$@"
