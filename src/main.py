from functions.scrape_with_api import scraper

if __name__ == "__main__":
    api_scraper = scraper()
    show_files: bool = True
    while True:
        if show_files:
            api_scraper.get_all_files()
            show_files = False
        user_input: str = input(
            "\nGive the file to scrape, return to exit. Type 'revert' to undo the previous color changes, or 'files' to see files again\n"  # noqa: E501
        )
        if user_input == "":
            break  # Not really necessary due to ctrl + c, but helps some users :)

        if user_input.lower() == "files":
            show_files = True

        if user_input.lower() == "revert":
            try:
                nodes_to_change_colors = api_scraper.nodes_that_have_changed_color
                if nodes_to_change_colors == []:
                    print("No nodes to change colors of, you silly billy")
                else:
                    api_scraper.update_node_colors(nodes_to_change_colors, file_number, color=1)
            except NameError:
                print("")

        else:
            try:
                file_number: int = int(user_input)
                api_scraper.scrape_file(
                    file_number,
                    # delimiter=";",
                    # replacement_delimiter=":"
                )  # Change this to change delimiter
                print("Done, file scraped and contents saved.")
            except ValueError:
                print("bad input, please try again :)")
