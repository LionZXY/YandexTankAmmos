#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import sys

def print_request(request):
    method = request.method.encode()
    path_url = request.path_url.encode()
    headers = (''.join('{0}: {1}\r\n'.format(k, v) for k, v in request.headers.items())).encode()
    body = (request.body) or ""
    req = b''.join(
        [
            method,
            b' ',
            path_url,
            b' HTTP/1.1\r\n',
            headers,
            b'\r\n',
            body
        ]
        )
    req_size = str(len(req)).encode()
    return b''.join([req_size,b'\n',req,b'\r\n'])

#POST multipart form data
def post_multipart(host, port, namespace, files, headers, payload):
    req = requests.Request(
        'POST',
        'https://{host}:{port}{namespace}'.format(
            host = host,
            port = port,
            namespace = namespace,
        ),
        headers = headers,
        data = payload,
        files = files
    )
    prepared = req.prepare()
    return print_request(prepared)

if __name__ == "__main__":
    #usage sample below
    #target's hostname and port
    #this will be resolved to IP for TCP connection
    host = 'test.host.ya.ru'
    port = '8080'
    namespace = '/some/path'
    #below you should specify or able to operate with
    #virtual server name on your target
    headers = {
        'Host': 'ya.ru'
    }
    payload = {
        'langName': 'en',
        'apikey': '123'
    }
    files = {
        # name, path_to_file, content-type, additional headers
        'file': ('image.jpeg', open('./image.jpeg', 'rb'), 'image/jpeg ', {'Expires': '0'})
    }

    sys.stdout.buffer.write(post_multipart(host, port, namespace, files, headers, payload))