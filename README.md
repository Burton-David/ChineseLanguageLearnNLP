# Learn Mandarin Chinese Effectively
**Datamining, Natural Language Processing, Machine Learning Translation, Google Cloud Integration**<br>
*Learn the most important words for any given topic*<br>
- Data Mines Wikipedia.ch<br>
- Generates a personalized vocabulary list for student<br>
## About <br>
- The user enters a search phrase in English
- The program returns a list of suggestions 
- The user chooses from that list of suggestions a topic that most closely matches the topic they would like to study 
- The program gathers pages from Wikipedia-China matching the users chosen topic
- The program uses Jieba to perform IF-IDF on the gathered pages and creates a list of the 20 most important words.
- The program uses Google-API(text-to-speech and translate) for a simple definition and audio pronunciation
- The program uses CC-Cedict database for a "better" translation of each word
- The program uses Pinyin library to create a latinized pronunciation of each word
- The user has a list of 20 words, pronunciations and flashcards to study and use as a cribsheet to learn from context!
## The Algorithms
- Term Frequency - Inverse Document Frequency <br>
![tfidf_{i,d} = tf_{i,d} \cdot idf_{i}](https://render.githubusercontent.com/render/math?math=tfidf_%7Bi%2Cd%7D%20%3D%20tf_%7Bi%2Cd%7D%20%5Ccdot%20idf_%7Bi%7D)

    - TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).<br>
    - IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
![idf\left ( t,D \right )= \log \left | D\left | 1+ \right |\left \{ d\epsilon D:t\epsilon d \right \} \right |](https://render.githubusercontent.com/render/math?math=idf%5Cleft%20(%20t%2CD%20%5Cright%20)%3D%20%5Clog%20%5Cleft%20%7C%20D%5Cleft%20%7C%201%2B%20%5Cright%20%7C%5Cleft%20%5C%7B%20d%5Cepsilon%20D%3At%5Cepsilon%20d%20%5Cright%20%5C%7D%20%5Cright%20%7C)
- Clusters similar documents of the TF-IDF weighted matrix
'''cos(θ)=v⋅w‖v‖‖w‖=∑ni=1viwi∑ni=1v2i‾‾‾‾‾‾‾√∑ni=1w2i‾‾‾‾‾‾‾‾√'''
## Who should use this repository
If you are studying Mandarin Chinese and want a more efficent highly customizable vocabulary lists based off of whatever topic you choose. Then this project will help you.  
## Prerequisites
-  [HSK level 2](https://www.digmandarin.com/hsk-1-vocabulary-list.html) You can use this project in parallel to studying the most common Mandarin words. However; to really get the full use of the program the user should already know common "Stop Words" that are excluded from the generated vocabulary lists.
- Obtain a [google cloud API key](https://cloud.google.com/docs/authentication/api-keys)
- Download and install [Jupyter Notebook](https://jupyter.readthedocs.io/en/latest/install.html)

## Curricula Ideology
The human brain is wired to learn language from context and the way we learned our first language as an infant can be the most efficent way to learn a new language.  This program provides the scaffolding necessary to learn Mandarin from context!  This is a better method than rote memorization or any store bought program because learning from context is easier to recall than rote memorization and it does not rely upon a 1:1 translation method.  It is also more efficent than any store bought program because you are learning what you want to actually talk about and use which makes the material engaging and useful.  While a vocabulary list and pronunciations are created for a learner to study. This list is just the scaffolding necessary for a learner to begin deciphering real world examples of any given topic in Mandarin, and that is where the majority of the learning will take place.  
## Extended Features That Can Be Used to Enhance Studying Results
TTS (Text-to-Speech) using Google API
STT (Speech-to-Text) using Google API
SRS (Spaced-Repition-Studying)Flashcard system using Anki API

# Using the Application
## Type in a Subject You'd Like to Study (this example uses Batman)
What would you like to search for?: Batman
    ['蝙蝠俠', '蝙蝠俠：開戰時刻', '蝙蝠俠：高譚騎士', '樂高蝙蝠俠電影', '蝙蝠侠 (动画影集)', '蝙蝠俠對超人：正義曙光', '蝙蝠侠归来', '蝙蝠俠智勇悍將', '蝙蝠侠与罗宾 (电影)', '永远的蝙蝠侠']
    try one of the following search phrases
    Batman
    Batman: The moment of war
    Batman: Gotham Knight
    Lego Batman Movie
    Batman (Animated Album)
    Batman vs Superman: Dawn of Justice
    Batman Returns
    Batman Wisdom
    Batman and Robin (Movie)
    Batman forever



```python
df = application()
```

    Type one of the above search suggestions here: Batman
    page added to content
    page added to content
    process finished, all content stored in myfile.txt


## An image taken from the data mining will appear here
<img src="https://upload.wikimedia.org/wikipedia/zh/2/29/Batman_was_spreading_the_cloak.jpg"/>

### The Database is Cached Locally to Optimize Memory Usage
    Building prefix dict from the default dictionary ...
    Loading model from cache /var/folders/vl/fdjj_g0d7gvgr2ry_y9bx0km0000gn/T/jieba.cache
    Loading model cost 0.867 seconds.
    Prefix dict has been built successfully.


### Personalize the Output to Suit Your Needs as a Learner
```python
# keep only simplified or traditional 
df.drop_duplicates(subset='English',keep='first', inplace=True)

# Rename the columns to something I like a bit better.
df.columns = ['漢字(traditional)', 'weight', 'pinyin(numbers)', 'English']


dictionary = pd.read_csv('cedict.csv',sep='|', skiprows=0)

dictionary.columns = ["漢字(traditional)", "汉字(simplified)", "pinyin(marks)", "English2"]

df2= pd.merge(df, dictionary, on="漢字(traditional)", how='left')

df2.columns

# rearrange the columns in a way that makes sense
df2 = df2[["English","English2","weight","漢字(traditional)","汉字(simplified)","pinyin(marks)","pinyin(numbers)"]]
df.columns = ['漢字(traditional)', 'weight', 'pinyin(numbers)', 'English']

# keep only simplified or traditional 
df.drop_duplicates(subset='English',keep='first', inplace=True)

df2= pd.merge(df, dictionary, on="漢字(traditional)", how='left')
df2 = df2[["漢字(traditional)","汉字(simplified)","English","English2","pinyin(marks)","pinyin(numbers)"]]
```
Simplified characters are displayed if they are different than traditional.  As you can see, in this example there are only traditional characters.  However, it is a good idea to keep this output as simplified characters are widely used in print media. 

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>漢字(traditional)</th>
      <th>汉字(simplified)</th>
      <th>English</th>
      <th>English2</th>
      <th>pinyin(marks)</th>
      <th>pinyin(numbers)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>蝙蝠侠</td>
      <td>NaN</td>
      <td>Batman</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>bian1-fu2-xia2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>蝙蝠</td>
      <td>NaN</td>
      <td>bat</td>
      <td>bat.</td>
      <td>biān fú</td>
      <td>bian1-fu2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>漫画</td>
      <td>NaN</td>
      <td>Comic</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>man4-hua4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>DC</td>
      <td>NaN</td>
      <td>DC</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>DC</td>
    </tr>
    <tr>
      <th>4</th>
      <td>罗宾</td>
      <td>NaN</td>
      <td>Robin</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>luo1-bin1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>布鲁斯</td>
      <td>NaN</td>
      <td>Bruce</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>bu4-lu3-si1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>故事</td>
      <td>NaN</td>
      <td>story</td>
      <td>old practice; CL:個/个[ge4].</td>
      <td>gù shì</td>
      <td>gu4-shi4</td>
    </tr>
    <tr>
      <th>7</th>
      <td>故事</td>
      <td>NaN</td>
      <td>story</td>
      <td>narrative; story; tale.</td>
      <td>gù shi</td>
      <td>gu4-shi4</td>
    </tr>
    <tr>
      <th>8</th>
      <td>凯恩</td>
      <td>NaN</td>
      <td>Kane</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>kai3-en1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>连载</td>
      <td>NaN</td>
      <td>Serialize</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>lian2-zai4</td>
    </tr>
    <tr>
      <th>10</th>
      <td>芬格</td>
      <td>NaN</td>
      <td>Finger</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>fen1-ge2</td>
    </tr>
    <tr>
      <th>11</th>
      <td>超人</td>
      <td>NaN</td>
      <td>Superman</td>
      <td>Superman, comic book superhero.</td>
      <td>Chāo rén</td>
      <td>chao1-ren2</td>
    </tr>
    <tr>
      <th>12</th>
      <td>超人</td>
      <td>NaN</td>
      <td>Superman</td>
      <td>superhuman; exceptional.</td>
      <td>chāo rén</td>
      <td>chao1-ren2</td>
    </tr>
    <tr>
      <th>13</th>
      <td>小丑</td>
      <td>NaN</td>
      <td>clown</td>
      <td>clown.</td>
      <td>xiǎo chǒu</td>
      <td>xiao3-chou3</td>
    </tr>
    <tr>
      <th>14</th>
      <td>角色</td>
      <td>NaN</td>
      <td>Roles</td>
      <td>role; character in a novel; persona; also pr. ...</td>
      <td>jué sè</td>
      <td>jiao3-se4</td>
    </tr>
    <tr>
      <th>15</th>
      <td>迪克</td>
      <td>NaN</td>
      <td>Dick</td>
      <td>Dick (person name).</td>
      <td>Dí kè</td>
      <td>di2-ke4</td>
    </tr>
    <tr>
      <th>16</th>
      <td>52</td>
      <td>NaN</td>
      <td>52</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>52</td>
    </tr>
    <tr>
      <th>17</th>
      <td>英雄</td>
      <td>NaN</td>
      <td>hero</td>
      <td>hero; CL:個/个[ge4].</td>
      <td>yīng xióng</td>
      <td>ying1-xiong2</td>
    </tr>
    <tr>
      <th>18</th>
      <td>黑暗</td>
      <td>NaN</td>
      <td>dark</td>
      <td>dark; darkly; darkness.</td>
      <td>hēi àn</td>
      <td>hei1-an4</td>
    </tr>
    <tr>
      <th>19</th>
      <td>侦探</td>
      <td>NaN</td>
      <td>detective</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>zhen1-tan4</td>
    </tr>
  </tbody>
</table>
</div>



### Practice Pronouncing The Words
#### Text-to-Speech Integration

```python
for index,row in df.iterrows():
    print(row['English'], row["漢字(traditional)"], row["pinyin(numbers)"])
    #time.sleep(10)
    pronounce_chinese(row['漢字(traditional)'])
```

    Batman 蝙蝠侠 bian1-fu2-xia2
    bat 蝙蝠 bian1-fu2
    Comic 漫画 man4-hua4
    DC DC DC
    Robin 罗宾 luo1-bin1
    Bruce 布鲁斯 bu4-lu3-si1
    story 故事 gu4-shi4
    Kane 凯恩 kai3-en1
    Serialize 连载 lian2-zai4
    Finger 芬格 fen1-ge2
    Superman 超人 chao1-ren2
    clown 小丑 xiao3-chou3
    Roles 角色 jiao3-se4
    Dick 迪克 di2-ke4
    52 52 52
    hero 英雄 ying1-xiong2
    dark 黑暗 hei1-an4
    detective 侦探 zhen1-tan4


### Put individual words in here to hear them one at a time


```python
pronounce_chinese('漫画')
```
