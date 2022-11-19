for file in `\find log -name '*.txt'`; do
    python3 convert.py  $file
done
