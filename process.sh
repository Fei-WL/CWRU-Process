for device in "DE" "FE"
do
    for nclass in 4 10
    do
        python process.py --device $device --nclass $nclass
    done
done
