"""Reproduce the headline numbers of the three studies from the published scores.

usage: python3 analyze.py            (run from eval/scripts, reads ../data/*.csv)

A PR is flagged when it fails at least one question in the set. Each comparison counts only
PRs where both scorers agree on that verdict, as every study's primary measure does.
Needs scipy.
"""
import csv, math, os
from collections import defaultdict
from scipy.stats import fisher_exact

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
ALL13 = [f'Q{i}' for i in range(1, 14)]
REQUIRED = ['Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q10', 'Q11', 'Q12', 'Q13']


def load(name):
    prs = defaultdict(dict)
    for r in csv.DictReader(open(os.path.join(DATA, name))):
        p = prs[(r['repo'], r['id'])]
        p['repo'], p['group'], p['close_category'] = r['repo'], r['group'], r['close_category']
        p[r['scorer']] = {q: r[q] for q in ALL13}
    return list(prs.values())


def newcombe(x1, n1, x2, n2, z=1.959964):
    def wilson(x, n):
        p = x / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
        h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
        return c - h, c + h
    p1, p2 = x1 / n1, x2 / n2; l1, u1 = wilson(x1, n1); l2, u2 = wilson(x2, n2); d = p1 - p2
    return d, d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)


def compare(prs, questions, low_groups, label):
    flag = lambda s: any(s[q] == 'F' for q in questions)
    prs = [p for p in prs if p['group'] in low_groups + ['merged']]
    agreed = [p for p in prs if flag(p['claude']) == flag(p['second_model'])]
    low = [p for p in agreed if p['group'] in low_groups]
    mer = [p for p in agreed if p['group'] == 'merged']
    a, n1 = sum(flag(p['claude']) for p in low), len(low)
    b, n2 = sum(flag(p['claude']) for p in mer), len(mer)
    _, pval = fisher_exact([[a, n1 - a], [b, n2 - b]])
    d, lo, hi = newcombe(a, n1, b, n2)
    bar = 'meets the bar' if pval < 0.05 and d >= 0.20 else 'does not meet the bar'
    print(f'  {label:44s} {"+".join(low_groups)} {a}/{n1} = {a/n1:.1%}  merged {b}/{n2} = {b/n2:.1%}  '
          f'gap {d*100:+.1f} pp [{lo*100:+.1f}, {hi*100:+.1f}]  p = {pval:.2f}  '
          f'dropped {len(prs) - len(agreed)}  {bar}')


def by_repo(prs, questions, low_groups, title):
    for repo in sorted({p['repo'] for p in prs}):
        compare([p for p in prs if p['repo'] == repo], questions, low_groups, f'{title}, {repo}')
    if len({p['repo'] for p in prs}) > 1:
        compare(prs, questions, low_groups, f'{title}, pooled')


print('Run 1, Godot (all 13 questions)')
run1 = load('run1-godot.csv')
compare(run1, ALL13, ['rejected'], 'all 13, godotengine/godot')

print('\nRun 2, three projects with no bots or policies (all 13 questions)')
run2 = load('run2-no-policy.csv')
by_repo(run2, ALL13, ['rejected', 'stale'], 'all 13')
compare(run2, ALL13, ['rejected'], 'all 13, pooled, rejected only')
compare(run2, ALL13, ['stale'], 'all 13, pooled, stale only')

print('\nRun 3, pre-registered: the ten required questions')
run3 = load('run3-preregistered.csv')
by_repo(run3, REQUIRED, ['rejected'], 'required')
compare(run3, ALL13, ['rejected'], 'all 13, pooled (for comparison)')
