# usage: policycheck.sh owner/repo  -> writes repo_checks/<owner_repo>.txt and copies of policy files
r=$1; o=$(echo $r | tr / _); D=./repo_checks; mkdir -p $D; out=$D/$o.txt
PAT='stale|auto-?close|close[-_ ]?(pr|pull)|pulls?.*close|closePullRequest|gh pr close|lock-threads|lock'
TXT='\bAI\b|\bLLM|generative|ChatGPT|Copilot|Claude|machine[- ]generated|new contributor|first[- ]time|newcomer|good first|stale|inactiv'
{
echo "=== $r  (checked $(TZ=America/Los_Angeles date '+%Y-%m-%d %H:%M %Z'))"
def=$(gh api repos/$r --jq .default_branch); echo "default_branch=$def"
echo "stale.yml: $(gh api repos/$r/contents/.github/stale.yml --jq .name 2>&1 | head -1)"
wfs=$(gh api repos/$r/contents/.github/workflows --jq '.[].name' 2>/dev/null); echo "workflows: $(echo $wfs | tr '\n' ' ')"
for w in $wfs; do c=$(gh api repos/$r/contents/.github/workflows/$w -H 'Accept: application/vnd.github.raw' 2>/dev/null); h=$(echo "$c" | grep -inE "$PAT" | grep -v '^\s*#' | head -8); [ -n "$h" ] && { echo "  WF $w:"; echo "$h" | sed 's/^/     /' | cut -c1-200; }; done
for f in CONTRIBUTING.md .github/CONTRIBUTING.md docs/CONTRIBUTING.md CONTRIBUTING.rst CONTRIBUTING .github/PULL_REQUEST_TEMPLATE.md .github/pull_request_template.md PULL_REQUEST_TEMPLATE.md .github/PULL_REQUEST_TEMPLATE/pull_request_template.md AGENTS.md CLAUDE.md .github/copilot-instructions.md AI_POLICY.md .github/AI_POLICY.md; do
  c=$(gh api repos/$r/contents/$f -H 'Accept: application/vnd.github.raw' 2>/dev/null) || continue
  echo "$c" | grep -q '"message": *"Not Found"' && continue
  [ -z "$c" ] && continue
  echo "$c" > "$D/${o}__$(echo $f | tr / _)"; echo "  [$f] ${#c} chars"; echo "$c" | grep -nE "$TXT" | head -12 | cut -c1-220 | sed 's/^/     /'
done
pins=$(gh api graphql -f query="{repository(owner:\"${r%/*}\",name:\"${r#*/}\"){pinnedIssues(first:5){nodes{issue{number title}}}}}" --jq '[.data.repository.pinnedIssues.nodes[].issue | "#\(.number) \(.title)"] | join("; ")' 2>&1)
echo "pinned: $pins"
} > $out 2>&1; cat $out
