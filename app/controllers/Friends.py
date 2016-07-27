from system.core.controller import *

class Friends(Controller):
    def __init__(self, action):
        super(Friends, self).__init__(action)
        self.load_model('User')
        self.db = self._app.db

    def friends(self):
        self.load_model('User')
        friendArray = self.models['User'].getFriends(session['currentUser']['id'])
        if not friendArray:
            flash("Looks like you need some friends")
        newbieArray = self.models['User'].getNotFriends(session['currentUser']['id'])
        return self.load_view('friends.html', friendArray=friendArray, newbieArray=newbieArray)

    def addFriend(self):
        self.load_model('User')
        self.models['User'].addFriendToUser(request.form)
        self.models['User'].addUserToFriend(request.form)
        return redirect('/friends')

    def removeFriend(self):
        self.load_model('User')
        self.models['User'].removeFriendFromUser(request.form)
        self.models['User'].removeUserFromFriend(request.form)
        return redirect('/friends')

    def getUsers(self, id):
        self.load_model('User')
        userArray = self.models['User'].getUserById(id)
        return self.load_view('user.html', userArray=userArray)
