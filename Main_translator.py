import googletrans
from googletrans import Translator
from tkinter import filedialog

# translator = Translator()
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

for index,sub_sentence in enumerate(Subtitle_text_array):
    try:
        if sub_sentence[0].isupper() or sub_sentence[1].isupper():
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

# print(*Sentence_string_list,sep='\n')
# print(*Meta_sentence_string_list,sep='\n')

translated_string_list = list()

for string in Sentence_string_list:
