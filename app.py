#products: Auth, RTDB, Store

import random
from enum import Enum
from firebase import Firebase

config = {
  "apiKey" : "AIzaSyA4Ya39dYNpYjCxcLgMNb6kwVixkjLLYEU",
  "authDomain" : "simplernggame.firebaseapp.com",
  "projectId" : "simplernggame",
  "storageBucket" : "simplernggame.appspot.com",
  "messagingSenderId" : "79591866349",
  "appId" : "1:79591866349:web:28d383e4c25adec77971e4",
  "measurementId" : "G-8Q5EYJFLTK",
  "databaseURL" : "https://simplernggame-default-rtdb.europe-west1.firebasedatabase.app/"
}


#firebase Auth module
firebase = Firebase(config)

auth = firebase.auth()

email = input("Please enter your email: ")
pwd = input("Please enter your password: ")
confPwd = input("Please confirm your password: ")

#create a user - remember to comment it!
if pwd == confPwd:
    try:
        user = auth.create_user_with_email_and_password(email, pwd)
        print("User created \n")
    except:
        print("User already exists \n")
        

#sign in metode
try:
    signin = auth.sign_in_with_email_and_password(email, pwd)
    print("Success! \n")
except:
    print("invalid user or password \n")

#before the 1 hour expiry
user = auth.refresh(user['refreshToken'])

#fresh token
user['idToken']
  
#veryfication by email
#auth.send_email_verification(signin['idToken'])
#print("veryfication email has been sent, check your mailbox")

#reset a password - remember to comment it!
#auth.send_password_reset_email(email)
#print("mail with reset link has been sent, check your mailbox")

#firebase RTDB module
db = firebase.database()
#storage module
storage = firebase.storage()

#code module
#aproximate from main value +/- in gold reward
def findApproximateValue(value):
    lowestValue = value - 0.1 * value
    highestValue = value + 0.1 * value
    return random.randint(lowestValue, highestValue)

Event = Enum('Event', ['Chest', 'Empty', 'Monster'])

#change for events
eventDictionary = {
                    Event.Chest: 0.4,
                    Event.Empty: 0.4,
                    Event.Monster: 0.2
                  }

eventList = list(eventDictionary.keys())
eventProbability = list(eventDictionary.values())

#Chest reward
colors = Enum('Colors' , ['blue', 'yellow', 'green', 'gold'])

colorsDictionary = {
                        colors.blue : 0.75,
                        colors.yellow : 0.2,
                        colors.green : 0.04,
                        colors.gold : 0.01
                    }                   
   
chestColorList = list(colorsDictionary.keys())
chestColorProbability = list(colorsDictionary.values())


rewordsChest = {
                    chestColorList[reward]: (reward + 1) * (reward + 1) * 100
                    for reward in range(len(chestColorList))
                }

#Monster events
MonsterEnemy = Enum('Demon', ['normal', 'medium', 'elite', 'deadly'])

MonsterOccur = {
                  MonsterEnemy.normal : 0.75,
                  MonsterEnemy.medium : 0.2,
                  MonsterEnemy.elite : 0.04,
                  MonsterEnemy.deadly : 0.01
                }

MonsterClassList = list(MonsterOccur.keys())
MonsterProbability = list(MonsterOccur.values())

gameLength = 5
summaryReward = 0


print("Welcome in Dungeon \n")
print("you have 5 level to check \n")

#main game system
while gameLength > 0:
    gameStart = input("Enter the lower level? type go to enter :\n")
    if(gameStart == "go"):
        print("you are in the dark Dungeon level", gameLength, "\n")
        eventResault = random.choices(eventList, eventProbability)[0]
#chest reward system
        if(eventResault == Event.Chest):
            print("chest reward!")
            rewardColor = random.choices(chestColorList, chestColorProbability)[0]
            print("quality of chest: \n", rewardColor.name)
            gamerReward = findApproximateValue(rewordsChest[rewardColor])
            summaryReward = summaryReward + gamerReward
#empty chest
        elif(eventResault == Event.Empty):
            print("Empty champer, run to the next one\n")
#monster event rolling
        elif(eventResault == Event.Monster):
            print("Monster, fight!\n")
            MonsterDraw = random.choices(MonsterClassList, MonsterProbability)[0]
            if(MonsterDraw.name == 'deadly'):
                print('you have been killed by', MonsterDraw.name , 'enemy\n')
                break
            elif(MonsterDraw.name == 'normal'):
                print('you found 7 gold\n')
                summaryReward = 7 + summaryReward
            elif(MonsterDraw.name == 'medium'):
                print('you found 10 gold\n')
                summaryReward = 10 + summaryReward
            elif(MonsterDraw.name == 'elite'):
                print('you found 13 gold\n')
                summaryReward = 13 + summaryReward
                
            else:
                print("you survived the fight with", MonsterDraw.name, "monster\n")
                continue
                  
    else:
        print("not this way... \n")
        continue
    
    gameLength = gameLength - 1
    
print("Gratz! you finished the Dungeon!")
print("your loot:", summaryReward,"gold \n")

#data to save in DB
data = {}
data["name"] = email
data["points"] = summaryReward

#creating own key in DB = players
db.child("users").child("Player").set(data)

#adding data as users in DB
print("record added to the score table. \n")
feedback = input("please give us a feedback: \n")
with open("feedback.txt", "a", encoding = "UTF-8") as file:
    file.write("\n" + feedback + "\n")

#moving file on cloud storage
storage.child("feedback/feedback.txt").put("feedback.txt")
print("====== thank you! ======")