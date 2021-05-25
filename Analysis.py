import pandas as pd
import nltk
import re
import pymorphy2
def Formation(examples):
        try:
            examples = re.sub(r'((http(s)?://)|(www.))\S+', '', examples)       #С помощью RegEx избавляюсь от ссылок.
        except:
            print('тут был трабл')
        try:
            examples = re.sub(r'ru_de[a-zA-Z]*[а-яА-ЯёЁ]*[ ]', '', examples)    #С помощью RegEx избавляюсь от никнеймов.
        except:
            print('тут был трабл')
        try:
            examples = re.sub(r'edited at -- :', '', examples)                  #С помощью RegEx избавляюсь от технических выставок на отредактированных постах.
        except:
            print('тут был трабл')
        try:
            examples = re.sub(r'[0-9]', '', examples)                           #С помощью RegEx избавляюсь от цифр.
        except:
            print('тут был трабл')
        try:
            examples = examples.lower()                                         #Избавляюсь от проблем с регистром
        except:
            examples = str(examples)
        return (examples)
    
def Intersentence_func(Sentences):
    Intersentence = re.findall(r'[а-яА-ЯёЁ]+[.?!:;] ?[a-zA-Z]+ [a-zA-Z]+]', str(Sentences))
    Intersentence_1 = re.findall(r'[a-zA-Z]+ [a-zA-Z]+[.?!:;] ?[а-яА-ЯёЁ]+', str(Sentences))
    if len(Intersentence) > 0 or len(Intersentence_1) > 0:
        #print('новое предложение с другого алфавита')
        #print(Sentences_of_post)
        for Sent_index in range(len(Sentences) - 1):
            Latyn_Prev = re.findall(r'[a-zA-Z]', str(Sentences[Sent_index]))
            Latyn_Next = re.findall(r'[a-zA-Z]', str(Sentences[Sent_index + 1]))
            Cyr_Prev = re.findall(r'[а-яА-ЯёЁ]', str(Sentences[Sent_index]))
            Cyr_Next = re.findall(r'[а-яА-ЯёЁ]', str(Sentences[Sent_index + 1]))
            if ((len(Cyr_Prev) > 1 and len(Latyn_Prev) < 1) and (len(Latyn_Next) > 1 and len(Cyr_Next) < 1)) \
                    or ((len(Cyr_Prev) < 1 and len(Latyn_Prev) > 1) and (len(Latyn_Next) < 1 and len(Cyr_Next) > 1)):
                print('ИНТЕРСЕНТЕНЦИОНАЛЬНОСТЬ')
                print(Sentences)

def Bigramms(sentence, token_based, index_of_token, dict_of_bi):                #Проверяю 4 слова до и 4 слова после существительного 
    if index_of_token > 4 and index_of_token + 4 < len(sentence):               #на предмет глагола. Такое количество циклов
        for index_of_verb in range(index_of_token - 4, index_of_token + 4):     #необходимо для того, чтобы не выходить
            if 'VERB' in morph.parse(sentence[index_of_verb])[0].tag:           #за границы предложения.
                if token_based in dict_of_bi:
                    temp_list_of_cs_verb = list(dict_of_bi[token_based])
                    temp_list_of_cs_verb.append(sentence[index_of_verb])
                    dictionary_of_bigramms[token_based] = temp_list_of_cs_verb
                else:
                    dictionary_of_bigramms[token_based] = {sentence[index_of_verb]}
    if index_of_token > 4 and index_of_token + 4 >= len(sentence):
        for index_of_verb in range(index_of_token - 4, len(sentence)):
            if 'VERB' in morph.parse(sentence[index_of_verb])[0].tag:
                if token_based in dict_of_bi:
                    temp_list_of_cs_verb = list(dict_of_bi[token_based])
                    temp_list_of_cs_verb.append(sentence[index_of_verb])
                    dictionary_of_bigramms[token_based] = temp_list_of_cs_verb
                else:
                    dictionary_of_bigramms[token_based] = {sentence[index_of_verb]}
    if index_of_token <= 4 and index_of_token + 4 < len(sentence):
        for index_of_verb in range(0, index_of_token + 4):
            if 'VERB' in morph.parse(sentence[index_of_verb])[0].tag:
                if token_based in dict_of_bi:
                    temp_list_of_cs_verb = list(dict_of_bi[token_based])
                    temp_list_of_cs_verb.append(sentence[index_of_verb])
                    dictionary_of_bigramms[token_based] = temp_list_of_cs_verb
                else:
                    dictionary_of_bigramms[token_based] = {sentence[index_of_verb]}
    if index_of_token <= 4 and index_of_token + 4 >= len(sentence):
        for index_of_verb in range(0, len(sentence)):
            if 'VERB' in morph.parse(sentence[index_of_verb])[0].tag:
                if token_based in dict_of_bi:
                    temp_list_of_cs_verb = list(dict_of_bi[token_based])
                    temp_list_of_cs_verb.append(sentence[index_of_verb])
                    dictionary_of_bigramms[token_based] = temp_list_of_cs_verb
                else:
                    dictionary_of_bigramms[token_based] = {sentence[index_of_verb]}
                    
morph = pymorphy2.MorphAnalyzer()
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
raw = open('RUS.txt').read()                            #Первой проблемой был вопрос: откуда брать список русских слов. Сначала я нашел любительский словарь 
extra_raw = open('dict.opcorpora.txt').read()           #в интернете, но он показал низкую эффективность. Словарь от OpenCorpora оказался куда эффективнее.
extra_vocab = set(re.findall('[а-яА-ЯёЁ]+', extra_raw.lower())) #При их пересечении эффективность оказалась максимальной.
vocab= set(re.findall('\w+', raw.lower()))
xlsx = pd.read_excel('LJ1.xlsx', header=0)               #Датафрейм строился из файла LJ1. Это публикации полученные с помощью граббера за 2004-2020
data_df = pd.DataFrame(xlsx)
dictionary = {}
cyr_dictionary = {}
temp_list_of_cs_verb = []                               #Строчки 13-17 технические
dictionary_of_bigramms = {}
count_of_intersentence = 0
list_of_top_cs_words = ['абх', 'уни', 'аок', 'кауциона', 'финанцамт', 'еур', 'фермитер', 'кранкенкасса', 'хебамма', 'бюргерамт', 'манунг']
post_index = 0                                          #Список слов из топа LJ, выбранный вручную
for post in data_df['Post']:
    if data_df['Date'][post_index] > 2003:
        post = Formation(post)
        count_of_cs_pro_post = 0
        Sentences_of_post = nltk.tokenize.sent_tokenize(examples)           #Разбиваю посты на предложения
        Intersentence_func(Sentences_of_post)
        for Sentence_of_post in Sentences_of_post:                          #Цикл для интрасентенциональной обработки
            count_of_cs_pro_sentence = 0
            token_prev_temp_F = 2
            Cyrillics = re.findall(r'[а-яА-ЯёЁ]+', Sentence_of_post)
            if len(Cyrillics) > 0:                                          #Проверка на то, не написано ли предложение полностью на немецком
                tokens = tokenizer.tokenize(Sentence_of_post)               #Разбиваю предложение на слова
                for token in tokens:
                    token_temp = morph.parse(token)[0].normal_form          #Привожу слова к предполагаемой начальной форме
                    if token_temp.lower() in list_of_top_cs_words:          #Дальше начинается цикл для построение биграмм формата Существительное + Глагол
                        index_of_token_temp = tokens.index(token)           #для самых частотных существительных.
                        Bigramms(tokens, token_temp, index_of_token_temp, dictionary_of_bigramms)
                    if token_temp not in extra_vocab and token_temp not in vocab:   #в этом цикле мы находим нерусские слова (см. Readme)
                        if 'ru_de' not in token_temp:
                            if token_prev_temp_F == 0:
                                count_of_cs_pro_sentence = count_of_cs_pro_sentence + 1
                            if token_temp in dictionary:                            #для всех видов слов.
                                dictionary.update({token_temp: int(dictionary[token_temp]) + 1})
                            else:
                                dictionary[token_temp] = '1'
                            token_prev_temp_F = 1
                            Cyrillic = re.findall(r'[а-яА-ЯёЁ]+', token_temp)       #для слов в кириллическом написании.
                            if len(Cyrillic) > 0:
                                if token_temp in cyr_dictionary:
                                    cyr_dictionary.update({token_temp: int(cyr_dictionary[token_temp]) + 1})
                                else:
                                    cyr_dictionary[token_temp] = '1'
                     else:
                        if token_prev_temp_F == 1:
                            count_of_cs_pro_sentence = count_of_cs_pro_sentence + 1
                        token_prev_temp_F = 0
            if count_of_cs_pro_sentence > 6:
                print(Sentence_of_post)
            count_of_cs_pro_post = count_of_cs_pro_post + count_of_cs_pro_sentence
        if count_of_cs_pro_post > 20:
            print(count_of_cs_pro_post)
            print(post)                
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
