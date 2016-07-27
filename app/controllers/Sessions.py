from system.core.controller import *

class Sessions(Controller):
    def __init__(self, action):
        super(Sessions, self).__init__(action)
        self.load_model('WelcomeModel')
        self.db = self._app.db

    def main(self):
        return self.load_view('index.html')

    def register(self):
        self.load_model('User')
        userArray = self.models['User'].registerUser(request.form)
        if userArray:
            flash(u'Congrats, you registered! Now Login to get shwifty.','success')
            return redirect('/main')
        else:
            flash(u'Failed to register. Password must contain at least one letter, at least one number, and be longer than six charaters.','regerror')
            return redirect('/main')

    def login(self):
        self.load_model('User')
        userArray = self.models['User'].loginUser(request.form)
        if userArray:
            session['currentUser'] = userArray[0]
            return redirect('/friends')
        else:
            flash(u'Sorry, that did not work, please try again.','logerror')
            return redirect('/main')

    def logout(self):
        session.pop('currentUser', None)
        return redirect('/main')
