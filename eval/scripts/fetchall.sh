# usage: fetchall.sh owner/repo prefix nrej nmer   (rejected fetched with the supersession check on)
r=$1; o=$2; D=$(pwd)/raw_$o; mkdir -p $D
head -n $3 ${o}_rej_order.tsv | cut -f1 | SUPER=1 xargs -P 4 -I{} python3 -I fetch.py $r {} $D
head -n $4 ${o}_mer_order.tsv | cut -f1 | xargs -P 4 -I{} python3 -I fetch.py $r {} $D
ls $D/*.json | wc -l
