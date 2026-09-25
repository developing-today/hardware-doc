import pypdf,re
r=pypdf.PdfReader('esp32-p4-datasheet.pdf')
for i in (13,14,15,16):
    t=r.pages[i].extract_text() or ''
    print(f"===== page {i+1} =====")
    print(' '.join(t.split()))
    print()
