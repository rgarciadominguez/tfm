import logging, json

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler,CallbackQueryHandler)

from airtable.airtable import Airtable
from datetime import date
from datetime import datetime


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

DECISION, CHALLENGENAME, JUDGENAME, JUDGEMAIL, JUDGE, JUDGE1, AMOUNT,DUEDATE, USERMAIL, ADDITIONAL, DATE, FINAL, EXISTING, FINAL1, REVIEW, DATE1, DUEDATE1, START= range(18)

#Configuration of Airtable
base_id = 'appQlPzd1zYwknW0b'
key = 'key9nBwO3xeJ3OcEj'
tabla = 'All'
tabla1= 'Users'
tabla2= 'Challenges'
tabla3= 'Judges'
airtable = Airtable(base_id, tabla, key)
airtable1= Airtable(base_id, tabla1, key)
airtable2= Airtable(base_id, tabla2, key)
airtable3= Airtable(base_id, tabla3, key)


#global variables
code = 1
code1 = 1
month = 0
day = 0
year = 0
completo=2
change=0
idioma=0
existing=0

name = "hola"
challengename= 0
duedate= "hola"
amount= 0
judge= "amperto"
result= "amperto2"
chat_id=0
judgeemail= "inicio"
useremail= "inicio1"
vfinal=0
nuevouser=0
nuevojudge=0
dia=0
mes=0
año=0
today=0

#variables buscar datos airtable
numerojudges=0
numerochallenges=0
numerousers=0
numchallenge=0
challenge=[]

#variables globales para guardar datos de database
challengename1="inicio"
challengename2="inicio"
challengename3="inicio"
challengename4="inicio"
challengename5="inicio"
challengename6="inicio"
challengename7="inicio"
challengename8="inicio"
challengename9="inicio"
challengename10="inicio"
challengename11="inicio"
challengename12="inicio"
judgenameJ= "inicio"
judgenameJ1= "inicio"
judgenameJ2= "inicio"
judgenameJ3= "inicio"
judgenameJ4= "inicio"
judgenameJ5= "inicio"
judgenameJ6= "inicio"
judgeemailJ= "inicio"
judgeemailJ1= "inicio"
judgeemailJ2= "inicio"
judgeemailJ3= "inicio"
judgeemailJ4= "inicio"
judgeemailJ5= "inicio"
judgeemailJ6= "inicio"

challengenameR="inicio"
amountR=0
duedateR="inicio"
judgeR= "inicio"
judgeemailR= "inicio"
useremailR= "inicio"
statusR= "inicio"

challengenameR1="inicio"
amountR1=0
duedateR1="inicio"
judgeR1= "inicio"
judgeemailR1= "inicio"
useremailR1= "inicio"
statusR1= "inicio"

challengenameR2="inicio"
amountR2=0
duedateR2="inicio"
judgeR2= "inicio"
judgeemailR2= "inicio"
useremailR2= "inicio"
statusR2= "inicio"



## PARTE 1
def start(update, context):
    keyboard = [[InlineKeyboardButton("Español", callback_data='Español'),
                 InlineKeyboardButton("English", callback_data='English')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Select you language.\n Selecciona tu idioma',
    reply_markup=reply_markup)

    return START

def start1(update, context):
    global code, chat_id, vfinal, nuevouser, nuevojudge, name, idioma
    idioma = update.callback_query.data
    print(idioma)
    numero = buscarcode()
    code = int(numero) + 1
    code = str(code)
    print(code)
    chat_id = str(update.effective_chat.id)

    #Actualizamos codigo del challenge
    verify = airtable.search('Code', code)
    while (verify != []):
        code= buscarcode()
        code = code + numero
        code = str(code)
        verify = airtable.search('Code', code)

    #Nuevo user o no
    verify1 = airtable1.search('User ID', chat_id)
    if verify1==[]:
        nuevouser==0
    else:
        ultimoemail = buscaruseremails()
        verify2 = ultimoemail[numerousers - 1]
        print(verify2)
        if (verify1 != []) and (verify2!="NA"):
            nuevouser = 1
            ultimo = buscarduedates()
            verify = ultimo[numerochallenges - 1]
            codes = buscarcode2()
            ultimocode = codes[numerochallenges - 1]
            print(verify)
            while verify == "NA":
                print("hola")
                airtable2.delete_by_field('Code', ultimocode)
                ultimo = buscarduedates()
                verify = ultimo[numerochallenges - 1]
        else:
            airtable1.delete_by_field('User ID',chat_id)
            codes = buscarcode2()
            ultimocode = codes[numerochallenges - 1]
            airtable2.delete_by_field('Code',ultimocode)
            nuevouser = 0

    print(nuevouser)
    #Nuevo judge o no
    verify2 = airtable3.search('JudgeID', chat_id)
    if (verify2 != []):
        nuevojudge = 1
    elif (verify1 == []):
        nuevojudge = 0

    name = update.effective_chat.first_name
    record = {'Code': code}
    record1= {'User ID': chat_id}
    record2 = {'User name': name}
    airtable.insert(record)
    rellenarairtable()

    airtable.update_by_field('Code', code, record1)
    airtable.update_by_field('Code', code, record2)

    if idioma=="English":
        keyboard = [[InlineKeyboardButton("Create", callback_data='Create'),
                     InlineKeyboardButton("Judge", callback_data='Judge'),
                     InlineKeyboardButton("My Challenges", callback_data='Review')]]
        keyboard1 = [[InlineKeyboardButton("Create", callback_data='Create'),
                     InlineKeyboardButton("Judge", callback_data='Judge')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_markup1 = InlineKeyboardMarkup(keyboard1)

        if nuevouser==0:
            context.bot.send_message(chat_id, text='Hello {}. Welcome to our Challengers Club. Here we want you to be the best of yourself and perform all the goals that you will to achieve'.format(name))
            context.bot.send_message(chat_id, text='I am here to help you. The following MENU is going to be useful whenever you want a change what you are doing. Select the action that you wanna do. ',
                                      reply_markup=reply_markup1,)
        else:
            context.bot.send_message(chat_id, text='Hi {}, how are you doing?'.format(name))
            context.bot.send_message(chat_id, text='The following MENU is going to be useful whenever you want a change what you are doing. Select the action that you wanna do. ',
                                      reply_markup=reply_markup)

        return DECISION
    elif idioma=="Español":
        keyboard = [[InlineKeyboardButton("Crear", callback_data='Create'),
                     InlineKeyboardButton("Juzgar", callback_data='Judge'),
                     InlineKeyboardButton("Mis Retos", callback_data='Review')]]
        keyboard1 = [[InlineKeyboardButton("Crear", callback_data='Create'),
                      InlineKeyboardButton("Juzgar", callback_data='Judge')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_markup1 = InlineKeyboardMarkup(keyboard1)

        if nuevouser == 0:
            context.bot.send_message(chat_id,
                                     text='Hola {}. Welcome to our Challengers Club. Here we want you to be the best of yourself and perform all the goals that you will to achieve'.format(
                                         name))
            context.bot.send_message(chat_id,
                                     text='Estoy aquí para ayudarte. The following MENU is going to be useful whenever you want a change what you are doing. Select the action that you wanna do. ',
                                     reply_markup=reply_markup1, )
        else:
            context.bot.send_message(chat_id, text='Hello {}, how are you doing?'.format(name))
            context.bot.send_message(chat_id,
                                     text='El siguiente Menu is going to be useful whenever you want a change what you are doing. Select the action that you wanna do. ',
                                     reply_markup=reply_markup)

        return DECISION

def start2(update, context):
    global code, chat_id, vfinal, nuevouser, nuevojudge, name, idioma
    idioma=update.message.text
    if idioma=="español" or idioma=="english":
        numero = 1
        code = int(code) + numero
        code = str(code)
        chat_id = str(update.effective_chat.id)

        # Actualizamos codigo del challenge
        verify = airtable.search('Code', code)
        while (verify != []):
            code = buscarcode()
            code = code + numero
            code = str(code)
            verify = airtable.search('Code', code)

        # Nuevo user o no
        verify1 = airtable1.search('User ID', chat_id)
        if verify1 == []:
            nuevouser == 0
        else:
            ultimoemail = buscaruseremails()
            verify2 = ultimoemail[numerousers - 1]
            print(verify2)
            if (verify1 != []) and (verify2 != "NA"):
                nuevouser = 1
            else:
                airtable1.delete_by_field('User ID', chat_id)
                nuevouser = 0

        print(nuevouser)
        # Nuevo judge o no
        verify2 = airtable3.search('JudgeID', chat_id)
        if (verify2 != []):
            nuevojudge = 1
        elif (verify1 == []):
            nuevojudge = 0

        name = update.effective_chat.first_name
        record = {'Code': code}
        record1 = {'User ID': chat_id}
        record2 = {'User name': name}
        airtable.insert(record)
        rellenarairtable()

        airtable.update_by_field('Code', code, record1)
        airtable.update_by_field('Code', code, record2)

        if idioma == "English":
            keyboard = [[InlineKeyboardButton("Create", callback_data='Create'),
                         InlineKeyboardButton("Judge", callback_data='Judge'),
                         InlineKeyboardButton("My Challenges", callback_data='Review')]]
            keyboard1 = [[InlineKeyboardButton("Create", callback_data='Create'),
                          InlineKeyboardButton("Judge", callback_data='Judge')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            reply_markup1 = InlineKeyboardMarkup(keyboard1)

            if nuevouser == 0:
                context.bot.send_message(chat_id,
                                         text='Hello {}. Welcome to our Challengers Club. Here we want you to be the best of yourself and perform all the goals that you will to achieve'.format(
                                             name))
                context.bot.send_message(chat_id,
                                         text='I am here to help you. The following MENU is going to be useful whenever you want a change what you are doing. Select the action that you wanna do. ',
                                         reply_markup=reply_markup1, )
            else:
                context.bot.send_message(chat_id, text='Hi {}, how are you doing?'.format(name))
                context.bot.send_message(chat_id,
                                         text='The following MENU is going to be useful whenever you want a change what you are doing. Select the action that you wanna do. ',
                                         reply_markup=reply_markup)

            return DECISION
        elif idioma=="Español":
            keyboard = [[InlineKeyboardButton("Crear", callback_data='Create'),
                         InlineKeyboardButton("Juzgar", callback_data='Judge'),
                         InlineKeyboardButton("Mis Retos", callback_data='Review')]]
            keyboard1 = [[InlineKeyboardButton("Crear", callback_data='Create'),
                          InlineKeyboardButton("Juzgar", callback_data='Judge')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            reply_markup1 = InlineKeyboardMarkup(keyboard1)

            if nuevouser == 0:
                context.bot.send_message(chat_id,
                                         text='Hola {}. Welcome to our Challengers Club. Here we want you to be the best of yourself and perform all the goals that you will to achieve'.format(
                                             name))
                context.bot.send_message(chat_id,
                                         text='Estoy aquí para ayudarte. The following MENU is going to be useful whenever you want a change what you are doing. Select the action that you wanna do. ',
                                         reply_markup=reply_markup1, )
            else:
                context.bot.send_message(chat_id, text='Hello {}, how are you doing?'.format(name))
                context.bot.send_message(chat_id,
                                         text='El siguiente Menu is going to be useful whenever you want a change what you are doing. Select the action that you wanna do. ',
                                         reply_markup=reply_markup)

            return DECISION
    else:
        keyboard = [[InlineKeyboardButton("Español", callback_data='Español'),
                     InlineKeyboardButton("English", callback_data='Ingles')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Sorry, I could not understand you. Select the languages pressing in the buttons below this message\n'
                                  'Perdona no te he entendido. Por favor, selecciona el idioma de los botones que aparecen debajo de este mensaje',
                                  reply_markup=reply_markup)

        return START

def decision(update, context):
    global chat_id, code, nuevouser, nuevojudge, challengename1, challengename2,challengename3,challengename4,challengename5,challengename6,challengename7
    global challengename8,challengename9,challengename10,challengename11,challengename12
    global numchallenge, challenge, completo
    verify1 = airtable1.search('User ID', chat_id)
    if verify1==[]:
        nuevouser==0
    else:
        ultimoemail = buscaruseremails()
        verify2 = ultimoemail[numerousers - 1]
        print(verify2)
        if (verify1 != []) and (verify2!="NA"):
            nuevouser = 1
        else:
            airtable1.delete_by_field('User ID',chat_id)
            nuevouser = 0
            codes = buscarcode2()
            ultimocode = codes[numerochallenges - 1]
            airtable2.delete_by_field('Code',ultimocode)
    query = update.callback_query.data
    print(query)
    chat_id = update.effective_chat.id
    if query == "Create":
        chat_id= str(chat_id)
        name = update.effective_chat.first_name
        record = {'Challenger or not': 'Yes'}
        record2 = {'Code': code}
        record3= {'User ID': chat_id}
        record4= {'User name': name}
        print("SIGUIENTE")
        print(nuevouser)
        if nuevouser!=0:
            ultimo=buscarduedates()
            verify=ultimo[numerochallenges-1]
            codes=buscarcode2()
            ultimocode=codes[numerochallenges-1]
            print(verify)
            while verify=="NA":
                print("hola")
                airtable2.delete_by_field('Code',ultimocode)
                verify3 = airtable3.search("Code", ultimocode)
                print(verify3)
                print(ultimocode)
                if verify3!=[]:
                     airtable3.delete_by_field("Code",ultimocode)
                ultimo = buscarduedates()
                verify = ultimo[len(ultimo) - 1]
                codes = buscarcode2()
                ultimocode = codes[len(codes) - 1]
        airtable2.insert(record2)
        rellenarairtable2()

        print(nuevouser)
        if nuevouser==0:
            completo=0
            airtable1.insert(record3)
            rellenarairtable1()
            airtable1.update_by_field('User ID', chat_id, record4)
            airtable.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record3)

            if idioma=="English":
                context.bot.send_message(chat_id, text='Great {}. Lets do it!'.format(name))
                context.bot.send_message(chat_id,
                                         text='How do you want to name the challenge?. Use the Menu above if you wanna change what to do.',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='Perfecto {}. Lets do it!'.format(name))
                context.bot.send_message(chat_id,
                                         text='¿Cómo quieres llamar al reto?. Use the Menu above if you wanna change what to do.',
                                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

            return CHALLENGENAME
        else:
            completo=0
            airtable.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record3)

            if idioma=="English":
                context.bot.send_message(chat_id, text='Great {}. Lets do it!'.format(name))
                context.bot.send_message(chat_id,
                                         text='How do you want to name the challenge?. Use the Menu above if you wanna change what to do.',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='Perfecto {}. Lets do it!'.format(name))
                context.bot.send_message(chat_id,
                                         text='¿Cómo quieres llamar al reto?. Use the Menu above if you wanna change what to do.',
                                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

            return CHALLENGENAME

    elif query == "Judge":
        completo=0
        record = {'Challenger or not': 'No'}
        airtable.update_by_field('Code', code, record)
        if idioma=="English":
            context.bot.send_message(chat_id, text='I see! Please, send the code of the challenge that you want to judge. Use the Menu above if you'
                                                   ' wanna change what to do. ',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
        elif idioma=="Español":
            context.bot.send_message(chat_id, text='I see! Please, send the code of the challenge that you want to judge. Use the Menu above if you wanna'
                                                   ' change what to do. ',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
        return JUDGE
    elif query == "Review":
        ultimo=buscarduedates()
        verify=ultimo[numerochallenges-1]
        codes=buscarcode2()
        ultimocode=codes[numerochallenges-1]
        print(verify)
        while verify=="NA":
            print("hola")
            airtable2.delete_by_field('Code',ultimocode)
            verify3 = airtable3.search("Code", ultimocode)
            print(verify3)
            print(ultimocode)
            if verify3!=[]:
                 airtable3.delete_by_field("Code",ultimocode)
            ultimo = buscarduedates()
            verify = ultimo[len(ultimo) - 1]
            codes = buscarcode2()
            ultimocode = codes[len(codes) - 1]
        completo=0
        challenge= buscarchallenges()
        print(challenge)
        print(challenge[0])
        numchallenge= len(challenge)
        print(numchallenge)
        record = {'Challenger or not': 'No'}
        airtable.update_by_field('Code', code, record)
        if numchallenge==1:
            print("AQII")
            challengename1=challenge[0]
            print(challengename1)
            keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if idioma=="English":
                context.bot.send_message(chat_id, text='You have the following challenges. See its descriptions and status pressing in its name'
                                                       ' in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup )
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='Tienes los siguientes retos. See its descriptions and status pressing in its name'
                                                       ' in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup )
            return REVIEW
        elif numchallenge==2:
            challengename1 = challenge[numchallenge - 1]
            challengename2 = challenge[numchallenge - 2]
            keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                        InlineKeyboardButton(challengename2, callback_data='Challenge2')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if idioma == "English":
                context.bot.send_message(chat_id,
                                         text='You have the following challenges. See its descriptions and status pressing in its name'
                                              ' in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup)
            elif idioma == "Español":
                context.bot.send_message(chat_id,
                                         text='Tienes los siguientes retos. See its descriptions and status pressing in its name'
                                              ' in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup)
            return REVIEW
        elif numchallenge==3:
            challengename1 = challenge[numchallenge - 1]
            challengename2 = challenge[numchallenge - 2]
            challengename3 = challenge[numchallenge - 3]
            keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                        InlineKeyboardButton(challengename2, callback_data='Challenge2'),
                        InlineKeyboardButton(challengename3, callback_data='Challenge3')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if idioma=="English":
                context.bot.send_message(chat_id, text='You have the following challenges. See its descriptions and status pressing in its name'
                                                       ' in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup )
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='Tienes los siguientes retos. See its descriptions and status pressing in its name'
                                                       ' in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup )
            return REVIEW
        elif numchallenge==4:
            challengename1 = challenge[numchallenge - 1]
            challengename2 = challenge[numchallenge - 2]
            challengename3 = challenge[numchallenge - 3]
            challengename4 = challenge[numchallenge - 4]
            keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                        InlineKeyboardButton(challengename2, callback_data='Challenge2')],
                        [InlineKeyboardButton(challengename3, callback_data='Challenge3'),
                        InlineKeyboardButton(challengename4, callback_data='Challenge4')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if idioma=="English":
                context.bot.send_message(chat_id, text='You have the following challenges. See its descriptions and status pressing in its name'
                                                       ' in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup )
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='Tienes los siguientes retos. See its descriptions and status pressing in its name'
                                                       ' in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup )
            return REVIEW
        elif numchallenge==4:
            challengename1 = challenge[numchallenge - 1]
            challengename2 = challenge[numchallenge - 2]
            challengename3 = challenge[numchallenge - 3]
            challengename4 = challenge[numchallenge - 4]
            keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                        InlineKeyboardButton(challengename2, callback_data='Challenge2')],
                        [InlineKeyboardButton(challengename3, callback_data='Challenge3'),
                        InlineKeyboardButton(challengename4, callback_data='Challenge4')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if idioma=="English":
                context.bot.send_message(chat_id, text='You have the following challenges. See its descriptions and status pressing in its name'
                                                       ' in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup )
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='Tienes los siguientes retos. See its descriptions and status pressing in its name'
                                                       ' in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup )
            return REVIEW
        elif numchallenge==5:
            challengename1 = challenge[numchallenge - 1]
            challengename2 = challenge[numchallenge - 2]
            challengename3 = challenge[numchallenge - 3]
            challengename4 = challenge[numchallenge - 4]
            challengename5 = challenge[numchallenge - 5]
            keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                        InlineKeyboardButton(challengename2, callback_data='Challenge2'),
                         InlineKeyboardButton(challengename3, callback_data='Challenge3')],
                        [InlineKeyboardButton(challengename4, callback_data='Challenge4'),
                        InlineKeyboardButton(challengename5, callback_data='Challenge5')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if idioma=="English":
                context.bot.send_message(chat_id, text='You have the following challenges. See its descriptions and status pressing in its name'
                                                       ' in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup )
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='Tienes los siguientes retos. See its descriptions and status pressing in its name'
                                                       ' in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup )
            return REVIEW
        elif numchallenge>=6:
            challengename1 = challenge[numchallenge - 1]
            challengename2 = challenge[numchallenge - 2]
            challengename3 = challenge[numchallenge - 3]
            challengename4 = challenge[numchallenge - 4]
            challengename5 = challenge[numchallenge - 5]
            challengename6 = challenge[numchallenge - 6]
            keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                        InlineKeyboardButton(challengename2, callback_data='Challenge2')],
                        [InlineKeyboardButton(challengename3, callback_data='Challenge3'),
                        InlineKeyboardButton(challengename4, callback_data='Challenge4')],
                        [InlineKeyboardButton(challengename5, callback_data='Challenge5'),
                         InlineKeyboardButton(challengename6, callback_data='Challenge6')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if idioma=="English":
                context.bot.send_message(chat_id, text='You have the following challenges. See its descriptions and status pressing in its name'
                                                       ' in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup )
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='Tienes los siguientes retos. See its descriptions and status pressing in its name'
                                                       ' in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup )
            return REVIEW

def decision1(update,context):
    global chat_id, name
    text= update.message.text
    verify1 = airtable1.search('User ID', chat_id)
    if verify1==[]:
        nuevouser==0
    else:
        ultimoemail = buscaruseremails()
        verify2 = ultimoemail[numerousers - 1]
        print(verify2)
        if (verify1 != []) and (verify2!="NA"):
            nuevouser = 1
        else:
            nuevouser = 0
    if text== "Create" or text== "create":
        chat_id = str(chat_id)
        name = update.effective_chat.first_name
        record = {'Challenger or not': 'Yes'}
        record2 = {'Code': code}
        record3 = {'User ID': chat_id}
        record4 = {'User name': name}
        if nuevouser!=0:
            ultimo=buscarduedates()
            verify=ultimo[numerochallenges-1]
            codes=buscarcode2()
            ultimocode=codes[numerochallenges-1]
            print(verify)
            while verify=="NA":
                print("hola")
                airtable2.delete_by_field('Code',ultimocode)
                verify3 = airtable3.search("Code", ultimocode)
                print(verify3)
                print(ultimocode)
                if verify3!=[]:
                     airtable3.delete_by_field("Code",ultimocode)
                ultimo = buscarduedates()
                verify = ultimo[len(ultimo) - 1]
                codes = buscarcode2()
                ultimocode = codes[len(codes) - 1]
        airtable2.insert(record2)
        rellenarairtable2()
        airtable2.update_by_field('Code',code,record3)

        print(nuevouser)
        if nuevouser == 0:
            airtable1.insert(record3)
            rellenarairtable1()
            airtable1.update_by_field('User ID', chat_id, record4)
            airtable.update_by_field('Code', code, record)

            if idioma=="English":
                context.bot.send_message(chat_id, text='Great {}. Lets do it!'.format(name))
                context.bot.send_message(chat_id,
                                         text='How do you want to name the challenge?. Use the Menu above if you wanna change what to do.',
                                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='Perfecto {}. Lets do it!'.format(name))
                context.bot.send_message(chat_id,
                                         text='¿Cómo quieres llamar el reto?. Use the Menu above if you wanna change what to do.',
                                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

            return CHALLENGENAME
        else:
            airtable.update_by_field('Code', code, record)

            if idioma=="English":
                context.bot.send_message(chat_id, text='Great {}. Lets do it!'.format(name))
                context.bot.send_message(chat_id,
                                         text='How do you want to name the challenge?. Use the Menu above if you wanna change what to do.',
                                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='Perfecto {}. Lets do it!'.format(name))
                context.bot.send_message(chat_id,
                                         text='¿Cómo quieres llamar el reto?. Use the Menu above if you wanna change what to do.',
                                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

            return CHALLENGENAME
    elif text== "Judge" or text=="judge":
        completo=0
        record = {'Challenger or not': 'No'}
        airtable.update_by_field('Code', code, record)
        if idioma=="English":
            context.bot.send_message(chat_id, text='I see! Please, send the code of the challenge that you want to judge. Use the Menu above if you wanna'
                                                   ' change what to do. ',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
        elif idioma=="Español":
            context.bot.send_message(chat_id, text='Enviame el código del reto que quieres juzgar por favor. Use the Menu above if you wanna'
                                                   ' change what to do. ',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
        return JUDGE
    elif text== "My challenges" or text=="my challenges":
        ultimo=buscarduedates()
        verify=ultimo[numerochallenges-1]
        codes=buscarcode2()
        ultimocode=codes[numerochallenges-1]
        print(verify)
        while verify=="NA":
            print("hola")
            airtable2.delete_by_field('Code',ultimocode)
            verify3 = airtable3.search("Code", ultimocode)
            print(verify3)
            print(ultimocode)
            if verify3!=[]:
                 airtable3.delete_by_field("Code",ultimocode)
            ultimo = buscarduedates()
            verify = ultimo[len(ultimo) - 1]
            codes = buscarcode2()
            ultimocode = codes[len(codes) - 1]
        completo=0
        challenge= buscarchallenges()
        numchallenge= len(challenge)
        print(numchallenge)
        record = {'Challenger or not': 'No'}
        airtable.update_by_field('Code', code, record)
        if numchallenge==1:
            challengename1=challenge[numchallenge-1]
            keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if idioma=="English":
                context.bot.send_message(chat_id, text=
                'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                reply_markup=reply_markup)
            elif idioma=="Español":
                context.bot.send_message(chat_id, text=
                'Tienes los siguientes retos. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                reply_markup=reply_markup)
            return REVIEW
        elif numchallenge==2:
            challengename1 = challenge[numchallenge - 1]
            challengename2 = challenge[numchallenge - 2]
            keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                        InlineKeyboardButton(challengename2, callback_data='Challenge2')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if idioma=="English":
                context.bot.send_message(chat_id, text=
                'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                reply_markup=reply_markup)
            elif idioma=="Español":
                context.bot.send_message(chat_id, text=
                'Tienes los siguientes retos. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                reply_markup=reply_markup)
            return REVIEW
        elif numchallenge==3:
            challengename1 = challenge[numchallenge - 1]
            challengename2 = challenge[numchallenge - 2]
            challengename3 = challenge[numchallenge - 3]
            keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                        InlineKeyboardButton(challengename2, callback_data='Challenge2'),
                        InlineKeyboardButton(challengename3, callback_data='Challenge3')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if idioma=="English":
                context.bot.send_message(chat_id, text=
                'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                reply_markup=reply_markup)
            elif idioma=="Español":
                context.bot.send_message(chat_id, text=
                'Tienes los siguientes retos. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                reply_markup=reply_markup)
            return REVIEW
        elif numchallenge==4:
            challengename1 = challenge[numchallenge - 1]
            challengename2 = challenge[numchallenge - 2]
            challengename3 = challenge[numchallenge - 3]
            challengename4 = challenge[numchallenge - 4]
            keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                        InlineKeyboardButton(challengename2, callback_data='Challenge2')],
                        [InlineKeyboardButton(challengename3, callback_data='Challenge3'),
                        InlineKeyboardButton(challengename4, callback_data='Challenge4')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if idioma=="English":
                context.bot.send_message(chat_id, text=
                'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                reply_markup=reply_markup)
            elif idioma=="Español":
                context.bot.send_message(chat_id, text=
                'Tienes los siguientes retos. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                reply_markup=reply_markup)
            return REVIEW
        elif numchallenge==4:
            challengename1 = challenge[numchallenge - 1]
            challengename2 = challenge[numchallenge - 2]
            challengename3 = challenge[numchallenge - 3]
            challengename4 = challenge[numchallenge - 4]
            keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                        InlineKeyboardButton(challengename2, callback_data='Challenge2')],
                        [InlineKeyboardButton(challengename3, callback_data='Challenge3'),
                        InlineKeyboardButton(challengename4, callback_data='Challenge4')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if idioma=="English":
                context.bot.send_message(chat_id, text=
                'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                reply_markup=reply_markup)
            elif idioma=="Español":
                context.bot.send_message(chat_id, text=
                'Tienes los siguientes retos. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                reply_markup=reply_markup)
            return REVIEW
        elif numchallenge==5:
            challengename1 = challenge[numchallenge - 1]
            challengename2 = challenge[numchallenge - 2]
            challengename3 = challenge[numchallenge - 3]
            challengename4 = challenge[numchallenge - 4]
            challengename5 = challenge[numchallenge - 5]
            keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                        InlineKeyboardButton(challengename2, callback_data='Challenge2'),
                         InlineKeyboardButton(challengename3, callback_data='Challenge3')],
                        [InlineKeyboardButton(challengename4, callback_data='Challenge4'),
                        InlineKeyboardButton(challengename5, callback_data='Challenge5')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if idioma=="English":
                context.bot.send_message(chat_id, text=
                'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                reply_markup=reply_markup)
            elif idioma=="Español":
                context.bot.send_message(chat_id, text=
                'Tienes los siguientes retos. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                reply_markup=reply_markup)
            return REVIEW
        elif numchallenge>=6:
            challengename1 = challenge[numchallenge - 1]
            challengename2 = challenge[numchallenge - 2]
            challengename3 = challenge[numchallenge - 3]
            challengename4 = challenge[numchallenge - 4]
            challengename5 = challenge[numchallenge - 5]
            challengename6 = challenge[numchallenge - 6]
            keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                        InlineKeyboardButton(challengename2, callback_data='Challenge2')],
                        [InlineKeyboardButton(challengename3, callback_data='Challenge3'),
                        InlineKeyboardButton(challengename4, callback_data='Challenge4')],
                        [InlineKeyboardButton(challengename5, callback_data='Challenge5'),
                         InlineKeyboardButton(challengename6, callback_data='Challenge6')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if idioma=="English":
                context.bot.send_message(chat_id, text=
                'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                reply_markup=reply_markup)
            elif idioma=="Español":
                context.bot.send_message(chat_id, text=
                'Tienes los siguientes retos. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                reply_markup=reply_markup)
            return REVIEW
    else:
        keyboard = [[InlineKeyboardButton("Create", callback_data='Create'),
                     InlineKeyboardButton("Judge", callback_data='Judge'),
                     InlineKeyboardButton("My Challenges", callback_data='Review')]]
        keyboard1 = [[InlineKeyboardButton("Create", callback_data='Create'),
                      InlineKeyboardButton("Judge", callback_data='Judge')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_markup1 = InlineKeyboardMarkup(keyboard1)
        if idioma == "English":
            update.message.reply_text(
                'Sorry you should decide what to do. Please, use the Menu below',
                reply_markup=reply_markup1)
        elif idioma == "Español":
            update.message.reply_text(
                'Lo siento tienes que decidir que quieres hacer. Please, use the Menu below',
                reply_markup=reply_markup)

        return DECISION

def decision2(update, context):
    global code, chat_id,nuevouser, change
    global judgenameJ, judgenameJ1, judgenameJ2, judgeemailJ2, judgeemailJ1, judgeemailJ, judgenameJ3, judgenameJ4, judgenameJ5, judgeemailJ3, judgeemailJ4, judgeemailJ5
    query = update.callback_query.data
    print("SIGUIENTE")
    print(change)
    if change==0:
        verify1 = airtable1.search('User ID', chat_id)
        if verify1==[]:
            nuevouser==0
        else:
            ultimoemail = buscaruseremails()
            verify2 = ultimoemail[numerousers - 1]
            print(verify2)
            if (verify1 != []) and (verify2!="NA"):
                nuevouser = 1
            else:
                airtable1.delete_by_field('User ID',chat_id)
                nuevouser = 0
        numero =buscarcode()
        code = numero + 1
        code = str(code)
        print(code)
        verify = airtable.search('Code', code)
        print(verify)
        while (verify != []):
            print("incorrecto")
            code = buscarcode()
            code = code + numero
            code = str(code)
            verify = airtable.search('Code', code)

        print("correcto")
        name = update.effective_chat.first_name
        chat_id = str(update.effective_chat.id)
        record = {'Code': code}
        record1= {'User ID': chat_id}
        record2 = {'User name': name}
        airtable.insert(record)
        rellenarairtable()

        print (code)

        airtable.update_by_field('Code', code, record1)
        airtable.update_by_field('Code', code, record2)
        query = update.callback_query.data
        print(query)
        chat_id = update.effective_chat.id
        if query == "Create":
            chat_id = str(chat_id)
            name = update.effective_chat.first_name
            record = {'Challenger or not': 'Yes'}
            record2 = {'Code': code}
            record3 = {'User ID': chat_id}
            record4 = {'User name': name}
            if nuevouser!=0:
                ultimo=buscarduedates()
                verify=ultimo[numerochallenges-1]
                codes=buscarcode2()
                ultimocode=codes[numerochallenges-1]
                print(verify)
                while verify=="NA":
                    print("hola")
                    airtable2.delete_by_field('Code',ultimocode)
                    verify3 = airtable3.search("Code", ultimocode)
                    print(verify3)
                    print(ultimocode)
                    if verify3!=[]:
                         airtable3.delete_by_field("Code",ultimocode)
                    ultimo = buscarduedates()
                    verify = ultimo[len(ultimo) - 1]
                    codes = buscarcode2()
                    ultimocode = codes[len(codes) - 1]
            airtable2.insert(record2)
            rellenarairtable2()
            airtable2.update_by_field('Code',code,record1)
            verify1 = airtable1.search('User ID', chat_id)
            if verify1 == []:
                nuevouser == 0
            else:
                ultimoemail = buscaruseremails()
                verify2 = ultimoemail[numerousers - 1]
                print(verify2)
                if (verify1 != []) and (verify2 != "NA"):
                    nuevouser = 1
                else:
                    airtable1.delete_by_field('User ID', chat_id)
                    nuevouser = 0

            print(nuevouser)
            if nuevouser == 0:
                print("SIGOAQUI0")
                airtable1.insert(record3)
                rellenarairtable1()
                airtable1.update_by_field('User ID', chat_id, record4)
                airtable.update_by_field('Code', code, record)

                if idioma=="English":
                    context.bot.send_message(chat_id, text='Hello {}. Nice to see you again. Let do it'.format(name),
                                             reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
                    context.bot.send_message(chat_id,
                                             text='How do you want to name the challenge?. Use the Menu above if you wanna change what to do.',
                                             reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
                elif idioma=="Español":
                    context.bot.send_message(chat_id, text='Hola {}. Nice to see you again. Let do it'.format(name),
                                             reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
                    context.bot.send_message(chat_id,
                                             text='¿Cómo quieres llamar al reto?. Use the Menu above if you wanna change what to do.',
                                             reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
                return CHALLENGENAME
            else:
                print("SIGOAQUI")
                if idioma=="English":
                    context.bot.send_message(chat_id, text='Hello {}. Nice to see you again. Let do it'.format(name),
                                             reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
                    context.bot.send_message(chat_id,
                                             text='How do you want to name the challenge?. Use the Menu above if you wanna change what to do.',
                                             reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
                elif idioma=="Español":
                    context.bot.send_message(chat_id, text='Hola {}. Nice to see you again. Let do it'.format(name),
                                             reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
                    context.bot.send_message(chat_id,
                                             text='¿Cómo quieres llamar al reto?. Use the Menu above if you wanna change what to do.',
                                             reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
                return CHALLENGENAME
        elif query == "Judge":
            record = {'Challenger or not': 'No'}
            airtable.update_by_field('Code', code, record)
            if idioma=="English":
                context.bot.send_message(chat_id,
                                     text='Hello {}. Nice to see you again. Please send me the code of the challenge to be judge, '
                                          'please.'.format(name),reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            elif idioma=="Español":
                context.bot.send_message(chat_id,
                                     text='Hola {}. Nice to see you again. Please send me the code of the challenge to be judge, '
                                          'please.'.format(name),reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            return JUDGE
        elif query == "Review":
            print("vale")
            ultimo=buscarduedates()
            print("vale")
            verify=ultimo[numerochallenges-1]
            codes=buscarcode2()
            print("vale")
            ultimocode=codes[numerochallenges-1]
            print(verify)
            while verify=="NA":
                print("hola")
                airtable2.delete_by_field('Code',ultimocode)
                verify3 = airtable3.search("Code", ultimocode)
                print(verify3)
                print(ultimocode)
                if verify3!=[]:
                     airtable3.delete_by_field("Code",ultimocode)
                ultimo = buscarduedates()
                verify = ultimo[len(ultimo) - 1]
                codes = buscarcode2()
                ultimocode = codes[len(codes) - 1]
            challenge= buscarchallenges()
            numchallenge= len(challenge)
            print(numchallenge)
            record = {'Challenger or not': 'No'}
            airtable.update_by_field('Code', code, record)
            if numchallenge==1:
                challengename1=challenge[numchallenge-1]
                keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if idioma == "English":
                    context.bot.send_message(chat_id, text=
                    'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                             reply_markup=reply_markup)
                elif idioma == "Español":
                    context.bot.send_message(chat_id, text=
                    'Tienes los siguientes retos. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                             reply_markup=reply_markup)
                return REVIEW
            elif numchallenge==2:
                challengename1 = challenge[numchallenge - 1]
                challengename2 = challenge[numchallenge - 2]
                keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                            InlineKeyboardButton(challengename2, callback_data='Challenge2')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if idioma == "English":
                    context.bot.send_message(chat_id, text=
                    'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                             reply_markup=reply_markup)
                elif idioma == "Español":
                    context.bot.send_message(chat_id, text=
                    'Tienes los siguientes retos. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                             reply_markup=reply_markup)
                return REVIEW
            elif numchallenge==3:
                challengename1 = challenge[numchallenge - 1]
                challengename2 = challenge[numchallenge - 2]
                challengename3 = challenge[numchallenge - 3]
                keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                            InlineKeyboardButton(challengename2, callback_data='Challenge2'),
                            InlineKeyboardButton(challengename3, callback_data='Challenge3')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if idioma == "English":
                    context.bot.send_message(chat_id, text=
                    'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                             reply_markup=reply_markup)
                elif idioma == "Español":
                    context.bot.send_message(chat_id, text=
                    'Tienes los siguientes retos. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                             reply_markup=reply_markup)
                return REVIEW
            elif numchallenge==4:
                challengename1 = challenge[numchallenge - 1]
                challengename2 = challenge[numchallenge - 2]
                challengename3 = challenge[numchallenge - 3]
                challengename4 = challenge[numchallenge - 4]
                keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                            InlineKeyboardButton(challengename2, callback_data='Challenge2')],
                            [InlineKeyboardButton(challengename3, callback_data='Challenge3'),
                            InlineKeyboardButton(challengename4, callback_data='Challenge4')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if idioma == "English":
                    context.bot.send_message(chat_id, text=
                    'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                             reply_markup=reply_markup)
                elif idioma == "Español":
                    context.bot.send_message(chat_id, text=
                    'Tienes los siguientes retos. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                             reply_markup=reply_markup)
                return REVIEW
            elif numchallenge==5:
                challengename1 = challenge[numchallenge - 1]
                challengename2 = challenge[numchallenge - 2]
                challengename3 = challenge[numchallenge - 3]
                challengename4 = challenge[numchallenge - 4]
                challengename5 = challenge[numchallenge - 5]
                keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                            InlineKeyboardButton(challengename2, callback_data='Challenge2'),
                             InlineKeyboardButton(challengename3, callback_data='Challenge3')],
                            [InlineKeyboardButton(challengename4, callback_data='Challenge4'),
                            InlineKeyboardButton(challengename5, callback_data='Challenge5')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if idioma == "English":
                    context.bot.send_message(chat_id, text=
                    'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                             reply_markup=reply_markup)
                elif idioma == "Español":
                    context.bot.send_message(chat_id, text=
                    'Tienes los siguientes retos. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                             reply_markup=reply_markup)
                return REVIEW
            elif numchallenge>=6:
                challengename1 = challenge[numchallenge - 1]
                challengename2 = challenge[numchallenge - 2]
                challengename3 = challenge[numchallenge - 3]
                challengename4 = challenge[numchallenge - 4]
                challengename5 = challenge[numchallenge - 5]
                challengename6 = challenge[numchallenge - 6]
                keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                            InlineKeyboardButton(challengename2, callback_data='Challenge2')],
                            [InlineKeyboardButton(challengename3, callback_data='Challenge3'),
                            InlineKeyboardButton(challengename4, callback_data='Challenge4')],
                            [InlineKeyboardButton(challengename5, callback_data='Challenge5'),
                             InlineKeyboardButton(challengename6, callback_data='Challenge6')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if idioma == "English":
                    context.bot.send_message(chat_id, text=
                    'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                             reply_markup=reply_markup)
                elif idioma == "Español":
                    context.bot.send_message(chat_id, text=
                    'Tienes los siguientes retos. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                             reply_markup=reply_markup)
                return REVIEW
    elif change==1:
        if query=="Name":
            if idioma=="English":
                context.bot.send_message(chat_id, text='How do you wanna name the challenge?', reply_markup=ReplyKeyboardRemove(
                remove_keyboard=True))
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='¿Cómo quieres llamar al reto?', reply_markup=ReplyKeyboardRemove(
                remove_keyboard=True))
            return CHALLENGENAME
        elif query=="Amount":
                keyboard = [['5€', '10€', '15€', ], ['20€', '25€', 'Other']]
                if idioma=="English":
                    context.bot.send_message(chat_id, text=
                    '\n\n'
                    'Select the quantity from the options below',
                                             reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
                elif idioma=="Español":
                    context.bot.send_message(chat_id, text=
                    '\n\n'
                    'Selecciona la cantidad de las opciones de debajo',
                                             reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
                return AMOUNT
        elif query=="Duedate":
            if idioma=="English":
                keyboard = [['January', 'February', 'March', 'April'], ['May', 'June', 'July', 'August'],
                            ['September', 'October', 'November', 'December']]
                context.bot.send_message(chat_id, text=
                '\n\n'
                'Select the month',
                                         reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
            elif idioma=="Español":
                keyboard = [['Enero', 'Febrero', 'Marzo', 'Abril'], ['Mayo', 'Junio', 'Julio', 'Agosto'],
                            ['Septiembre', 'Octubre', 'Noviembre', 'Diciembre']]
                context.bot.send_message(chat_id, text=
                '\n\n'
                'Selecciona el mes',
                                         reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
            return DATE
        elif query=="Judgename":
            print("AQIIIII")
            if nuevouser == 1:
                prueba = buscarjueces()
                jueces = buscarjuecesmail()
                longitud = len(prueba)
                print(longitud)
                if longitud == 1:
                    judgenameJ = prueba[longitud - 1]
                    judgeemailJ = jueces[longitud - 1]
                    if idioma=="English":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1')],
                                    [InlineKeyboardButton("New", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id, text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                            reply_markup=reply_markup)
                    elif idioma=="Español":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1')],
                                    [InlineKeyboardButton("Nuevo", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    return EXISTING
                elif longitud == 2:
                    judgenameJ = prueba[longitud - 1]
                    judgenameJ1 = prueba[longitud - 2]
                    judgeemailJ = jueces[longitud - 1]
                    judgeemailJ1 = jueces[longitud - 2]
                    if idioma=="English":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                                    [InlineKeyboardButton("New", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id, text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                            reply_markup=reply_markup)
                    elif idioma=="Español":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                                    [InlineKeyboardButton("Nuevo", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    return EXISTING
                elif longitud == 3:
                    judgenameJ = prueba[longitud - 1]
                    judgenameJ1 = prueba[longitud - 2]
                    judgenameJ2 = prueba[longitud - 3]
                    judgeemailJ = jueces[longitud - 1]
                    judgeemailJ1 = jueces[longitud - 2]
                    judgeemailJ2 = jueces[longitud - 3]
                    if idioma=="English":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2'),
                                     InlineKeyboardButton(judgenameJ2, callback_data='Judge3')],
                                    [InlineKeyboardButton("New", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id, text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                            reply_markup=reply_markup)
                    elif idioma=="Español":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2'),
                                     InlineKeyboardButton(judgenameJ2, callback_data='Judge3')],
                                    [InlineKeyboardButton("Nuevo", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    return EXISTING
                elif longitud == 4:
                    judgenameJ = prueba[longitud - 1]
                    judgenameJ1 = prueba[longitud - 2]
                    judgenameJ2 = prueba[longitud - 3]
                    judgenameJ3 = prueba[longitud - 4]
                    judgeemailJ = jueces[longitud - 1]
                    judgeemailJ1 = jueces[longitud - 2]
                    judgeemailJ2 = jueces[longitud - 3]
                    judgeemailJ3 = jueces[longitud - 4]
                    if idioma=="English":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                                    [InlineKeyboardButton(judgenameJ2, callback_data='Judge3'),
                                     InlineKeyboardButton(judgenameJ3, callback_data='Judge4')],
                                    [InlineKeyboardButton("New", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id, text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                            reply_markup=reply_markup)
                    elif idioma=="Español":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                                    [InlineKeyboardButton(judgenameJ2, callback_data='Judge3'),
                                     InlineKeyboardButton(judgenameJ3, callback_data='Judge4')],
                                    [InlineKeyboardButton("Nuevo", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    return EXISTING
                elif longitud == 5:
                    judgenameJ = prueba[longitud - 1]
                    judgenameJ1 = prueba[longitud - 2]
                    judgenameJ2 = prueba[longitud - 3]
                    judgenameJ3 = prueba[longitud - 4]
                    judgenameJ4 = prueba[longitud - 5]
                    judgeemailJ = jueces[longitud - 1]
                    judgeemailJ1 = jueces[longitud - 2]
                    judgeemailJ2 = jueces[longitud - 3]
                    judgeemailJ3 = jueces[longitud - 4]
                    judgeemailJ4 = jueces[longitud - 5]
                    if idioma=="English":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2'),
                                     InlineKeyboardButton(judgenameJ2, callback_data='Judge3')],
                                    [InlineKeyboardButton(judgenameJ3, callback_data='Judge4'),
                                     InlineKeyboardButton(judgenameJ4, callback_data='Judge5')],
                                    [InlineKeyboardButton("New", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id, text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                            reply_markup=reply_markup)
                    elif idioma=="Español":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2'),
                                     InlineKeyboardButton(judgenameJ2, callback_data='Judge3')],
                                    [InlineKeyboardButton(judgenameJ3, callback_data='Judge4'),
                                     InlineKeyboardButton(judgenameJ4, callback_data='Judge5')],
                                    [InlineKeyboardButton("Nuevo", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    return EXISTING
                elif longitud >= 6:
                    judgenameJ = prueba[longitud - 1]
                    judgenameJ1 = prueba[longitud - 2]
                    judgenameJ2 = prueba[longitud - 3]
                    judgenameJ3 = prueba[longitud - 4]
                    judgenameJ4 = prueba[longitud - 5]
                    judgenameJ5 = prueba[longitud - 6]
                    judgeemailJ = jueces[longitud - 1]
                    judgeemailJ1 = jueces[longitud - 2]
                    judgeemailJ2 = jueces[longitud - 3]
                    judgeemailJ3 = jueces[longitud - 4]
                    judgeemailJ4 = jueces[longitud - 5]
                    judgeemailJ5 = jueces[longitud - 6]
                    if idioma=="English":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                                    [InlineKeyboardButton(judgenameJ2, callback_data='Judge3'),
                                     InlineKeyboardButton(judgenameJ3, callback_data='Judge4')],
                                    [InlineKeyboardButton(judgenameJ4, callback_data='Judge5'),
                                     InlineKeyboardButton(judgenameJ5, callback_data='Judge6')],
                                    [InlineKeyboardButton("New", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id, text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                            reply_markup=reply_markup)
                    elif idioma=="Español":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                                    [InlineKeyboardButton(judgenameJ2, callback_data='Judge3'),
                                     InlineKeyboardButton(judgenameJ3, callback_data='Judge4')],
                                    [InlineKeyboardButton(judgenameJ4, callback_data='Judge5'),
                                     InlineKeyboardButton(judgenameJ5, callback_data='Judge6')],
                                    [InlineKeyboardButton("New", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    return EXISTING

            elif nuevouser == 0:
                record = {'Code': code}
                airtable3.delete_by_field('Code',code)
                airtable3.insert(record)
                rellenarairtable3()
                if idioma=="English":
                    context.bot.send_message(chat_id, text='Who is going to be the judge?, send me his/her name please ',
                                              reply_markup=ReplyKeyboardRemove(
                                                  remove_keyboard=True))
                elif idioma=="Español":
                    context.bot.send_message(chat_id, text='¿Quién va a ser el juez?, send me his/her name please ',
                                              reply_markup=ReplyKeyboardRemove(
                                                  remove_keyboard=True))
                return JUDGENAME
        elif query=="JudgeEmail":
            if idioma=="English":
                context.bot.send_message(chat_id, text='Provide me the judge email, please', reply_markup=ReplyKeyboardRemove(
                remove_keyboard=True))
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='Enviame el correo del juez por favor', reply_markup=ReplyKeyboardRemove(
                remove_keyboard=True))
            return JUDGEMAIL
        elif query=="UserEmail":
            if idioma=="English":
                context.bot.send_message(chat_id, text=
                'Could you provide me your email? You will receive an email confirming the challenge and future updates.',
                reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif idioma=="Español":
                context.bot.send_message(chat_id, text=
                '¿Puedes darme tu email? You will receive an email confirming the challenge and future updates.',
                reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            return USERMAIL

##FIN PARTE 1


## ITINERARIO CREAR RETO
def challengename(update, context):
    global challengename,change, chat_id,user,vfinal ,nuevouser, judgenameJ, judgenameJ1, judgenameJ2, judgeemailJ2, judgeemailJ1, judgeemailJ, judgenameJ3, judgenameJ4, judgenameJ5, judgeemailJ3, judgeemailJ4, judgeemailJ5
    print ("He llegado")
    text= update.message.text
    challengename=text
    record= {'Name': text}
    airtable2.update_by_field('Code',code,record)
    print(change)
    if change==1:
        challengename=text

        if idioma=="English":
            reply_keyboard = [['Change'], ['OK']]
            context.bot.send_message(chat_id, text='Thank you!')
            context.bot.send_message(chat_id,
                                     text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                         challengename, amount, duedate, judge, judgeemail, useremail),
                                     parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            update.message.reply_text(
                '\n\n'
                ' If there is any mistake, press the change button. Otherwise press Ok button.',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            reply_keyboard = [['Cambiar'], ['OK']]
            context.bot.send_message(chat_id, text='Gracias!!')
            context.bot.send_message(chat_id,
                                     text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                         challengename, amount, duedate, judge, judgeemail, useremail),
                                     parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            update.message.reply_text(
                '\n\n'
                ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return FINAL
    else:
        if nuevouser == 0:
            record = {'Code': code}
            airtable3.insert(record)
            rellenarairtable3()
            if idioma=="English":
                update.message.reply_text('Who is going to be the judge?, send me his/her name please ',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            elif idioma=="Español":
                update.message.reply_text('¿Quién va a ser el juez?, send me his/her name please ',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))

            return JUDGENAME

        else:
            challengename = text
            record = {'Challenge name': text}
            airtable.update_by_field('Code', code, record)
            if nuevouser==1:
                prueba = buscarjueces()
                jueces = buscarjuecesmail()
                longitud = len(prueba)
                print(longitud)
                if longitud == 1:
                    judgenameJ = prueba[longitud - 1]
                    judgeemailJ = jueces[longitud - 1]
                    if idioma == "English":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1')],
                                    [InlineKeyboardButton("New", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    elif idioma == "Español":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1')],
                                    [InlineKeyboardButton("Nuevo", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    return EXISTING
                elif longitud == 2:
                    judgenameJ = prueba[longitud - 1]
                    judgenameJ1 = prueba[longitud - 2]
                    judgeemailJ = jueces[longitud - 1]
                    judgeemailJ1 = jueces[longitud - 2]
                    if idioma == "English":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                                    [InlineKeyboardButton("New", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    elif idioma == "Español":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                                    [InlineKeyboardButton("Nuevo", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    return EXISTING
                elif longitud == 3:
                    judgenameJ = prueba[longitud - 1]
                    judgenameJ1 = prueba[longitud - 2]
                    judgenameJ2 = prueba[longitud - 3]
                    judgeemailJ = jueces[longitud - 1]
                    judgeemailJ1 = jueces[longitud - 2]
                    judgeemailJ2 = jueces[longitud - 3]
                    if idioma == "English":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2'),
                                     InlineKeyboardButton(judgenameJ2, callback_data='Judge3')],
                                    [InlineKeyboardButton("New", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    elif idioma == "Español":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2'),
                                     InlineKeyboardButton(judgenameJ2, callback_data='Judge3')],
                                    [InlineKeyboardButton("Nuevo", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    return EXISTING
                elif longitud == 4:
                    judgenameJ = prueba[longitud - 1]
                    judgenameJ1 = prueba[longitud - 2]
                    judgenameJ2 = prueba[longitud - 3]
                    judgenameJ3 = prueba[longitud - 4]
                    judgeemailJ = jueces[longitud - 1]
                    judgeemailJ1 = jueces[longitud - 2]
                    judgeemailJ2 = jueces[longitud - 3]
                    judgeemailJ3 = jueces[longitud - 4]
                    if idioma == "English":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                                    [InlineKeyboardButton(judgenameJ2, callback_data='Judge3'),
                                     InlineKeyboardButton(judgenameJ3, callback_data='Judge4')],
                                    [InlineKeyboardButton("New", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    elif idioma == "Español":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                                    [InlineKeyboardButton(judgenameJ2, callback_data='Judge3'),
                                     InlineKeyboardButton(judgenameJ3, callback_data='Judge4')],
                                    [InlineKeyboardButton("Nuevo", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    return EXISTING
                elif longitud == 5:
                    judgenameJ = prueba[longitud - 1]
                    judgenameJ1 = prueba[longitud - 2]
                    judgenameJ2 = prueba[longitud - 3]
                    judgenameJ3 = prueba[longitud - 4]
                    judgenameJ4 = prueba[longitud - 5]
                    judgeemailJ = jueces[longitud - 1]
                    judgeemailJ1 = jueces[longitud - 2]
                    judgeemailJ2 = jueces[longitud - 3]
                    judgeemailJ3 = jueces[longitud - 4]
                    judgeemailJ4 = jueces[longitud - 5]
                    if idioma == "English":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2'),
                                     InlineKeyboardButton(judgenameJ2, callback_data='Judge3')],
                                    [InlineKeyboardButton(judgenameJ3, callback_data='Judge4'),
                                     InlineKeyboardButton(judgenameJ4, callback_data='Judge5')],
                                    [InlineKeyboardButton("New", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    elif idioma == "Español":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2'),
                                     InlineKeyboardButton(judgenameJ2, callback_data='Judge3')],
                                    [InlineKeyboardButton(judgenameJ3, callback_data='Judge4'),
                                     InlineKeyboardButton(judgenameJ4, callback_data='Judge5')],
                                    [InlineKeyboardButton("Nuevo", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    return EXISTING
                elif longitud >= 6:
                    print("LLEGE!!!")
                    judgenameJ = prueba[longitud - 1]
                    judgenameJ1 = prueba[longitud - 2]
                    judgenameJ2 = prueba[longitud - 3]
                    judgenameJ3 = prueba[longitud - 4]
                    judgenameJ4 = prueba[longitud - 5]
                    judgenameJ5 = prueba[longitud - 6]
                    judgeemailJ = jueces[longitud - 1]
                    judgeemailJ1 = jueces[longitud - 2]
                    judgeemailJ2 = jueces[longitud - 3]
                    judgeemailJ3 = jueces[longitud - 4]
                    judgeemailJ4 = jueces[longitud - 5]
                    judgeemailJ5 = jueces[longitud - 6]
                    if idioma=="English":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                                    [InlineKeyboardButton(judgenameJ2, callback_data='Judge3'),
                                     InlineKeyboardButton(judgenameJ3, callback_data='Judge4')],
                                    [InlineKeyboardButton(judgenameJ4, callback_data='Judge5'),
                                     InlineKeyboardButton(judgenameJ5, callback_data='Judge6')],
                                    [InlineKeyboardButton("New", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id, text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                            reply_markup=reply_markup)
                    elif idioma=="Español":
                        keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                                     InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                                    [InlineKeyboardButton(judgenameJ2, callback_data='Judge3'),
                                     InlineKeyboardButton(judgenameJ3, callback_data='Judge4')],
                                    [InlineKeyboardButton(judgenameJ4, callback_data='Judge5'),
                                     InlineKeyboardButton(judgenameJ5, callback_data='Judge6')],
                                    [InlineKeyboardButton("New", callback_data='New')]]

                        reply_markup = InlineKeyboardMarkup(keyboard)
                        context.bot.send_message(chat_id,
                                                 text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                                 reply_markup=reply_markup)
                    return EXISTING
            elif nuevouser==0:
                record={'Code': code}
                airtable3.insert(record)
                rellenarairtable3()
                if idioma=="English":
                    update.message.reply_text('Who is going to be the judge?, send me his/her name please ',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
                elif idioma=="Español":
                    update.message.reply_text('¿Quién va a ser el juez?, send me his/her name please ',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))

                return JUDGENAME

def existingjudge(update, context):
    global judge, judgeemail, final1, existing
    existing=1
    query = update.callback_query.data
    print(query)
    if change==0:
        if query=="Judge1":
            #actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
            ###aquí codigo para hacer lo de arriba
            #actualizo airtable de Challenges y All con nombre y email del judge elegido
            record = {'Judge name': judgenameJ}
            record1 = {'Email judge': judgeemailJ}
            judge= judgenameJ
            judgeemail= judgeemailJ
            airtable.update_by_field('Code', code, record)
            airtable.update_by_field('Code', code, record1)
            airtable2.update_by_field('Code',code, record)
            airtable2.update_by_field('Code', code, record1)
            if idioma=="English":
                reply_keyboard = [['Insert Quantity']]

                context.bot.send_message(chat_id,text=
                    'How many money do you want to bet?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma=="Español":
                reply_keyboard = [['Insertar Cantidad']]

                context.bot.send_message(chat_id, text=
                '¿Cuánto dinero quieres apostar?',
                                         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return ADDITIONAL
        elif query=="Judge2":
            #actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
            ###aquí codigo para hacer lo de arriba
            #actualizo airtable de Challenges y All con nombre y email del judge elegido
            record = {'Judge name': judgenameJ1 }
            record1 = {'Email judge': judgeemailJ1}
            judge= judgenameJ1
            judgeemail= judgeemailJ1
            airtable.update_by_field('Code', code, record)
            airtable.update_by_field('Code', code, record1)
            airtable2.update_by_field('Code',code, record)
            airtable2.update_by_field('Code', code, record1)

            if idioma=="English":
                reply_keyboard = [['Insert Quantity']]

                context.bot.send_message(chat_id,text=
                    'How many money do you want to bet?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma=="Español":
                reply_keyboard = [['Insertar Cantidad']]

                context.bot.send_message(chat_id, text=
                '¿Cuánto dinero quieres apostar?',
                                         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return ADDITIONAL
        elif query=="Judge3":
            # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
            ###aquí codigo para hacer lo de arriba
            # actualizo airtable de Challenges y All con nombre y email del judge elegido
            record = {'Judge name': judgenameJ2}
            record1 = {'Email judge': judgeemailJ2}
            judge = judgenameJ2
            judgeemail = judgeemailJ2
            airtable.update_by_field('Code', code, record)
            airtable.update_by_field('Code', code, record1)
            airtable2.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record1)
            if idioma=="English":
                reply_keyboard = [['Insert Quantity']]

                context.bot.send_message(chat_id,text=
                    'How many money do you want to bet?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma=="Español":
                reply_keyboard = [['Insertar Cantidad']]

                context.bot.send_message(chat_id, text=
                '¿Cuánto dinero quieres apostar?',
                                         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return ADDITIONAL
        elif query=="Judge4":
            # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
            ###aquí codigo para hacer lo de arriba
            # actualizo airtable de Challenges y All con nombre y email del judge elegido
            record = {'Judge name': judgenameJ3}
            record1 = {'Email judge': judgeemailJ3}
            judge = judgenameJ3
            judgeemail = judgeemailJ3
            airtable.update_by_field('Code', code, record)
            airtable.update_by_field('Code', code, record1)
            airtable2.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record1)
            if idioma=="English":
                reply_keyboard = [['Insert Quantity']]

                context.bot.send_message(chat_id,text=
                    'How many money do you want to bet?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma=="Español":
                reply_keyboard = [['Insertar Cantidad']]

                context.bot.send_message(chat_id, text=
                '¿Cuánto dinero quieres apostar?',
                                         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return ADDITIONAL
        elif query=="Judge5":
            # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
            ###aquí codigo para hacer lo de arriba
            # actualizo airtable de Challenges y All con nombre y email del judge elegido
            record = {'Judge name': judgenameJ4}
            record1 = {'Email judge': judgeemailJ4}
            judge = judgenameJ4
            judgeemail = judgeemailJ4
            airtable.update_by_field('Code', code, record)
            airtable.update_by_field('Code', code, record1)
            airtable2.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record1)
            if idioma=="English":
                reply_keyboard = [['Insert Quantity']]

                context.bot.send_message(chat_id,text=
                    'How many money do you want to bet?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma=="Español":
                reply_keyboard = [['Insertar Cantidad']]

                context.bot.send_message(chat_id, text=
                '¿Cuánto dinero quieres apostar?',
                                         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return ADDITIONAL
        elif query=="Judge6":
            # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
            ###aquí codigo para hacer lo de arriba
            # actualizo airtable de Challenges y All con nombre y email del judge elegido
            record = {'Judge name': judgenameJ5}
            record1 = {'Email judge': judgeemailJ5}
            judge = judgenameJ5
            judgeemail = judgeemailJ5
            airtable.update_by_field('Code', code, record)
            airtable.update_by_field('Code', code, record1)
            airtable2.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record1)
            if idioma=="English":
                reply_keyboard = [['Insert Quantity']]

                context.bot.send_message(chat_id,text=
                    'How many money do you want to bet?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma=="Español":
                reply_keyboard = [['Insertar Cantidad']]

                context.bot.send_message(chat_id, text=
                '¿Cuánto dinero quieres apostar?',
                                         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return ADDITIONAL
        elif query=="New":
            existing=0
            record = {'Code': code}
            airtable3.insert(record)
            rellenarairtable3()
            if idioma=="English":
                context.bot.send_message(chat_id, text='Who is going to be the judge?, send me his/her name please ',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='¿Quién va a ser el juez?, send me his/her name please ',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))

            return JUDGENAME
    elif change==1:
        final1=0
        if query == "Judge1":
            record = {'Judge name': judgenameJ}
            record1 = {'Email judge': judgeemailJ}
            judge = judgenameJ
            judgeemail = judgeemailJ
            airtable.update_by_field('Code', code, record)
            airtable.update_by_field('Code', code, record1)
            airtable2.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record1)

            if idioma == "English":
                reply_keyboard = [['Change'], ['OK']]
                context.bot.send_message(chat_id, text='Thank you!')
                context.bot.send_message(chat_id,
                                         text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' If there is any mistake, press the change button. Otherwise press Ok button.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                reply_keyboard = [['Cambiar'], ['OK']]
                context.bot.send_message(chat_id, text='Gracias!!')
                context.bot.send_message(chat_id,
                                         text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return FINAL
        elif query == "Judge2":
            # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
            ###aquí codigo para hacer lo de arriba
            # actualizo airtable de Challenges y All con nombre y email del judge elegido
            record = {'Judge name': judgenameJ1}
            record1 = {'Email judge': judgeemailJ1}
            judge = judgenameJ1
            judgeemail = judgeemailJ1
            airtable.update_by_field('Code', code, record)
            airtable.update_by_field('Code', code, record1)
            airtable2.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record1)

            if idioma == "English":
                reply_keyboard = [['Change'], ['OK']]
                context.bot.send_message(chat_id, text='Thank you!')
                context.bot.send_message(chat_id,
                                         text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' If there is any mistake, press the change button. Otherwise press Ok button.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                reply_keyboard = [['Cambiar'], ['OK']]
                context.bot.send_message(chat_id, text='Gracias!!')
                context.bot.send_message(chat_id,
                                         text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return FINAL
        elif query == "Judge3":
            # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
            ###aquí codigo para hacer lo de arriba
            # actualizo airtable de Challenges y All con nombre y email del judge elegido
            record = {'Judge name': judgenameJ2}
            record1 = {'Email judge': judgeemailJ2}
            judge = judgenameJ2
            judgeemail = judgeemailJ2
            airtable.update_by_field('Code', code, record)
            airtable.update_by_field('Code', code, record1)
            airtable2.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record1)

            if idioma == "English":
                reply_keyboard = [['Change'], ['OK']]
                context.bot.send_message(chat_id, text='Thank you!')
                context.bot.send_message(chat_id,
                                         text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' If there is any mistake, press the change button. Otherwise press Ok button.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                reply_keyboard = [['Cambiar'], ['OK']]
                context.bot.send_message(chat_id, text='Gracias!!')
                context.bot.send_message(chat_id,
                                         text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return FINAL
        elif query == "Judge4":
            # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
            ###aquí codigo para hacer lo de arriba
            # actualizo airtable de Challenges y All con nombre y email del judge elegido
            record = {'Judge name': judgenameJ3}
            record1 = {'Email judge': judgeemailJ3}
            judge = judgenameJ3
            judgeemail = judgeemailJ3
            airtable.update_by_field('Code', code, record)
            airtable.update_by_field('Code', code, record1)
            airtable2.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record1)

            if idioma == "English":
                reply_keyboard = [['Change'], ['OK']]
                context.bot.send_message(chat_id, text='Thank you!')
                context.bot.send_message(chat_id,
                                         text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' If there is any mistake, press the change button. Otherwise press Ok button.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                reply_keyboard = [['Cambiar'], ['OK']]
                context.bot.send_message(chat_id, text='Gracias!!')
                context.bot.send_message(chat_id,
                                         text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return FINAL
        elif query == "Judge5":
            # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
            ###aquí codigo para hacer lo de arriba
            # actualizo airtable de Challenges y All con nombre y email del judge elegido
            record = {'Judge name': judgenameJ4}
            record1 = {'Email judge': judgeemailJ4}
            judge = judgenameJ4
            judgeemail = judgeemailJ4
            airtable.update_by_field('Code', code, record)
            airtable.update_by_field('Code', code, record1)
            airtable2.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record1)
            if idioma == "English":
                reply_keyboard = [['Change'], ['OK']]
                context.bot.send_message(chat_id, text='Thank you!')
                context.bot.send_message(chat_id,
                                         text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' If there is any mistake, press the change button. Otherwise press Ok button.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                reply_keyboard = [['Cambiar'], ['OK']]
                context.bot.send_message(chat_id, text='Gracias!!')
                context.bot.send_message(chat_id,
                                         text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return FINAL
        elif query == "Judge6":
            # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
            ###aquí codigo para hacer lo de arriba
            # actualizo airtable de Challenges y All con nombre y email del judge elegido
            record = {'Judge name': judgenameJ5}
            record1 = {'Email judge': judgeemailJ5}
            judge = judgenameJ5
            judgeemail = judgeemailJ5
            airtable.update_by_field('Code', code, record)
            airtable.update_by_field('Code', code, record1)
            airtable2.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record1)

            if idioma == "English":
                reply_keyboard = [['Change'], ['OK']]
                context.bot.send_message(chat_id, text='Thank you!')
                context.bot.send_message(chat_id,
                                         text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' If there is any mistake, press the change button. Otherwise press Ok button.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                reply_keyboard = [['Cambiar'], ['OK']]
                context.bot.send_message(chat_id, text='Gracias!!')
                context.bot.send_message(chat_id,
                                         text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return FINAL
        elif query == "New":
            existing=0
            record = {'Code': code}
            airtable3.insert(record)
            rellenarairtable3()
            if idioma=="English":
                context.bot.send_message(chat_id, text='Who is going to be the judge?, send me his/her name please ',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='¿Quién va a ser el juez?, enviame su nombre por favor ',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            return JUDGENAME

def existingjudge1(update, context):
    global judgeemail, judge, existing
    existing=1
    query=update.message.text
    if query == "Judge1":
        # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
        ###aquí codigo para hacer lo de arriba
        # actualizo airtable de Challenges y All con nombre y email del judge elegido
        record = {'Judge name': judgenameJ}
        record1 = {'Email judge': judgeemailJ}
        judge = judgenameJ
        judgeemail = judgeemailJ
        airtable.update_by_field('Code', code, record)
        airtable.update_by_field('Code', code, record1)
        airtable2.update_by_field('Code', code, record)
        airtable2.update_by_field('Code', code, record1)
        if idioma=="English":
            reply_keyboard = [['Insert Quantity']]

            context.bot.send_message(chat_id, text=
            'How many money do you want to bet?',
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            reply_keyboard = [['Insertar Cantidad']]

            context.bot.send_message(chat_id, text=
            '¿Cuánto dinero quieres apostar?',
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return ADDITIONAL
    elif query == "Judge2":
        # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
        ###aquí codigo para hacer lo de arriba
        # actualizo airtable de Challenges y All con nombre y email del judge elegido
        record = {'Judge name': judgenameJ1}
        record1 = {'Email judge': judgeemailJ1}
        judge = judgenameJ1
        judgeemail = judgeemailJ1
        airtable.update_by_field('Code', code, record)
        airtable.update_by_field('Code', code, record1)
        airtable2.update_by_field('Code', code, record)
        airtable2.update_by_field('Code', code, record1)

        if idioma=="English":
            reply_keyboard = [['Insert Quantity']]

            context.bot.send_message(chat_id, text=
            'How many money do you want to bet?',
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            reply_keyboard = [['Insertar Cantidad']]

            context.bot.send_message(chat_id, text=
            '¿Cuánto dinero quieres apostar?',
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return ADDITIONAL
    elif query == "Judge3":
        # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
        ###aquí codigo para hacer lo de arriba
        # actualizo airtable de Challenges y All con nombre y email del judge elegido
        record = {'Judge name': judgenameJ2}
        record1 = {'Email judge': judgeemailJ2}
        judge = judgenameJ2
        judgeemail = judgeemailJ2
        airtable.update_by_field('Code', code, record)
        airtable.update_by_field('Code', code, record1)
        airtable2.update_by_field('Code', code, record)
        airtable2.update_by_field('Code', code, record1)

        if idioma=="English":
            reply_keyboard = [['Insert Quantity']]

            context.bot.send_message(chat_id, text=
            'How many money do you want to bet?',
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            reply_keyboard = [['Insertar Cantidad']]

            context.bot.send_message(chat_id, text=
            '¿Cuánto dinero quieres apostar?',
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return ADDITIONAL
    elif query == "Judge4":
        # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
        ###aquí codigo para hacer lo de arriba
        # actualizo airtable de Challenges y All con nombre y email del judge elegido
        record = {'Judge name': judgenameJ3}
        record1 = {'Email judge': judgeemailJ3}
        judge = judgenameJ3
        judgeemail = judgeemailJ3
        airtable.update_by_field('Code', code, record)
        airtable.update_by_field('Code', code, record1)
        airtable2.update_by_field('Code', code, record)
        airtable2.update_by_field('Code', code, record1)
        if idioma=="English":
            reply_keyboard = [['Insert Quantity']]

            context.bot.send_message(chat_id, text=
            'How many money do you want to bet?',
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            reply_keyboard = [['Insertar Cantidad']]

            context.bot.send_message(chat_id, text=
            '¿Cuánto dinero quieres apostar?',
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return ADDITIONAL
    elif query == "Judge5":
        # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
        ###aquí codigo para hacer lo de arriba
        # actualizo airtable de Challenges y All con nombre y email del judge elegido
        record = {'Judge name': judgenameJ4}
        record1 = {'Email judge': judgeemailJ4}
        judge = judgenameJ4
        judgeemail = judgeemailJ4
        airtable.update_by_field('Code', code, record)
        airtable.update_by_field('Code', code, record1)
        airtable2.update_by_field('Code', code, record)
        airtable2.update_by_field('Code', code, record1)
        if idioma=="English":
            reply_keyboard = [['Insert Quantity']]

            context.bot.send_message(chat_id, text=
            'How many money do you want to bet?',
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            reply_keyboard = [['Insertar Cantidad']]

            context.bot.send_message(chat_id, text=
            '¿Cuánto dinero quieres apostar?',
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return ADDITIONAL
    elif query == "Judge6":
        # actualizo judgenameJ pidiendoselo a la función buscar (hay que crearla): le pido el 1 del vector que reciba
        ###aquí codigo para hacer lo de arriba
        # actualizo airtable de Challenges y All con nombre y email del judge elegido
        record = {'Judge name': judgenameJ5}
        record1 = {'Email judge': judgeemailJ5}
        judge = judgenameJ5
        judgeemail = judgeemailJ5
        airtable.update_by_field('Code', code, record)
        airtable.update_by_field('Code', code, record1)
        airtable2.update_by_field('Code', code, record)
        airtable2.update_by_field('Code', code, record1)
        if idioma=="English":
            reply_keyboard = [['Insert Quantity']]

            context.bot.send_message(chat_id, text=
            'How many money do you want to bet?',
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            reply_keyboard = [['Insertar Cantidad']]

            context.bot.send_message(chat_id, text=
            '¿Cuánto dinero quieres apostar?',
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return ADDITIONAL
    elif query == "New":
        existing=0
        record = {'Code': code}
        airtable3.insert(record)
        rellenarairtable3()
        if idioma == "English":
            context.bot.send_message(chat_id, text='Who is going to be the judge?, send me his/her name please ',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        elif idioma == "Español":
            context.bot.send_message(chat_id, text='¿Quién va a ser el juez?, enviame su nombre por favor ',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        return JUDGENAME
    else:
        prueba = buscarjueces()
        jueces = buscarjuecesmail()
        longitud = len(prueba)
        if longitud == 1:
            judgenameJ = prueba[longitud - 1]
            judgeemailJ = jueces[longitud - 1]
            if idioma == "English":
                keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1')],
                            [InlineKeyboardButton("New", callback_data='New')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id,
                                         text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                                         reply_markup=reply_markup)
            elif idioma == "Español":
                keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1')],
                            [InlineKeyboardButton("Nuevo", callback_data='New')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id,
                                         text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                         reply_markup=reply_markup)
            return EXISTING
        elif longitud == 2:
            judgenameJ = prueba[longitud - 1]
            judgenameJ1 = prueba[longitud - 2]
            judgeemailJ = jueces[longitud - 1]
            judgeemailJ1 = jueces[longitud - 2]
            if idioma == "English":
                keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                             InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                            [InlineKeyboardButton("New", callback_data='New')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id,
                                         text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                                         reply_markup=reply_markup)
            elif idioma == "Español":
                keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                             InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                            [InlineKeyboardButton("Nuevo", callback_data='New')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id,
                                         text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                         reply_markup=reply_markup)
            return EXISTING
        elif longitud == 3:
            judgenameJ = prueba[longitud - 1]
            judgenameJ1 = prueba[longitud - 2]
            judgenameJ2 = prueba[longitud - 3]
            judgeemailJ = jueces[longitud - 1]
            judgeemailJ1 = jueces[longitud - 2]
            judgeemailJ2 = jueces[longitud - 3]
            if idioma == "English":
                keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                             InlineKeyboardButton(judgenameJ1, callback_data='Judge2'),
                             InlineKeyboardButton(judgenameJ2, callback_data='Judge3')],
                            [InlineKeyboardButton("New", callback_data='New')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id,
                                         text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                                         reply_markup=reply_markup)
            elif idioma == "Español":
                keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                             InlineKeyboardButton(judgenameJ1, callback_data='Judge2'),
                             InlineKeyboardButton(judgenameJ2, callback_data='Judge3')],
                            [InlineKeyboardButton("Nuevo", callback_data='New')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id,
                                         text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                         reply_markup=reply_markup)
            return EXISTING
        elif longitud == 4:
            judgenameJ = prueba[longitud - 1]
            judgenameJ1 = prueba[longitud - 2]
            judgenameJ2 = prueba[longitud - 3]
            judgenameJ3 = prueba[longitud - 4]
            judgeemailJ = jueces[longitud - 1]
            judgeemailJ1 = jueces[longitud - 2]
            judgeemailJ2 = jueces[longitud - 3]
            judgeemailJ3 = jueces[longitud - 4]
            if idioma == "English":
                keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                             InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                            [InlineKeyboardButton(judgenameJ2, callback_data='Judge3'),
                             InlineKeyboardButton(judgenameJ3, callback_data='Judge4')],
                            [InlineKeyboardButton("New", callback_data='New')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id,
                                         text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                                         reply_markup=reply_markup)
            elif idioma == "Español":
                keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                             InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                            [InlineKeyboardButton(judgenameJ2, callback_data='Judge3'),
                             InlineKeyboardButton(judgenameJ3, callback_data='Judge4')],
                            [InlineKeyboardButton("Nuevo", callback_data='New')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id,
                                         text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                         reply_markup=reply_markup)
            return EXISTING
        elif longitud == 5:
            judgenameJ = prueba[longitud - 1]
            judgenameJ1 = prueba[longitud - 2]
            judgenameJ2 = prueba[longitud - 3]
            judgenameJ3 = prueba[longitud - 4]
            judgenameJ4 = prueba[longitud - 5]
            judgeemailJ = jueces[longitud - 1]
            judgeemailJ1 = jueces[longitud - 2]
            judgeemailJ2 = jueces[longitud - 3]
            judgeemailJ3 = jueces[longitud - 4]
            judgeemailJ4 = jueces[longitud - 5]
            if idioma == "English":
                keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                             InlineKeyboardButton(judgenameJ1, callback_data='Judge2'),
                             InlineKeyboardButton(judgenameJ2, callback_data='Judge3')],
                            [InlineKeyboardButton(judgenameJ3, callback_data='Judge4'),
                             InlineKeyboardButton(judgenameJ4, callback_data='Judge5')],
                            [InlineKeyboardButton("New", callback_data='New')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id,
                                         text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                                         reply_markup=reply_markup)
            elif idioma == "Español":
                keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                             InlineKeyboardButton(judgenameJ1, callback_data='Judge2'),
                             InlineKeyboardButton(judgenameJ2, callback_data='Judge3')],
                            [InlineKeyboardButton(judgenameJ3, callback_data='Judge4'),
                             InlineKeyboardButton(judgenameJ4, callback_data='Judge5')],
                            [InlineKeyboardButton("Nuevo", callback_data='New')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id,
                                         text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                         reply_markup=reply_markup)
            return EXISTING
        elif longitud >= 6:
            judgenameJ = prueba[longitud - 1]
            judgenameJ1 = prueba[longitud - 2]
            judgenameJ2 = prueba[longitud - 3]
            judgenameJ3 = prueba[longitud - 4]
            judgenameJ4 = prueba[longitud - 5]
            judgenameJ5 = prueba[longitud - 6]
            judgeemailJ = jueces[longitud - 1]
            judgeemailJ1 = jueces[longitud - 2]
            judgeemailJ2 = jueces[longitud - 3]
            judgeemailJ3 = jueces[longitud - 4]
            judgeemailJ4 = jueces[longitud - 5]
            judgeemailJ5 = jueces[longitud - 6]
            if idioma == "English":
                keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                             InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                            [InlineKeyboardButton(judgenameJ2, callback_data='Judge3'),
                             InlineKeyboardButton(judgenameJ3, callback_data='Judge4')],
                            [InlineKeyboardButton(judgenameJ4, callback_data='Judge5'),
                             InlineKeyboardButton(judgenameJ5, callback_data='Judge6')],
                            [InlineKeyboardButton("New", callback_data='New')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id,
                                         text='You have one judge before. Select it, or press NEW if you want a new judge for this challenge.',
                                         reply_markup=reply_markup)
            elif idioma == "Español":
                keyboard = [[InlineKeyboardButton(judgenameJ, callback_data='Judge1'),
                             InlineKeyboardButton(judgenameJ1, callback_data='Judge2')],
                            [InlineKeyboardButton(judgenameJ2, callback_data='Judge3'),
                             InlineKeyboardButton(judgenameJ3, callback_data='Judge4')],
                            [InlineKeyboardButton(judgenameJ4, callback_data='Judge5'),
                             InlineKeyboardButton(judgenameJ5, callback_data='Judge6')],
                            [InlineKeyboardButton("New", callback_data='New')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id,
                                         text='Has utilizado los siguientes jueces. Select it, or press NEW if you want a new judge for this challenge.',
                                         reply_markup=reply_markup)
            return EXISTING


def judgename(update, context):
    global judge, chat_id, user, vfinal, nuevouser
    text = update.message.text
    judge = text
    record = {'Judge name': text}
    record1 = {'Name': text}
    airtable.update_by_field('Code', code, record)
    airtable2.update_by_field('Code', code, record)
    airtable3.update_by_field('Code', code, record1)
    if idioma=="English":
        update.message.reply_text('Provide me the judge email, please',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
    elif idioma=="Español":
        update.message.reply_text('Por favor, enviame el email del juez',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
    return JUDGEMAIL

def judgemail(update, context):
    global chat_id, user, judgeemail, vfinal, existing
    print("He llegado")
    text = update.message.text
    if ("@" in text) and ("." in text):
        a=1
    else:
        a=0
    print(a)
    if a==0:
        if idioma=="English":
            context.bot.send_message(chat_id, text='Sorry, this format is not accepted. ')
            update.message.reply_text('Please, verify that you have sent a valid email and resend it to me.')
        elif idioma=="Español":
            context.bot.send_message(chat_id, text='Sorry, this format is not accepted. ')
            update.message.reply_text('Please, verify that you have sent a valid email and resend it to me.')
        return JUDGEMAIL
    else:
        record = {'Email judge': text}
        airtable.update_by_field('Code', code, record)
        airtable2.update_by_field('Code',code, record)
        print("1111111111111111")
        print(change)
        if change==0:
            judgeemail = text
            record = {'Email judge': text}
            airtable.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record)
            emails=todosjuecesemails()
            if (text in emails):
                airtable3.delete_by_field('Code',code)
            else:
                airtable3.update_by_field('Code', code, record)

            if idioma == "English":
                if existing==0:
                    reply_keyboard = [['Insert Quantity'],['Return']]

                    context.bot.send_message(chat_id, text=
                    'How many money do you want to bet?',
                                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                elif existing==1:
                    existing=0
                    reply_keyboard = [['Insert Quantity']]

                    context.bot.send_message(chat_id, text=
                    'How many money do you want to bet?',
                                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                if existing==0:
                    reply_keyboard = [['Insertar Cantidad'],['Volver Atrás']]

                    context.bot.send_message(chat_id, text=
                    '¿Cuánto dinero quieres apostar?',
                                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                elif existing==1:
                    existing=0
                    reply_keyboard = [['Insertar Cantidad']]

                    context.bot.send_message(chat_id, text=
                    '¿Cuánto dinero quieres apostar?',
                                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return ADDITIONAL
        elif change==1:
            emails=todosjuecesemails()
            print(emails)
            print(judgeemail)
            if (judgeemail in emails):
                sigue=0
            else:
                sigue=1
            while sigue==0:
                print(text)
                emails =todosjuecesemails()
                record = {'Email judge': text}
                airtable3.update_by_field('Email judge', judgeemail, record)
                if (judgeemail in emails):
                    sigue = 0
                else:
                    sigue = 1

            judgeemail = text
            airtable3.update_by_field('Code', code, record)
            if idioma == "English":
                reply_keyboard = [['Change'], ['OK']]
                context.bot.send_message(chat_id, text='Thank you!')
                context.bot.send_message(chat_id,
                                         text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' If there is any mistake, press the change button. Otherwise press Ok button.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                reply_keyboard = [['Cambiar'], ['OK']]
                context.bot.send_message(chat_id, text='Gracias!!')
                context.bot.send_message(chat_id,
                                         text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return FINAL

def metercantidad(update,context):
    if idioma=="English":
        update.message.reply_text('Provide me the judge email, please',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
    elif idioma=="Español":
        update.message.reply_text('Por favor, enviame el email del juez',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
    return JUDGEMAIL

def amount1(update,context):
    global chat_id,amount, vfinal
    text=update.message.text
    print(text)
    if text == "Insert Quantity" or text=="Insertar Cantidad":
        if idioma=="English":
            keyboard = [['5€', '10€', '15€', ], ['20€', '25€', 'Other']]
            context.bot.send_message(chat_id, text=
            '\n\n'
            'Select the quantity from the options below',
                                     reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            keyboard = [['5€', '10€', '15€', ], ['20€', '25€', 'Other']]
            context.bot.send_message(chat_id, text=
            '\n\n'
            'Selecciona la cantidad de las opciones de abajo',
                                     reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        return AMOUNT
    else:
        try:
            text = int(text)
            print("af")
            text1 = str(text) + str("€")
            amount = text1
            record = {'Amount': text1}
            record2 = {'Amount': text1}
            airtable.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record2)
            if change==0:
                if idioma=="English":
                    reply_keyboard = [['Insert Date'],['Return']]

                    update.message.reply_text(
                        '\n\n'
                        'When must the challenge be done?',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                elif idioma=="Español":
                    reply_keyboard = [['Insertar Fecha'],['Volver Atrás']]

                    update.message.reply_text(
                        '\n\n'
                        '¿Cuándo debe de estar hecho el reto?',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                return DUEDATE
            elif change==1:
                if idioma == "English":
                    reply_keyboard = [['Change'], ['OK']]
                    context.bot.send_message(chat_id, text='Thank you!')
                    context.bot.send_message(chat_id,
                                             text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                 challengename, amount, duedate, judge, judgeemail, useremail),
                                             parse_mode="Markdown",
                                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    update.message.reply_text(
                        '\n\n'
                        ' If there is any mistake, press the change button. Otherwise press Ok button.',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                elif idioma == "Español":
                    reply_keyboard = [['Cambiar'], ['OK']]
                    context.bot.send_message(chat_id, text='Gracias!!')
                    context.bot.send_message(chat_id,
                                             text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                 challengename, amount, duedate, judge, judgeemail, useremail),
                                             parse_mode="Markdown",
                                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    update.message.reply_text(
                        '\n\n'
                        ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                return FINAL
        except ValueError:
            print("faf")
            prueba2 = text.find("€")
            if prueba2 == -1:
                context.bot.send_message(chat_id, text='Sorry, I cannot storage text',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
                if idioma == "English":
                    reply_keyboard = [['Insert Quantity']]

                    context.bot.send_message(chat_id, text=
                    'How many money do you want to bet?',
                                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                elif idioma == "Español":
                    reply_keyboard = [['Insertar Cantidad']]

                    context.bot.send_message(chat_id, text=
                    '¿Cuánto dinero quieres apostar?',
                                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                return ADDITIONAL
            elif prueba2 != -1:
                text1 = str(text)
                prueba = text1.find("€")
                if prueba == -1:
                    text1 = str(text) + str("€")
                elif prueba != -1:
                    text1 = str(text)

                amount = text1
                record = {'Amount': text1}
                record2 = {'Amount': text1}
                airtable.update_by_field('Code', code, record)
                airtable2.update_by_field('Code', code, record2)

                if change==0:
                    if idioma == "English":
                        reply_keyboard = [['Insert Date'],['Return']]

                        update.message.reply_text(
                            '\n\n'
                            'When must the challenge be done?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                    elif idioma == "Español":
                        reply_keyboard = [['Insertar Fecha'],['Volver Atrás']]

                        update.message.reply_text(
                            '\n\n'
                            '¿Cuándo debe de estar hecho el reto?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                    return DUEDATE
                elif change==1:
                    if idioma == "English":
                        reply_keyboard = [['Change'], ['OK']]
                        context.bot.send_message(chat_id, text='Thank you!')
                        context.bot.send_message(chat_id,
                                                 text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                     challengename, amount, duedate, judge, judgeemail, useremail),
                                                 parse_mode="Markdown",
                                                 reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                        update.message.reply_text(
                            '\n\n'
                            ' If there is any mistake, press the change button. Otherwise press Ok button.',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                    elif idioma == "Español":
                        reply_keyboard = [['Cambiar'], ['OK']]
                        context.bot.send_message(chat_id, text='Gracias!!')
                        context.bot.send_message(chat_id,
                                                 text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                     challengename, amount, duedate, judge, judgeemail, useremail),
                                                 parse_mode="Markdown",
                                                 reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                        update.message.reply_text(
                            '\n\n'
                            ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                    return FINAL

            else:
                text1 = str(text)
                prueba = text1.find("€")
                if prueba == -1:
                    text1 = str(text) + str("€")
                elif prueba != -1:
                    text1 = str(text)

                amount = text1
                record = {'Amount': text1}
                record2 = {'Amount': text1}
                airtable.update_by_field('Code', code, record)
                airtable2.update_by_field('Code',code, record2)
                if change==0:
                    if idioma == "English":
                        reply_keyboard = [['Insert Date'],['Return']]

                        update.message.reply_text(
                            '\n\n'
                            'When must the challenge be done?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                    elif idioma == "Español":
                        reply_keyboard = [['Insertar Fecha'],['Volver Atrás']]

                        update.message.reply_text(
                            '\n\n'
                            '¿Cuándo debe de estar hecho el reto?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                    return DUEDATE
                elif change==1:
                    vfinal=0
                    if idioma == "English":
                        reply_keyboard = [['Change'], ['OK']]
                        context.bot.send_message(chat_id, text='Thank you!')
                        context.bot.send_message(chat_id,
                                                 text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                     challengename, amount, duedate, judge, judgeemail, useremail),
                                                 parse_mode="Markdown",
                                                 reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                        update.message.reply_text(
                            '\n\n'
                            ' If there is any mistake, press the change button. Otherwise press Ok button.',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                    elif idioma == "Español":
                        reply_keyboard = [['Cambiar'], ['OK']]
                        context.bot.send_message(chat_id, text='Gracias!!')
                        context.bot.send_message(chat_id,
                                                 text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                     challengename, amount, duedate, judge, judgeemail, useremail),
                                                 parse_mode="Markdown",
                                                 reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                        update.message.reply_text(
                            '\n\n'
                            ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                    return FINAL

def amount(update, context):
    global amount,chat_id, vfinal
    print("He llegado")
    text = update.message.text
    if change==1:
        if (text == "Other"):
            if idioma=="English":
                update.message.reply_text('Please, send me the amount that you want to bet in €.',
                                          reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif idioma=="Español":
                update.message.reply_text('Envíame la cantidad que quieres apostar en €.',
                                          reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            return ADDITIONAL
        else:
            amount = text
            record = {'Amount': text}
            record2 = {'Amount': text}
            airtable.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record2)
            if idioma == "English":
                reply_keyboard = [['Change'], ['OK']]
                context.bot.send_message(chat_id, text='Thank you!')
                context.bot.send_message(chat_id,
                                         text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' If there is any mistake, press the change button. Otherwise press Ok button.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                reply_keyboard = [['Cambiar'], ['OK']]
                context.bot.send_message(chat_id, text='Gracias!!')
                context.bot.send_message(chat_id,
                                         text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return FINAL
    else:
        if (text == "Other"):
            if idioma=="English":
                update.message.reply_text('Please, send me the amount that you want to bet in €.',
                                          reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif idioma=="Español":
                update.message.reply_text('Envíame la cantidad que quieres apostar en €.',
                                          reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            return ADDITIONAL
        elif (text != "Other"):
            amount = text
            record = {'Amount': text}
            record2 = {'Amount': text}
            airtable.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record2)
            if (vfinal)==0:
                if idioma == "English":
                    reply_keyboard = [['Insert Date'],['Return']]

                    update.message.reply_text(
                        '\n\n'
                        'When must the challenge be done?',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                elif idioma == "Español":
                    reply_keyboard = [['Insertar Fecha'],['Volver Atrás']]

                    update.message.reply_text(
                        '\n\n'
                        '¿Cuándo debe de estar hecho el reto?',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                return DUEDATE
            else:
                vfinal=0
                if idioma == "English":
                    reply_keyboard = [['Change'], ['OK']]
                    context.bot.send_message(chat_id, text='Thank you!')
                    context.bot.send_message(chat_id,
                                             text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                 challengename, amount, duedate, judge, judgeemail, useremail),
                                             parse_mode="Markdown",
                                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    update.message.reply_text(
                        '\n\n'
                        ' If there is any mistake, press the change button. Otherwise press Ok button.',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                elif idioma == "Español":
                    reply_keyboard = [['Cambiar'], ['OK']]
                    context.bot.send_message(chat_id, text='Gracias!!')
                    context.bot.send_message(chat_id,
                                             text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                 challengename, amount, duedate, judge, judgeemail, useremail),
                                             parse_mode="Markdown",
                                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    update.message.reply_text(
                        '\n\n'
                        ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                return FINAL


def additional(update, context):
    global amount,chat_id
    print("He llegado")
    chat_id = update.effective_chat.id
    text = update.message.text
    print(text)
    try:
        text = int(text)
    except ValueError:
        print("12314")
        prueba2=text.find("€")
        if prueba2 == -1:
            context.bot.send_message(chat_id, text='Sorry, I cannot storage text',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            update.message.reply_text('Please, send me again the quantity as a number instead of a text',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            return ADDITIONAL
        elif prueba2 !=-1:
            text1 = str(text)
            prueba = text1.find("€")
            if prueba == -1:
                text1 = str(text) + str("€")
            elif prueba != -1:
                text1 = str(text)
            if change==0:
                amount = text1
                record = {'Amount': text1}
                record2 = {'Amount': text1}
                airtable.update_by_field('Code', code, record)
                airtable2.update_by_field('Code', code, record2)
                if idioma == "English":
                    reply_keyboard = [['Insert Date'],['Return']]

                    update.message.reply_text(
                        '\n\n'
                        'When must the challenge be done?',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                elif idioma == "Español":
                    reply_keyboard = [['Insertar Fecha'],['Volver Atrás']]

                    update.message.reply_text(
                        '\n\n'
                        '¿Cuándo debe de estar hecho el reto?',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                return DUEDATE
            elif change==1:
                if idioma == "English":
                    reply_keyboard = [['Change'], ['OK']]
                    context.bot.send_message(chat_id, text='Thank you!')
                    context.bot.send_message(chat_id,
                                             text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                 challengename, amount, duedate, judge, judgeemail, useremail),
                                             parse_mode="Markdown",
                                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    update.message.reply_text(
                        '\n\n'
                        ' If there is any mistake, press the change button. Otherwise press Ok button.',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                elif idioma == "Español":
                    reply_keyboard = [['Cambiar'], ['OK']]
                    context.bot.send_message(chat_id, text='Gracias!!')
                    context.bot.send_message(chat_id,
                                             text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                 challengename, amount, duedate, judge, judgeemail, useremail),
                                             parse_mode="Markdown",
                                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    update.message.reply_text(
                        '\n\n'
                        ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                return FINAL

    else:
        print("9852")
        text1= str(text)
        prueba=text1.find("€")
        if prueba == -1:
            text1=str(text)+str("€")
        elif prueba != -1:
            text1=str(text)

        amount= text1
        record = {'Amount': text1}
        record2 = {'Amount': text1}
        airtable.update_by_field('Code', code, record)
        airtable2.update_by_field('Code', code, record2)
        if change==0:
            if idioma == "English":
                reply_keyboard = [['Insert Date'],['Return']]

                update.message.reply_text(
                    '\n\n'
                    'When must the challenge be done?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                reply_keyboard = [['Insertar Fecha'],['Volver Atrás']]

                update.message.reply_text(
                    '\n\n'
                    '¿Cuándo debe de estar hecho el reto?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return DUEDATE
        elif change==1:
            if idioma == "English":
                reply_keyboard = [['Change'], ['OK']]
                context.bot.send_message(chat_id, text='Thank you!')
                context.bot.send_message(chat_id,
                                         text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' If there is any mistake, press the change button. Otherwise press Ok button.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                reply_keyboard = [['Cambiar'], ['OK']]
                context.bot.send_message(chat_id, text='Gracias!!')
                context.bot.send_message(chat_id,
                                         text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                             challengename, amount, duedate, judge, judgeemail, useremail),
                                         parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                update.message.reply_text(
                    '\n\n'
                    ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return FINAL
def meterfecha(update, context):
    keyboard = [['5€', '10€', '15€', ], ['20€', '25€', 'Other']]
    if idioma == "English":
        context.bot.send_message(chat_id, text=
        '\n\n'
        'Select the quantity from the options below',
                                 reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    elif idioma == "Español":
        context.bot.send_message(chat_id, text=
        '\n\n'
        'Selecciona la cantidad de las opciones de debajo',
                                 reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return AMOUNT

def date(update,context):
    global chat_id, vfinal
    text= update.message.text
    if text== "Insert Date" or text=="Insertar Fecha" or (text=="/Duedate" and (vfinal)==1):
        if idioma=="English":
            keyboard = [['January', 'February', 'March', 'April'], ['May', 'June', 'July', 'August'],
                        ['September', 'October', 'November', 'December']]
            context.bot.send_message(chat_id, text=
            '\n\n'
            'Select the month',
                                     reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            keyboard = [['Enero', 'Febrero', 'Marzo', 'Abril'], ['Mayo', 'Junio', 'Julio', 'Agosto'],
                        ['Septiembre', 'Octubre', 'Noviembre', 'Diciembre']]
            context.bot.send_message(chat_id, text=
            '\n\n'
            'Seleccione el mes',
                                     reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        return DATE
    else:
        if idioma == "English":
            reply_keyboard = [['Insert Date'],['Return']]

            update.message.reply_text(
                '\n\n'
                'When must the challenge be done?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma == "Español":
            reply_keyboard = [['Insertar Fecha'],['Volver Atrás']]

            update.message.reply_text(
                '\n\n'
                '¿Cuándo debe de estar hecho el reto?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return DUEDATE

def month(update,context):
    global  month,chat_id
    print("TodoOK")
    text = update.message.text
    month = text
    vals31 = ["January","March","May","July","August","October","December","Enero","Marzo","Mayo","Julio","Agosto","Octubre","Diciembre"]
    vals30 = ["April","June","September","November","Abril","Junio","Septiembre","Noviembre"]
    vals28 = ["February","Febrero"]

    if month in vals31:
        reply_keyboard = [['1', '2', '3','4','5','6','7'],['8', '9', '10','11','12','13','14'],['15', '16', '17','18','19','20','21'],
                          ['22', '23', '24','25','26','27','28'],['29','30','31','_','_','_','_']]
        if idioma=="English":
            update.message.reply_text(
                '\n\n'
                'Select the day',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            update.message.reply_text(
                '\n\n'
                'Selecciona el día',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DATE1
    elif month in vals30:
        reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                          ['15', '16', '17', '18', '19', '20', '21'],
                          ['22', '23', '24', '25', '26', '27', '28'], ['29', '30','_','_','_','_','_']]

        if idioma=="English":
            update.message.reply_text(
                '\n\n'
                'Select the day',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            update.message.reply_text(
                '\n\n'
                'Selecciona el día',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DATE1
    elif month in vals28:
        reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                          ['15', '16', '17', '18', '19', '20', '21'],
                          ['22', '23', '24', '25', '26', '27', '28']]

        if idioma=="English":
            update.message.reply_text(
                '\n\n'
                'Select the day',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            update.message.reply_text(
                '\n\n'
                'Selecciona el día',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DATE1

def month1(update, context):
    global month
    text=update.message.text
    vals31 = ["January", "March", "May", "July", "August", "October", "December","january", "march", "may", "july", "august", "october", "december","Enero","Marzo","Mayo","Julio","Agosto","Octubre","Diciembre" ]
    vals30 = ["April", "June", "September", "November","april", "june", "september", "november","Abril","Junio","Septiembre","Noviembre"]
    vals28 = ["February","february","Febrero"]

    if text in vals31:
        month = text
        print("llegue")
        reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                          ['15', '16', '17', '18', '19', '20', '21'],
                          ['22', '23', '24', '25', '26', '27', '28'], ['29', '30', '31', '_', '_', '_', '_']]

        if idioma=="English":
            update.message.reply_text(
                '\n\n'
                'Select the day',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            update.message.reply_text(
                '\n\n'
                'Selecciona el día',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DATE1
    elif text in vals30:
        month = text
        reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                          ['15', '16', '17', '18', '19', '20', '21'],
                          ['22', '23', '24', '25', '26', '27', '28'], ['29', '30', '_', '_', '_', '_', '_']]

        if idioma=="English":
            update.message.reply_text(
                '\n\n'
                'Select the day',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            update.message.reply_text(
                '\n\n'
                'Selecciona el día',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DATE1
    elif text in vals28:
        month = text
        reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                          ['15', '16', '17', '18', '19', '20', '21'],
                          ['22', '23', '24', '25', '26', '27', '28']]

        if idioma=="English":
            update.message.reply_text(
                '\n\n'
                'Select the day',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            update.message.reply_text(
                '\n\n'
                'Selecciona el día',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DATE1
    else:
        if idioma=="English":
            keyboard = [['January', 'February', 'March', 'April'], ['May', 'June', 'July', 'August'],
                        ['September', 'October', 'November', 'December']]
            context.bot.send_message(chat_id, text=
            '\n\n'
            'Select the month',
                                     reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            keyboard = [['Enero', 'Febrero', 'Marzo', 'Abril'], ['Mayo', 'Junio', 'Julio', 'Agosto'],
                        ['Septiembre', 'Octubre', 'Noviembre', 'Diciembre']]
            context.bot.send_message(chat_id, text=
            '\n\n'
            'Seleccione el mes',
                                     reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
        return DATE

def day(update,context):
    global day,chat_id, month
    print("TodoOK")
    vals28=['1', '2', '3', '4', '5', '6', '7','8', '9', '10', '11', '12', '13', '14','15', '16', '17', '18', '19', '20', '21','22', '23', '24', '25', '26', '27', '28']
    vals30=['1', '2', '3', '4', '5', '6', '7','8', '9', '10', '11', '12', '13', '14','15', '16', '17', '18', '19', '20', '21','22', '23', '24', '25', '26', '27', '28', '29','30']
    vals31=['1', '2', '3', '4', '5', '6', '7','8', '9', '10', '11', '12', '13', '14','15', '16', '17', '18', '19', '20', '21','22', '23', '24', '25', '26', '27', '28','29','30','31']
    text = update.message.text
    print(text)
    if month == "January" or month == "March" or month == "May" or month == "July" or month == "August" or month == "October" or month == "December" or month == "january"\
        or month == "march" or month == "may" or month == "july" or month == "august" or month == "october" or month == "december" or month == "Enero" or month=="Marzo"\
        or month == "Mayo" or month=="Julio" or month=="Agosto" or month=="Octubre" or month=="Diciembre":
        a=1
    else:
        if month=="April" or month=="June" or month=="September" or month=="November" or month=="april" or month=="june" or month=="september" \
            or month=="november" or month == "Abril" or month=="Junio" or month=="Septiembre" or month=="Noviembre":
            a=2
        else:
            if month=="February" or month=="february" or month=="Febrero":
                 a=3
    if (text in vals31) and (text in vals30) and (text in vals28):
        b=1
    else:
        if (text in vals31) and (text in vals30) and ((text in vals28)==False):
            b=2
        else:
            if (text in vals31) and ((text in vals30)==False):
                b=3
            else:
                b=4
    print(a)
    print(b)
    print(text)
    if b==2 and a==3:
        reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                          ['15', '16', '17', '18', '19', '20', '21'],
                          ['22', '23', '24', '25', '26', '27', '28']]


        if idioma=="English":
            update.message.reply_text(
                '\n\n'
                'Select the day',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            update.message.reply_text(
                '\n\n'
                'Selecciona el día',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DATE1
    elif b==3 and a==2:
        reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                          ['15', '16', '17', '18', '19', '20', '21'],
                          ['22', '23', '24', '25', '26', '27', '28'], ['29', '30', '_', '_', '_', '_', '_']]


        if idioma=="English":
            update.message.reply_text(
                '\n\n'
                'Select the day',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            update.message.reply_text(
                '\n\n'
                'Selecciona el día',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DATE1
    elif b==4:
        if a==1:
            reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                              ['15', '16', '17', '18', '19', '20', '21'],
                              ['22', '23', '24', '25', '26', '27', '28'], ['29', '30', '31', '_', '_', '_', '_']]

            if idioma == "English":
                update.message.reply_text(
                    '\n\n'
                    'Select the day',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                update.message.reply_text(
                    '\n\n'
                    'Selecciona el día',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return DATE1
        elif a==2:
            reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                              ['15', '16', '17', '18', '19', '20', '21'],
                              ['22', '23', '24', '25', '26', '27', '28'], ['29', '30', '_', '_', '_', '_', '_']]

            if idioma == "English":
                update.message.reply_text(
                    '\n\n'
                    'Select the day',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                update.message.reply_text(
                    '\n\n'
                    'Selecciona el día',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return DATE1
        elif a==3:
            reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                              ['15', '16', '17', '18', '19', '20', '21'],
                              ['22', '23', '24', '25', '26', '27', '28']]

            if idioma == "English":
                update.message.reply_text(
                    '\n\n'
                    'Select the day',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                update.message.reply_text(
                    '\n\n'
                    'Selecciona el día',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return DATE1
    else:
        print("a1")
        day=text
        reply_keyboard = [['2020'], ['2021'], ['2022'], ['2023']]

        if idioma=="English":
            update.message.reply_text(
                '\n\n'
                'Select the year',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            update.message.reply_text(
                '\n\n'
                'Selecciona el año',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DUEDATE1



def day1(update,context):
    global day,chat_id, month
    print("TodoOK22")
    vals28=['1', '2', '3', '4', '5', '6', '7','8', '9', '10', '11', '12', '13', '14','15', '16', '17', '18', '19', '20', '21','22', '23', '24', '25', '26', '27', '28']
    vals30=['1', '2', '3', '4', '5', '6', '7','8', '9', '10', '11', '12', '13', '14','15', '16', '17', '18', '19', '20', '21','22', '23', '24', '25', '26', '27', '28', '29','30']
    vals31=['1', '2', '3', '4', '5', '6', '7','8', '9', '10', '11', '12', '13', '14','15', '16', '17', '18', '19', '20', '21','22', '23', '24', '25', '26', '27', '28','29','30','31']
    text = update.message.text
    print(text)
    if month == "January" or month == "March" or month == "May" or month == "July" or month == "August" or month == "October" or month == "December" or month == "january"\
        or month == "march" or month == "may" or month == "july" or month == "august" or month == "october" or month == "december" or month == "Enero" or month=="Marzo"\
        or month == "Mayo" or month=="Julio" or month=="Agosto" or month=="Octubre" or month=="Diciembre":
        a=1
    else:
        if month=="April" or month=="June" or month=="September" or month=="November" or month=="april" or month=="june" or month=="september" \
            or month=="november" or month == "Abril" or month=="Junio" or month=="Septiembre" or month=="Noviembre":
            a=2
        else:
            if month=="February" or month=="february" or month=="Febrero":
                 a=3
    if (text in vals31) and (text in vals30) and (text in vals28):
        b=1
    else:
        if (text in vals31) and (text in vals30) and ((text in vals28)==False):
            b=2
        else:
            if (text in vals31) and ((text in vals30)==False) and ((text in vals28)==False):
                b=3
            else:
                b=4
    print(a)
    print(b)
    print(text)
    if (b==2 or b==3) and a==3:
        reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                          ['15', '16', '17', '18', '19', '20', '21'],
                          ['22', '23', '24', '25', '26', '27', '28']]

        if idioma == "English":
            update.message.reply_text(
                '\n\n'
                'Select the day',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma == "Español":
            update.message.reply_text(
                '\n\n'
                'Selecciona el día',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DATE1
    elif b==3 and a==2:
        reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                          ['15', '16', '17', '18', '19', '20', '21'],
                          ['22', '23', '24', '25', '26', '27', '28'], ['29', '30', '_', '_', '_', '_', '_']]

        if idioma == "English":
            update.message.reply_text(
                '\n\n'
                'Select the day',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma == "Español":
            update.message.reply_text(
                '\n\n'
                'Selecciona el día',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DATE1
    elif b==4:
        if a==1:
            reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                              ['15', '16', '17', '18', '19', '20', '21'],
                              ['22', '23', '24', '25', '26', '27', '28'], ['29', '30', '31', '_', '_', '_', '_']]

            if idioma == "English":
                update.message.reply_text(
                    '\n\n'
                    'Select the day',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                update.message.reply_text(
                    '\n\n'
                    'Selecciona el día',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return DATE1
        elif a==2:
            reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                              ['15', '16', '17', '18', '19', '20', '21'],
                              ['22', '23', '24', '25', '26', '27', '28'], ['29', '30', '_', '_', '_', '_', '_']]

            if idioma == "English":
                update.message.reply_text(
                    '\n\n'
                    'Select the day',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                update.message.reply_text(
                    '\n\n'
                    'Selecciona el día',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return DATE1
        elif a==3:
            reply_keyboard = [['1', '2', '3', '4', '5', '6', '7'], ['8', '9', '10', '11', '12', '13', '14'],
                              ['15', '16', '17', '18', '19', '20', '21'],
                              ['22', '23', '24', '25', '26', '27', '28']]

            if idioma == "English":
                update.message.reply_text(
                    '\n\n'
                    'Select the day',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                update.message.reply_text(
                    '\n\n'
                    'Selecciona el día',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return DATE1
    else:
        print("a1")
        day=text
        reply_keyboard = [['2020'], ['2021'], ['2022'], ['2023']]

        if idioma=="English":
            update.message.reply_text(
                '\n\n'
                'Select the year',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            update.message.reply_text(
                '\n\n'
                'Selecciona el año',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DUEDATE1

def year(update, context):
    global year, month, day, duedate,chat_id, vfinal, dia, mes, año, today,useremail
    print("He llegado")
    text = update.message.text
    if text=="/UserEmail" and (vfinal)==1:
        if idioma=="English":
            update.message.reply_text(
                'Could you provide me your email? You will receive an email confirming the challenge and future updates.',reply_markup = ReplyKeyboardRemove(
        remove_keyboard=True))
            return  USERMAIL
        elif idioma=="Español":
            update.message.reply_text(
                'Por favor, enviame tu email. Recibirás un correo confirmando que has creado el reto y futuras actualizaciones de este.',
                reply_markup=ReplyKeyboardRemove(
                    remove_keyboard=True))
            return USERMAIL
    else:
        year = text
        if month == "January" or month == "january" or month== "Enero":
            month = '01'
        elif month == "February" or month == "february" or month== "Febrero":
            month = '02'
        elif month == "March"or month == "march" or month== "Marzo":
            month = '03'
        elif month == "April" or month == "april" or month== "Abril":
            month = '04'
        elif month == "May" or month == "may" or month== "Mayo":
            month = '05'
        elif month == "June" or month == "june" or month== "Junio":
            month = '06'
        elif month == "July" or month == "july" or month== "Julio":
            month = '07'
        elif month == "August" or month == "august" or month== "Agosto":
            month = '08'
        elif month == "September" or month == "september" or month== "Septiembre":
            month = '09'
        elif month == "October" or month == "october" or month== "Octubre":
            month = '10'
        elif month == "November" or month == "november" or month== "Noviembre":
            month = '11'
        elif month == "December" or month == "december" or month== "Diciembre":
            month = '12'

        today = datetime.today()
        print(today)
        dia=today.day
        mes=today.month
        año=today.year

        date = day + "/" + month + "/" + year
        date1=datetime.strptime(date, "%d/%m/%Y")
        print(date1)

        if date1 < today:
            print("novale")
            if idioma == "English":
                reply_keyboard = [['Insert Date'],['Return']]

                update.message.reply_text(
                    '\n\n'
                    'When must the challenge be done?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma == "Español":
                reply_keyboard = [['Insertar Fecha'],['Volver Atrás']]

                update.message.reply_text(
                    '\n\n'
                    '¿Cuándo debe de estar hecho el reto?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return DUEDATE
        else:
            print("vale")

            duedate = date
            record = {'Due date': date}
            record1 = {'Due date': date}
            airtable.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record1)
            print(vfinal)
            if (vfinal==0)and nuevouser==0:
                if idioma == "English":
                    update.message.reply_text(
                        'Could you provide me your email? You will receive an email confirming the challenge and future updates.',
                        reply_markup=ReplyKeyboardRemove(
                            remove_keyboard=True))
                    return USERMAIL
                elif idioma == "Español":
                    update.message.reply_text(
                        'Por favor, enviame tu email. Recibirás un correo confirmando que has creado el reto y futuras actualizaciones de este.',
                        reply_markup=ReplyKeyboardRemove(
                            remove_keyboard=True))
                    return USERMAIL
            if (vfinal)==1:
                if idioma == "English":
                    reply_keyboard = [['Change'], ['OK']]
                    context.bot.send_message(chat_id, text='Thank you!')
                    context.bot.send_message(chat_id,
                                             text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                 challengename, amount, duedate, judge, judgeemail, useremail),
                                             parse_mode="Markdown",
                                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    update.message.reply_text(
                        '\n\n'
                        ' If there is any mistake, press the change button. Otherwise press Ok button.',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                elif idioma == "Español":
                    reply_keyboard = [['Cambiar'], ['OK']]
                    context.bot.send_message(chat_id, text='Gracias!!')
                    context.bot.send_message(chat_id,
                                             text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                 challengename, amount, duedate, judge, judgeemail, useremail),
                                             parse_mode="Markdown",
                                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    update.message.reply_text(
                        '\n\n'
                        ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                return FINAL

            if (nuevouser)==1:
                emails = buscaruseremails()
                useremail = emails[len(emails) - 1]
                if idioma == "English":
                    reply_keyboard = [['Change'], ['OK']]
                    context.bot.send_message(chat_id, text='Thank you!')
                    context.bot.send_message(chat_id,
                                             text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                 challengename, amount, duedate, judge, judgeemail, useremail),
                                             parse_mode="Markdown",
                                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    update.message.reply_text(
                        '\n\n'
                        ' If there is any mistake, press the change button. Otherwise press Ok button.',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                elif idioma == "Español":
                    reply_keyboard = [['Cambiar'], ['OK']]
                    context.bot.send_message(chat_id, text='Gracias!!')
                    context.bot.send_message(chat_id,
                                             text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                 challengename, amount, duedate, judge, judgeemail, useremail),
                                             parse_mode="Markdown",
                                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    update.message.reply_text(
                        '\n\n'
                        ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                return FINAL

def year1(update, context):
    global year, month, day, duedate,chat_id, vfinal
    text= update.message.text
    if text=="2020" or text=="2021" or text=="2022" or text=="2023":
        year = text
        if month == "January" or month == "january" or month == "Enero":
            month = '01'
        elif month == "February" or month == "february" or month == "Febrero":
            month = '02'
        elif month == "March" or month == "march" or month == "Marzo":
            month = '03'
        elif month == "April" or month == "april" or month == "Abril":
            month = '04'
        elif month == "May" or month == "may" or month == "Mayo":
            month = '05'
        elif month == "June" or month == "june" or month == "Junio":
            month = '06'
        elif month == "July" or month == "july" or month == "Julio":
            month = '07'
        elif month == "August" or month == "august" or month == "Agosto":
            month = '08'
        elif month == "September" or month == "september" or month == "Septiembre":
            month = '09'
        elif month == "October" or month == "october" or month == "Octubre":
            month = '10'
        elif month == "November" or month == "november" or month == "Noviembre":
            month = '11'
        elif month == "December" or month == "december" or month == "Diciembre":
            month = '12'
        today = datetime.today()
        print(today)

        date = day + "/" + month + "/" + year
        date1 = datetime.strptime(date, "%d/%m/%Y")
        print(date1)

        if date1 < today:
            print("novale")
            if idioma=="English":
                reply_keyboard = [['Insert Date'],['Return']]

                update.message.reply_text(
                    '\n\n'
                    'Sorry, the date selected has passed. Please select a future date',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            elif idioma=="Español":
                reply_keyboard = [['Insertar Fecha'],['Volver Atrás']]

                update.message.reply_text(
                    '\n\n'
                    'Lo siento, la fecha seleccionada ya ha pasado. Por favor, seleccione una fecha futura.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return DUEDATE
        else:

            duedate = date
            record = {'Due date': date}
            record1 = {'Due date': date}
            airtable.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record1)
            print(vfinal)
            if (vfinal == 0) and nuevouser == 0:
                if idioma=="English":
                    update.message.reply_text(
                    'The last step. Could you provide me your email? You will receive an email confirming the challenge and future updates.',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
                elif idioma=="Español":
                    update.message.reply_text(
                        'El último paso.¿Puedes, por favor, enviarme tu email? Recibirás un email confirmando el reto que se ha creado el reto y futuras actualizaciones',
                        reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

                return USERMAIL
            if (vfinal) == 1:
                if idioma == "English":
                    reply_keyboard = [['Change'], ['OK']]
                    context.bot.send_message(chat_id, text='Thank you!')
                    context.bot.send_message(chat_id,
                                             text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                 challengename, amount, duedate, judge, judgeemail, useremail),
                                             parse_mode="Markdown",
                                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    update.message.reply_text(
                        '\n\n'
                        ' If there is any mistake, press the change button. Otherwise press Ok button.',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                elif idioma == "Español":
                    reply_keyboard = [['Cambiar'], ['OK']]
                    context.bot.send_message(chat_id, text='Gracias!!')
                    context.bot.send_message(chat_id,
                                             text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                 challengename, amount, duedate, judge, judgeemail, useremail),
                                             parse_mode="Markdown",
                                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    update.message.reply_text(
                        '\n\n'
                        ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                return FINAL


            if (nuevouser) == 1:
                emails = buscaruseremails()
                useremail = emails[len(emails) - 1]
                if idioma == "English":
                    reply_keyboard = [['Change'], ['OK']]
                    context.bot.send_message(chat_id, text='Thank you!')
                    context.bot.send_message(chat_id,
                                             text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                 challengename, amount, duedate, judge, judgeemail, useremail),
                                             parse_mode="Markdown",
                                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    update.message.reply_text(
                        '\n\n'
                        ' If there is any mistake, press the change button. Otherwise press Ok button.',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                elif idioma == "Español":
                    reply_keyboard = [['Cambiar'], ['OK']]
                    context.bot.send_message(chat_id, text='Gracias!!')
                    context.bot.send_message(chat_id,
                                             text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                                 challengename, amount, duedate, judge, judgeemail, useremail),
                                             parse_mode="Markdown",
                                             reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
                    update.message.reply_text(
                        '\n\n'
                        ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

                return FINAL

            else:
                reply_keyboard = [['2020'], ['2021'], ['2022'], ['2023']]

                if idioma == "English":
                    update.message.reply_text(
                        '\n\n'
                        'Select the year',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                elif idioma == "Español":
                    update.message.reply_text(
                        '\n\n'
                        'Selecciona el año',
                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                return DUEDATE1


def usermail(update, context):
    global amount, challengename, duedate, chat_id, useremail, judgeemail, judge, vfinal
    vfinal =1
    print(vfinal)
    print("He llegado")
    chat_id = str(update.effective_chat.id)
    text = update.message.text
    useremail=text
    if ("@" in text) and ("." in text):
        print("He llegado")
        a=1
    else:
        print("He llegado")
        a=0
    print(a)
    if a==0:
        if idioma=="English":
            context.bot.send_message(chat_id, text='Sorry, this format is not accepted. ',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            update.message.reply_text('Please, verify that you have sent a valid email and resend it to me.',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
        elif idioma=="Español":
            context.bot.send_message(chat_id, text='Lo siento, este formato no se acepta. ',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            update.message.reply_text('Por favor, verifica que el correo está bien y reenviamelo.',
                                      reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

        return USERMAIL
    else:
        print("1234556")
        record = {'User email': text}
        airtable.update_by_field('Code', code, record)
        airtable1.update_by_field('User ID',chat_id,record )
        if idioma == "English":
            reply_keyboard = [['Change'], ['OK']]
            context.bot.send_message(chat_id, text='Thank you!')
            context.bot.send_message(chat_id,
                                     text='You have created this challenge \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                         challengename, amount, duedate, judge, judgeemail, useremail),
                                     parse_mode="Markdown",
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            update.message.reply_text(
                '\n\n'
                ' If there is any mistake, press the change button. Otherwise press Ok button.',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma == "Español":
            reply_keyboard = [['Cambiar'], ['OK']]
            context.bot.send_message(chat_id, text='Gracias!!')
            context.bot.send_message(chat_id,
                                     text='Has creado el siguiente reto: \n\n  *Name 🔖 :* {}  \n *Amount 💸 :* {} \n *DueDate 📅 :* {} \n *Judge 👨🏽‍⚖️:* {} \n  *JudgeEmail 📩 :* {}  \n *UserEmail 👤 :* {}  \n  Has been created'.format(
                                         challengename, amount, duedate, judge, judgeemail, useremail),
                                     parse_mode="Markdown",
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            update.message.reply_text(
                '\n\n'
                ' Si hay algún error presiona el botón de cambiar. Si todo está bien presiona Ok.',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return FINAL


def final(update, context):
    global chat_id, vfinal, change
    query = update.message.text
    print(query)
    if query == "Change" or query=="Cambiar":
        vfinal=1
        change=1
        if idioma=="English":
            keyboard = [[InlineKeyboardButton("Name", callback_data='Name'),
                         InlineKeyboardButton("Judge", callback_data='Judgename'),
                         InlineKeyboardButton("Judge Email", callback_data='JudgeEmail')],
                        [InlineKeyboardButton("Amount", callback_data='Amount'),
                         InlineKeyboardButton("DueDate", callback_data='Duedate'),
                         InlineKeyboardButton("User Email", callback_data='UserEmail')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                'Press the item you want to change before finish creating the challenge',
                reply_markup=reply_markup)
        elif idioma=="Español":
            keyboard = [[InlineKeyboardButton("Nombre", callback_data='Name'),
                         InlineKeyboardButton("Juez", callback_data='Judgename'),
                         InlineKeyboardButton("Email juez", callback_data='JudgeEmail')],
                        [InlineKeyboardButton("Cantidad", callback_data='Amount'),
                         InlineKeyboardButton("Fecha", callback_data='Duedate'),
                         InlineKeyboardButton("Email usuario", callback_data='UserEmail')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                'Presiona el elemento que quieras modificar antes de terminar de crear el reto',
                reply_markup=reply_markup)
        return FINAL1
    elif query == "OK":
        change=0
        vfinal=0
        if idioma=="English":
            context.bot.send_message(chat_id, text='Thank you for you confidence in us. We are sure that you are going to perform your challenge.',reply_markup = ReplyKeyboardRemove(
            remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Create", callback_data='Create'),
                         InlineKeyboardButton("Judge", callback_data='Judge'),
                         InlineKeyboardButton("My Challenges", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                'The following MENU will be useful if you want to create a new challenge, judge or review your existing challenges in the future. \n Looking forward to hearing from you. ',
                reply_markup=reply_markup)
        elif idioma=="Español":
            context.bot.send_message(chat_id,
                                     text='Gracias por tu confianza en nosotros. Estamos seguros de que conseguirá el reto 💪.',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Crear", callback_data='Create'),
                         InlineKeyboardButton("Juzgar", callback_data='Judge'),
                         InlineKeyboardButton("Mis Retos", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, text=
            'El siguiente Menu te será de ayuda para cuando quieras Crear, Juzgar o Revisar tus retos. \n Esperamos verte pronto por aquí',
                                     reply_markup=reply_markup)
        return FINAL1
    else:
        if idioma=="English":
            reply_keyboard = [['Change'], ['OK']]
            update.message.reply_text(
                '\n\n'
                'Sorry you have to select the OK button or send it manually before starting again. Otherwise if you have made a mistake press change button',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            reply_keyboard = [['Cambiar'], ['OK']]
            update.message.reply_text(
                '\n\n'
                'Lo siento, tienes que pulsar el boton de Ok, o enviar ok manualmente. Si lo que quieres es cambiar algo del reto, presiona el botón de cambiar',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return FINAL1

def final1(update, context):
    global vfinal, change
    vfinal = 0
    query = update.message.text
    print(query)
    if query == "Change" or query=="Cambiar":
        vfinal=1
        change=1
        if idioma == "English":
            keyboard = [[InlineKeyboardButton("Name", callback_data='Name'),
                         InlineKeyboardButton("Judge", callback_data='Judgename'),
                         InlineKeyboardButton("Judge Email", callback_data='JudgeEmail')],
                        [InlineKeyboardButton("Amount", callback_data='Amount'),
                         InlineKeyboardButton("DueDate", callback_data='Duedate'),
                         InlineKeyboardButton("User Email", callback_data='UserEmail')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                'Press the item you want to change before finish creating the challenge',
                reply_markup=reply_markup)
        elif idioma == "Español":
            keyboard = [[InlineKeyboardButton("Nombre", callback_data='Name'),
                         InlineKeyboardButton("Juez", callback_data='Judgename'),
                         InlineKeyboardButton("Email juez", callback_data='JudgeEmail')],
                        [InlineKeyboardButton("Cantidad", callback_data='Amount'),
                         InlineKeyboardButton("Fecha", callback_data='Duedate'),
                         InlineKeyboardButton("Email usuario", callback_data='UserEmail')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                'Presiona el elemento que quieras modificar antes de terminar de crear el reto',
                reply_markup=reply_markup)
        return FINAL1
    elif query == "OK":
        change=0
        vfinal=0
        completo==1
        if idioma=="English":
            context.bot.send_message(chat_id, text='Thank you for you confidence in us. We are sure that you are going to perform your challenge.',reply_markup = ReplyKeyboardRemove(
            remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Create", callback_data='Create'),
                         InlineKeyboardButton("Judge", callback_data='Judge'),
                         InlineKeyboardButton("My Challenges", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                'The following MENU will be useful if you want to create a new challenge, judge or review your existing challenges in the future. \n Looking forward to hearing from you. ',
                reply_markup=reply_markup)
        elif idioma=="Español":
            context.bot.send_message(chat_id,
                                     text='Gracias por tu confianza en nosotros. Estamos seguros de que conseguirá el reto 💪.',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Crear", callback_data='Create'),
                         InlineKeyboardButton("Juzgar", callback_data='Judge'),
                         InlineKeyboardButton("Mis Retos", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, text=
            'El siguiente Menu te será de ayuda para cuando quieras Crear, Juzgar o Revisar tus retos. \n Esperamos verte pronto por aquí',
                                     reply_markup=reply_markup)
        return FINAL1
    else:
        if idioma=="English":
            reply_keyboard = [['Change'], ['OK']]
            update.message.reply_text(
                '\n\n'
                'Sorry you have to select the OK button or send it manually before starting again. Otherwise if you have made a mistake press change button',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            reply_keyboard = [['Cambiar'], ['OK']]
            update.message.reply_text(
                '\n\n'
                'Lo siento, tienes que pulsar el boton de Ok, o enviar ok manualmente. Si lo que quieres es cambiar algo del reto, presiona el botón de cambiar',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return FINAL1
#FIN DE ITINERARIO CREAR RETO

#ESTADOESPERA

#ITINERARIO JUZGAR RETO
def judge(update, context):
    global code1,chat_id
    text= update.message.text
    code1 = text
    vector=buscarcode2()
    if code1 in vector:
        juzgado = buscarstatus1(code1)
    else:
        juzgado=1
    chat_id = str(chat_id)
    verify = airtable2.search('Code', code1)
    if (verify != []) and juzgado=="NA":
        record = {'JudgeID': chat_id}
        airtable3.update_by_field('Code',code1,record)
        if idioma=="English":
            reply_keyboard = [['Achieve'],['Not Achieve']]
            update.message.reply_text(
                '\n\n'
                'Did the user reach his/her goal?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            reply_keyboard = [['Conseguido'],['No Conseguido']]
            update.message.reply_text(
                '\n\n'
                '¿Ha conseguido el reto?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return JUDGE1
    else:
        if idioma=="English":
            context.bot.send_message(chat_id, text='Incorrect code',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            update.message.reply_text('Please, verify the code and resend it me. Otherwise,use the Menu above if you wanna change what to do.',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
        elif idioma=="Español":
            context.bot.send_message(chat_id, text='Código incorrecto',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            update.message.reply_text(
                'Por favor, verifica el código que has recibido y envíamelo de nuevo. Si quieres cambiar lo que hacer utiliza el primer Menu.',
                reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

        return JUDGE

def judge1(update, context):
    global code1, result,chat_id, completo
    print ("afaa")
    text= update.message.text
    if (text=="Achieve" or text=="achieve" or text=="Not Achieve" or text=="not achieve" or text=="Not achieve" or text=="Conseguido" or text=="No Conseguido"):
        completo=1
        print(text)
        chat_id = str(update.effective_chat.id)

        result = text
        record = {'Challenge status': text}
        record2 = {'Status': text}
        airtable.update_by_field('Code', code1, record)
        airtable2.update_by_field('Code',code1, record2)
        if idioma=="English":
            update.message.reply_text('Thank you for your help',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            context.bot.send_message(chat_id,text='The challenge with code: {} \n Result: {} \n Has been suscessfully judged'.format(code1, result,reply_markup = ReplyKeyboardRemove(remove_keyboard=True)))


            keyboard = [[InlineKeyboardButton("Create", callback_data='Create'),
                         InlineKeyboardButton("Judge", callback_data='Judge'),
                         InlineKeyboardButton("My Challenges", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                'The following MENU will be useful if you want to create a new challenge, judge or review your existing challenges in the future. \n Looking forward to hearing from you. ',
                reply_markup=reply_markup)
        elif idioma=="Español":
            update.message.reply_text('Gracias por tu ayuda', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            context.bot.send_message(chat_id,
                                     text='El reto con código: {} \n *Resultado 🏁:* {} \n Ha sido juzgado con éxito'.format(
                                         code1, result), parse_mode="Markdown", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

            keyboard = [[InlineKeyboardButton("Crear", callback_data='Create'),
                         InlineKeyboardButton("Juzgar", callback_data='Judge'),
                         InlineKeyboardButton("Mis Retos", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                'El siguiente Menu te será de ayuda para cuando quieras Crear, Juzgar o Revisar tus retos. \n Esperamos verte pronto por aquí',
                reply_markup=reply_markup)
        return FINAL1
    else:
        if idioma=="English":
            reply_keyboard = [['Achieve'],['Not Achieve']]
            update.message.reply_text(
                '\n\n'
                'Please select the result of the challenge from the options below.',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        elif idioma=="Español":
            reply_keyboard = [['Conseguido'],['No Conseguido']]
            update.message.reply_text(
                '\n\n'
                'Selecciona el resultado del reto',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return JUDGE1

#FIN DE ITINERARIO JUZGAR RETO


#ITINERARIO VER MI RETO

def review(update, context):
    global completo
    global challengenameR, amountR, duedateR, judgeR, judgeemailR, useremailR, statusR
    global challengenameR1, amountR1, duedateR1, judgeR1, judgeemailR1, useremailR1, statusR1
    global challengenameR2, amountR2, duedateR2, judgeR2, judgeemailR2, useremailR2, statusR2
    global challengenameR3, amountR3, duedateR3, judgeR3, judgeemailR3, useremailR3, statusR3
    global challengenameR4, amountR4, duedateR4, judgeR4, judgeemailR4, useremailR4, statusR4
    global challengenameR5, amountR5, duedateR5, judgeR5, judgeemailR5, useremailR5, statusR5
    global challengenameR6, amountR6, duedateR6, judgeR6, judgeemailR6, useremailR6, statusR6
    completo=1
    query = update.callback_query.data
    print(query)
    vectorchallenge=["Challenge1","Challenge2","Challenge3","Challenge4","Challenge5","Challenge6","Challenge7","Challenge8","Challenge9","Challenge10","Challenge11","Challenge12"]
    if query in vectorchallenge:
        challengenames = buscarchallenges()
        challengeamounts = buscaramounts()
        challengeduedates = buscarduedates()
        challengejudges = buscarjueces1()
        challengejudgemails = buscarjuecesmail1()
        challengeuseremails = buscaruseremails()
        challengestatus = buscarstatus()
    else:
        if query == "Create" or query == "create":
            record = {'Challenger or not': 'Yes'}
            record2 = {'Code': code}
            airtable.update_by_field('Code', code, record)
            airtable2.update_by_field('Code', code, record2)
            name = update.effective_chat.first_name
            if idioma=="English":
                context.bot.send_message(chat_id, text='Great {}. Lets do it!'.format(name))
                context.bot.send_message(chat_id,
                                         text='How do you want to name the challenge?. Use the Menu above if you wanna change what to do.',
                                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif idioma=="Español":
                context.bot.send_message(chat_id, text='Perfecto {}. Vamos a ello!'.format(name))
                context.bot.send_message(chat_id,
                                         text='¿Cómo quieres llamar al reto?. Usa el Menu de arriba si quieres cambiar lo que hacer.',
                                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

            return CHALLENGENAME
        elif query == "Judge" or query == "judge":
            record = {'Challenger or not': 'No'}
            airtable.update_by_field('Code', code, record)
            user = update.message.from_user
            logger.info("%s want to: %s", user.first_name, update.message.text)
            if idioma=="English":
                context.bot.send_message(chat_id,
                                     text='I see! Please, send the code of the challenge that you want to judge. Use the Menu above if you wanna change what to do',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            elif idioma=="Español":
                context.bot.send_message(chat_id,
                                     text='Por favor envíame el código del reto que quieres juzgar. Usa el Menu de arriba si quieres cambiar lo que hacer',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

            return JUDGE
        elif query == "My challenges" or query == "my challenges":
            challenge = buscarchallenges()
            numchallenge = len(challenge)
            print(numchallenge)
            record = {'Challenger or not': 'No'}
            airtable.update_by_field('Code', code, record)
            if numchallenge == 1:
                challengename1 = challenge[numchallenge]
                keyboard = [InlineKeyboardButton(challengename1, callback_data='Challenge1')]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if idioma=="English":
                    context.bot.send_message(chat_id, text=
                    'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup)
                elif idioma=="Español":
                    context.bot.send_message(chat_id, text=
                    'Tienes el siguiente reto. Presiona sobre el nombre para ver las características del reto y su estado. Si quieres cambiar lo que hacer utiliza el Menu anterior',
                                         reply_markup=reply_markup)
                return REVIEW
            elif numchallenge == 2:
                challengename1 = challenge[numchallenge - 1]
                challengename2 = challenge[numchallenge - 2]
                keyboard = [InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                            InlineKeyboardButton(challengename2, callback_data='Challenge2')]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if idioma=="English":
                    context.bot.send_message(chat_id, text=
                    'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup)
                elif idioma=="Español":
                    context.bot.send_message(chat_id, text=
                    'Tienes los siguientes retos. Presiona sobre el nombre para ver las características del reto y su estado. Si quieres cambiar lo que hacer utiliza el Menu anterior',
                                         reply_markup=reply_markup)
                return REVIEW
            elif numchallenge == 3:
                challengename1 = challenge[numchallenge - 1]
                challengename2 = challenge[numchallenge - 2]
                challengename3 = challenge[numchallenge - 3]
                keyboard = [InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                            InlineKeyboardButton(challengename2, callback_data='Challenge2'),
                            InlineKeyboardButton(challengename3, callback_data='Challenge3')]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if idioma=="English":
                    context.bot.send_message(chat_id, text=
                    'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup)
                elif idioma=="Español":
                    context.bot.send_message(chat_id, text=
                    'Tienes los siguientes retos. Presiona sobre el nombre para ver las características del reto y su estado. Si quieres cambiar lo que hacer utiliza el Menu anterior',
                                         reply_markup=reply_markup)
                return REVIEW
            elif numchallenge == 4:
                challengename1 = challenge[numchallenge - 1]
                challengename2 = challenge[numchallenge - 2]
                challengename3 = challenge[numchallenge - 3]
                challengename4 = challenge[numchallenge - 4]
                keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                             InlineKeyboardButton(challengename2, callback_data='Challenge2')],
                            [InlineKeyboardButton(challengename3, callback_data='Challenge3'),
                             InlineKeyboardButton(challengename4, callback_data='Challenge4')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if idioma=="English":
                    context.bot.send_message(chat_id, text=
                    'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup)
                elif idioma=="Español":
                    context.bot.send_message(chat_id, text=
                    'Tienes los siguientes retos. Presiona sobre el nombre para ver las características del reto y su estado. Si quieres cambiar lo que hacer utiliza el Menu anterior',
                                         reply_markup=reply_markup)
                return REVIEW
            elif numchallenge == 4:
                challengename1 = challenge[numchallenge - 1]
                challengename2 = challenge[numchallenge - 2]
                challengename3 = challenge[numchallenge - 3]
                challengename4 = challenge[numchallenge - 4]
                keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                             InlineKeyboardButton(challengename2, callback_data='Challenge2')],
                            [InlineKeyboardButton(challengename3, callback_data='Challenge3'),
                             InlineKeyboardButton(challengename4, callback_data='Challenge4')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if idioma=="English":
                    context.bot.send_message(chat_id, text=
                    'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup)
                elif idioma=="Español":
                    context.bot.send_message(chat_id, text=
                    'Tienes los siguientes retos. Presiona sobre el nombre para ver las características del reto y su estado. Si quieres cambiar lo que hacer utiliza el Menu anterior',
                                         reply_markup=reply_markup)
                return REVIEW
            elif numchallenge == 5:
                challengename1 = challenge[numchallenge - 1]
                challengename2 = challenge[numchallenge - 2]
                challengename3 = challenge[numchallenge - 3]
                challengename4 = challenge[numchallenge - 4]
                challengename5 = challenge[numchallenge - 5]
                keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                             InlineKeyboardButton(challengename2, callback_data='Challenge2'),
                             InlineKeyboardButton(challengename3, callback_data='Challenge3')],
                            [InlineKeyboardButton(challengename4, callback_data='Challenge4'),
                             InlineKeyboardButton(challengename5, callback_data='Challenge5')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if idioma=="English":
                    context.bot.send_message(chat_id, text=
                    'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup)
                elif idioma=="Español":
                    context.bot.send_message(chat_id, text=
                    'Tienes los siguientes retos. Presiona sobre el nombre para ver las características del reto y su estado. Si quieres cambiar lo que hacer utiliza el Menu anterior',
                                         reply_markup=reply_markup)
                return REVIEW
            elif numchallenge >= 6:
                challengename1 = challenge[numchallenge - 1]
                challengename2 = challenge[numchallenge - 2]
                challengename3 = challenge[numchallenge - 3]
                challengename4 = challenge[numchallenge - 4]
                challengename5 = challenge[numchallenge - 5]
                challengename6 = challenge[numchallenge - 6]
                keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                             InlineKeyboardButton(challengename2, callback_data='Challenge2')],
                            [InlineKeyboardButton(challengename3, callback_data='Challenge3'),
                             InlineKeyboardButton(challengename4, callback_data='Challenge4')],
                            [InlineKeyboardButton(challengename5, callback_data='Challenge5'),
                             InlineKeyboardButton(challengename6, callback_data='Challenge6')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if idioma=="English":
                    context.bot.send_message(chat_id, text=
                    'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                         reply_markup=reply_markup)
                elif idioma=="Español":
                    context.bot.send_message(chat_id, text=
                    'Tienes los siguientes retos. Presiona sobre el nombre para ver las características del reto y su estado. Si quieres cambiar lo que hacer utiliza el Menu anterior',
                                         reply_markup=reply_markup)
                return REVIEW

    if query == "Challenge1":
        if idioma=="English":
            context.bot.send_message(chat_id,
                                     text='*STATE OF THE CHALLENGE:*\n\n*Name 🔖 :* {}  \n*Amount 💸 :* {} \n*DueDate 📅 :* {} \n*Judge 👨🏽‍⚖️:* {} \n*JudgeEmail 📩 :* {}  \n*Status 🏁:* {} '.format(
                                         challengenames[numerochallenges-1], challengeamounts[numerochallenges-1], challengeduedates[numerochallenges-1], challengejudges[numerochallenges-1], challengejudgemails[numerochallenges-1],
                                         challengestatus[numerochallenges-1])
                                     ,parse_mode='Markdown',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            context.bot.send_message(chat_id, text='Thank you for you confidence in us. We are sure that you are going to perform your challenge.',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Create", callback_data='Create'),
                         InlineKeyboardButton("Judge", callback_data='Judge'),
                         InlineKeyboardButton("My challenges", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, text=
                'The following MENU will be useful if you want to create a new challenge, judge or review your existing challenges in the future. \n Looking forward to hearing from you. ',
                reply_markup=reply_markup)
            return FINAL1
        elif idioma=="Español":
            context.bot.send_message(chat_id,
                                     text='*ESTADO DEL RETO:*\n\n*Nombre 🔖 :* {}  \n*Cantidad 💸 :* {} \n*Fecha 📅 :* {} \n*Juez 👨🏽‍⚖️:* {} \n*Email Juez 📩 :* {}  \n*Estado 🏁:* {} '.format(
                                         challengenames[numerochallenges - 1], challengeamounts[numerochallenges - 1],
                                         challengeduedates[numerochallenges - 1], challengejudges[numerochallenges - 1],
                                         challengejudgemails[numerochallenges - 1],
                                         challengestatus[numerochallenges - 1])
                                     , parse_mode='Markdown', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            context.bot.send_message(chat_id,
                                     text='Gracias por tu confianza en nosotros. Estamos seguros de que conseguirá el reto 💪.',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Crear", callback_data='Create'),
                         InlineKeyboardButton("Juzgar", callback_data='Judge'),
                         InlineKeyboardButton("Mis Retos", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, text=
            'El siguiente Menu te será de ayuda para cuando quieras Crear, Juzgar o Revisar tus retos. \n Esperamos verte pronto por aquí',
                                     reply_markup=reply_markup)
        return FINAL1
    elif query == "Challenge2":
        if idioma == "English":
            context.bot.send_message(chat_id,
                                     text='*STATE OF THE CHALLENGE:*\n\n*Name 🔖 :* {}  \n*Amount 💸 :* {} \n*DueDate 📅 :* {} \n*Judge 👨🏽‍⚖️:* {} \n*JudgeEmail 📩 :* {}  \n*Status 🏁:* {} '.format(
                                         challengenames[numerochallenges - 2], challengeamounts[numerochallenges - 2],
                                         challengeduedates[numerochallenges - 2], challengejudges[numerochallenges - 2],
                                         challengejudgemails[numerochallenges - 2],
                                         challengestatus[numerochallenges - 2])
                                     , parse_mode='Markdown', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            context.bot.send_message(chat_id,
                                     text='Thank you for you confidence in us. We are sure that you are going to perform your challenge.',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Create", callback_data='Create'),
                         InlineKeyboardButton("Judge", callback_data='Judge'),
                         InlineKeyboardButton("My challenges", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, text=
            'The following MENU will be useful if you want to create a new challenge, judge or review your existing challenges in the future. \n Looking forward to hearing from you. ',
                                     reply_markup=reply_markup)
            return FINAL1
        elif idioma == "Español":
            context.bot.send_message(chat_id,
                                     text='*ESTADO DEL RETO:*\n\n*Nombre 🔖 :* {}  \n*Cantidad 💸 :* {} \n*Fecha 📅 :* {} \n*Juez 👨🏽‍⚖️:* {} \n*Email Juez 📩 :* {}  \n*Estado 🏁:* {} '.format(
                                         challengenames[numerochallenges - 2], challengeamounts[numerochallenges - 2],
                                         challengeduedates[numerochallenges - 2], challengejudges[numerochallenges - 2],
                                         challengejudgemails[numerochallenges - 2],
                                         challengestatus[numerochallenges - 2])
                                     , parse_mode='Markdown', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            context.bot.send_message(chat_id,
                                     text='Gracias por tu confianza en nosotros. Estamos seguros de que conseguirá el reto 💪.',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Crear", callback_data='Create'),
                         InlineKeyboardButton("Juzgar", callback_data='Judge'),
                         InlineKeyboardButton("Mis Retos", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, text=
            'El siguiente Menu te será de ayuda para cuando quieras Crear, Juzgar o Revisar tus retos. \n Esperamos verte pronto por aquí',
                                     reply_markup=reply_markup)
        return FINAL1
    elif query == "Challenge3":
        if idioma == "English":
            context.bot.send_message(chat_id,
                                     text='*STATE OF THE CHALLENGE:*\n\n*Name 🔖 :* {}  \n*Amount 💸 :* {} \n*DueDate 📅 :* {} \n*Judge 👨🏽‍⚖️:* {} \n*JudgeEmail 📩 :* {}  \n*Status 🏁:* {} '.format(
                                         challengenames[numerochallenges - 2], challengeamounts[numerochallenges - 2],
                                         challengeduedates[numerochallenges - 2], challengejudges[numerochallenges - 2],
                                         challengejudgemails[numerochallenges - 2],
                                         challengestatus[numerochallenges - 2])
                                     , parse_mode='Markdown', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            context.bot.send_message(chat_id,
                                     text='Thank you for you confidence in us. We are sure that you are going to perform your challenge.',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Create", callback_data='Create'),
                         InlineKeyboardButton("Judge", callback_data='Judge'),
                         InlineKeyboardButton("My challenges", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, text=
            'The following MENU will be useful if you want to create a new challenge, judge or review your existing challenges in the future. \n Looking forward to hearing from you. ',
                                     reply_markup=reply_markup)
            return FINAL1
        elif idioma == "Español":
            context.bot.send_message(chat_id,text='*ESTADO DEL RETO:*\n\n*Nombre 🔖 :* {}  \n*Cantidad 💸 :* {} \n*Fecha 📅 :* {} \n*Juez 👨🏽‍⚖️:* {} \n*Email Juez 📩 :* {}  \n*Estado 🏁:* {} '.format(
                                         challengenames[numerochallenges - 3], challengeamounts[numerochallenges - 3],
                                         challengeduedates[numerochallenges - 3], challengejudges[numerochallenges - 3],
                                         challengejudgemails[numerochallenges - 3],
                                         challengestatus[numerochallenges - 3])
                                     ,parse_mode='Markdown', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            context.bot.send_message(chat_id,
                                     text='Gracias por tu confianza en nosotros. Estamos seguros de que conseguirá el reto 💪.',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Crear", callback_data='Create'),
                         InlineKeyboardButton("Juzgar", callback_data='Judge'),
                         InlineKeyboardButton("Mis Retos", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, text=
            'El siguiente Menu te será de ayuda para cuando quieras Crear, Juzgar o Revisar tus retos. \n Esperamos verte pronto por aquí',
                                     reply_markup=reply_markup)
        return FINAL1
    elif query == "Challenge4":
        if idioma=="English":
            context.bot.send_message(chat_id,
                                     text='*STATE OF THE CHALLENGE:*\n\n*Name 🔖 :* {}  \n*Amount 💸 :* {} \n*DueDate 📅 :* {} \n*Judge 👨🏽‍⚖️:* {} \n*JudgeEmail 📩 :* {}  \n*Status 🏁:* {} '.format(
                                         challengenames[numerochallenges-4], challengeamounts[numerochallenges-4], challengeduedates[numerochallenges-4], challengejudges[numerochallenges-4], challengejudgemails[numerochallenges-4],
                                         challengestatus[numerochallenges-4])
                                     ,parse_mode='Markdown',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            context.bot.send_message(chat_id, text='Thank you for you confidence in us. We are sure that you are going to perform your challenge.',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Create", callback_data='Create'),
                         InlineKeyboardButton("Judge", callback_data='Judge'),
                         InlineKeyboardButton("My challenges", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, text=
                'The following MENU will be useful if you want to create a new challenge, judge or review your existing challenges in the future. \n Looking forward to hearing from you. ',
                reply_markup=reply_markup)

            return FINAL1
        elif idioma=="Español":
            context.bot.send_message(chat_id,
                                     text='*ESTADO DEL RETO:*\n\n*Nombre 🔖 :* {}  \n*Cantidad 💸 :* {} \n*Fecha 📅 :* {} \n*Juez 👨🏽‍⚖️:* {} \n*Email Juez 📩 :* {}  \n*Estado 🏁:* {} '.format(
                                         challengenames[numerochallenges - 4], challengeamounts[numerochallenges - 4],
                                         challengeduedates[numerochallenges - 4], challengejudges[numerochallenges - 4],
                                         challengejudgemails[numerochallenges - 4],
                                         challengestatus[numerochallenges - 4])
                                     , parse_mode='Markdown', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            context.bot.send_message(chat_id,
                                     text='Gracias por tu confianza en nosotros. Estamos seguros de que conseguirá el reto 💪.',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Crear", callback_data='Create'),
                         InlineKeyboardButton("Juzgar", callback_data='Judge'),
                         InlineKeyboardButton("Mis Retos", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, text=
            'El siguiente Menu te será de ayuda para cuando quieras Crear, Juzgar o Revisar tus retos. \n Esperamos verte pronto por aquí',
                                     reply_markup=reply_markup)
        return FINAL1
    elif query == "Challenge5":
        if idioma == "English":
            context.bot.send_message(chat_id,
                                     text='*STATE OF THE CHALLENGE:*\n\n*Name 🔖 :* {}  \n*Amount 💸 :* {} \n*DueDate 📅 :* {} \n*Judge 👨🏽‍⚖️:* {} \n*JudgeEmail 📩 :* {}  \n*Status 🏁:* {} '.format(
                                         challengenames[numerochallenges - 5], challengeamounts[numerochallenges - 5],
                                         challengeduedates[numerochallenges - 5], challengejudges[numerochallenges - 5],
                                         challengejudgemails[numerochallenges - 5],
                                         challengestatus[numerochallenges - 5])
                                     , parse_mode='Markdown', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            context.bot.send_message(chat_id,
                                     text='Thank you for you confidence in us. We are sure that you are going to perform your challenge.',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Create", callback_data='Create'),
                         InlineKeyboardButton("Judge", callback_data='Judge'),
                         InlineKeyboardButton("My challenges", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, text=
            'The following MENU will be useful if you want to create a new challenge, judge or review your existing challenges in the future. \n Looking forward to hearing from you. ',
                                     reply_markup=reply_markup)
            return FINAL1
        elif idioma == "Español":
            context.bot.send_message(chat_id,
                                     text='*ESTADO DEL RETO:*\n\n*Nombre 🔖 :* {}  \n*Cantidad 💸 :* {} \n*Fecha 📅 :* {} \n*Juez 👨🏽‍⚖️:* {} \n*Email Juez 📩 :* {}  \n*Estado 🏁:* {} '.format(
                                         challengenames[numerochallenges - 5], challengeamounts[numerochallenges - 5],
                                         challengeduedates[numerochallenges - 5], challengejudges[numerochallenges - 5],
                                         challengejudgemails[numerochallenges - 5],
                                         challengestatus[numerochallenges - 5])
                                     , parse_mode='Markdown', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            context.bot.send_message(chat_id,
                                     text='Gracias por tu confianza en nosotros. Estamos seguros de que conseguirá el reto 💪.',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Crear", callback_data='Create'),
                         InlineKeyboardButton("Juzgar", callback_data='Judge'),
                         InlineKeyboardButton("Mis Retos", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, text=
            'El siguiente Menu te será de ayuda para cuando quieras Crear, Juzgar o Revisar tus retos. \n Esperamos verte pronto por aquí',
                                     reply_markup=reply_markup)
        return FINAL1
    elif query == "Challenge6":
        if idioma=="English":
            context.bot.send_message(chat_id,
                                     text='*STATE OF THE CHALLENGE:*\n\n*Name 🔖 :* {}  \n*Amount 💸 :* {} \n*DueDate 📅 :* {} \n*Judge 👨🏽‍⚖️:* {} \n*JudgeEmail 📩 :* {}  \n*Status 🏁:* {} '.format(
                                         challengenames[numerochallenges-6], challengeamounts[numerochallenges-6], challengeduedates[numerochallenges-6], challengejudges[numerochallenges-6], challengejudgemails[numerochallenges-6],
                                         challengestatus[numerochallenges-6])
                                     ,parse_mode='Markdown',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            context.bot.send_message(chat_id, text='Thank you for you confidence in us. We are sure that you are going to perform your challenge.',reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Create", callback_data='Create'),
                         InlineKeyboardButton("Judge", callback_data='Judge'),
                         InlineKeyboardButton("My challenges", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, text=
                'The following MENU will be useful if you want to create a new challenge, judge or review your existing challenges in the future. \n Looking forward to hearing from you. ',
                reply_markup=reply_markup)

            return FINAL1
        elif idioma=="Español":
            context.bot.send_message(chat_id,
                                     text='*ESTADO DEL RETO:*\n\n*Nombre 🔖 :* {}  \n*Cantidad 💸 :* {} \n*Fecha 📅 :* {} \n*Juez 👨🏽‍⚖️:* {} \n*Email Juez 📩 :* {}  \n*Estado 🏁:* {} '.format(
                                         challengenames[numerochallenges - 6], challengeamounts[numerochallenges - 6],
                                         challengeduedates[numerochallenges - 6], challengejudges[numerochallenges - 6],
                                         challengejudgemails[numerochallenges - 6],
                                         challengestatus[numerochallenges - 6])
                                     , parse_mode='Markdown', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            context.bot.send_message(chat_id,
                                     text='Gracias por tu confianza en nosotros. Estamos seguros de que conseguirá el reto 💪.',
                                     reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            keyboard = [[InlineKeyboardButton("Crear", callback_data='Create'),
                         InlineKeyboardButton("Juzgar", callback_data='Judge'),
                         InlineKeyboardButton("Mis Retos", callback_data='Review')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, text=
            'El siguiente Menu te será de ayuda para cuando quieras Crear, Juzgar o Revisar tus retos. \n Esperamos verte pronto por aquí',
                                     reply_markup=reply_markup)
        return FINAL1



def review1(update, context):
    challenge = buscarchallenges()
    numchallenge = len(challenge)
    print(numchallenge)
    record = {'Challenger or not': 'No'}
    airtable.update_by_field('Code', code, record)
    if numchallenge == 1:
        challengename1 = challenge[numchallenge]
        keyboard = [InlineKeyboardButton(challengename1, callback_data='Challenge1')]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if idioma == "English":
            context.bot.send_message(chat_id, text=
            'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                     reply_markup=reply_markup)
        elif idioma == "Español":
            context.bot.send_message(chat_id, text=
            'Tienes el siguiente reto. Presiona sobre el nombre para ver las características del reto y su estado. Si quieres cambiar lo que hacer utiliza el Menu anterior',
                                     reply_markup=reply_markup)
        return REVIEW
    elif numchallenge == 2:
        challengename1 = challenge[numchallenge - 1]
        challengename2 = challenge[numchallenge - 2]
        keyboard = [InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                    InlineKeyboardButton(challengename2, callback_data='Challenge2')]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if idioma == "English":
            context.bot.send_message(chat_id, text=
            'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                     reply_markup=reply_markup)
        elif idioma == "Español":
            context.bot.send_message(chat_id, text=
            'Tienes los siguientes retos. Presiona sobre el nombre para ver las características del reto y su estado. Si quieres cambiar lo que hacer utiliza el Menu anterior',
                                     reply_markup=reply_markup)
        return REVIEW
    elif numchallenge == 3:
        challengename1 = challenge[numchallenge - 1]
        challengename2 = challenge[numchallenge - 2]
        challengename3 = challenge[numchallenge - 3]
        keyboard = [InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                    InlineKeyboardButton(challengename2, callback_data='Challenge2'),
                    InlineKeyboardButton(challengename3, callback_data='Challenge3')]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if idioma == "English":
            context.bot.send_message(chat_id, text=
            'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                     reply_markup=reply_markup)
        elif idioma == "Español":
            context.bot.send_message(chat_id, text=
            'Tienes los siguientes retos. Presiona sobre el nombre para ver las características del reto y su estado. Si quieres cambiar lo que hacer utiliza el Menu anterior',
                                     reply_markup=reply_markup)
        return REVIEW
    elif numchallenge == 4:
        challengename1 = challenge[numchallenge - 1]
        challengename2 = challenge[numchallenge - 2]
        challengename3 = challenge[numchallenge - 3]
        challengename4 = challenge[numchallenge - 4]
        keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                     InlineKeyboardButton(challengename2, callback_data='Challenge2')],
                    [InlineKeyboardButton(challengename3, callback_data='Challenge3'),
                     InlineKeyboardButton(challengename4, callback_data='Challenge4')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if idioma == "English":
            context.bot.send_message(chat_id, text=
            'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                     reply_markup=reply_markup)
        elif idioma == "Español":
            context.bot.send_message(chat_id, text=
            'Tienes los siguientes retos. Presiona sobre el nombre para ver las características del reto y su estado. Si quieres cambiar lo que hacer utiliza el Menu anterior',
                                     reply_markup=reply_markup)
        return REVIEW
    elif numchallenge == 4:
        challengename1 = challenge[numchallenge - 1]
        challengename2 = challenge[numchallenge - 2]
        challengename3 = challenge[numchallenge - 3]
        challengename4 = challenge[numchallenge - 4]
        keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                     InlineKeyboardButton(challengename2, callback_data='Challenge2')],
                    [InlineKeyboardButton(challengename3, callback_data='Challenge3'),
                     InlineKeyboardButton(challengename4, callback_data='Challenge4')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if idioma == "English":
            context.bot.send_message(chat_id, text=
            'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                     reply_markup=reply_markup)
        elif idioma == "Español":
            context.bot.send_message(chat_id, text=
            'Tienes los siguientes retos. Presiona sobre el nombre para ver las características del reto y su estado. Si quieres cambiar lo que hacer utiliza el Menu anterior',
                                     reply_markup=reply_markup)
        return REVIEW
    elif numchallenge == 5:
        challengename1 = challenge[numchallenge - 1]
        challengename2 = challenge[numchallenge - 2]
        challengename3 = challenge[numchallenge - 3]
        challengename4 = challenge[numchallenge - 4]
        challengename5 = challenge[numchallenge - 5]
        keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                     InlineKeyboardButton(challengename2, callback_data='Challenge2'),
                     InlineKeyboardButton(challengename3, callback_data='Challenge3')],
                    [InlineKeyboardButton(challengename4, callback_data='Challenge4'),
                     InlineKeyboardButton(challengename5, callback_data='Challenge5')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if idioma == "English":
            context.bot.send_message(chat_id, text=
            'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                     reply_markup=reply_markup)
        elif idioma == "Español":
            context.bot.send_message(chat_id, text=
            'Tienes los siguientes retos. Presiona sobre el nombre para ver las características del reto y su estado. Si quieres cambiar lo que hacer utiliza el Menu anterior',
                                     reply_markup=reply_markup)
        return REVIEW
    elif numchallenge >= 6:
        challengename1 = challenge[numchallenge - 1]
        challengename2 = challenge[numchallenge - 2]
        challengename3 = challenge[numchallenge - 3]
        challengename4 = challenge[numchallenge - 4]
        challengename5 = challenge[numchallenge - 5]
        challengename6 = challenge[numchallenge - 6]
        keyboard = [[InlineKeyboardButton(challengename1, callback_data='Challenge1'),
                     InlineKeyboardButton(challengename2, callback_data='Challenge2')],
                    [InlineKeyboardButton(challengename3, callback_data='Challenge3'),
                     InlineKeyboardButton(challengename4, callback_data='Challenge4')],
                    [InlineKeyboardButton(challengename5, callback_data='Challenge5'),
                     InlineKeyboardButton(challengename6, callback_data='Challenge6')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if idioma == "English":
            context.bot.send_message(chat_id, text=
            'You have this challenges. See its description and status pressing in its name in the following MENU. Otherwise, change what you want to do using the previous MENU',
                                     reply_markup=reply_markup)
        elif idioma == "Español":
            context.bot.send_message(chat_id, text=
            'Tienes los siguientes retos. Presiona sobre el nombre para ver las características del reto y su estado. Si quieres cambiar lo que hacer utiliza el Menu anterior',
                                     reply_markup=reply_markup)
        return REVIEW



#FIN DE ITINERARIO VER MI RETO

#RELLENAR AIRTABLE
def rellenarairtable():
    record1 = {'User ID': "NA"}
    record2 = {'Challenger or not': "NA"}
    record3 =  {'Challenge name': "NA"}
    record4=  {'User name': "NA"}
    record5=  {'Judge name': "NA"}
    record6=  {'Email judge': "NA"}
    record7=  {'User email': "NA"}
    record8=  {'Due date': "NA"}
    record9=  {'Amount': "NA"}
    record10=  {'Challenge status': "NA"}
    airtable.update_by_field('Code',code, record1)
    airtable.update_by_field('Code', code, record2)
    airtable.update_by_field('Code', code, record3)
    airtable.update_by_field('Code', code, record4)
    airtable.update_by_field('Code', code, record5)
    airtable.update_by_field('Code', code, record6)
    airtable.update_by_field('Code', code, record7)
    airtable.update_by_field('Code', code, record8)
    airtable.update_by_field('Code', code, record9)
    airtable.update_by_field('Code', code, record10)
    return

def rellenarairtable1():
    record1 = {'User name': "NA"}
    record2 = {'User email': "NA"}
    airtable1.update_by_field('User ID',chat_id, record1)
    airtable1.update_by_field('User ID', chat_id, record2)
    return

def rellenarairtable2():
    record1 = {'User ID': "NA"}
    record2 = {'Name': "NA"}
    record5=  {'Judge name': "NA"}
    record6=  {'Email judge': "NA"}
    record8=  {'Due date': "NA"}
    record9=  {'Amount': "NA"}
    record10=  {'Status': "NA"}
    airtable2.update_by_field('Code',code, record1)
    airtable2.update_by_field('Code', code, record2)
    airtable2.update_by_field('Code', code, record5)
    airtable2.update_by_field('Code', code, record6)
    airtable2.update_by_field('Code', code, record8)
    airtable2.update_by_field('Code', code, record9)
    airtable2.update_by_field('Code', code, record10)
    return

def rellenarairtable3():
    record1 = {'JudgeID': "NA"}
    record2 = {'Name': "NA"}
    record6=  {'Email judge': "NA"}
    airtable3.update_by_field('Code',code, record1)
    airtable3.update_by_field('Code', code, record2)
    airtable3.update_by_field('Code', code, record6)
    return
#BUSCAR EN AIRTABLE

def buscarcode():
    excodes=airtable.get_all(view='Grid view', fields=['Code'])
    longitud=len(excodes)
    posicion=longitud-1
    x = json.dumps(excodes)
    y = json.loads(x)
    excode=int(y[posicion]["fields"]["Code"])
    return  excode

def buscarcode2():
    global numerochallenges
    chat_id1 = "'{}'".format(chat_id)
    prueba22 = airtable2.get_all(view='Grid view', fields=['Code'],
                                 formula="{{User ID}}={valor}".format(valor=chat_id1))
    numerochallenges = len(prueba22)
    x = json.dumps(prueba22)
    y = json.loads(x)
    i = 0
    while (i < (numerochallenges)):
        resultado = (y[i]["fields"]["Code"])
        if i == 0:
            vector = [resultado]
            i = i + 1
        else:
            vector.insert(i, resultado)
            i = i + 1
    return vector

def buscarjueces():
    global numerojudges
    chat_id1 = "'{}'".format(chat_id)
    prueba11 = airtable2.get_all(view='Grid view', fields=['Judge name'],
                                 formula="{{User ID}}={valor}".format(valor=chat_id1))
    numerojudges = len(prueba11)
    x = json.dumps(prueba11)
    y = json.loads(x)
    i=0
    while (i < (numerojudges-1)):
        resultado=(y[i]["fields"]["Judge name"])
        if i==0:
            vector = [resultado]
            i = i + 1
        else:
            vector.insert(i, resultado)
            i = i + 1

    res = []
    [res.append(x) for x in vector if x not in res]
    return res

def buscarjuecesmail():
    chat_id1 = "'{}'".format(chat_id)
    prueba11 = airtable2.get_all(view='Grid view', fields=['Email judge'],
                                 formula="{{User ID}}={valor}".format(valor=chat_id1))
    x = json.dumps(prueba11)
    y = json.loads(x)
    i=0
    while (i < (numerojudges-1)):
        resultado=(y[i]["fields"]["Email judge"])
        if i==0:
            vector = [resultado]
            i = i + 1
        else:
            vector.insert(i, resultado)
            i = i + 1

    res = []
    [res.append(x) for x in vector if x not in res]
    return res

def buscarchallenges():
    global  numerochallenges
    chat_id1 = "'{}'".format(chat_id)
    prueba22 = airtable2.get_all(view='Grid view', fields=['Name'],
                                 formula="{{User ID}}={valor}".format(valor=chat_id1))
    numerochallenges = len(prueba22)
    x = json.dumps(prueba22)
    y = json.loads(x)
    i=0
    while (i < (numerochallenges)):
        resultado=(y[i]["fields"]["Name"])
        if i==0:
            vector = [resultado]
            i = i + 1
        else:
            vector.insert(i, resultado)
            i = i + 1
    return vector

def buscarjueces1():
    global numerojudges
    chat_id1 = "'{}'".format(chat_id)
    prueba11 = airtable2.get_all(view='Grid view', fields=['Judge name'],
                                 formula="{{User ID}}={valor}".format(valor=chat_id1))
    numerojudges = len(prueba11)
    x = json.dumps(prueba11)
    y = json.loads(x)
    i=0
    while (i < (numerojudges)):
        resultado=(y[i]["fields"]["Judge name"])
        if i==0:
            vector = [resultado]
            i = i + 1
        else:
            vector.insert(i, resultado)
            i = i + 1
    return vector

def buscarjuecesmail1():
    chat_id1 = "'{}'".format(chat_id)
    prueba11 = airtable2.get_all(view='Grid view', fields=['Email judge'],
                                 formula="{{User ID}}={valor}".format(valor=chat_id1))
    x = json.dumps(prueba11)
    y = json.loads(x)
    i=0
    while (i < (numerojudges)):
        resultado=(y[i]["fields"]["Email judge"])
        if i==0:
            vector = [resultado]
            i = i + 1
        else:
            vector.insert(i, resultado)
            i = i + 1

    return vector

def todosjuecesemails():
    prueba11 = airtable3.get_all(view='Grid view', fields=['Email judge'])
    x = json.dumps(prueba11)
    y = json.loads(x)
    i=0
    while (i < (len(prueba11))):
        resultado=(y[i]["fields"]["Email judge"])
        if i==0:
            vector = [resultado]
            i = i + 1
        else:
            vector.insert(i, resultado)
            i = i + 1

    return vector

def buscaramounts():
    global  numerochallenges
    chat_id1 = "'{}'".format(chat_id)
    prueba22 = airtable2.get_all(view='Grid view', fields=['Amount'],
                                 formula="{{User ID}}={valor}".format(valor=chat_id1))
    numerochallenges = len(prueba22)
    x = json.dumps(prueba22)
    y = json.loads(x)
    i=0
    while (i < (numerochallenges)):
        resultado=(y[i]["fields"]["Amount"])
        if i==0:
            vector = [resultado]
            i = i + 1
        else:
            vector.insert(i, resultado)
            i = i + 1
    return vector

def buscarduedates():
    global  numerochallenges
    chat_id1 = "'{}'".format(chat_id)
    prueba22 = airtable2.get_all(view='Grid view', fields=['Due date'],
                                 formula="{{User ID}}={valor}".format(valor=chat_id1))
    print(prueba22)
    numerochallenges = len(prueba22)
    x = json.dumps(prueba22)
    y = json.loads(x)
    i=0
    while (i < (numerochallenges)):
        resultado=(y[i]["fields"]["Due date"])
        if i==0:
            vector = [resultado]
            i = i + 1
        else:
            vector.insert(i, resultado)
            i = i + 1
    return vector


def buscaruseremails():
    global  numerousers
    chat_id1 = "'{}'".format(chat_id)
    prueba22 = airtable1.get_all(view='Grid view', fields=['User email'],
                                 formula="{{User ID}}={valor}".format(valor=chat_id1))
    numerousers = len(prueba22)
    x = json.dumps(prueba22)
    y = json.loads(x)
    i=0
    while (i < (numerousers)):
        resultado=(y[i]["fields"]["User email"])
        if i==0:
            vector = [resultado]
            i = i + 1
        else:
            vector.insert(i, resultado)
            i = i + 1
    print(vector)
    return vector

def buscarstatus():
    global  numerochallenges
    chat_id1 = "'{}'".format(chat_id)
    prueba22 = airtable2.get_all(view='Grid view', fields=['Status'],
                                 formula="{{User ID}}={valor}".format(valor=chat_id1))
    numerochallenges = len(prueba22)
    x = json.dumps(prueba22)
    y = json.loads(x)
    i=0
    while (i < (numerochallenges)):
        resultado=(y[i]["fields"]["Status"])
        if i==0:
            vector = [resultado]
            i = i + 1
        else:
            vector.insert(i, resultado)
            i = i + 1
    return vector

def buscarstatus1(codigo):
    chat_id1 = "'{}'".format(codigo)
    prueba22 = airtable2.get_all(view='Grid view', fields=['Status'],
                                 formula="{{Code}}={valor}".format(valor=chat_id1))
    x = json.dumps(prueba22)
    y = json.loads(x)
    resultado = (y[0]["fields"]["Status"])
    print(resultado)
    return resultado

#FUNCIONES DE SALIDA
def cancel(update, context):
    verify = airtable.search("Code",code)
    verify2 = airtable2.search("Code", code)
    verify3= airtable3.search("Code", code)
    if verify!=[]:
        airtable.delete_by_field("Code", code)
        if verify2!=[]:
            airtable2.delete_by_field("Code", code)
            if verify3!=[]:
                 airtable3.delete_by_field("Code",code)
    if idioma=="English":
        keyboard = [[InlineKeyboardButton("Create", callback_data='Create'),
                     InlineKeyboardButton("Judge", callback_data='Judge'),
                     InlineKeyboardButton("My Challenges", callback_data='Review')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            '{}, no worries. You are in the main Menu, select the action you wanna do to start again.'.format(name),
            reply_markup=reply_markup)
    elif idioma=="Español":
        keyboard = [[InlineKeyboardButton("Crear", callback_data='Create'),
                     InlineKeyboardButton("Juzgar", callback_data='Judge'),
                     InlineKeyboardButton("Mis Retos", callback_data='Review')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            '{}, no te preocupes. Estás en el Menu principal, selecciona la acción que quieres hacer para empezar de nuevo.'.format(name),
            reply_markup=reply_markup)

    return FINAL1



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)



def main():
    while(1):
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater("1096144510:AAGl7StYAWIPdZ-WfiPRP5JUAgYWN3gPgvU", use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],

            states={

                START: [CallbackQueryHandler(start1), MessageHandler(Filters.all, start2)],

                DECISION: [CallbackQueryHandler(decision),CommandHandler('cancel', cancel),MessageHandler(Filters.all, decision1)],

                CHALLENGENAME: [CallbackQueryHandler(decision),CommandHandler('cancel', cancel),MessageHandler(Filters.all, challengename)],

                AMOUNT: [CallbackQueryHandler(decision2),MessageHandler(Filters.regex('^(5€|10€|15€|20€|25€|Other)$'), amount),CommandHandler('cancel', cancel),MessageHandler(Filters.all, amount1)],

                DATE: [CallbackQueryHandler(decision2),MessageHandler(Filters.regex('^(January|February|March|April|May|June|July|August|September|October|November|December|'
                                                    'Enero|Febrero|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre)$'), month),
                         CommandHandler('cancel', cancel),MessageHandler(Filters.all, month1)],

                DATE1: [CallbackQueryHandler(decision2),MessageHandler(Filters.regex('^(1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31)$'),day),
                        CommandHandler('cancel', cancel), MessageHandler(Filters.all, day1)],

                ADDITIONAL: [CallbackQueryHandler(decision2),MessageHandler(Filters.regex('^(Insert Quantity|Insertar Cantidad)$'), amount1),MessageHandler(Filters.regex('^(Return|Volver Atrás)$'), metercantidad),
                             CommandHandler('cancel', cancel),MessageHandler(Filters.all, amount1)],

                DUEDATE: [CallbackQueryHandler(decision2),MessageHandler(Filters.regex('^(Insert Date|Insertar Fecha)$'), date),MessageHandler(Filters.regex('^(Return|Volver Atrás)$'), meterfecha),CommandHandler('cancel', cancel),MessageHandler(Filters.all, date)],

                DUEDATE1: [CallbackQueryHandler(decision2),MessageHandler(Filters.regex('^(2020|2021|2022|2023|2024)$'), year),CommandHandler('cancel', cancel), MessageHandler(Filters.all, year1)],

                USERMAIL: [CallbackQueryHandler(decision2),CommandHandler('cancel', cancel),MessageHandler(Filters.all, usermail)],

                JUDGE: [CallbackQueryHandler(decision),CommandHandler('cancel', cancel),MessageHandler(Filters.all, judge)],

                JUDGE1: [CallbackQueryHandler(decision2),MessageHandler(Filters.regex('^(Achieve|Not Achieve|Conseguido|No Conseguido)$'), judge1),CommandHandler('cancel', cancel), MessageHandler(Filters.all, judge1)],

                JUDGENAME: [CallbackQueryHandler(decision2),CommandHandler('cancel', cancel),MessageHandler(Filters.all, judgename)],

                JUDGEMAIL: [CallbackQueryHandler(decision2),CommandHandler('cancel', cancel),MessageHandler(Filters.all, judgemail)],

                FINAL: [CallbackQueryHandler(decision2),MessageHandler(Filters.regex('^(Change|OK|Cambiar)$'),final),CommandHandler('cancel', cancel),MessageHandler(Filters.all, final1)],

                EXISTING: [CallbackQueryHandler(existingjudge),CommandHandler('cancel', cancel),MessageHandler(Filters.all, existingjudge1)],

                FINAL1: [MessageHandler(Filters.regex('^(Change|OK|Cambiar)$'), final),CommandHandler('cancel', cancel),
                         CallbackQueryHandler(decision2),MessageHandler(Filters.all, decision1)],

                REVIEW: [CallbackQueryHandler(review),CommandHandler('cancel', cancel), MessageHandler(Filters.all, review1)]

            },

            fallbacks=[CommandHandler('cancel', cancel)]
        )

        dp.add_handler(conv_handler)

        # log all errors
        dp.add_error_handler(error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
