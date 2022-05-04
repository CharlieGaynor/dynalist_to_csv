import requests
import json

class scraper():
    """
    Use the API to scrape dynalist to get the dom
    """

    def __init__(self):
        self.token = json.load(open('../../api_token.json')).get("token")

    def get_all_files(self):
        """
        grabs all folders and files from within dynalist by querying the API
        Stores information about the files in self.file_info
        Stores dictionary of file id: file name, to be able to fetch the full doc
        """
        
        response = requests.post("https://dynalist.io/api/v1/file/list", json.dumps({'token': self.token})).text
        
        # Now convert the text representation of a dictionary, into a dictionary
        response = eval(response.replace('false', 'False').replace('true', 'True'))
        
        print(response)
        files_info: list[str] = []
        filename_id_map: dict[str: str] = {}

        for file in response['files']:
            title = file['title']
            file_type = file['type']
            id = file['id']

            files_info.append(f"{title} ({file_type})")
            filename_id_map[title] = id
        
        self.files = files_info
        self.filename_id_map = filename_id_map