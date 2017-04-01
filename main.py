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
    return PWD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <link rel="stylesheet" type="text/css" href="/stylesheets/stylesheet.css" />
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

        username = self.request.get("username")
        email = self.request.get("email")
        usernameError = self.request.get("usernameError")
        passwordError = self.request.get("passwordError")
        confirmPasswordError = self.request.get("confirmPasswordError")
        emailError = self.request.get("emailError")

        if usernameError:
            usernameError_element = '<td class="error">' + cgi.escape(usernameError, quote=True) + '</td>'
        else:
            usernameError_element = ''

        if passwordError:
            passwordError_element = '<td class="error">' + cgi.escape(passwordError, quote=True) + '</td>'
        else:
            passwordError_element = ''

        if confirmPasswordError:
            confirmPasswordError_element = '<td class="error">' + cgi.escape(confirmPasswordError, quote=True) + '</td>'
        else:
            confirmPasswordError_element = ''

        if emailError:
            emailError_element = '<td class="error">' + cgi.escape(emailError, quote=True) + '</td>'
        else:
            emailError_element = ''

        usernameBox = """
                    <td class="label">Username</td>
                    <td><input type="text" name="username" value="{0}" /><td>
                    """.format(username)
        usernameEntry = "<tr>" + usernameBox + usernameError_element + "</tr>"

        passwordBox = """
                    <td class="label">Password</td>
                    <td><input type="password" name="password" /></td>
                    """
        passwordEntry = "<tr>" + passwordBox + passwordError_element + "</tr>"

        confirmPasswordBox = """
                    <td class="label">Confirm password</td>
                    <td><input type="password" name="confirmpassword" /></td>
                    """
        confirmPasswordEntry = "<tr>" + confirmPasswordBox + confirmPasswordError_element + "</tr>"

        emailBox = """
                    <td class="label">Email (optional)</td>
                    <td><input type="text" name="email" value="{0}" /></td>
                    """.format(email)
        emailEntry = "<tr>" + emailBox + emailError_element + "</tr>"

        button = """
                    <tr>
                    <td></td>
                    <td class="button"><input type="submit" value="Submit" /></td>
                    </tr>
                    """

        add_form = ("<form action='/submit' method='post'><table>" +
                    usernameEntry + passwordEntry + confirmPasswordEntry + emailEntry + button +
                    "</table></form>")

        content = page_header + add_form + page_footer

        self.response.write(content)

class SubmitForm(webapp2.RequestHandler):

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        confirmPassword = self.request.get("confirmpassword")
        email = self.request.get("email")
        queries = "/?username=" + username + "&email=" + email
        errors = False

        if not valid_username(username):
            usernameError = "Please enter a valid username."
            queries += "&usernameError=" + usernameError
            errors = True

        if not valid_password(password):
            passwordError = "Please enter a valid password."
            queries += "&passwordError=" + passwordError
            errors = True

        if password != confirmPassword:
            confirmPasswordError = "Passwords do not match."
            queries += "&confirmPasswordError=" + confirmPasswordError
            errors = True

        if email and not valid_email(email):
            emailError = "Email address is not valid."
            queries += "&emailError=" + emailError
            errors = True

        if errors:
            self.redirect(queries)
        else:
            # self.response.write("<h1>Thanks for logging in, " + username + "!</h1>")
            self.redirect('/success?username=' + username)

class Success(webapp2.RequestHandler):

    def get(self):
        username = self.request.get("username")
        if valid_username(username):
            self.response.write("<h1>Thanks for logging in, {0}!</h1>".format(username))
        else:
            self.redirect("/")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', SubmitForm),
    ('/success', Success)
], debug=True)
