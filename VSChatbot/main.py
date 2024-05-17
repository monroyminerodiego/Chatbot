# Author: Ashley Kelso
# This is a victims compensation chatbot designed to lead users through a series of questions to determine what
# assistance they may be entitled to and to refer them to helpful services

import os
import json
import pickle
import numpy as np

class Chatbot:
    def __init__(self):
        # Set the directory to the location of the script
        os.chdir(os.path.dirname(__file__))
        
        # Loading classifiers
        self.forest = pickle.load(open("randomForest.p", "rb"))
        self.supportV = pickle.load(open("NewSVC.p", "rb"))
        self.bayes = pickle.load(open("MultiNB.p", "rb"))
        self.state = {'previous_question': 'main menu', 'category': ''}
        with open('conversations.json', 'r', encoding='UTF-8') as file:
            self.conversations = json.load(file)
        print("Chatbot initialized")

    def respond(self, message, language='en'):
        # Handle the user's message and return the appropriate response
        response_text = self.stateManager(message, language)
        return response_text

    def response(self, key, language='en'):
        """
        Retrieve a predefined response from the chatbot based on the given key.

        Args:
            key (str): The key corresponding to a specific chatbot response.

        Returns:
            str: The response string associated with the provided key.
        """
        return self.conversations[key][language]

    def stateManager(self, user_response, language='en'):
        """
        Manage the state of the chatbot conversation based on user responses.

        Args:
            user_response (str): The response provided by the user.
            language (str): The language in which responses should be managed.

        Returns:
            str: The response string based on the updated state.
        """
        # Define options based on language
        if language == 'es':
            yes = ['sí', 'si', 'claro', 'correcto', 'ok']
            no = ['no', 'nah', 'nop', "no", "no era", 'no']
            legal = ["abogado", "asesor", "legal","servicios","1"]
            victimsComp = ["victimas", "compensacion", "compensaciones", "dinero", "financiera", "victima","2"]
            counseling = ["asesoramiento", "consejeria", "terapia", "psicologo", "psicologa","3"]
        elif language == 'mayan':
            yes = ["je'ela'", "je'el", "ma'alo'ob", "u ja", "ok"]
            no = ["ma'", "maja", "ma' in wilaj", "ma'", "ma' k'a'ba", "ma'"]
            legal = ["k'i'ik'", "asesor", "ley","1"]
            victimsComp = ["víctima", "compensación", "compensaciones", "dinero", "financiera","2"]
            counseling = ["asesoramiento", "consejería", "consejeria", "xoknáalo'ob", "terapia","3"]
        else:  # Default to English
            yes = ['yep', 'yeah', 'yes', 'yup', 'correct', "ok"]
            no = ['no', 'nah', 'nope', "didn't", "wasn't", 'not']
            legal = ["lawyer", "solicitor", "legal","1"]
            victimsComp = ["victims", "compensation", "victim's", "comp", "money", "financial", "victim","2"]
            counseling = ["counselling", "counseling", "psychologist", "therapy", "counsellor", "therapist","3"]

        state = self.state

        if state['previous_question'] == 'main menu':
            for s in user_response.split():
                if s in victimsComp:
                    state['previous_question'] = 'briefly'
                    return f"{self.response('victims compensation', language)}\n{self.response('briefly', language)}"
                elif s in counseling:
                    state['previous_question'] = 'other_services'
                    return f"{self.response('counselling', language)}\n{self.response('other_services', language)}"
                elif s in legal:
                    state['previous_question'] = 'main menu'
                    return f"{self.response('free legal services', language)}\n{self.response('main menu', language)}"
                elif s in no:
                    state['previous_question'] = 'bye'
                    return f"{self.response('limit', language)}\n{self.response('bye', language)}"
                else:
                    if s == user_response.split()[-1]:
                        state['previous_question'] = 'main menu'
                        return f"{self.response('error', language)}\n{self.response('main menu', language)}"

        elif state['previous_question'] == 'other_services':
            for s in user_response.split():
                if s in yes:
                    state['previous_question'] = 'briefly'
                    return f"{self.response('victims compensation', language)}\n{self.response('briefly', language)}"
                elif s in no:
                    state['previous_question'] = 'legal services'
                    return self.response('legal services', language)
                else:
                    if s == user_response.split()[-1]:
                        return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

        elif state['previous_question'] == 'legal services':
            state['previous_question'] = 'main menu'
            return f"{self.response('free legal services', language)}\n{self.response('main menu', language)}"

        elif state['previous_question'] == 'briefly':
            category = self.classifier(user_response)
            state['previous_question'] = category
            return self.response(category, language)

        # Sexual abuse questions
        elif state['previous_question'] == 'sexual abuse':
            for s in user_response.split():
                if s in yes:
                    state['category'] = 'sexual abuse'
                    state['previous_question'] = 'sexual series'
                    return f"{self.response('further questions', language)}\n{self.response('sexual series', language)}"
                elif s in no:
                    state['previous_question'] = 'attempt'
                    return self.response('attempt', language)
                else:
                    if s == user_response.split()[-1]:
                        return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

        elif state['previous_question'] == 'sexual series':
            for s in user_response.split():
                if s in yes:
                    state['previous_question'] = 'Category B'
                    self.application()
                    return self.response('Category B', language)
                elif s in no:
                    state['previous_question'] = 'aggravated'
                    return self.response('aggravated', language)
                else:
                    if s == user_response.split()[-1]:
                        return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

        elif state['previous_question'] == 'aggravated':
            for s in user_response.split():
                if s in yes:
                    state['previous_question'] = 'Category B'
                    self.application()
                    return self.response('Category B', language)
                elif s in no:
                    state['previous_question'] = 'penetrate'
                    return self.response('penetrate', language)
                else:
                    if s == user_response.split()[-1]:
                        return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

        elif state['previous_question'] == 'penetrate':
            for s in user_response.split():
                if s in yes:
                    state['previous_question'] = 'Category C'
                    self.application()
                    return self.response('Category C', language)
                elif s in no:
                    state['previous_question'] = 'attempt penetrate'
                    return self.response('attempt penetrate', language)
                else:
                    if s == user_response.split()[-1]:
                        return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

        elif state['previous_question'] == 'attempt penetrate':
            for s in user_response.split():
                if s in yes:
                    state['previous_question'] = 'injuries'
                    return self.response('injuries', language)
                elif s in no:
                    state['previous_question'] = 'Category D'
                    self.application()
                    return self.response('Category D', language)
                else:
                    if s == user_response.split()[-1]:
                        return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

        elif state['previous_question'] == 'injuries':
            for s in user_response.split():
                if s in yes:
                    state['previous_question'] = 'Category C'
                    self.application()
                    return self.response('Category C', language)
                elif s in no:
                    state['previous_question'] = 'Category D'
                    self.application()
                    return self.response('Category D', language)
                else:
                    if s == user_response.split()[-1]:
                        return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

        # Handling re-attempts at classifying the offence
        elif state['previous_question'] == 'attempt':
            for s in user_response.split():
                if s in yes:
                    state['previous_question'] = 'briefly'
                    return self.response('briefly', language)
                elif s in no:
                    state['previous_question'] = 'match error'
                    return self.response('match error', language)
                else:
                    if s == user_response.split()[-1]:
                        return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

        elif state['previous_question'] == 'match error':
            for s in user_response.split():
                if s in yes:
                    state['previous_question'] = 'main menu'
                    return f"{self.response('free legal services', language)}\n{self.response('main menu', language)}"
                elif s in no:
                    state['previous_question'] = 'main menu'
                    return self.response('main menu', language)
                else:
                    if s == user_response.split()[-1]:
                        return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

        # Assault questions
        elif state['previous_question'] == 'assault':
            for s in user_response.split():
                if s in yes:
                    state['category'] = 'assault'
                    state['previous_question'] = 'serious harm'
                    return f"{self.response('further questions', language)}\n{self.response('serious harm', language)}"
                elif s in no:
                    state['previous_question'] = 'attempt'
                    return self.response('attempt', language)
                else:
                    if s == user_response.split()[-1]:
                        return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

        elif state['previous_question'] == 'serious harm':
            for s in user_response.split():
                if s in yes:
                    state['previous_question'] = 'Category C'
                    self.application()
                    return self.response('Category C', language)
                elif s in no:
                    state['previous_question'] = 'eighteen'
                    return self.response('eighteen', language)
                else:
                    if s == user_response.split()[-1]:
                        return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

        elif state['previous_question'] == 'eighteen':
            for s in user_response.split():
                if s in yes:
                    state['previous_question'] = 'child'
                    return self.response('child', language)
                elif s in no:
                    state['previous_question'] = 'Category D'
                    self.application()
                    return self.response('Category D', language)
                else:
                    if s == user_response.split()[-1]:
                        return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

        elif state['previous_question'] == 'child':
            for s in user_response.split():
                if s in yes:
                    state['previous_question'] = 'Category C'
                    self.application()
                    return self.response('Category C', language)
                elif s in no:
                    self.application()
                    state['previous_question'] = 'Category D'
                    return self.response('Category D', language)
                else:
                    if s == user_response.split()[-1]:
                        return self.response('error', language)

        elif state['previous_question'] == 'application':
            for s in user_response.split():
                if s in yes:
                    state['previous_question'] = 'legal services'
                    return self.response('legal services', language)
                elif s in no:
                    return self.response('bye', language)
                else:
                    if s == user_response.split()[-1]:
                        return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

        elif state['previous_question'] == 'application advice':
            for s in user_response.split():
                if s in yes:
                    state['previous_question'] = 'main menu'
                    return f"{self.response('free legal services', language)}\n{self.response('main menu', language)}"
                elif s in no:
                    state['previous_question'] = 'main menu'
                    return self.response('main menu', language)
                else:
                    if s == user_response.split()[-1]:
                        return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

        else:
            return f"{self.response('error', language)}\n{self.response(state['previous_question'], language)}"

    def application(self):
        response_text = self.response('application', 'en')  # Assuming default language as English
        # providing further resources based on category of offence
        response_text += '\n\n you may also find this information helpful:\n\n'
        if self.state['category'] == 'sexual abuse':
            response_text += f"{self.response('sexual abuse information', 'en')}\n"
        else:
            response_text += f"{self.response('AVO', 'en')}\n"
        response_text += f"{self.response('disclaimer', 'en')}\n{self.response('application advice', 'en')}"
        self.state['previous_question'] = 'application advice'
        return response_text

    def classifier(self, user_response):
        # call trained classifier to discern 'assault' or 'sexual abuse'

        vote = {'assault': 0,'sexual abuse': 0}

        s = self.supportV.predict(np.array([user_response]))[0]

        vote[s] += 1

        r = self.forest.predict(np.array([user_response]))[0]

        vote[r] += 1

        b = self.bayes.predict(np.array([user_response]))[0]

        vote[b] += 1

        if vote['sexual abuse'] > vote['assault']:
            return 'sexual abuse'
        else:
            return 'assault'

    def get_initial_messages(self, language):
        if language == 'es':
            return [
                "Hola, soy un chatbot. \nMi trabajo es ayudar a las personas con información sobre los servicios de apoyo a las víctimas en Nueva Gales del Sur. Si has sido víctima de abuso físico o sexual, me gustaría ayudarte.\n\n",
                "¿Te gustaría obtener información sobre: \n1. Servicios legales gratuitos \n2. Consejería \n3. Compensación a víctimas \n\n"
            ]
        elif language == 'mayan':
            return [
                "Ba'ax ka wa'alik, in kaambal. \nIn k'aaba' yéetel u k'áatchi'ob u k'i'ik'ib tuméen kuxtal. Wa k'a'a' k'uxtal na'at, in k'a'atech ku je'elo'ob.\n\n",
                "Ba'ax ka wa'alik yaan a k'i'ik'baj? \n1. U k'i'ik'ib yéetel yaan a k'i'ik'ib \n2. Consejería \n3. Compensación a víctimas \n\n"
            ]
        else:  # Default to English
            return [
                "Hi, I'm a chatbot. \nMy job is to help people with information about victims support services in New South Wales. If you have been the victim of physical or sexual abuse I'd like to help you \n\n",
                "Would you like some information on: \n1. Free legal services \n2. Counselling \n3. Victims Compensation \n\n"
            ]

    def get_chatbot_response(self, message, language):
        if language == 'es':
            if message.lower() == 'hola':
                return '¡Hola! ¿Cómo puedo ayudarte hoy?'
            elif message.lower() == 'adiós':
                return '¡Adiós! Que tengas un buen día.'
            else:
                return self.respond(message, language)
        elif language == 'mayan':
            if message.lower() == "ba'ax ka wa'alik":
                return "Ba'ax ka wa'alik! Káaj máako'ob óolal teech."
            elif message.lower() == "ka xi'ik tech utsil":
                return "Ka xi'ik tech utsil! Ja'ats'uts áak'ab teech."
            else:
                return self.respond(message, language)
        else:  # Default to English
            if message.lower() == 'hello':
                return 'Hello! How can I help you today?'
            elif message.lower() == 'goodbye':
                return 'Goodbye! Have a great day.'
            else:
                return self.respond(message, language)

if __name__ == '__main__':
    chatbot = Chatbot()

    state = {'category': "", 'previous_question': ""}

    language = input("Select language (en/es/mayan): ").strip().lower()

    initial_messages = chatbot.get_initial_messages(language)
    for message in initial_messages:
        print(message)

    state['previous_question'] = 'main menu'

    while True:
        user_response = input().lower().strip("`~@!#$%^&*()_+=?/\\|,./*1234567890")

        if user_response == "bye":
            print(chatbot.response('bye', language))
            break
        else:
            response = chatbot.respond(user_response, language)
            print(response)
            state['previous_question'] = response
        if state['previous_question'] == 'bye':
            break
