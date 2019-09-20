import xpinyin


from xpinyin import Pinyin
p = Pinyin()
# default splitter is `-`
print(p.get_pinyin(u"上海"))                            #'shang-hai'

# show tone marks
print(p.get_pinyin(u"上海", tone_marks='marks'))         #'shàng-hǎi'
print(p.get_pinyin(u"上海", tone_marks='numbers'))       #'shang4-hai3'

# remove splitter
print(p.get_pinyin(u"上海", ''))                          #'shanghai'

# set splitter as whitespace
print(p.get_pinyin(u"上海", ' '))                         #'shang hai'
