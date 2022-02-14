#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import unicodedata
import re
import pandas as pd
import spacy
from deeppavlov import build_model
from deeppavlov import configs
from deeppavlov.core.common.file import read_json
from deeppavlov.core.commands.infer import build_model
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter, ConversationHandler
spacy.load('en_core_web_sm')
token = ''

#itauModel = build_model(configs.faq.tfidf_logreg_en_faq_Itau, download = True)
#bbModel = build_model(configs.faq.tfidf_logreg_en_faq_BB, download = True)
#bradescoModel = build_model(configs.faq.tfidf_logreg_en_faq_Bradesco, download = True)
itauModel = build_model("C:/Users/CTOSMGBit/AppData/Local/Programs/Python/Python36/Lib/site-packages/deeppavlov/configs/faq/tfidf_logreg_en_faq_Itau.json")
bbModel = build_model("C:/Users/CTOSMGBit/AppData/Local/Programs/Python/Python36/Lib/site-packages/deeppavlov/configs/faq/tfidf_logreg_en_faq_BB.json")
bradescoModel = build_model("C:/Users/CTOSMGBit/AppData/Local/Programs/Python/Python36/Lib/site-packages/deeppavlov/configs/faq/tfidf_logreg_en_faq_Bradesco.json")


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

apresentacoes = ['oi','ola','boa tarde','bom dia','tudo bem?','e ai']

BANCO, BIO, ITAU, BRADESCO, BANCOBRASIL  = range(5)


class StartFilter(BaseFilter):
    def filter(self, message):
        return 'hi' in message.text.lower() or 'hello' in message.text.lower()


def removerAcentosECaracteresEspeciais(palavra):

    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)

def start_message(update, context):
    """Send a message when the command /start is issued."""
    logger.info('start message issued by user: "%s", id: "%s"', update.effective_user.full_name,
                update.effective_user.id)
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    logger.info('/help command issued by user: "%s", id: "%s"', update.effective_user.full_name,
                update.effective_user.id)
    update.message.reply_text('Help!')


def talk(update, context):
    reply_keyboard = [['Itau', 'Banco do Brasil', 'Bradesco']]

    update.message.reply_text(
        'Ola! Seja bem vindo ao assistente brasileiro de Bancos. '
        'Digite /banco e nos informe qual o seu banco para que eu possa te ajudar. Se não quiser mais conversar comigo, é só digitar /cancel .\n\n'
        'Me diga, qual o banco que deseja tirar dúvidas?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return BANCO

def banco(update, context):
    reply_keyboard = [['Itau', 'Banco do Brasil', 'Bradesco']]

    update.message.reply_text(
        'Me diga, qual o banco que deseja tirar dúvidas? Se não quiser mais conversar comigo, é só digitar /cancelar.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return BANCO

def bancoText(update, context):
    if ('bradesco' in update.message.text.lower()):
        update.message.reply_text('Você deseja informações a respeito do Banco Bradesco! Vamos lá, me deixe te ajudar, qual seria sua dúvida? '
                              'Se quiser cancelar, é só digitar /cancelar.',
                              reply_markup=ReplyKeyboardRemove())
        return BRADESCO
    elif ('banco do brasil' in update.message.text.lower() or 'bb' in update.message.text.lower()):
        update.message.reply_text('Você deseja informações a respeito do Banco do Brasil! Vamos lá, me deixe te ajudar, qual seria sua dúvida? '
                              'Se quiser cancelar, é só digitar /cancelar.',
                              reply_markup=ReplyKeyboardRemove())
        return BANCOBRASIL
    elif ('itau' in update.message.text.lower()):
        update.message.reply_text('Você deseja informações a respeito do Banco Itau! Vamos lá, me deixe te ajudar, qual seria sua dúvida? '
                              'Se quiser cancelar, é só digitar /cancelar.',
                              reply_markup=ReplyKeyboardRemove())
        return ITAU
    elif('banco' in update.message.text.lower()):
        reply_keyboard = [['Itau', 'Banco do Brasil', 'Bradesco']]
        update.message.reply_text(
            'Me diga, qual o banco que deseja tirar dúvidas? Se não quiser mais conversar comigo, é só digitar /cancelar.',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return BANCO
    else:
        response_message = "Desculpa, acredito que você tenha digitado incorretamente, porque não tenta digitar /banco para conversarmos?"
        context.bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def bancoEscolhido(update, context):
    user = update.message.from_user
    logger.info("O Banco escolhido do %s foi: %s", user.first_name, update.message.text)
    if update.message.text == "Itau":
        update.message.reply_text('Certo, Itau! Vamos lá, me deixe te ajudar, qual seria sua dúvida? '
                              'Se quiser cancelar, é só digitar /cancelar.',
                              reply_markup=ReplyKeyboardRemove())
        return ITAU
    elif update.message.text == "Banco do Brasil":
        update.message.reply_text('Certo, Banco do Brasil! Vamos lá, me deixe te ajudar, qual seria sua dúvida? '
                              'Se quiser cancelar, é só digitar /cancelar.',
                              reply_markup=ReplyKeyboardRemove())
        return BANCOBRASIL
    else:
        update.message.reply_text('Certo, Bradesco! Vamos lá, me deixe te ajudar, qual seria sua dúvida? '
                              'Se quiser cancelar, é só digitar /cancelar.',
                              reply_markup=ReplyKeyboardRemove())
        return BRADESCO



def itau(update, context):
    user = update.message.from_user
    logger.info("Entrou no Itau do %s foi: %s", user.first_name, update.message.text)
    if update.message.text.lower() in apresentacoes:
        resposta = 'Olá, me faça alguma pergunta e vamos ver se consigo te ajudar =)'
    else:
        print(itauModel([update.message.text])[0])
        predict = (itauModel([update.message.text])[1][0][0])*100
        print(predict)
        if(predict < 0.005):
            resposta = 'Desculpe mas não conseguirei ajudar sobre esse assunto, podemos tentar outro? =)'
        else:
            resposta = str(itauModel([update.message.text])[0])
            resposta = removerAcentosECaracteresEspeciais(resposta)
    
    update.message.reply_text(resposta)
    #update.message.reply_text('Acho que não possuo resposta para isso =(')
    return ITAU

def bradesco(update, context):
    user = update.message.from_user
    logger.info("Entrou no Bradesco do %s foi: %s", user.first_name, update.message.text)
    bradescoModel([update.message.text])
    print(bradescoModel([update.message.text])[0])
    print(bradescoModel([update.message.text])[1][0])
    predict = (bradescoModel([update.message.text])[1][0][0])*100
    print(predict)
    if(predict < 0.0010):
        resposta = 'Desculpe mas não conseguirei ajudar sobre esse assunto, podemos tentar outro? =)'
    else:
        resposta = str(bradescoModel([update.message.text])[0])
        resposta = removerAcentosECaracteresEspeciais(resposta)
    
    update.message.reply_text(resposta.replace('\\',''))

    return BRADESCO

def bancobb(update, context):
    user = update.message.from_user
    logger.info("Entrou no Banco BB do %s foi: %s", user.first_name, update.message.text)

    print(bbModel([update.message.text])[0])
    predict = (bbModel([update.message.text])[1][0][0])*100
    print(predict)
    if(predict < 0.005):
        resposta = 'Desculpe mas não conseguirei ajudar sobre esse assunto, podemos tentar outro? =)'
    else:
        resposta = str(bbModel([update.message.text])[0])
        resposta = removerAcentosECaracteresEspeciais(resposta)
    
    update.message.reply_text(resposta)
    return BANCOBRASIL


def cancelText(update, context):
    user = update.message.from_user
    if('cancelar' in update.message.text.lower()):
        logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text('Obrigado pelo seu tempo, espero ter ajudado =)',
                                reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Obrigado pelo seu tempo, espero ter ajudado =)',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END




def unknown(update, context):
    logger.info('/unknown command issued by user: "%s", id: "%s"', update.effective_user.full_name,
                update.effective_user.id)
    response_message = "Desculpa, acredito que você tenha digitado incorretamente, porque não tenta digitar /banco para conversarmos?"
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )
    # update.message.reply_text(response_message)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text('Ops! Houve algum problema comigo, desculpe pelo inconveniente =(')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('start', banco))
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('banco', banco), MessageHandler(Filters.text, bancoText)],
        states={
            BANCO: [MessageHandler(Filters.regex('^(Itau|Banco do Brasil|Bradesco)$'), bancoEscolhido)],

            ITAU: [MessageHandler(Filters.text, itau)],

            BANCOBRASIL: [MessageHandler(Filters.text, bancobb)],

            BRADESCO: [MessageHandler(Filters.text, bradesco)],
        },

        fallbacks=[CommandHandler('cancelar', cancel), MessageHandler(Filters.text, cancelText)]
    )

    dp.add_handler(conv_handler)

    start_filter = StartFilter()

    dp.add_handler(MessageHandler(Filters.text & start_filter, start_message))

    dp.add_handler(MessageHandler(Filters.command, unknown))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    logger.info("Chatbot is running! Press CTRL + C to cancel.")
    main()
