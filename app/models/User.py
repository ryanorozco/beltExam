from system.core.model import Model

import re

NAME_REGEX = re.compile(r'^[a-zA-Z]')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASS_REGEX = re.compile(r'^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)[0-9a-zA-Z]{6,}$')

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def registerUser(self, userData):
        hasErrors = False
        if len(userData['email']) < 2:
            hasErrors = True
        elif not NAME_REGEX.match(userData['name']):
            hasErrors = True
        elif not NAME_REGEX.match(userData['alias']):
            hasErrors = True
        elif not EMAIL_REGEX.match(userData['email']):
            hasErrors = True
        elif not PASS_REGEX.match(userData['password']):
            hasErrors = True
        elif userData['password'] != userData['confirm_password']:
            hasErrors = True
        elif userData['dob'] == None:
            hasErrors = True
        elif hasErrors == True:
            return False
        else:
            query = 'INSERT INTO users (name, alias, email, password, dob) VALUES (:name, :alias, :email, :password, :dob)'
            data = {
                'email': userData['email'],
                'name': userData['name'],
                'alias': userData['alias'],
                'password': userData['password'],
                'dob': userData['dob']
                }
            return self.db.query_db(query, data)

    def loginUser(self, userData):
        hasErrors = False
        if len(userData['email']) < 2:
            hasErrors = True
        elif not EMAIL_REGEX.match(userData['email']):
            hasErrors = True
        elif hasErrors == False:
            query = "SELECT * FROM users WHERE email = :email AND password = :password"
            data = {'email': userData['email'],'password': userData['password']}
            return self.db.query_db(query, data)
        else:
            return False

    def getFriends(self, userId):
        query = 'SELECT b.id, b.name, b.alias FROM friends f JOIN users a ON f.user_id=a.id JOIN users b ON f.friend_id=b.id WHERE a.id=:userId'
        data = {'userId': userId}
        return self.db.query_db(query, data)

    def getNotFriends(self, userId):
        query = 'SELECT a.id, a.alias FROM users a WHERE a.id NOT IN (SELECT f.friend_id FROM friends f WHERE user_id = :userId AND f.friend_id != user_id) AND a.id != :userId'
        data = {'userId': userId}
        return self.db.query_db(query, data)

    def addFriendToUser(self, userData):
        query = 'INSERT INTO friends (user_id, friend_id) VALUES (:userId, :friendId)'
        data = {'userId': userData['userId'], 'friendId': userData['friendId']}
        self.db.query_db(query, data)

    def addUserToFriend(self, userData):
        query = 'INSERT INTO friends (user_id, friend_id) VALUES (:userId, :friendId)'
        data = {'userId': userData['friendId'], 'friendId': userData['userId']}
        self.db.query_db(query, data)

    def removeFriendFromUser(self, userData):
        query = 'DELETE FROM friends WHERE user_id = :userId AND friend_id = :friendId'
        data = {'userId': userData['userId'], 'friendId': userData['friendId']}
        self.db.query_db(query, data)

    def removeUserFromFriend(self, userData):
        query = 'DELETE FROM friends WHERE user_id = :userId AND friend_id = :friendId'
        data = {'userId': userData['friendId'], 'friendId': userData['userId']}
        self.db.query_db(query, data)

    def getUserById(self, userId):
        query ='SELECT name, alias, email FROM users WHERE id=:userId'
        data = {'userId': userId}
        return self.db.query_db(query, data)
