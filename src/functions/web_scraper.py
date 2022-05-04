import requests

class scraper():
    """
    Use to scrape dynalist to get the dom
    First login, then grab the dom :D
    """

    def __init__(self, web_address: str):
        self.address = web_address

    def get_dom(web_address: str) -> str:
        """
        Grabs the DOM from the web address given

        Args:
            web_address (str): address of dynalist file in browser

        Returns:
            str: THE DOM :D
        """
    
    def login(self, username: str, password: str):
        """logs-in to dynalist

        Args:
            username (str): username to log in with
            password (str): password to log in with
        """
        pass