from http.server import BaseHTTPRequestHandler, HTTPServer
import os


class Handler:
    """docstring for Handler"""
    def __init__(self):
        self.max_file_size = 24000000
        self.max_files_total_size = 150000
        self.unique_client_id = 0
        self.unique_file_id = 0
        self.loaded_files_names = []
        self.unacceptable_extensions = ['.exe']
        self.client_upload_length = {}
        self.file_id_and_name = {}

        self.ERROR = 'Error'
        self.FILE_PATH = 'Documents/python/KSIS/Laba3/server/'
        self.CONTENT_NAME = 'Content-Name'
        self.CONTENT_EXT = 'Content-Extension'
        self.CONTENT_LEN = 'Content-Length'
        self.CONTENT_SIZE = 'Content-Size'
        self.CLIENT_ID = 'Client-id'
        self.CONTENT_ID = 'Content-id'
        self.REMOVABLE_TYPE = 'Removable-Type'
        self.NO_SUCH_FILE = 'No such file'
        self.NONE = 'None'


    def get_unique_client_id(self):
        self.unique_client_id += 1
        return self.unique_client_id


    def get_unique_file_id(self):
        self.unique_file_id += 1
        return self.unique_file_id


    def get_value_from_header(self, headers, desired_header):
        for header in str(headers).split('\n'):
            if header.startswith(desired_header):
                return header[len(desired_header)+2:]
        return False


    def save_file(self, file, file_name, file_extension, file_length, client_id):
        saved_file_name = f'{file_name}{file_extension}'

        file_id = self.get_unique_file_id()
        self.file_id_and_name[file_id] = saved_file_name
        self.loaded_files_names.append(file_name)

        saved_file = open(f'{self.FILE_PATH}{saved_file_name}', 'wb')
        saved_file.write(file) 
        self.client_upload_length[client_id] += file_length

        return file_id


    def delete_file(self, file_id, client_id, removable_type):
        try:
            full_file_name = self.file_id_and_name[file_id]

            if removable_type == 'upload':
                file_size = os.path.getsize(f'{self.FILE_PATH}{full_file_name}')
                self.client_upload_length[client_id] -= file_size

            os.remove(f'{self.FILE_PATH}{full_file_name}')
            self.file_id_and_name.pop(file_id)
            file_name = os.path.splitext(full_file_name)[0]
            self.loaded_files_names.remove(file_name)
            return True
        except:
            return False


    def check_file(self, file_name, file_extension, file_length, client_id):
        error = 'max file size'
        if file_length <= self.max_file_size:

            error = 'unacceptable extension'
            if not file_extension in self.unacceptable_extensions:

                error = 'max file total size'
                if self.client_upload_length[client_id]+file_length <= self.max_files_total_size:

                    error = 'file name already loaded'
                    if not file_name in self.loaded_files_names:

                        error = 'client already exists'
                        if str(client_id) != handler.NONE:
                            return
        return error


class HttpServer:
    def __init__(self, address, port):
        self.address = address
        self.port = port


    def start_server(self):
        self.server = HTTPServer((self.address, self.port), HttpRequestHandler)
        self.server.serve_forever()


class HttpRequestHandler(BaseHTTPRequestHandler):
    global handler
    handler = Handler()

    def do_INIT(self):
        client_id = handler.get_value_from_header(self.headers, handler.CLIENT_ID)
        if client_id == handler.NONE:
            unique_client_id = handler.get_unique_client_id()
            handler.client_upload_length[unique_client_id] = 0

            self.send_response(200)
            self.send_header(handler.CLIENT_ID, str(unique_client_id))
            self.end_headers()
        else:
            self.send_response(403)
            self.send_header(handler.ERROR, 'client already exists')
            self.end_headers()


    def do_GET(self):
        file_id = int(handler.get_value_from_header(self.headers, handler.CONTENT_ID))
        try:
            full_file_name = handler.file_id_and_name[file_id]

            self.send_response(200)
            self.end_headers()

            file = open(f'{handler.FILE_PATH}{full_file_name}', 'rb').read()
            self.wfile.write(file)
        except:
            self.send_response(404)
            self.send_header(handler.ERROR, handler.NO_SUCH_FILE)
            self.end_headers()


    def do_TEST(self):
        file_name = handler.get_value_from_header(self.headers, handler.CONTENT_NAME)
        file_extension = handler.get_value_from_header(self.headers, handler.CONTENT_EXT)
        file_length = int(handler.get_value_from_header(self.headers, handler.CONTENT_LEN))
        client_id = int(handler.get_value_from_header(self.headers, handler.CLIENT_ID))

        error = handler.check_file(file_name, file_extension, file_length, client_id)

        if not error:
            self.send_response(200)
            self.end_headers()

        else:
            self.send_response(411)
            self.send_header(handler.ERROR, error)
            self.end_headers()


    def do_PUT(self):
        file_name = str(handler.get_value_from_header(self.headers, handler.CONTENT_NAME))
        file_extension = handler.get_value_from_header(self.headers, handler.CONTENT_EXT)
        file_length = int(handler.get_value_from_header(self.headers, handler.CONTENT_LEN))
        client_id = int(handler.get_value_from_header(self.headers, handler.CLIENT_ID))

        error = handler.check_file(file_name, file_extension, file_length, client_id)

        if not error:
            file = self.rfile.read(file_length)
            file_id = handler.save_file(file, file_name, file_extension, file_length, client_id)

            self.send_response(200)
            self.send_header(handler.CONTENT_ID, file_id)
            self.end_headers()
            return

        self.send_response(411)
        self.send_header(handler.ERROR, error)
        self.end_headers()


    def do_HEAD(self):
        file_id = int(handler.get_value_from_header(self.headers, handler.CONTENT_ID))
        try:
            full_file_name = handler.file_id_and_name[file_id]
            file_size = os.path.getsize(f'{handler.FILE_PATH}{full_file_name}')

            self.send_response(200)
            self.send_header(handler.CONTENT_SIZE, file_size)
            self.end_headers()
        except:
            self.send_response(404)
            self.send_header(handler.ERROR, handler.NO_SUCH_FILE)
            self.end_headers()


    def do_DELETE(self):
        file_id = int(handler.get_value_from_header(self.headers, handler.CONTENT_ID))
        client_id = int(handler.get_value_from_header(self.headers, handler.CLIENT_ID))
        removable_type = handler.get_value_from_header(self.headers, handler.REMOVABLE_TYPE)

        if handler.delete_file(file_id, client_id, removable_type):
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header(handler.ERROR, handler.NO_SUCH_FILE)
            self.end_headers()


    def do_CLEAR(self):
        client_id = int(handler.get_value_from_header(self.headers, handler.CLIENT_ID))
        handler.client_upload_length[client_id] = 0
        self.send_response(200)
        self.end_headers()



if __name__ == '__main__':
    serv = HttpServer('', 8000)
    serv.start_server()
