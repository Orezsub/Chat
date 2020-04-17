import http.client
import os


class HttpClient():
    def __init__(self):
        self.client_id = None
        self.unique_file_id = 256
        self.file_id_and_name_dict = {}

        self.ERROR = 'Error'
        self.CONTENT_NAME = 'Content-Name'
        self.CONTENT_EXT = 'Content-Extension'
        self.CONTENT_LEN = 'Content-Length'
        self.CONTENT_SIZE = 'Content-Size'
        self.CLIENT_ID = 'Client-id'
        self.CONTENT_ID = 'Content-id'
        self.REMOVABLE_TYPE = 'Removable-Type'
        self.DOWNLOAD_TYPE = 'download'
        self.UPLOAD_TYPE = 'upload'


    def connect_to_server(self, address, port):
        self.connection = http.client.HTTPConnection(address, port)


    def get_unique_file_id(self):
        self.unique_file_id += 1
        return id(self.unique_file_id)


    def initialization(self):
        headers = {self.CLIENT_ID: str(self.client_id)}
        self.connection.request(method='INIT', url='/', body='', headers=headers)
        response = self.connection.getresponse()
        error = response.getheader(self.ERROR)

        if not error:
            self.client_id = response.getheader(self.CLIENT_ID)

        return response.status, response.reason, error


    def upload_file(self, file_path):
        full_file_name = os.path.basename(file_path)
        file_name = str(self.get_unique_file_id())
        file_extension = os.path.splitext(full_file_name)[1]
        file_size = os.path.getsize(file_path)

        headers = {self.CONTENT_NAME: file_name,
                   self.CONTENT_EXT: file_extension,
                   self.CLIENT_ID: str(self.client_id),
                   self.CONTENT_LEN: str(file_size)}

        self.connection.request(method='TEST', url='/', headers=headers)
        response = self.connection.getresponse()
        error = response.getheader(self.ERROR)
        if not error:
            try:
                file = open(file_path, 'rb').read()
                self.connection.request(method='PUT', url='/', body=file, headers=headers)
                response = self.connection.getresponse()
                info = response.getheader(self.ERROR)

                if not error:
                    file_id = response.getheader(self.CONTENT_ID)
                    self.file_id_and_name_dict[file_id] = file_name
                    info = file_id
                    
            except Exception as error:
                info = error

            return response.status, response.reason, info

        return response.status, response.reason, error


    def download_file(self, file_id, file_path):
        headers = {self.CONTENT_ID: str(file_id)}
        self.connection.request(method='GET', url='/', headers=headers)

        response = self.connection.getresponse()
        error = response.getheader(self.ERROR)

        if not error:
            file = response.read()

            saved_file = open(file_path, 'wb')
            saved_file.write(file)
            error = None

        return response.status, response.reason, error


    def get_info_about_file(self, file_id, file_name):
        headers = {self.CONTENT_ID: str(file_id)}
        self.connection.request(method='HEAD', url='/', headers=headers)

        response = self.connection.getresponse()
        error = response.getheader(self.ERROR)

        if not error:
            file_size = response.getheader(self.CONTENT_SIZE)
            return response.status, response.reason, f'Name => {file_name}\nSize => {file_size}'

        return response.status, response.reason, error


    def delete_file(self, file_id, removable_type):
        headers = {self.CONTENT_ID: str(file_id),
                    self.CLIENT_ID: str(self.client_id),
                    self.REMOVABLE_TYPE: removable_type}

        self.connection.request(method='DELETE', url='/', headers=headers)

        response = self.connection.getresponse()
        error = response.getheader(self.ERROR)
        return response.status, response.reason, error


    def delete_download_file(self, file_id):
        return self.delete_file(file_id, self.DOWNLOAD_TYPE)


    def delete_upload_file(self, file_id):
        return self.delete_file(file_id, self.UPLOAD_TYPE)


    def clear_download_buffer(self):
        headers = {self.CLIENT_ID: str(self.client_id)}
        self.connection.request(method='CLEAR', url='/', headers=headers)
        response = self.connection.getresponse()
