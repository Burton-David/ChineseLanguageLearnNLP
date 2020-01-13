# ChineseLanguageLearnNLP
Uses NLP to make learning mandarin as efficient as possible.
# Who should use this repository
If you are studying Mandarin Chinese and want a more efficent highly customizable vocabulary lists based off of whatever topic you choose. Then this project will help you.  
## Prerequisites
-  [HSK level 2](https://www.digmandarin.com/hsk-1-vocabulary-list.html) You can use this project in parallel to studying the most common Mandarin words. However; to really get the full use of the program the user should already know common "Stop Words" that are excluded from the generated vocabulary lists.
- Obtain a [google cloud API key](https://cloud.google.com/docs/authentication/api-keys)
- Download and install [Jupyter Notebook](https://jupyter.readthedocs.io/en/latest/install.html)
## About
- The user enters a search phrase in English
- The program returns a list of suggestions 
- The user chooses from that list of suggestions a topic that most closely matches the topic they would like to study 
- The program gathers pages from Wikipedia-China matching the users chosen topic
- The program uses Jieba to perform IF-IDF on the gathered pages and creates a list of the 20 most important words.
- The program uses Google-API(text-to-speech and translate) for a simple definition and audio pronunciation
- The program uses CC-Cedict database for a "better" translation of each word
- The program uses Pinyin library to create a latinized pronunciation of each word
- The user has a list of 20 words, pronunciations and flashcards to study and use as a cribsheet to learn from context!
## Curricula Ideology
The human brain is wired to learn language from context and the way we learned our first language as an infant can be the most efficent way to learn a new language.  This program provides the scaffolding necessary to learn Mandarin from context!  This is a better method than rote memorization or any store bought program because learning from context is easier to recall than rote memorization and it does not rely upon a 1:1 translation method.  It is also more efficent than any store bought program because you are learning what you want to actually talk about and use which makes the material engaging and useful.  While a vocabulary list and pronunciations are created for a learner to study. This list is just the scaffolding necessary for a learner to begin deciphering real world examples of any given topic in Mandarin, and that is where the majority of the learning will take place.  
## Extended Features That Can Be Used to Enhance Studying Results
