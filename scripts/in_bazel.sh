#!/usr/bin/env bash

current_offenders() {
    comm -23 \
        <(git ls-files "*\.$ext" ":!doc/*" ":!.claude/*" ":!.github/*" | sort) \
        <(
            bazel cquery '
           kind("source file", deps(kind("'"$kind"'", //...)))
       ' |
                grep -E "\.$ext " |
                sed -E 's| \([^)]*\)$||; s|^//([^:]+):|\1/|' |
                sort
        )
}

main() {
    if [[ $# -ne 2 && $# -ne 3 ]]; then
        echo "Usage: $0 <EXTENSION> <KIND> [<LIMIT>]" >&2
        exit 1
    fi

    ext=$1
    kind=$2
    limit=${3:-0}

    current=$(current_offenders)

    count=$(echo "$current" | wc -l)
    echo "Found $count \".$ext\" files not declared as $kind, expected exactly $limit"
    echo "-----"
    echo "$current"

    if ((count != limit)); then
        exit 1
    fi
}

main "$@"
