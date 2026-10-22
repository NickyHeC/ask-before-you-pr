# usage: collect.sh owner/repo outprefix
# Lists PRs closed in the window 2026-04-22..2026-10-21 (Pacific time), merged and unmerged, into <outprefix>_merged.tsv and <outprefix>_unmerged.tsv.
r=$1; o=$2
months="2026-04-22T07:00:00Z..2026-05-22T06:59:59Z 2026-05-22T07:00:00Z..2026-06-22T06:59:59Z 2026-06-22T07:00:00Z..2026-07-22T06:59:59Z 2026-07-22T07:00:00Z..2026-08-22T06:59:59Z 2026-08-22T07:00:00Z..2026-09-22T06:59:59Z 2026-09-22T07:00:00Z..2026-10-22T06:59:59Z"
for st in unmerged merged; do : > ${o}_$st.tsv
 for m in $months; do for p in 1 2 3 4 5 6 7 8 9 10; do
  out=$(gh api -X GET search/issues -f q="repo:$r is:pr is:closed is:$st closed:$m" -f per_page=100 -f page=$p --jq '.items[] | [.number, .user.login, .user.type, .author_association, .created_at, .closed_at, (.draft|tostring), .title] | @tsv' 2>/dev/null)
  [ -z "$out" ] && break; echo "$out" >> ${o}_$st.tsv; n=$(echo "$out" | wc -l); sleep 2.5; [ $n -lt 100 ] && break; done; done; done
sort -u -o ${o}_unmerged.tsv ${o}_unmerged.tsv; sort -u -o ${o}_merged.tsv ${o}_merged.tsv
wc -l ${o}_*.tsv
