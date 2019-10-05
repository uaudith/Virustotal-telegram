import requests
import json
from config import Config

apikey = Config.VIRUSTOTAL_API


class virus():
    def __init__(self,file_path):
        self.path=file_path
        self.res=True

    def smallfiles(self):
        path=self.path
        url = 'https://www.virustotal.com/vtapi/v2/file/scan'
        name=path.split('/')[-1]
        params = {'apikey': apikey}

        files = {'file': (name, open(path, 'rb'))}

        response = requests.post(url, files=files, params=params)
        if response==False:
            self.res=False
            return
        
        self.sha1=( response.json()['sha1'])
        print(response.json()['verbose_msg'])
        self.verbose=response.json()['verbose_msg']

    def large_files(self):
        path=self.path
        
        url = 'https://www.virustotal.com/vtapi/v2/file/scan/upload_url'

        params = {'apikey':apikey}

        response = requests.get(url, params=params)
        if response==False:
            self.res=False
            return
        upload_url_json = response.json()
        upload_url = upload_url_json['upload_url']
        print('upload url is',upload_url)
        
        files = {'file': (path, open(path, 'rb'))}
        response = requests.post(upload_url, files=files)
        self.sha1=response.json()['sha1']
        print(response.json()['verbose_msg'])
        self.verbose=response.json()['verbose_msg']
 
    def get_report(self):
        url = 'https://www.virustotal.com/vtapi/v2/file/report'
        sha1=self.sha1

        params = {'apikey': apikey, 'resource': sha1,'allinfo':'false'}

        response = requests.get(url, params=params)
        try:
            self.report=response.json()['scans']
            self.link=response.json()['permalink']
        except Exception as e:
            self.report=e
        print(response.json())
