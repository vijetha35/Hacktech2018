# Inspiration
Weaponization of healthcare and the destruction of medical facilities in conflict zones of Syria has profound impacts on lives of many. With not much internet connectivity in war zones, it is hard to contact any medical administrator as well. We have come up with the traditional SMS/MMS/Call way to solve this problem, SIREA911.

# What it does
The only thing you can truly give to anyone is information, this application exists solely for the same purpose, providing users in war zones and rural areas with life-saving information by the medium of traditional communication channels like SMS/MMS and Calls. Over 150,000 lives are lost each year due to lack of proper First Aid offered to them at the most critical time. A user can query First Aid for several emergencies like heart attack, broken legs etc and can even detect the type of injury if the description or Image is offered. Moreover, a user can snap for reporting calamities like Fires, Bombarding and Hostile Situations and all of this via simple text messages and multimedia messages.

SMS/MMS +1 (786)-420-6890 for immediate First Aid

# How we built it
We built the web app using cognitive APIs exposed by Microsoft for Custom Vision services and Language Understanding as well as the Twilio Messaging API. We customized the state-of-the-art computer vision models offered by Microsoft for our unique use cases such as for identification of an ailment from the image or identification of fire or bombing. Language Understanding (LUIS) helped build a great conversation interface for the application, We pass user input to a LUIS instance and receive relevant, detailed information back and extract meaning from it. We derived the user intention or the ailment related to the user's query based on the symptoms/description of the query for providing him with the relevant First Aid. We also made use of Twilio Messaging and Voice API to make it easy to send and receive texts, MMS messages and call, which particularly helps people with no internet service, to be able to get immediate assistance and all the life-saving information in their hands within minutes

# Challenges we ran into
One of the technical challenges we ran into was to debug integration between Twilio api and web server responses for Azure. Developers from Microsoft made our life easy by introducing us to the wonderful log streams for the Azure applications. Another area of difficulty was to gather training and validation data set to train LUIS (Language Understanding api) model as well as Custom Vision API to identify main ailment (intent) from user's description about the symptoms they are seeking first aid. After multiple iterations, we could achieve reasonable precision scores.

# What we learned
Working on new cognitive search API's - Custom Vision and LUIS, Azure Cloud platform (reading the server logs especially :P ) and mobile Platform - Twilio. I think one of the most important parts we could learn and achieve was the maximization of results with teamwork. Making and breaking of the application over Azure version control.

# What's next for SIREA911
We would enhance current theme by adding support for responses in different foreign languages by utilizing Cognitive Translation API's to reply user's queries in their native language for maximization of life support. Also, we intend to add a feature called SOS which will jointly alert groups of people in a particular area for any immediate emergencies and attacks.
