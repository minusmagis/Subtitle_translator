import googletrans
from googletrans import Translator
from tkinter import filedialog
import math

translator = Translator()
# print(translator.translate('Hola',dest= 'ca',src='es'))

Source_language = 'es'
Destination_language = 'ca'

# Subtitle_file = filedialog.askopenfilename(title='Select the input subtitle file', initialdir=r'C:\Users\minus\Documents\Fedellando\Video 5 Sand Filter\Subtitles', filetypes=(('sbv', '*.sbv'), ('All files', '*.*')))  # Prompt the user to open a file that contains the subtitle file to be translated.
Subtitle_file = r'C:\Users\minus\Documents\Fedellando\Video 5 Sand Filter\Subtitles\Full spanish captions.sbv'
Subtitle_text = open(Subtitle_file, "r",encoding='utf-8')
Subtitle_text_array = Subtitle_text.read().split('\n')
# print(Subtitle_text.read().split('\n'))

Sentence_string = str()
Meta_sentence_string = str()
First_append = True

for index,sub_sentence in enumerate(Subtitle_text_array):
    try:
        if sub_sentence[0].isupper() or sub_sentence[1].isupper():
            if First_append:
                Sentence_string +=(sub_sentence)
                Meta_sentence_string+=(str(index))
                First_append = False
            else:
                Sentence_string +=('\n'+sub_sentence)
                Meta_sentence_string+=('\n'+str(index))
            # print(sub_sentence[0])
            # print(sub_sentence)
        elif sub_sentence[0] != '0':
            Sentence_string +=(' '+sub_sentence)
            Meta_sentence_string+=(','+str(index))
            # print(sub_sentence[0])
            # print(sub_sentence)

    except Exception as e:
        # print(e)
        pass

# print(Sentence_string)
# print(Meta_sentence_string)

Sentence_string_list = Sentence_string.split('\n')
Meta_sentence_string_list = Meta_sentence_string.split('\n')

for index,metadata in enumerate(Meta_sentence_string_list):
    Meta_sentence_string_list[index] = metadata.split(',')


# print(*Sentence_string_list,sep='\n')
# print(*Meta_sentence_string_list,sep='\n')

translated_string_list = list()

for string in Sentence_string_list:
    if string:
        # print(string+' to translate')
        # translated_sentence = translator.translate(string,dest= Destination_language,src=Source_language)
        translated_sentence = string
        # translated_string_list.append(translated_sentence.text)
        translated_string_list.append(translated_sentence)

# print(*translated_string_list,sep='\n')

translated_string_list_formatted = list()


for index,translated_sentence_full in enumerate(translated_string_list):
    if len(Meta_sentence_string_list[index])>=2:
        translated_sentence_full_temporal = translated_sentence_full
        print('------------Loop start-------------')
        # print(translated_sentence_full)
        print(Meta_sentence_string_list[index])
        print(len(Meta_sentence_string_list[index]))
        Comma_ammount = 0
        Comma_indexes = []
        Cutting_commas = list()
        White_space_ammount = 0
        White_space_indexes = []
        Cutting_whitespaces = list()
        for sub_index,character in enumerate(translated_sentence_full):
            if character == ',':
                Comma_ammount+=1
                Comma_indexes.append(sub_index)
            elif character == ' ':
                White_space_ammount += 1
                White_space_indexes.append(sub_index)
        for index_1,_ in enumerate(Meta_sentence_string_list[index]):
            if index_1 == 0:
                continue
            else:
                if Comma_ammount >0:
                    Cutting_commas.append(Comma_indexes[math.floor(index_1*Comma_ammount/len(Meta_sentence_string_list[index]))])
                else:
                    Cutting_whitespaces.append(White_space_indexes[math.floor(index_1*White_space_ammount/len(Meta_sentence_string_list[index]))])
        cutting_index = 0
        for index_1,_ in enumerate(Meta_sentence_string_list[index]):



        print('White spaces = '+str(White_space_ammount)+','+str(Cutting_whitespaces)+','+str(White_space_indexes))
        print('Commas = ' + str(Comma_ammount) + ',' + str(Cutting_commas) + ',' + str(Comma_indexes))
        print(translated_sentence_full)



# translated_file = str()
#
# for index,sub_sentence in enumerate(Subtitle_text_array):
#     for sub_indexes in Meta_sentence_string_list:
#         if index in sub_indexes:

