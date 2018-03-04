from flask import Flask, request
import requests
import json
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import sys
import json

app = Flask(__name__)

# Your Account SID from twilio.com/console
#account_sid = "AC1461e56cf2e8ac12cf643c44aa281fd6"
account_sid = "ACcf2f3a7354f881c369416235b6f87553" #new number

# Your Auth Token from twilio.com/console
#auth_token = "1e126e8e87c7641c85649359b58f4e9c"
auth_token = "9840792f8886bcca9abd2fa24e1c0c9e" #new number

client = Client(account_sid, auth_token)
new_number  = "+17864206890"
old_number  = "+18705764157"

@app.route("/getMessage", methods=['GET', 'POST'])
def getMessage():
    """Respond to incoming messages with a friendly SMS."""

    patient = request.values.get('From')
    user_message = request.values.get('Body')
    image = request.values.get('MediaContentType0')
    fromcity = request.values.get('FromCity') if request.values.get('FromCity') else "Unknown"
    fromzip = request.values.get('FromZip') if request.values.get('FromZip') else "Unknown"

    if image:
        image_url =  request.values.get('MediaUrl0')
        print(image_url,file=sys.stderr)
        ailment = get_image_ailment(str(image_url))
    else:
        ailment = get_text_ailment(str(user_message))

    #message = client.messages.create(to=patient, from_=old_number, body=get_aid(ailment)) # Old Call
    #message = client.messages.create(to=patient, from_=new_number, body=get_aid(ailment))

    emergency_contact = "+12132699074"
    if ailment == 'Hostiles':
        message = client.messages.create(to=emergency_contact, from_=new_number,
                                         body="Hostiles spotted in {0} at pincode {1} \n reported by {2}".format(fromcity,fromzip,patient))
        message = client.messages.create(to=patient, from_=new_number, body="Police Authorities of nearby location have been alerted, get cover and try moving to a safe location")
    elif ailment =='Fire':
        message = client.messages.create(to=emergency_contact, from_=new_number,
                                         body=" Fire/Bombarding in {0} at pincode {1} \n reported by {2}".format(fromcity, fromzip,patient))
        message = client.messages.create(to=patient, from_=new_number, body="Fire Authorities of nearby location have been alerted,\n Stay away from the fire")

    else:
        message = client.messages.create(to=patient, from_=new_number, body=get_aid(ailment))

    #message = client.messages.create(to=patient, from_=old_number, body=get_aid(ailment))


    return "<?xml version='1.0' encoding='UTF-8'?> <message>Success</message>"



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


if __name__ == "__main__":
    app.run(debug=True)
