
# ------------------------- This script main function is to take a sbv subtitle file (with the timings) and extract the sentences, translate them as full sentences to minimize the loss of information within the
# ------------------------- translation process and then it chops them again and readds the timings. This only works if the sentences are properly capitalized, otherwise it has no way of knowing when a sentence starts or ends

# GERMAN WARNING ATCHUNG: If you want to translate from german or to german change the separator character to some character that does not appear in the text

separator_character = 'ß'

# Debugging mode disables the translation to avoid hitting the translation limit imposed by google when debugging the program
Debugging = True

from googletrans import Translator                                          # First we import the necessary libraries
from tkinter import filedialog
import math
import Small_Functions as sf
import os

# We set the source language and the desired Destination language for more information on the language codes go to the end of this document.(1)
Source_language = 'en'
Destination_language = 'ca'

# We import the translator instance to be used later on the translation process
if not Debugging:
    translator = Translator()

# This function returns the separated characters of a string
def String_to_char(Input_String):
    return [char for char in Input_String]

# We prompt the to select the subtitle file that it wants to translate
Subtitle_file = filedialog.askopenfilename(title='Select the input subtitle file', initialdir=r'C:\Users\minus\Documents\Fedellando\Video 5 Sand Filter\Subtitles', filetypes=(('sbv', '*.sbv'), ('All files', '*.*')))  # Prompt the user to open a file that contains the subtitle file to be translated.

# We extract the directory of the subtitle file and if it does not exist we create a folder on that same directory that will hold the translated files
Save_file_directory = sf.Full_path_adder('Translated Subtitle Files', os.path.dirname(Subtitle_file))
if not os.path.exists(Save_file_directory):
    os.mkdir(Save_file_directory)

# We extract the text from the subtitle file with universal encoding and we split the wile to an array at each newline character for further processing
Subtitle_text = open(Subtitle_file, "r",encoding='utf-8')
Subtitle_text_array = Subtitle_text.read().split('\n')

# We initialize some variables
Sentence_string = str()                 # This string will hold the entire script reconstructed
Meta_sentence_string = str()            # This string will hold the indices of the Text array that are actually text and not formatting strings
First_append = True

# We loof through the text in search for capitalized letters that will be set as the start of a sentence
for index,sub_sentence in enumerate(Subtitle_text_array):
    # We set a try statement because some sentences are blank (because of the formatting) and those will raise an error that will be ignored
    try:
        # If the sentence starts with an upper case it means it will be a new sentence so:
        if sub_sentence[0].isupper() or sub_sentence[1].isupper():

            # If it is the first sentence append we just append the sentence to the sentence string (which should be empty at this stage)
            # and we append the index to the Meta_sentence_string so that we know at which lines there is a string
            if First_append:
                Sentence_string +=(sub_sentence)
                Meta_sentence_string+=(str(index))
                First_append = False

            # If it is not the first append but the sub_sentence is still capitalized, we append this sentence with a newline character in front because it will be seen as the next independent sentence
            # We also append the index in a new line, this way we can know how many lines there are in each sentence
            else:
                Sentence_string +=('\n'+sub_sentence)
                Meta_sentence_string+=('\n'+str(index))

        # If the first letter is not capitalized and it is not a 0 (usually the formatting lines start with a 0) we append the sub_sentence as a continuation to the currently existing sentence,
        # and we also append the index as a continuation to the already existing indices to count the amount of lines at the current sentence
        elif sub_sentence[0] != '0':
            Sentence_string +=(' '+sub_sentence)
            Meta_sentence_string+=(','+str(index))

    # When a sentence is blank an error will be raised but we will ignore it. Yes I know the exception is too broad but for this purpose it works :3
    except Exception as e:
        # print(e)
        pass

# Some prints for debugging purposes
# print(Sentence_string)
# print(Meta_sentence_string)


# Now we split the generated strings at each new line to generate arrays, that will hold the sentences separated and the Metadata about the sentences.
Sentence_string_list = Sentence_string.split('\n')
Meta_sentence_string_list = Meta_sentence_string.split('\n')

# This list will hold the indices of the sentences that are spread out across more than one line
Meta_sentence_string_replace_list = list()

# For loop that transforms the Meta_sentence_string_list from string array to int array
for index,metadata in enumerate(Meta_sentence_string_list):
    # For each sentence is the Meta_sentence_string_list separate the numbers by each coma
    Meta_sentence_string_list[index] = metadata.split(',')

    # If the length is greater than 2
    if len(Meta_sentence_string_list[index])>=2:
        # Append the data into the new array with the sentences that will be spread across more than two lines
        Meta_sentence_string_replace_list.append(Meta_sentence_string_list[index])

# Prints for debugging purposes
# print(*Sentence_string_list,sep='\n')
# print(*Meta_sentence_string_list,sep='\n')
# print(*Meta_sentence_string_replace_list,sep='\n')

# This variable will hold the translated string
translated_string_list = list()

# We will loop through the entirety ow the Sentence_string_list and for each string we will translate it and store it in the translated_string_list
for string in Sentence_string_list:

    # Only execute if the string is not empty
    if string:

        if not Debugging:
            # Translate the current string with the specified source and destination language and append the text to the translated_string_list
            translated_sentence = translator.translate(string,dest= Destination_language,src=Source_language)
            translated_string_list.append(translated_sentence.text)

        if Debugging:
            translated_string_list.append(string)

# Print the translation for debugging purposes
# print(*translated_string_list,sep='\n')

# This variable will hold the translated string formatted to be split for the subtitle file
translated_string_list_formatted = list()

# If the destination language is NOT japanese, the sentences will be split either at comas or at whitespace characters. (In japanese, since they do not have space characters the sentences will be split only by character count)
if Destination_language != 'ja':

    # We loop through each translated sentence
    for index,translated_sentence_full in enumerate(translated_string_list):

        # If the original sentence was spread through more than one line, chances are that this one will have to be as well
        if len(Meta_sentence_string_list[index])>=2:

            # So we first chop the translated string into its constituent characters
            translated_sentence_full_temporal = String_to_char(translated_sentence_full)

            # Then we initialize the variables that will hold the amount of whitespaces in the current sentence, the places at which they are located and the ones most suitable to cut the string through.
            White_space_ammount = 0
            White_space_indexes = []
            Cutting_whitespaces = list()

            # Now we loop through each character within the chopped translated sentence and we search for the whitespaces
            for sub_index,character in enumerate(translated_sentence_full):

                # If the character is indeed a whitespace we increase the Whitespace count and we append its position to the White_space_indexes list
                if character == ' ':
                    White_space_ammount += 1
                    White_space_indexes.append(sub_index)

            # Once we have found all whitespaces we decide where to cut the string. To decide how many cuts the string will have we count the number of lines the original sentence was spread across. (it will be one less)
            for index_1,_ in enumerate(Meta_sentence_string_list[index]):

                # We reset the commafound variable to false at each loop
                commafound = False

                # If the index is 0 we skip the cutting. This way we will cut n-1 times (for example we will only cut 2 times if the sentence is spread across 3 lines).
                if index_1 == 0:
                    continue

                # After avoiding the first cut:
                else:
                    # We set the optimal white space to cut as the one that occupies the position corresponding to the current division over the total amount of needed divisions (for example if we need 3 divisions
                    # the current whitespace to cut will be placed first 1/3 of the way on the index list (if the list is 60 indices long it will be placed on index 20) and then on the next loop it will be placed 2/3
                    # of the way on the index list (if the list is 60 indices long it will be placed on index 40). This way the sentence can be easily divided into n lines
                    white_space_to_cut = White_space_indexes[math.floor(index_1*White_space_ammount/len(Meta_sentence_string_list[index]))]
                    # We append the currently selected white_space_to_cut to the list of cutting spaces for further cutting down the code
                    Cutting_whitespaces.append(white_space_to_cut)

                    # Since separating through a comma makes much more sense than separating through a whitespace (which can lead to broken sentences) we search around the selected cutting_whitespace (20 characters above
                    # and 20 characters below) for a comma. If such a comma exists we add a separator character that will indicate that the sentence is to be broken there (where the comma was).
                    for i in range(40):
                        if translated_sentence_full_temporal[min(max(0,white_space_to_cut - 20 +i),len(translated_sentence_full)-1)] == ',':
                            translated_sentence_full_temporal[min(max(0,white_space_to_cut - 20 +i),len(translated_sentence_full)-1)] = (','+separator_character)
                            # We set the comma found variable to true to indicate we have found a comma, and we break the loop to stop the search
                            commafound = True
                            break

                    # If a comma has not been found we add the separator character that will indicate that the sentence is to be broken there on the cutting whitespace location
                    if not commafound:
                        translated_sentence_full_temporal[white_space_to_cut] = separator_character

            # We join the characters from the chopped translated sentence into a full sentence
            translated_sentence_full_temporal = ''.join(translated_sentence_full_temporal)
            # And we split the sentence again through the selected separator characters
            translated_sentence_full_temporal = translated_sentence_full_temporal.split(separator_character)

            # And finally we append the current formatted sentence to the list of formatted sentences
            translated_string_list_formatted.append(translated_sentence_full_temporal)

        # Otherwise, if the original sentence is not spread across multiple lines we can just append the original sentence to the formatted list
        else:
            translated_string_list_formatted.append(translated_sentence_full)


# In the case that the destination language is japanese, we will split the strings based on character count, this is far from ideal since it means words can be broken, but making this work would probably lead to too much effort
elif Destination_language == 'ja':

    # We loop through each translated sentence
    for index, translated_sentence_full in enumerate(translated_string_list):

        # If the original sentence was spread through more than one line, chances are that this one will have to be as well
        if len(Meta_sentence_string_list[index]) >= 2:

            # So we first chop the translated string into its constituent characters
            translated_sentence_full_temporal = String_to_char(translated_sentence_full)

            # Once we have chopped we decide where to cut the string. To decide how many cuts the string will have we count the number of lines the original sentence was spread across. (it will be one less)
            for index_1, _ in enumerate(Meta_sentence_string_list[index]):

                # We reset the commafound variable to false at each loop
                commafound = False

                # If the index is 0 we skip the cutting. This way we will cut n-1 times (for example we will only cut 2 times if the sentence is spread across 3 lines).
                if index_1 == 0:
                    continue

                # After avoiding the first cut:
                else:
                    # We set the optimal place to cut as the one that occupies the position corresponding to the current division over the total amount of needed divisions (for example if we need 3 divisions
                    # the current place to cut will be placed first 1/3 of the way on the string (if the string is 60 characters long it will be placed on character 20) and then on the next loop it will be placed 2/3
                    # of the way on the string (if the string is 60 characters long it will be placed on character 40). This way the sentence can be easily divided into n lines
                    place_to_cut = math.floor(index_1 * len(translated_sentence_full_temporal) / len(Meta_sentence_string_list[index]))

                    # Since separating through a comma makes much more sense than separating through characters (which can lead to broken words) we search around the selected place_to_cut (20 characters above
                    # and 20 characters below) for a comma. If such a comma exists we add a separator character that will indicate that the sentence is to be broken there (where the comma was).
                    for i in range(40):
                        if translated_sentence_full_temporal[min(max(0,place_to_cut - 20 +i),len(translated_sentence_full_temporal)-1)] == ',':
                            translated_sentence_full_temporal[min(max(0,place_to_cut - 20 +i),len(translated_sentence_full_temporal)-1)] = (','+separator_character)
                            # We set the comma found variable to true to indicate we have found a comma, and we break the loop to stop the search
                            commafound = True
                            break

                    # If a comma has not been found we add the separator character that will indicate that the sentence is to be broken there on the cutting place location
                    if not commafound:
                        translated_sentence_full_temporal[place_to_cut] = separator_character

            # We join the characters from the chopped translated sentence into a full sentence
            translated_sentence_full_temporal = ''.join(translated_sentence_full_temporal)
            # And we split the sentence again through the selected separator characters
            translated_sentence_full_temporal = translated_sentence_full_temporal.split(separator_character)

            # And finally we append the current formatted sentence to the list of formatted sentences
            translated_string_list_formatted.append(translated_sentence_full_temporal)

        # Otherwise, if the original sentence is not spread across multiple lines we can just append the original sentence to the formatted list
        else:
            translated_string_list_formatted.append(translated_sentence_full)

# Some printing for debugging purposes
# print(*translated_string_list_formatted,sep='\n')

# This for loop erases all the leading and trailing whitespaces that would lead to ugly subtitle files.
# We loop through the translated list formatted
for index,sublist in enumerate(translated_string_list_formatted):

    # In the case that there is more than one sentence within the list we have to strip all the sub_sentences within the list
    if isinstance(sublist,list):

        # For each sub_sentence we strip it from the unnecessary whitespaces
        for sub_index,sentence in enumerate(sublist):
            translated_string_list_formatted[index][sub_index] = sentence.strip()

    # If the sublist is just one string we can strip it alone
    else:
        translated_string_list_formatted[index]= sublist.strip()

# We copy the original file to a new variable in which we will substitute the translated sentences but will leave the timings alone
translated_file = Subtitle_text_array

# Now we loop through the original file array substituting the old sentences for the translated ones
for main_index,sub_sentence in enumerate(Subtitle_text_array):

    # We have to loop through each Meta_sentence_string_list item in search for the index that corresponds to the original sentence
    for Meta_string_index,replace_index_list in enumerate(Meta_sentence_string_list):

        # We set a try because if the main index is not found on the current line of the Meta_sentence_string_list an ValueError is raised
        try:
            # We search for the main index within the replace_index_list, for each loop, (normally each replace index list will consist in anywhere from 1 to 5 values (could be more)
            # depending on how long the sentence is. If the main index is found within the current replace_index_list we return the place that the selected index holds within the current replace index list.
            # See end of the script for further explanation.(2)
            index_to_replace = replace_index_list.index(main_index)

            # If the translated_string_list_formatted correspondent to the current Meta_string_index is a list we have to extract only the selected sentence from within the list
            if isinstance(translated_string_list_formatted[Meta_string_index],list):
                translated_file[main_index] = translated_string_list_formatted[Meta_string_index][index_to_replace]

            # Otherwise if the translated_string_list_formatted correspondent to the current Meta_string_index is a string, we need to take it as a whole.
            else:
                translated_file[main_index] = translated_string_list_formatted[Meta_string_index]

        # Finally if the main index is not in the current line of the Meta_sentence_string_list we just pass onto the next
        except ValueError as e:
            # print(e)                          # For debugging purposes
            pass

# Finally we print the translated file for debugging purposes
# print(*translated_file,sep='\n')

# We set a name and path for the translated file with the destination language to easily differentiate the files within the save directory
Subtitle_file_translated = sf.Full_path_adder(('Captions in '+str(Destination_language)+' file.sbv'),Save_file_directory)

# Finally we open or create the file and we write line by line the translated file with a new line character per line, and of course we close the file to avoid crashes
Subtitle_file_sbv = open(Subtitle_file_translated,'w',encoding="utf-8")
for line in translated_file:
    Subtitle_file_sbv.write(str(line) + '\n')
    # print(current_image_hash)
    # print(file_duplicate_list)
Subtitle_file_sbv.close()

# (1)    ---------------------------------- Suported languages and corresponding codes: -----------------------------------------
#
#
# Language Name	Language Code
# Afrikaans	    af
# Irish	        ga
# Albanian	    sq
# Italian	    it
# Arabic	    ar
# Japanese	    ja
# Azerbaijani	az
# Kannada	    kn
# Basque	    eu
# Korean	    ko
# Bengali	    bn
# Latin	        la
# Belarusian	be
# Latvian	    lv
# Bulgarian 	bg
# Lithuanian	lt
# Catalan	    ca
# Macedonian	mk
# Chinese Simplified	zh-CN
# Malay	        ms
# Chinese Traditional	zh-TW
# Maltese	    mt
# Croatian	    hr
# Norwegian 	no
# Czech	        cs
# Persian	    fa
# Danish	    da
# Polish	    pl
# Dutch	        nl
# Portuguese	pt
# English	    en
# Romanian	    ro
# Esperanto 	eo
# Russian	    ru
# Estonian  	et
# Serbian	    sr
# Filipino  	tl
# Slovak    	sk
# Finnish   	fi
# Slovenian 	sl
# French	    fr
# Spanish	    es
# Galician  	gl
# Swahili	    sw
# Georgian	    ka
# Swedish	    sv
# German	    de
# Tamil	        ta
# Greek	        el
# Telugu	    te
# Gujarati	    gu
# Thai	        th
# Haitian Creole	ht
# Turkish	    tr
# Hebrew	    iw
# Ukrainian 	uk
# Hindi     	hi
# Urdu	        ur
# Hungarian 	hu
# Vietnamese	vi
# Icelandic	    is
# Welsh	        cy
# Indonesian	id
# Yiddish	    yi

# (2)    ---------------------------------- Further explanation about the unnecessarily complicated list search index selection process -----------------------------------------

# Now we loop through the original file array substituting the old sentences for the translated ones
# for main_index,sub_sentence in enumerate(Subtitle_text_array):
#
#     # We have to loop through each Meta_sentence_string_list item in search for the index that corresponds to the original sentence
#     for Meta_string_index,replace_index_list in enumerate(Meta_sentence_string_list):
#
#         # We set a try because some strings are empty which raises an error
#         try:
#             # We search for the main index within the replace_index_list, for each loop, (normally each replace index list will consist in anywhere from 1 to 5 values (could be more)
#             # depending on how long the sentence is. If the main index is found within the current replace_index_list we return the place that the selected index holds within the current replace index list.
#             index_to_replace = replace_index_list.index(main_index)
#
#             if isinstance(translated_string_list_formatted[Meta_string_index],list):
#                 translated_file[main_index] = translated_string_list_formatted[Meta_string_index][index_to_replace]
#             else:
#                 translated_file[main_index] = translated_string_list_formatted[Meta_string_index]
#
#             Example: originally the Meta_sentence_string_list could be something like the following:
#
#             [1,2]
#             [3]
#             [4,5,6,7]
#             [8]
#             [9,10]
#
#             Imagine the main_index (which we are searching for) is 6. Then the second for loop would loop through the Meta_sentence_string_list searching each line for the number 6, it would try and fail for the
#             first 2 loops and on the third it would find the 6 we are looking for and it would return the position of the 6 within the current replace index list which is 2. This will be used to extract the sentence which
#             is located in the translated_string_list_formatted list which has exactly the same shape as the Meta_sentence_string_list but instead of the indices it has the translated sentences that correspond, this way we can
#             substitute the original sentences with the translated ones on the correct location.