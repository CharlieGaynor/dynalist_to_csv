from typing import Union
import requests
import json
import time
from data_classes.response import Response

class scraper:
    """
    Use the API to scrape dynalist to get the dom
    """

    def __init__(self) -> None:
        self.token = json.load(open("api_token.json")).get("token")
        self.file_contents: dict = {}
        self.file_questions_map: dict[str, dict[str, str]] = {}
        self.nodes_that_have_changed_color: list = []

    @staticmethod
    def response_to_dict(response: str) -> Response:
        """
        Converts a response from dynalist,from text,
        and returns it
        """
        return eval(response.replace("false", "False").replace("true", "True"))

    def test_connection(self):

        response = requests.post(
            "https://dynalist.io/api/v1/file/list", json.dumps({"token": self.token})
        ).text

        # Now convert the text representation of a dictionary, into a dictionary∏
        response = self.response_to_dict(response)
        code = response.get("_code", None)
        if code is None:
            print("Nothing found, code not working :(")
        else:
            print("Token seems to work")

    def get_all_files(self) -> None:
        """
        grabs all folders and files from within dynalist by querying the API
        Stores information about the files in self.file_info
        Stores dictionary of file id: file name, to be able to fetch the full doc
        """

        raw_response: str = requests.post(
            "https://dynalist.io/api/v1/file/list", json.dumps({"token": self.token})
        ).text

        # Now convert the text representation of a dictionary, into a dictionary∏
        response = self.response_to_dict(raw_response)

        # files_info has form: name (type): number
        files_info: list[str] = []
        filenumber_id_map: dict[int, str] = {}

        current_file: int = 1
        for file in response["files"]:
            title = file["title"]
            file_type = file["type"]
            id = file["id"]

            files_info.append(f"{title} ({file_type}): {current_file}")
            filenumber_id_map[current_file] = id

            current_file += 1

        self.files = files_info
        self.filenumber_id_map = filenumber_id_map
        print("Files to choose from:")
        print("\t", "\n\t".join(self.files), sep="")

    def get_file_contents(self, filenumber: int) -> None:

        file_id = self.filenumber_id_map[filenumber]
        args = {"token": self.token, "file_id": file_id}

        response = requests.post(
            "https://dynalist.io/api/v1/doc/read", json.dumps(args)
        ).text
        self.file_contents[file_id] = self.response_to_dict(response)

    def scrape_file(self, filenumber: int) -> None:
        """
        Gets all the question: answers from the file.
        Also updates the colors to green, to mark as 'done'

        Args:
            filenumber (int): Which file to scrape?
        """

        self.get_file_contents(filenumber)

        file_id = self.filenumber_id_map[filenumber]
        file_contents = self.file_contents[file_id]
        file_title = file_contents["title"]

        question_answer_map: dict[str, str] = {}
        id_node_store: dict[str, dict] = {}

        if file_contents.get("nodes", None) is None:
            print("Nothing found within this document - did you specify a folder?")
            return

        nodes: list[dict] = file_contents["nodes"]
        for node in nodes:
            id_node_store[node["id"]] = node

        question_strings = [
            "question:",
            "questions:",
            "question",
            "questions",
        ]

        nodes_to_change_color: list[str] = []

        for node in nodes:

            node_text: str = node["content"]
            if node_text.lower().strip() in question_strings:

                question_ids: list[str] = node["children"]
                for question_id in question_ids:

                    # Now need to search for the node with this id
                    question_node = id_node_store[question_id]
                    try:
                        question_color = question_node["color"]
                    except KeyError:
                        question_color = 1

                    if question_color != 4:  # Color 4 == Green

                        question = question_node["content"]
                        nodes_to_change_color.append(question_id)
                        # Process the answers to this question and store
                        answer = ""
                        # Try getting child nodes. If there are none, it's a bad flashcard, skip it
                        # This could be changed to allow single side flashcards
                        try:
                            answer_ids = question_node["children"]
                        except KeyError:
                            continue
                        for answer_id in answer_ids:
                            answer_node = id_node_store[answer_id]
                            answer += answer_node["content"]
                            answer += "<br/>"

                        answer = answer[:-5]  # Removing the last <br/>
                        question_answer_map[question] = answer

        self.file_questions_map[file_title] = question_answer_map

        # Storing nodes incase we want to change back later
        self.nodes_that_have_changed_color = nodes_to_change_color
        self.update_node_colors(nodes_to_change_color, filenumber)

        print("Saving to CSV")
        with open(f"csvs/{file_title}.csv", "w") as f:
            for question, answer in question_answer_map.items():
                f.write(f"{question},{answer}\n")

    def update_node_colors(
        self, nodes_to_change_color: list[str], filenumber: int, color: int = 4
    ) -> None:

        file_id = self.filenumber_id_map[filenumber]
        file_contents = self.file_contents[file_id]

        changes: list[dict] = []
        for node in nodes_to_change_color:
            node_change = {"action": "edit", "node_id": node, "color": color}
            changes.append(node_change)

        changes_file = {
            "token": self.token,
            "file_id": self.filenumber_id_map[filenumber],
            "changes": changes,
        }

        raw_response = requests.post(
            "https://dynalist.io/api/v1/doc/edit", json.dumps(changes_file)
        ).text
        response = self.response_to_dict(raw_response)
        if response.get("_code", None) is None:
            print("Failed to update node_colors :(")
        else:
            print("Sucessfully updated node colors :)")
            if color != 4:
                self.nodes_that_have_changed_color = []
            time.sleep(1.5)
