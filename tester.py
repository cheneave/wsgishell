'''
Created on 2015-5-1

@author: cheneave
'''

from wsgishell import ShellMiddleware


def app(environ, start_response):
    start_response(
        "200 OK", [("Content-type", 'text/plain'), ('charset', 'utf-8')])
    return ["not implemented"]

application = ShellMiddleware(app, app, "123123", url_path="webshel")

if __name__ == '__main__':

    from wsgiref import simple_server

    svr = simple_server.make_server("localhost", 8080, application)
    print("server running on localhost:8080, press ctrl+c to exit")
    svr.serve_forever()
