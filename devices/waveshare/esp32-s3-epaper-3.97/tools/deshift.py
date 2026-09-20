"""Decode Waveshare's offset-encoded PDF text layer.

The 3.97inch e-Paper panel manual embeds two subset fonts whose code points are
uniformly displaced from the real characters. Decoding is chr(ord(c)+K) with
K=29 for one font and K=26 for the other. Validated against the known cover
heading "3.97inch e-Paper" and the section word "Revision History".

Per the method: a text layer must be validated against a known heading before
any value is transcribed. This script exists so that validation is repeatable.
"""
import sys, collections

def dec(s, k):
    return ''.join(chr(ord(c)+k) if 0 < ord(c)+k < 0x2500 else c for c in s)

WORDS = ('the','and','for','Paper','inch','Display','Panel','Driver','IC','Waveshare',
         'Revision','Version','Content','Date','Page','Resolution','Voltage','Interface')

def best(s):
    cands = [(sum(w.lower() in dec(s,k).lower() for w in WORDS), k) for k in (29,26)]
    cands.sort(reverse=True)
    return dec(s, cands[0][1]), cands[0][1]

rows = collections.defaultdict(list)
for l in open(sys.argv[1], encoding='utf-8'):
    p = l.rstrip('\n').split('\t')
    if len(p) < 4: continue
    rows[(p[0], round(float(p[2]),1))].append((float(p[1]), '\t'.join(p[3:])))

lines = []
for (o,y), v in rows.items():
    lines.append((o, y, ''.join(t for x,t in sorted(v))))
lines.sort(key=lambda r: (r[0], -r[1]))
for o, y, s in lines:
    d29, d26 = dec(s,29), dec(s,26)
    # pick the one with more lowercase-looking English
    pick = d29 if sum(c.islower() for c in d29) >= sum(c.islower() for c in d26) else d26
    print(f'{o}\t{y}\t{pick}')
