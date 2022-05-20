import random
from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin
from cryptography.fernet import Fernet

import sys
sys.path.insert(0,"/var/www/html/API/")

from words import WORD_LIST
from gusses import GUESS_LIST

fernet = Fernet(b'Fvk6zsnBUT4IqsFtwlPjbvXePJ7bYxjU7EC5FpCU-k4=')

server = 'https://oci.sebright.synology.me/wurdle/'

#sudo /etc/init.d/apache2 restart
#WSGIScriptAlias /wurdle /var/www/html/API/api.py
#sudo cp /config/workspace/API /var/www/html/ -r
#sudo rm /var/www/html/API -R && sudo cp /config/workspace/API /var/www/html/ -r

application = Flask(__name__)

@application.route('/')
def home():
    return render_template('indexClass.html')
    #return render_template('indexApi.html')

@application.route('/v1/')
def homev2():
   return render_template('indexAllHTML.html')

# @application.route ('/v2/')
# def homev1():
#    return render_template('indexClass.html')

cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'
api = Api(application)

chosenword = None
usedLetters = ""
foundLetters = ""
wordlist = []
usedwords = []
respnoses = []
count = 0

class Check(Resource):
    def get(self):
        word = str(request.args.get('word','')).upper()
        if word.lower() not in WORD_LIST and word.lower() not in GUESS_LIST: return False, 200  # return data and 200 OK code
        return True, 200

class Word(Resource):
    def get(self):
        enc = request.args.get('enc')
        return {"word": fernet.decrypt(enc.encode()).decode()},200

class GuessStateless(Resource):
    def get(self):
        enc = request.args.get('session','')
        guess = str(request.args.get('guess','')).upper()
        response = ''
        found = ''
        word = ''

        #https://wordle.sebright.synology.me/wordleSl
        if enc == '' or guess == '':
            return {"Found": False, "Error": "invalidparameters", "Msg": f"Incorrect parameters passed enc:'{enc}' guess:'{guess}'"}, 200  # return data and 200 OK code
        
        #https://wordle.sebright.synology.me/wordleSl?enc=H7Nu_5EBtkZDA==&guess=poser
        try:
            word = fernet.decrypt(enc.encode()).decode().upper()
        except: 
            return {"Found": False, "Error": "invalidenc", "Msg": f"Invalid encrypted word string"}, 200  # return data and 200 OK code

        #https://wordle.sebright.synology.me/wordleSl?enc=gAAAAABiBRVmXL3Bcs_5soigOKks5q3G8iFobfGG60OtX45NYgx-hfHK3Yl1zLAYGyh7NVBEW9qLchbvDDp3o4LEffwnk8k0kg==&guess=pause
        if len(word) != 5:
            return {"Found": False, "Error": "invalidenc", "Msg": f"Invalid decrypted word lenght passed {len(word)} not 5 characters"}, 200  # return data and 200 OK code

        #If word found
        #https://wordle.sebright.synology.me/wordleSl?enc=gAAAAABiBRB-9E_vNV8pAw4UUz9edf5X1hrlccCHxBdMurpWFbVhwxqYqzV5SbSy6hTy6GuxRocApywF-wZwWH7Nu_5EBtkZDA==&guess=poser
        if guess == word: return {"Found": True, "Error": None}, 200  # return data and 200 OK code
    
        #If guess length wrong
        #https://wordle.sebright.synology.me/wordleSl?enc=gAAAAABiBRB-9E_vNV8pAw4UUz9edf5X1hrlccCHxBdMurpWFbVhwxqYqzV5SbSy6hTy6GuxRocApywF-wZwWH7Nu_5EBtkZDA==&guess=pose
        if len(guess) != 5: return {"Found": False, "Error": "invalidguesslength", "Msg": f"Your guess {guess} needs to be of {len(word)} characters in length not {len(word)-1}"}
        
        #If a valid word or guess
        #https://wordle.sebright.synology.me/wordleSl?enc=gAAAAABiBRB-9E_vNV8pAw4UUz9edf5X1hrlccCHxBdMurpWFbVhwxqYqzV5SbSy6hTy6GuxRocApywF-wZwWH7Nu_5EBtkZDA==&guess=pause
        if guess.lower() not in WORD_LIST and guess.lower() not in GUESS_LIST: return {"valid": False, "Found": False, "Error": "invalidnotword", "Response": '', "Msg": f"{guess} is not a valid word"}, 200  # return data and 200 OK code

        #Find exact positioned letters as capitals
        for n in range(0, len(guess)):
            wordLetter = (word[n:n+1])
            guessLetter = (guess[n:n+1])
            if wordLetter == guessLetter: 
                response = response + wordLetter
                found = found + wordLetter
            else: 
                response = response + "?"

        #Find misplaced letters as lowercase
        for n in range(0, len(guess)):
            wordLetter = (guess[n:n+1])
            if wordLetter in word and wordLetter not in found: 
                response = response[:n] + wordLetter.lower() + response[n+1:]
    
        return {"Found": False, "Error": None, "Guess": guess, "Response": response}, 200
          
class Guess(Resource):
    def get(self):

        guess = str(request.args.get('guess','')).upper()
        enc = str(request.args.get('session',fernet.encrypt(random.choice(WORD_LIST).upper().encode()).decode()))
        hide = request.args.get('hide',True)
        
        #enc = fernet.encrypt('SWAMP'.encode()).decode()

        global chosenword, count, usedLetters, usedwords, respnoses, foundLetters

        if guess.upper() == '': 
            chosenword = None
            usedLetters = ""
            foundLetters = ""
            wordlist = []
            usedwords = []
            respnoses = []
            count = 0
            print(fernet.decrypt(enc.encode()).decode())
            return  {"server": f"{server}", "URL": f"{server}/wordle?hide={hide}&guess=xxxxx&session={enc}", "Note": "Replace guess", "enc": enc}

        resp = ""
        found = ""
        nopos = ""
        view = ""
        max = 6
        fnd = True
        
        word = fernet.decrypt(enc.encode()).decode()
        chosenword = word
        
        #If guess length wrong
        if len(word) != len(guess): return f"Error: Your guess needs to be of {len(guess)-1} characters in length not {len(guess)}"
        #If a valid word or guess
        if guess.lower() not in WORD_LIST and guess.lower() not in GUESS_LIST: return {"found": False, 'guess': guess, "Error": "not a valid word"}, 200  # return data and 200 OK code
          
        #Find exact positioned letters as capitals
        for n in range(0, len(guess)):
            wordLetter = (word[n:n+1])
            guessLetter = (guess[n:n+1])
            usedLetters = usedLetters + guessLetter
            if wordLetter == guessLetter: 
                resp = resp + "1"
                found = found + wordLetter
                view = view + wordLetter
                foundLetters = foundLetters + wordLetter.upper()
            else: 
                resp = resp + "0"
                view = view + "?"
                if fnd == True: fnd = False

        #Find misplaced letters as lowercase
        for n in range(0, len(guess)):
            wordLetter = (guess[n:n+1])
            if wordLetter in word and wordLetter not in found:
                nopos = nopos + wordLetter
                resp = resp[:n] + "2" + resp[n+1:]
                view = view[:n] + wordLetter.lower() + view[n+1:]
                foundLetters = foundLetters + wordLetter

        #Sort letters used
        usedLetters = ''.join(sorted(set(usedLetters)))
        foundLetters = ''.join(sorted(set(foundLetters)))

        #Hide answer
        if hide == "True": word = "[hidden]"

        #If guess already made
        if guess in usedwords: 
            msg = f"Keep trying and have another guess, you have taken {count} attempts so far"
            #if collatedResp is None: collatedResp = "?????"

            try: collatedResp
            except NameError: collatedResp = "?????"

            return {"found": False, "Message": msg, 'Word': word, 'Guess': guess, "Positioned": collatedResp, "GuessHistory": respnoses, "FoundLetters": foundLetters, "UsedLetters": usedLetters, "Guesses": usedwords, "AttemptCount": count}, 200  # return data and 200 OK code

        #add registers
        count = count + 1
        usedwords.append(guess)
        respnoses.append(view)

        #get positioned guesses from history
        collatedResp = ""
        for response in respnoses:
            #print(response)
            for n in range(0, len(response)):
                responseLetter = response[n:n+1]
                #if responseLetter.isupper():
                #collatedResp = collatedResp[:n] + responseLetter + collatedResp[n+1:]
                if responseLetter != '?':
                    collatedResp = collatedResp + responseLetter

        collatedResp = ''.join(sorted(set(collatedResp)))

        #if word found or too many attempts
        if fernet.decrypt(enc.encode()).decode() == guess: fnd = True
        #print(fernet.decrypt(enc.encode()).decode())

        att = "attempt"
        att = "attempt" if count == 1 else "attempts"
        print(count)

        if fnd or count >= max: 
            word = fernet.decrypt(enc.encode()).decode()

            msg = f"Well done you found the word '{word}' in {count} attempts" if count > 1 else f"Well done you found the word '{word}' on your first attempt"
            if fnd: ret = {"found": True, "Message": msg, 'Word': word, 'Guess': guess, "Positioned": collatedResp, "GuessHistory": respnoses, "FoundLetters": foundLetters, "UsedLetters": usedLetters, "Guesses": usedwords, "AttemptCount": count}, 200  # return data and 200 OK code

            if count >= max and fnd == False: 
                msg = f"Unlucky you failed to find the word '{word}'"
                ret = {"found": False, "Message": msg, 'Word': word, 'Guess': guess, "Positioned": collatedResp, "GuessHistory": respnoses, "FoundLetters": foundLetters, "UsedLetters": usedLetters, "Guesses": usedwords, "AttemptCount": count}, 200  # return data and 200 OK code
            count = 0
            chosenword = None
            usedwords = []
            respnoses = []
            return ret
        else:
            msg = ""
            if len(foundLetters) > 1: msg = f"Well done you have found {len(foundLetters)} letters '{foundLetters}' so far in {count} " + att
            elif len(foundLetters) == 0: msg = f"Well done you have found {len(foundLetters)} letter '{foundLetters}' so far in {count} " + att
            else: msg = f"Keep trying and have another guess, you have taken {count} {att} so far"
            return {"Message": msg, 'Word': word, 'Guess': guess, "Positioned": collatedResp, "GuessHistory": respnoses, "FoundLetters": foundLetters, "UsedLetters": usedLetters, "Guesses": usedwords, "AttemptCount": count}, 200  # return data and 200 OK code

api.add_resource(Guess, '/wurdle')  
api.add_resource(GuessStateless, '/wurdleSl')  
api.add_resource(Check, '/wurdle/check')  
api.add_resource(Word, '/wurdle/word')  

if __name__ == '__main__':
    application.run(host='172.17.0.3', port=8005)