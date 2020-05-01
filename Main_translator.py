import googletrans
from googletrans import Translator
from tkinter import filedialog
import math
import os
import Small_Functions as sf

def split(word):
    return [char for char in word]

translator = Translator()
# print(translator.translate('Hola',dest= 'ca',src='es'))

Source_language = 'es'
Destination_language = 'ca'

# Subtitle_file = filedialog.askopenfilename(title='Select the input subtitle file', initialdir=r'C:\Users\minus\Documents\Fedellando\Video 5 Sand Filter\Subtitles', filetypes=(('sbv', '*.sbv'), ('All files', '*.*')))  # Prompt the user to open a file that contains the subtitle file to be translated.
Save_file_directory = filedialog.askdirectory(title='Select the directory where you want to save the resulting subtitle file', initialdir=r'C:\Users\minus\Documents\Fedellando\Video 5 Sand Filter\Subtitles', mustexist=True)  # Ask for the directory where the resulting subtitle file will be saved


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
Meta_sentence_string_replace_list = list()

for index,metadata in enumerate(Meta_sentence_string_list):
    Meta_sentence_string_list[index] = metadata.split(',')
    if len(Meta_sentence_string_list[index])>=2:
        Meta_sentence_string_replace_list.append(Meta_sentence_string_list[index])
    for sub_index,data in enumerate(Meta_sentence_string_list[index]):
        Meta_sentence_string_list[index][sub_index] = int(data)

for index,sublist in enumerate(Meta_sentence_string_replace_list):
    for sub_index,sub_value in enumerate(sublist):
        Meta_sentence_string_replace_list[index][sub_index] = int(sub_value)


# print(*Sentence_string_list,sep='\n')
# print(*Meta_sentence_string_list,sep='\n')
# print(*Meta_sentence_string_replace_list,sep='\n')

translated_string_list = list()

for string in Sentence_string_list:
    if string:
        # print(string+' to translate')
        translated_sentence = translator.translate(string,dest= Destination_language,src=Source_language)
        # translated_sentence = string
        translated_string_list.append(translated_sentence.text)
        # translated_string_list.append(translated_sentence)

# print(*translated_string_list,sep='\n')

translated_string_list_formatted = list()


for index,translated_sentence_full in enumerate(translated_string_list):
    if len(Meta_sentence_string_list[index])>=2:
        translated_sentence_full_temporal = split(translated_sentence_full)
        # print('------------Loop start-------------')
        # print(translated_sentence_full)
        # print(Meta_sentence_string_list[index])
        # print(len(Meta_sentence_string_list[index]))
        White_space_ammount = 0
        White_space_indexes = []
        Cutting_whitespaces = list()
        for sub_index,character in enumerate(translated_sentence_full):
            if character == ' ':
                White_space_ammount += 1
                White_space_indexes.append(sub_index)
        for index_1,_ in enumerate(Meta_sentence_string_list[index]):
            commafound = False
            if index_1 == 0:
                continue
            else:
                white_space_to_cut = White_space_indexes[math.floor(index_1*White_space_ammount/len(Meta_sentence_string_list[index]))]
                Cutting_whitespaces.append(white_space_to_cut)
                for i in range(40):
                    if translated_sentence_full_temporal[white_space_to_cut-20+i] == ',':
                        translated_sentence_full_temporal[white_space_to_cut - 20 + i] = ',ß'
                        commafound = True
                        break
                if not commafound:
                    translated_sentence_full_temporal[white_space_to_cut] = 'ß'

        # for index_1, _ in enumerate(Meta_sentence_string_list[index]):
        #
        translated_sentence_full_temporal = ''.join(translated_sentence_full_temporal)
        translated_sentence_full_temporal = translated_sentence_full_temporal.split('ß')

        # print('White spaces = '+str(White_space_ammount)+','+str(Cutting_whitespaces)+','+str(White_space_indexes))
        # print(translated_sentence_full_temporal)

        translated_string_list_formatted.append(translated_sentence_full_temporal)
    else:
        translated_string_list_formatted.append(translated_sentence_full)

# print(*translated_string_list_formatted,sep='\n')

for index,sublist in enumerate(translated_string_list_formatted):
    if isinstance(sublist,list):
        for sub_index,sentence in enumerate(sublist):
            translated_string_list_formatted[index][sub_index] = sentence.strip()
    else:
        translated_string_list_formatted[index]= sublist.strip()


translated_file = Subtitle_text_array

for main_index,sub_sentence in enumerate(Subtitle_text_array):
    for Meta_string_index,replace_index_list in enumerate(Meta_sentence_string_list):
        try:
            index_to_replace = replace_index_list.index(main_index)
            # print('current line to replace= '+str(main_index)+'   Index of the meta string to replace = '+str(index_to_replace))
            # print(translated_string_list_formatted[Meta_string_index])
            if isinstance(translated_string_list_formatted[Meta_string_index],list):
                translated_file[main_index] = translated_string_list_formatted[Meta_string_index][index_to_replace]
            else:
                translated_file[main_index] = translated_string_list_formatted[Meta_string_index]
            # print('replaced')
            # print('--------------')
            # print('Pre replacement: '+str(sub_sentence))
            # print('Post replacement: ' + str(translated_file[main_index]))
        except ValueError as e:
            # print(e)
            pass
    # print(translated_file)

print(*translated_file,sep='\n')

Subtitle_file_translated = sf.Full_path_adder(('Captions in '+str(Destination_language)+' file.sbv'),Save_file_directory)

Subtitle_file_sbv = open(Subtitle_file_translated,'w',encoding="utf-8")
for line in translated_file:
    Subtitle_file_sbv.write(str(line) + '\n')
    # print(current_image_hash)
    # print(file_duplicate_list)
Subtitle_file_sbv.close()

