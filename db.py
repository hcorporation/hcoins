from peewee import *
from dotenv import load_dotenv
import os

load_dotenv()

db = PostgresqlDatabase("postgres", user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), host=os.getenv("DB_URL"), port=os.getenv("DB_PORT"))

class CoinUser(Model):
    name = CharField()
    coins = IntegerField()
    class Meta:
        database = db

class dbUtils:
    def __init__(self):
        self.db = db
        self.errorMsg = "the following error occurred. you can report it here: https://github.com/hcorporation/hcoins"
        self.CoinUser = CoinUser
        self.db.connect(reuse_if_open=True)
        self.db.create_tables([self.CoinUser])
        self.db.close()
    
    def get_user(self, user):
        if self.db.is_closed() == True:
            self.db.connect()
        check = self.CoinUser.get_or_none(self.CoinUser.name == user)
        if check == None:
            print("none")
            return False
        else:
            print("yes")
            return True
    
    # getting a user's coin amount
    def get_coins(self, user):
        if self.db.is_closed() == True:
            self.db.connect()
        try:
            userfound = self.CoinUser.get(self.CoinUser.name == user)
            self.db.close()
            return "**" + userfound.name + "** has **" + str(userfound.coins) + "** hCoins."
        except Exception as e:
            self.db.close()
            return self.errorMsg + "\n\n```\n" + str(e) + "\n```"

    # creating a user
    def create_user(self, user):
        if self.db.is_closed() == True:
            self.db.connect()
        try:
            self.CoinUser.create(name=user, coins=100)
            self.db.close()
            return True
        except Exception as e:
            self.db.close()
            return False

    # adding coins to a user
    def update_user(self, sender, recipient, coins, action):
        if self.db.is_closed() == True:
            self.db.connect()
        try:
            coinrecipient = self.CoinUser.get(self.CoinUser.name == recipient)
            coinsender = self.CoinUser.get(self.CoinUser.name == sender)
            coins_int = int(coins)
            if coinsender.coins >= coins_int:
                coinsender.coins = coinsender.coins - coins_int
                coinsender.save()
            else:
                raise Exception("error")
            if action == 1:
                coinrecipient.coins = coinrecipient.coins + coins_int
                coinrecipient.save()
                self.db.close()
                return "**u/" + sender + "** gave **" + coins + "** hCoins to **u/" + recipient + "**"
            elif action == 0:
                coinrecipient.coins = coinrecipient.coins - coins_int
                coinrecipient.save()
                self.db.close()
                return "**" + coins + "** hCoins were taken from both **u/" + sender + "**'s account and **u/" + recipient + "**'s account."
        except Exception as e:
            self.db.close()
            return self.errorMsg + "\n\n```\n" + str(e) + "\n```"

    def get_leaderboard(self):
        if self.db.is_closed() == True:
            self.db.connect()
        try:
            allUsers = self.CoinUser.select().order_by(self.CoinUser.coins.desc())
            table = "this is a ranking of all users by their hCoins wealth.\n\n user | coins \n -- | --"
            for user in allUsers:
                table = table + "\n" + user.name + " | " + "Ħ" + str(user.coins)
            return table
        except Exception as e:
            self.db.close()
            return self.errorMsg + "\n\n```\n" + str(e) + "\n```"