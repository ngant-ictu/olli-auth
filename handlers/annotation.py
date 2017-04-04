#!/usr/bin/python
# coding: utf-8

from handlers.web_base import WebHandler
from libs.decorators import web_user_required
from models.intent_speech import IntentSpeech
from models.intent_music_play_slot import IntentMusicPlaySlot
import json
import pprint
from google.appengine.api import users

class Debug(pprint.PrettyPrinter):
    """
        Simple print UTF8 character to debug
    """
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

class ListHandler(WebHandler):
    """
        Speech record list
    """
    @web_user_required
    def get(self):
        template_args = {}
        output = []

        # get all speech record
        speechQuery = IntentSpeech.query().order(-IntentSpeech.datecreated)
        mySpeechs = speechQuery.fetch()

        if len(mySpeechs) > 0:
            for speech in mySpeechs:
                output.append(generateHighlightSlot(speech))

            # Debug().pprint(output)

            template_args['mySpeechs'] = output
        else:
            template_args['mySpeechs'] = []

        template_args['logout_url'] = users.create_logout_url(self.request.path)

        return self.render_template('annotation/list.html', **template_args)

class SlotCreateHandler(WebHandler):
    """
        Create Slot
    """
    @web_user_required
    def post(self):
        speechId = int(self.request.get('fspeechid'))
        speechText = self.request.get('fspeechorigin')
        selectedText = self.request.get('fselectedtext').strip()
        slotType = self.request.get('fslottype')
        hlTimestamp = int(self.request.get('fhltimestamp'))

        # get position start / end of selected text in speech
        mySpeechArr = speechText.split(' ')
        mySelected = selectedText.split(' ')
        startWord = mySpeechArr.index(mySelected[0])
        endWord = mySpeechArr.index(mySelected[-1])

        # write to datastore
        myIntentMusicPlaySlot = IntentMusicPlaySlot(
            speech_id = speechId,
            start = startWord,
            end = endWord,
            content = selectedText,
            type = slotType.upper(),
            hltimestamp = hlTimestamp
        )

        try:
            myIntentMusicPlaySlot.put()
        except Exception as e:
            raise e

        output = {
            'success': True,
            'msg': 'Create slot success',
            'id': myIntentMusicPlaySlot.key.id()
        }

        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        return self.response.out.write(json.dumps(output))

class SlotDeleteHandler(WebHandler):
    """
        Delete Slot
    """
    @web_user_required
    def post(self):
        slotId = int(self.request.get('fid'))
        mySlot = IntentMusicPlaySlot.get_by_id(slotId)

        if mySlot:
            try:
                mySlot.key.delete()
            except Exception as e:
                raise e

        output = {
            'success': True,
            'msg': 'Delete slot success',
            'text': mySlot.content.encode('utf8')
        }

        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        return self.response.out.write(json.dumps(output))

class SpeechResetHandler(WebHandler):
    """
        Reset speech
    """
    @web_user_required
    def post(self):
        speechId = int(self.request.get('fid'))
        mySpeech = IntentSpeech.get_by_id(speechId)

        output = {
            'success': True,
            'stringHtml': generateHighlightSlot(mySpeech)
        }

        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        return self.response.out.write(json.dumps(output))

class SpeechDeleteHandler(WebHandler):
    """
        Delete Speech
    """
    @web_user_required
    def post(self):
        speechId = int(self.request.get('fid'))
        mySpeech = IntentSpeech.get_by_id(speechId)

        if mySpeech:
            try:
                mySpeech.key.delete()
            except Exception as e:
                raise e

        output = {
            'success': True,
            'msg': 'Delete speech success'
        }

        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        return self.response.out.write(json.dumps(output))

class AnnotationSampleHandler(WebHandler):
    """
        Create sample speech record
    """
    @web_user_required
    def get(self):
        template_args = {}

        return self.render_template('annotation/create.html', **template_args);

    @web_user_required
    def post(self):
        content = self.request.get('fcontent')

        mySpeech = IntentSpeech()
        mySpeech.intent = 'PlayMusic'
        mySpeech.content = content

        mySpeech.put()

        template_args = {
            'message': content
        }

        return self.render_template('annotation/create.html', **template_args);

def generateHighlightSlot(speech):
    mySpeechOutput = {
        'id': 0,
        'content': [],
        'intent': '',
        'origin': ''
    }

    # get slot of each speech type PlayMusic
    speechId = speech.key.id()
    mySpeechArr = {v: k for v, k in enumerate(speech.content.split(' '))}
    # Debug().pprint(mySpeechArr)

    mySpeechOutput['id'] = speechId
    mySpeechOutput['intent'] = speech.intent
    mySpeechOutput['origin'] = speech.content

    slotQuery = IntentMusicPlaySlot.query().filter(IntentMusicPlaySlot.speech_id == speechId)
    mySlots = slotQuery.fetch()
    if len(mySlots) > 0:
        for slot in mySlots:
            # remove range postion of slot content in speech
            for i in range(slot.start, slot.end + 1):
                del mySpeechArr[i]

            # replace with array information of slot
            customSlot = {
                'timestamp': slot.hltimestamp,
                'text': slot.content,
                'type': slot.type,
                'id': slot.key.id()
            }

            mySpeechArr[slot.start] = customSlot

        # turn array content to html content
        htmlString = ''
        for key, word in mySpeechArr.iteritems():
            if type(word) is dict:
                htmlString += '<span class="highlighted disable-select '+ str(word['type'].lower()) +'" data-timestamp="'+ str(word['timestamp']) +'" data-id="'+ str(word['id']) +'"'
                htmlString += ' data-highlighted="true">'
                htmlString += '<button class="hover-tool" onclick="return removeHighlight('+ str(word['id']) +');">'
                htmlString += '<span>x</span>'
                htmlString += '</button>'
                htmlString += word['text'].encode('utf8')
                htmlString += '<span class="intent '+ str(word['type'].lower()) +' disable-select">'
                htmlString += '<span>'+ str(word['type']) +'</span>'
                htmlString += '</span>'
                htmlString += '</span>' + ' '
            else:
                htmlString += word.encode('utf8') + ' '

        # resolve custom speech
        mySpeechOutput['content'] = htmlString
        # Debug().pprint(mySpeechOutput)
    else:
        mySpeechOutput['content'] = speech.content.encode('utf8')

    return mySpeechOutput
