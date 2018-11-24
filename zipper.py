import subprocess
import os

totals = {}

for song in os.listdir('/app/songs'):
    if not song.endswith('txt'):
        continue

    tmp = '/app/tmp.txt'
    os.system(f"cat '/app/songs/{song}' | sed 's/[[:upper:]]*/\L&/g' | sed -e 's/[,:;\.!?()_-]//g' | sed 'y/абвгджзийклмнопрстуфхыэе/abvgdjzijklmnoprstufhyee/' | sed 's/[ьъ]//g; s/ё/yo/g; s/ц/ts/g; s/ч/ch/g; s/ш/sh/g; s/щ/sh/g; s/ю/yu/g; s/я/ya/g' > {tmp}")
    
    pre = subprocess.check_output(f"cat {tmp} | wc -c", shell=True)
    pre = int(pre)

    literals = subprocess.check_output(f"./zopfli/zopfli -c --gzip {tmp} | ./infgen/infgen | grep literal", shell=True)
    matches = subprocess.check_output(f"./zopfli/zopfli -c --gzip {tmp} | ./infgen/infgen | grep match", shell=True)
    lit_cnt = 0
    for lit in literals.decode('utf-8').split('\n'):
        lit_cnt += len(lit[lit.find("'")+1:])
    match_cnt = len(matches.decode('utf-8').split('\n')) - 1

    post = lit_cnt + 3 * match_cnt
    res = round((1 - post/pre) * 100, 1)
    totals[song[:-4]] = res

for song, res in sorted(totals.items(), key=lambda a: a[1]):
    print(f"{song}: {res}%")

avg = round(sum(totals.values()) / len(totals), 1)

print('---------------')
print(f"AVG: {avg}%")