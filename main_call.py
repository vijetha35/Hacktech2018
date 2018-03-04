from flask import Flask, request
import requests
import json
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import sys
import json
from twilio.twiml.voice_response import VoiceResponse,Say


app = Flask(__name__)

# Your Account SID from twilio.com/console
account_sid = "AC1461e56cf2e8ac12cf643c44aa281fd6"
# Your Auth Token from twilio.com/console
auth_token = "1e126e8e87c7641c85649359b58f4e9c"
client = Client(account_sid, auth_token)


@app.route("/getMessage", methods=['GET', 'POST'])
def getMessage():
    """Respond to incoming messages with a friendly SMS."""

    patient = request.values.get('From')
    user_message = request.values.get('Body')
    image = request.values.get('MediaContentType0')
    if image:
        image_url =  request.values.get('MediaUrl0')
        print(image_url,file=sys.stderr)
        ailment = get_image_ailment(str(image_url))
    else:
        ailment = get_text_ailment(str(user_message))

    message = client.messages.create(to=patient, from_="+18705764157", body=get_aid(ailment))


    return "Success"



def get_aid(ailment):
    with open("first-aid.json", 'r') as fileHandler:
        jsonRes = json.load(fileHandler)

        aid = jsonRes[ailment]

    return str("You most likely may be having a {} ".format(ailment)+ aid)


def get_text_ailment(text):
    """Respond to incoming symtoms by giving the ailment"""

    r = requests.get(
        'https://westus.api.cognitive.microsoft.com/'
        'luis/v2.0/apps/5eec8509-3101-406e-8176-9c3622fad58d?subscription-key=72cb6849a915419a88dacbc11b062154&verbose'
        '=true&timezoneOffset=0&q=' + text)
    ailment = r.json()['topScoringIntent']['intent']

    # Keeping the threshold at 0.5 for now can be changed later.
    #ailment = r.json()['topScoringIntent']['score']
    return str(ailment)


def get_image_ailment(image_url):
    """Respond to incoming image by giving the ailment"""

    print(image_url,file=sys.stderr)
    url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v1.1/Prediction/823232eb-9667-4534-b198-dfbda044fd38/url"
    headers = {'Content-Type': 'application/json', 'Prediction-Key': '616aa03926514184bc8f56936171708b'}
    #image_url='https://s3-external-1.amazonaws.com/media.twiliocdn.com/AC1461e56cf2e8ac12cf643c44aa281fd6/e4b22c2f9109ee2db6cbb474e861ae33'
    payload = json.dumps({'Url':str(image_url)})

    print(payload,file = sys.stderr)
    # Note : Use only Raw content for Payload
    r = requests.post(url, headers=headers, data=payload)
    print(r.json(),file = sys.stderr)
    ailment = r.json()['Predictions'][0]['Tag']
    return ailment


@app.route("/getRecordedVoice", methods=['GET', 'POST'])
def getRecordedVoice():
    transcription = request.values.get('SpeechResult')
    ailment = get_text_ailment(transcription)
    #print(ailment)
    first_aid = get_aid(ailment)
    #print(first_aid)
    response = VoiceResponse()
    response.say(first_aid,voice='man',language='en')
    message = client.messages.create(to="+12132759231", from_="+18705764157", body=first_aid)

    return str(response)#"<?xml version='1.0' encoding='UTF-8'?> <message>Success</message>"

@app.route("/status", methods=['GET', 'POST'])
def get_status():
    return 'True'


if __name__ == "__main__":
    app.run(debug=True)
