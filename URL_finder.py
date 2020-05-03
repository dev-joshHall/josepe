"""
File name: URL_finder.py
Purpose: Finds valid URL links within a file and gives the user the option to navigate to a link.
"""
import re
import webbrowser as wb


def get_urls(file):
    with open(file, "r") as f:
        pattern = re.compile(r'(https?://)?(www.)?([a-zA-Z0-9.]+)(\.com|\.org|\.edu)([a-zA-Z0-9+/_.-]*)')
        matches = pattern.finditer(f.read())
        websites = [f"{match.group(3)}{match.group(4)}{match.group(5)}" for match in matches]
    return websites


def main():
    read_file = input("File Name: ")
    websites = get_urls(read_file)
    site_dict = {}
    print("Here are the links we found within the file.")
    for i, site in enumerate(websites):
        site_dict[i] = site
        print(f"({i}) {site}")  # available links for user to choose from
    visit_site = input("Would you like to visit one of these sites(Y/N)? ").upper()
    if visit_site in ("Y" or "YES"):
        site_num = int(input("Enter the number for you like to visit: "))
        wb.open(site_dict[site_num])


if __name__ == '__main__':
    main()
