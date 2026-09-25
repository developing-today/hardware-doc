import sys,pypdf,re
r=pypdf.PdfReader('esp32-p4-datasheet.pdf')
for i,p in enumerate(r.pages[:40]):
    t=p.extract_text() or ''
    if re.search(r'Pin\s*Overview|Pin Layout|Appendix A', t, re.I):
        print(f"=== page {i+1} ===")
        print(' '.join(t.split())[:900]); print()
