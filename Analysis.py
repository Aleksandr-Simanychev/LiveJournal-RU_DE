import pandas as pd
import nltk
import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
raw = open('RUS.txt').read()                            #Первой проблемой был вопрос: откуда брать список русских слов. Сначала я нашел любительский словарь 
extra_raw = open('dict.opcorpora.txt').read()           #в интернете, но он показал низкую эффективность. Словарь от OpenCorpora оказался куда эффективнее.
extra_vocab = set(re.findall('[а-яА-ЯёЁ]+', extra_raw.lower())) #При их пересечении эффективность оказалась максимальной.
vocab= set(re.findall('\w+', raw.lower()))
csv = pd.read_excel('LJ2.xlsx', header=1)               #Датафрейм строился из файла LJ2. Это публикации полученные с помощью граббера, но только за 2013-2020
data_df = pd.DataFrame(csv)
dictionary = {}
cyr_dictionary = {}
temp_list_of_cs_verb = []                               #Строчки 13-17 технические
dictionary_of_bigramms = {}
count_of_intersentence = 0
list_of_top_cs_words = ['абх', 'уни', 'аок', 'кауциона', 'финанцамт', 'еур', 'фермитер', 'кранкенкасса', 'хебамма', 'бюргерамт', 'манунг']
post_index = 0                                          #Список слов из топа LJ, выбранный вручную
for post in data_df['Post']:
    if data_df['Date'][post_index] == 2014:
        try:
            post = re.sub(r'www.\S+', '', post)                             #С помощью RegEx избавляюсь от ссылок.
        except:
            print('тут был трабл')
        try:
            post = re.sub(r'ru_de[a-zA-Z]*[а-яА-ЯёЁ]*[ ]', '', post)        #С помощью RegEx избавляюсь от никнеймов.
        except:
            print('тут был трабл')
        try:
            post = re.sub(r'edited at -- :', '', post)                      #С помощью RegEx избавляюсь от технических выставок на отредактированных постах.
        except:
            print('тут был трабл')
        try:
            post = re.sub(r'http\S+', '', post)                             #С помощью RegEx избавляюсь от ссылок.
        except:
            print('тут был трабл')
        try:
            post = re.sub(r'[0-9]', '', post)                               #С помощью RegEx избавляюсь от цифр.
        except:
            print('тут был трабл')
        try:
            examples = post.lower()                                         #Избавляюсь от проблем с регистром
        except:
            examples = str(post)
        Sentences_of_post = nltk.tokenize.sent_tokenize(examples)           #Разбиваю посты на предложения
        Intersentence = re.findall(r'[а-яА-ЯёЁ]+[.?!:;][ ]?[a-zA-Z]+[ ][a-zA-Z]+]', str(Sentences_of_post))     #Строки 47-48 ищу переключение кода на границах
        Intersentence_1 = re.findall(r'[a-zA-Z]+[ ][a-zA-Z]+[.?!:;][ ]?[а-яА-ЯёЁ]+', str(Sentences_of_post))    #предложения. Больше чем single word insertion.
        if len(Intersentence) > 0 or len(Intersentence_1) > 0:
            count_of_intersentence = count_of_intersentence + 1
            print('ИНТЕРСЕНТЕНЦИОНАЛЬНОЕ ПК')           
            print(Sentences_of_post)                                        #Вывожу на экран, так как пока еще не измерил точность работы такого подхода
        for Sentence_of_post in Sentences_of_post:                          #Цикл для интрасентенциональной обработки
            Cyrillics = re.findall(r'[а-яА-ЯёЁ]+', Sentence_of_post)
            if len(Cyrillics) > 0:                                          #Проверка на то, не написано ли предложение полностью на немецком
                tokens = tokenizer.tokenize(Sentence_of_post)               #Разбиваю предложение на слова
                for token in tokens:
                    token_temp = morph.parse(token)[0].normal_form          #Привожу слова к предполагаемой начальной форме
                    if token_temp.lower() in list_of_top_cs_words:          #Дальше начинается цикл для построение биграмм формата Существительное + Глагол
                        index_of_token_temp = tokens.index(token)           #для самых частотных существительных.
                        if index_of_token_temp > 4 and index_of_token_temp + 4 < len(tokens):        #Проверяю 4 слова до и 4 слова после существительного 
                            for index_of_verb in range(index_of_token_temp - 4, index_of_token_temp + 4):       #на предмет глагола. Такое количество циклов 
                                if 'VERB' in morph.parse(tokens[index_of_verb])[0].tag:                         #необходимо для того, чтобы не выходить
                                    if token_temp in dictionary_of_bigramms:                                    #за границы предложения.
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
                    if token_temp not in extra_vocab and token_temp not in vocab:   #в этом цикле мы находим нерусские слова (см. Readme)
                        if 'ru_de' not in token_temp:
                            if token_temp in dictionary:                            #для всех видов слов.
                                dictionary.update({token_temp: int(dictionary[token_temp]) + 1})
                            else:
                                dictionary[token_temp] = '1'
                            Cyrillic = re.findall(r'[а-яА-ЯёЁ]+', token_temp)       #для слов в кириллическом написании.
                            if len(Cyrillic) > 0:
                                if token_temp in cyr_dictionary:
                                    cyr_dictionary.update({token_temp: int(cyr_dictionary[token_temp]) + 1})
                                else:
                                    cyr_dictionary[token_temp] = '1'
    post_index = post_index + 1
print(count_of_intersentence)
print(dictionary_of_bigramms)
colNames = ['счетчик']
df1 = pd.DataFrame.from_dict(dictionary, orient='index')
df1.columns = colNames
df1.reset_index(inplace=True)
df1.to_csv('Dict1New2014.csv')
print(df1)
cyr_df1 = pd.DataFrame.from_dict(cyr_dictionary, orient='index')
cyr_df1.reset_index(inplace=True)
cyr_df1.to_csv('extra_Dict1New2014.csv')
print(cyr_df1)
