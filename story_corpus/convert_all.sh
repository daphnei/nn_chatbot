for f in *; do
    if [[ -d $f ]]; then
        python2 clean_stories.py $f
    fi
done