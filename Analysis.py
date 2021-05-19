import pandas as pd
import nltk
import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
raw = open('RUS.txt').read()
extra_raw = open('dict.opcorpora.txt').read()
extra_vocab = set(re.findall('[а-яА-ЯёЁ]+', extra_raw.lower()))
vocab= set(re.findall('\w+', raw.lower()))
csv = pd.read_excel('LJ2.xlsx', header=1)
data_df = pd.DataFrame(csv)
file = open('Usernames.txt', 'r')
file = file.read()
usernames = file.split(',')
dictionary = {}
cyr_dictionary = {}
temp_list_of_cs_verb = []
dictionary_of_bigramms = {}
list_of_top_cs_words = ['абх', 'уни', 'аок', 'кауциона', 'финанцамт', 'еур', 'фермитер', 'кранкенкасса', 'хебамма', 'бюргерамт', 'манунг']
post_index = 0
for post in data_df['Post']:
    if data_df['Date'][post_index] == '2012':
        try:
            post = re.sub(r'www.\S+', '', post)
        except:
            print('тут был трабл')
        try:
            post = re.sub(r'http\S+', '', post)
        except:
            print('тут был трабл')
        try:
            post = re.sub(r'[0-9]', '', post)
        except:
            print('тут был трабл')
        try:
            examples = post.lower()
        except:
            examples = str(post)
        Sentences_of_post = nltk.tokenize.sent_tokenize(examples)
        for Sentence_of_post in Sentences_of_post:
            Cyrillics = re.findall(r'[а-яА-ЯёЁ]+', Sentence_of_post)
            if 'für' in Sentence_of_post:
                print(Sentence_of_post)
            if len(Cyrillics) > 0:
                tokens = tokenizer.tokenize(Sentence_of_post)
                for token in tokens:
                    token_temp = morph.parse(token)[0].normal_form
                    if token_temp.lower() in list_of_top_cs_words:
                        index_of_token_temp = tokens.index(token)
                        if index_of_token_temp > 4 and index_of_token_temp + 4 < len(tokens):
                            for index_of_verb in range(index_of_token_temp - 4, index_of_token_temp + 4):
                                if 'VERB' in morph.parse(tokens[index_of_verb])[0].tag:
                                    if token_temp in dictionary_of_bigramms:
                                        temp_list_of_cs_verb = list(dictionary_of_bigramms[token_temp])
                                        temp_list_of_cs_verb.append(tokens[index_of_verb])
                                        dictionary_of_bigramms[token_temp] = temp_list_of_cs_verb
                                    else:
                                        dictionary_of_bigramms[token_temp] = {tokens[index_of_verb]}
                        if index_of_token_temp > 4 and index_of_token_temp + 4 >= len(tokens):
                            for index_of_verb in range(index_of_token_temp - 4, len(tokens)):
                                if 'VERB' in morph.parse(tokens[index_of_verb])[0].tag:
                                    if token_temp in dictionary_of_bigramms:
                                        temp_list_of_cs_verb = list(dictionary_of_bigramms[token_temp])
                                        temp_list_of_cs_verb.append(tokens[index_of_verb])
                                        dictionary_of_bigramms[token_temp] = temp_list_of_cs_verb
                                    else:
                                        dictionary_of_bigramms[token_temp] = {tokens[index_of_verb]}
                        if index_of_token_temp <= 4 and index_of_token_temp + 4 < len(tokens):
                            for index_of_verb in range(0, index_of_token_temp + 4):
                                if 'VERB' in morph.parse(tokens[index_of_verb])[0].tag:
                                    if token_temp in dictionary_of_bigramms:
                                        temp_list_of_cs_verb = list(dictionary_of_bigramms[token_temp])
                                        temp_list_of_cs_verb.append(tokens[index_of_verb])
                                        dictionary_of_bigramms[token_temp] = temp_list_of_cs_verb
                                    else:
                                        dictionary_of_bigramms[token_temp] = {tokens[index_of_verb]}
                        if index_of_token_temp <= 4 and index_of_token_temp + 4 >= len(tokens):
                            for index_of_verb in range(0, len(tokens)):
                                if 'VERB' in morph.parse(tokens[index_of_verb])[0].tag:
                                    if token_temp in dictionary_of_bigramms:
                                        temp_list_of_cs_verb = list(dictionary_of_bigramms[token_temp])
                                        temp_list_of_cs_verb.append(tokens[index_of_verb])
                                        dictionary_of_bigramms[token_temp] = temp_list_of_cs_verb
                                    else:
                                        dictionary_of_bigramms[token_temp] = {tokens[index_of_verb]}
                    if token_temp not in extra_vocab and token_temp not in vocab:
                        if 'ru_de' not in token_temp:
                            if token_temp in dictionary:
                                dictionary.update({token_temp: int(dictionary[token_temp]) + 1})
                            else:
                                dictionary[token_temp] = '1'
                            Cyrillic = re.findall(r'[а-яА-ЯёЁ]+', token_temp)
                            if len(Cyrillic) > 0:
                                if token_temp in cyr_dictionary:
                                    cyr_dictionary.update({token_temp: int(cyr_dictionary[token_temp]) + 1})
                                else:
                                    cyr_dictionary[token_temp] = '1'
    post_index = post_index + 1
print(dictionary_of_bigramms)
colNames = ['счетчик']
df1 = pd.DataFrame.from_dict(dictionary, orient='index')
df1.columns = colNames
df1.reset_index(inplace=True)
df1.to_csv('Dict1New2012.csv')
print(df1)
cyr_df1 = pd.DataFrame.from_dict(cyr_dictionary, orient='index')
cyr_df1.reset_index(inplace=True)
cyr_df1.to_csv('extra_Dict1New2012.csv')
print(cyr_df1)