import pywhatkit
import speech_recognition as sr 
import pyttsx3
import datetime as dt
import time
#name = Finn

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

rate = engine.getProperty('rate')
engine.setProperty('rate', 150)

volume = engine.getProperty('volume')
engine.setProperty('volume',0.4)


def speak(command):
    '''Function used to make Finn speak'''

    engine.say(command)
    engine.runAndWait()



def listen_tts():
    '''Function to capture audio data and turn it into text
        @r = database to recognize speech
        @source = microphone with which he listens
        @voice = audio data recorded from source
        @command = text converted by google api from voice (audio data)'''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        audio = r.listen(source)
        transcription = ''
        try:
            transcription = r.recognize_google(audio, language='en-UK')
        except:
            pass
    return transcription.lower()



def whatsmsg(command):
    '''Send a whatsapp message to a registered contact of your choice
    @contacts must be inserted manually for now'''

    contacts = {'edoardo':'edoardo','eduardo':'edoardo','beo':'edoardo','balduz':'edoardo','balduzz':'edoardo','balducci':'edoardo','papi':'papi','papà':'papi','daddy':'papi','padre':'papi','dad':'papi','mami':'mami','mamma':'mami','madre':'mami','mom':'mami','mum':'mami','vicky':'vicky','vicks':'vicky','vittoria':'vicky','viko':'vicky','vichi':'vicky','vico':'vicky','tommy':'tommy','tommaso':'tommy','tommi':'tommy','tom':'tommy','diego':'diego','dieguz':'diego','bonfo':'bonfo','franscesco ognibene':'bonfo','ogni':'bonfo'}
    references = {'edoardo':'+39 347 965 7274','papi':'+39 338 851 5838','diego':'+39 331 480 7591','mami':'+39 392 050 7778','vicky':'+39 348 031 0890','tommy':'+39 349 939 6779','bonfo':'+39 328 398 4807'}

    splitcommand = set(command.split(' '))
    chooser = list(splitcommand.intersection(set(contacts)))
    
    person = contacts[chooser[0]]
    tnumber = references[person]

    msgcontent = ''
    while len(msgcontent) == 0:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            speak('What is the content of the message?')
            audio = r.listen(source)
            transcription = ''
            transcription = r.recognize_google(audio, language='en-UK')
            msgcontent = transcription.lower()

    pywhatkit.sendwhatmsg_instantly(tnumber,msgcontent,15,True,3)



def dateandtime(command):
    ''' Function needed to tell the time, day, month, year, either separately or together'''

    try:
        date = ['date','day','today','year','month']
        day_name = ['day','today']
        orario = ['hour','time']
        now = dt.datetime.now()
        if any(word in command for word in date):
            if 'date' in command:
                fulldate = now.strftime('%A %d %B')
                speak(fulldate)
            elif any(word in command for word in day_name):
                daywn = now.strftime('%A %d')
                speak(daywn)
            elif 'year' in command:
                year = now.strftime('%Y')
                speak(year)
            elif 'month' in command:
                month = now.strftime('%B')
                speak(month)
        elif any(word in command for word in orario):
            time = now.strftime('%H %M')
            speak(time)
    except:
        speak('dateandtime did not respond')



def funzione():
    pass



def sort():
    Wake = ('Finn','finn','fin','thin','pin')
    order = listen_tts()
    iterable = order.lower().split(' ')
    if any(i in Wake for i in iterable):
        #checks if there is a correspondence in name
        for name in Wake:
            if name in order:
                order = order.replace(name + ' ','')
                command = order
        try:
            try:
                a_array = ['send a message','send a whatsapp']
                if any(phrase in command for phrase in a_array):
                    whatsmsg(command)

                b_array = ['which day is it','what day is it','what is today','which time is it','which time is it','what day is today','what time is it','which day is today','what year is it','what month is it','which year is it','which month is it']
                if any(phrase in command for phrase in b_array):
                    dateandtime(command)
                
                c_array = []
                if any(phrase in command for phrase in c_array):
                    funzione(command)
                
                sort()

            except:
                speak('Sorry, I did not understand')
        except KeyboardInterrupt():
            pass
            
    else:
        sort()

sort()