# Python program to translate
# speech to text and text to speech
import speech_recognition as sr
import pyttsx3
import pandas as pd
import numpy as np

# Read the CSV file containing all books of the bible
book = pd.read_csv('Books.csv')

# List all the bible chapters names
bibleNames = book['BookName'].tolist()

# Read the CSV file containing King James bible
bible = pd.read_csv('KJV_fixed.csv')

# Initialize the recognizer
r = sr.Recognizer()

# Function to convert text to
# speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 145)
    engine.say(command)
    engine.runAndWait()

# Loop infinitely for user to
# speak=
while (1):
    # Exception handling to handle
    # exceptions at the runtime
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=1)

            print("Ask me to read a chapter or verse of the bible")

            # listens for the user's input
            audio2 = r.listen(source2)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.upper()

            # Display the converted speech text
            print("Recognized Speech Text: ", str(MyText).upper())

            # Change converted speech text to Uppercase characters
            newCommand: str = str(MyText).upper()

            # Replace all empty space between words to #
            newCommand = newCommand.replace(" ", "#")

            # Split the user input text command
            splitCommand = newCommand.split("#")

            # Convert all word in the list to uppercase
            converted_list = [x.upper() for x in bibleNames]

            # print("Check: ", len(splitCommand), splitCommand)

            try:
                # Check for command keywords
                if splitCommand[0] == "READ" and "CHAPTER" in str(MyText).upper() or \
                        splitCommand[0] == "READ" and ":" in str(MyText).upper():

                    # Remove command keywords from the sentence
                    newCommand = newCommand.replace("READ#", "")

                    # Replace all empty space between words to #
                    newCommand = newCommand.replace(" ", "#")

                    # Set error state variable to 0
                    errorState = 0

                    # Split the user input text command
                    splitCommand = newCommand.split("#")

                    # Check if some keywords are present in the text command
                    if splitCommand[0] == "1st":
                        newCommand = newCommand.replace("1st#", "1 ")
                    if splitCommand[0] == "FIRST":
                        newCommand = newCommand.replace("FIRST#", "1 ")
                    if splitCommand[0] == "1ST":
                        newCommand = newCommand.replace("1ST#", "1 ")
                    # Check 2
                    if splitCommand[0] == "2nd":
                        newCommand = newCommand.replace("2nd#", "2 ")
                    if splitCommand[0] == "SECOND":
                        newCommand = newCommand.replace("SECOND#", "2 ")
                    if splitCommand[0] == "2ND":
                        newCommand = newCommand.replace("2ND#", "2 ")
                    # Check 3
                    if splitCommand[0] == "3rd":
                        newCommand = newCommand.replace("3rd#", "3 ")
                    if splitCommand[0] == "THIRD":
                        newCommand = newCommand.replace("THIRD#", "3 ")
                    if splitCommand[0] == "3RD":
                        newCommand = newCommand.replace("3RD#", "3 ")

                    # Split final input text
                    splitCommand = newCommand.split("#")

                    # Display the final command
                    print("Valid Command: ", newCommand.replace("#", " "))

                    # Scan through user input text command
                    for newData in splitCommand:

                        # Scan through the whole bible chapters for a match
                        for i in range(len(bibleNames)):
                            checkName: str = bibleNames[i].upper()

                            # Check if user input chapter and bible chapter match
                            if checkName == newData:

                                # Get the first split value
                                leftPart: str = newCommand.split(checkName)[0]

                                # Check if the first split value is empty or null
                                if leftPart == "" or leftPart == " ":
                                    rightPart: str = newCommand.split(checkName)[1]

                                    # Replace keywords CHAPTER and VERSE with empty values
                                    if "CHAPTER" in rightPart:
                                        rightPart = rightPart.replace("CHAPTER", "")
                                    if "VERSE" in rightPart:
                                        rightPart = rightPart.replace("VERSE", ":")

                                    # Check if the Chapter and verse is present separated using # and :
                                    if rightPart[0] == "#":

                                        # Replace the character # with an empty string
                                        rightPart = rightPart.replace("#", "")

                                        # Check if : is still in the sentence (for bible chapter and verse)
                                        if ":" in rightPart:
                                            # Split the chapter from the verse
                                            chapterVerse = rightPart.split(":")

                                            # Get the bible chapter
                                            chapter: int = int(chapterVerse[0])

                                            # Get the bible verse
                                            verse: int = int(chapterVerse[1])

                                            # Display the requested bible name, chapter and verse
                                            print("Book Index: ", i + 1)
                                            print("Read Book: ", checkName, " Chapter: ", chapter, ", Verse: ", verse)

                                            # Get the row with the requested bible name, chapter, and verse
                                            readRow = bible.loc[
                                                      (bible['BOOK'] == i + 1) & (bible['CHAPTER'] == chapter) &
                                                      (bible['VERSE'] == verse), :]

                                            # Convert the dataframe text to string value
                                            readText: str = ' '.join(readRow['TEXT'].tolist())
                                            print(readText)

                                            # Convert bible text to speech
                                            SpeakText(readText)

                                        # Do this if no bible verse is found
                                        else:
                                            # Replace keywords CHAPTER and VERSE with empty values
                                            if "CHAPTER" in rightPart:
                                                rightPart = rightPart.replace("CHAPTER", "")

                                            # Convert bible chapter text to integer value
                                            chapter: int = int(rightPart)

                                            # Display the requested bible name, chapter and verse
                                            print("Book Index: ", i + 1)
                                            print("Read Book: ", checkName, " Chapter: ", chapter)

                                            # Get the row with the requested bible name, chapter, and verse
                                            readRow = bible.loc[
                                                      (bible['BOOK'] == i + 1) & (bible['CHAPTER'] == chapter), :]

                                            # Convert the dataframe text to string value
                                            readText: str = ' '.join(readRow['TEXT'].tolist())
                                            print(readText)

                                            # Convert bible text to speech
                                            SpeakText(readText)

                                    # Do this if 1st, 2nd, 3rd keyword is before the bible chapter name
                                    else:
                                        # Check if : is still in the sentence (for bible chapter and verse)
                                        if ":" in rightPart:

                                            # Split the chapter from the verse
                                            chapterVerse = rightPart.split(":")

                                            # Convert bible chapter text to integer value
                                            chapter: int = int(chapterVerse[0])

                                            # Convert bible verse text to integer value
                                            verse: int = int(chapterVerse[1])

                                            # Display the requested bible name, chapter and verse
                                            print("Book Index: ", i + 1)
                                            print("Read Book: ", checkName, " Chapter: ", chapter, ", Verse: ", verse)

                                            # Get the row with the requested bible name, chapter, and verse
                                            readRow = bible.loc[
                                                      (bible['BOOK'] == i + 1) & (bible['CHAPTER'] == chapter) &
                                                      (bible['VERSE'] == verse), :]

                                            # Convert the dataframe text to string value
                                            readText: str = ' '.join(readRow['TEXT'].tolist())
                                            print(readText)

                                            # Convert bible text to speech
                                            SpeakText(readText)

                                        # Do this if only chapter is found and no verse
                                        else:
                                            # Replace chapter word with empty string value
                                            if "CHAPTER" in rightPart:
                                                rightPart = rightPart.replace("CHAPTER", "")

                                            # Convert bible chapter text to integer value
                                            chapter: int = int(rightPart)

                                            # Display the requested bible name and chapter
                                            print("Book Index: ", i + 1)
                                            print("Read Book: ", checkName, " Chapter: ", chapter)

                                            # Get the row with the requested bible name, chapter
                                            readRow = bible.loc[
                                                      (bible['BOOK'] == i + 1) & (bible['CHAPTER'] == chapter), :]

                                            # Convert the dataframe text to string value
                                            readText: str = ' '.join(readRow['TEXT'].tolist())
                                            print(readText)

                                            # Convert bible text to speech
                                            SpeakText(readText)
            except ValueError as e:
                print('Please Repeat Command')

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        errorState = 1
        print("No valid speech recognized")
