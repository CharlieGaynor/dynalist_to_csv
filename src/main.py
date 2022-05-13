from functions.scrape_with_api import scraper


if __name__ == "__main__":
    api_scraper = scraper()
    while True:
        api_scraper.get_all_files()
        user_input: str = input(
            "Give file to scrape, return to exit. Type 'revert' to undo the previous color changes\n"
        )
        if user_input == "":
            break

        if user_input.lower() == "revert":
            try:
                nodes_to_change_colors = api_scraper.nodes_that_have_changed_color
                if nodes_to_change_colors == []:
                    print("No nodes to change colors u silly billy")
                else:
                    api_scraper.update_node_colors(
                        nodes_to_change_colors, file_number, color=1
                    )
            except NameError:
                print("")

        else:
            try:
                file_number = int(user_input)
                api_scraper.scrape_file(file_number)
                print("scraped file :D")
            except ValueError:
                print("bad input, please try again :)")

        
        
