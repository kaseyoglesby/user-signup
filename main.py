#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, re, cgi

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PWD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return USER_RE.match(password)

def valid_email(email):
    return USER_RE.match(email)

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">User Signup</a>
    </h1>
"""

page_footer = """
</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):

    def get(self):

        usernameError = self.request.get("usernameError")
        passwordError = self.request.get("passwordError")
        confirmPasswordError = self.request.get("confirmPasswordError")

        if usernameError:
            usernameError_esc = cgi.escape(usernameError, quote=True)
            usernameError_element = '<span class="error">' + usernameError_esc + '</span>'
        else:
            usernameError_element = ''

        if passwordError:
            passwordError_esc = cgi.escape(passwordError, quote=True)
            passwordError_element = '<span class="error">' + passwordError_esc + '</span>'
        else:
            passwordError_element = ''

        if confirmPasswordError:
            confirmPasswordError_esc = cgi.escape(confirmPasswordError, quote=True)
            confirmPasswordError_element = '<span class="error">' + confirmPasswordError_esc + '</span>'
        else:
            confirmPasswordError_element = ''

        usernameBox = """
            <label>Username</label>
            <input type="text" name="username" class="box" />
        """

        passwordBox = """
            <label>Password</label>
            <input type="password" name="password" class="box" />
        """

        confirmPasswordBox = """
            <label>Confirm password</label>
            <input type="password" name="confirmpassword" class="box" />
        """

        emailBox = """
            <label>Email</label>
            <input type="text" name="email"/>
        """

        button = '<br><br><input type="submit" value="Submit" class="box" />'

        add_form = "<form action='/submit' method='post'>" + usernameBox + usernameError_element + "<br>" + passwordBox + passwordError_element + "<br>" + confirmPasswordBox + confirmPasswordError_element + "<br>" + emailBox + button + "</form>"

        content = page_header + add_form + page_footer

        self.response.write(content)

class SubmitForm(webapp2.RequestHandler):

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        confirmPassword = self.request.get("confirmpassword")
        email = self.request.get("email")
        errorMessages = ""

        if not valid_username(username):
            usernameError = "Please enter a valid username."
        else:
            usernameError = ""

        if not valid_password(password):
            passwordError = "Please enter a valid password."
        else:
            passwordError = ""

        if password == confirmPassword:
            confirmPasswordError = ""
        else:
            confirmPasswordError = "Passwords do not match."

        if usernameError or passwordError or confirmPasswordError:
            errorMessages = "/?usernameError=" + usernameError + "&passwordError=" + passwordError + "&confirmPasswordError=" + confirmPasswordError
            self.redirect(errorMessages)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', SubmitForm)
], debug=True)
