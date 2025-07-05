from bs4 import BeautifulSoup

with open('src/tools/n5-page-1.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

rows = soup.select('tr.jl-row')
for row in rows:
    tds = row.find_all('td')
    if len(tds) < 5:
        continue
    # 单词
    word = tds[1].get_text(strip=True)
    # hiragana
    vr_a = tds[2].find('a')
    hira = ''
    if vr_a:
        p = vr_a.find('p')
        if p:
            hira = p.get_text(strip=True)
    # 词性
    pos = tds[3].get_text(strip=True)
    # 释义
    meaning = tds[4].get_text(strip=True)
    print(f"{word}\t{hira}\t{pos}\t{meaning}") 