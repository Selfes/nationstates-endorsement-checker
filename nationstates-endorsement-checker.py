#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree as ET
import time, sys

def get_api_data(url: str, your_nation: str) -> bytes:
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        return response.read()


def parse_nationstates_data(data_tag: str, xml_data: bytes) -> list[str]:
    root = ET.fromstring(xml_data)
    data = root.find(data_tag)
    if data is not None and data.text:
        return sorted(data.text.split(','))
    return []


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    Taken from https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)

    # clear the line
    sys.stdout.write('\r\033[K')

    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def get_endorsable_nations(your_nation: str, exclude_list: list[str]) -> list[str]:
    # get the region
    region_url = f"https://www.nationstates.net/cgi-bin/api.cgi?nation={your_nation}&q=region"
    region = parse_nationstates_data("REGION", get_api_data(region_url, your_nation))[0]

    # get a list of WA nations in the region
    wanation_url = f"https://www.nationstates.net/cgi-bin/api.cgi?region={region}&q=wanations"
    wa_nations = set(parse_nationstates_data("UNNATIONS", get_api_data(wanation_url, your_nation)))

    # Remove unnecessary nations
    wa_nations = wa_nations - {your_nation} - set(exclude_list)

    endorsable = []
    l = len(wa_nations)
    printProgressBar(0, l, prefix = 'Progress []:', suffix = 'Complete', length = 50)

    for i, nation_to_check in enumerate(wa_nations):
        printProgressBar(i+1, l, prefix = f'Progress [{nation_to_check}]:', suffix = 'Complete', length = 50)
        if nation_to_check == your_nation and nation_to_check in exclude_list:
            continue

        time.sleep(0.65)  # Respect rate limit

        nation_url = f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nation_to_check}&q=endorsements"
        current_endorsements = parse_nationstates_data("ENDORSEMENTS", get_api_data(nation_url, your_nation))

        if current_endorsements is not None and your_nation not in current_endorsements:
            endorsable.append(nation_to_check)

    return sorted(endorsable)


def nation_to_url(nation: str) -> str:
    return f"https://www.nationstates.net/nation={nation.lower().replace(' ', '_')}"


html_template = """
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <title>Nationstates Endorsement List for {nation}</title>
    <script>
        function openLinksWithDelay() {{
            // Get all <li> elements inside the list
            const links = document.querySelectorAll('#nations-to-endorse li a');

            let index = 0;

            function openNextLink() {{
                if (index < links.length) {{
                    const url = links[index].href; // Get the href attribute of the <a> tag
                    window.open(url, '_blank'); // Open the link in a new tab
                    index++;
                    setTimeout(openNextLink, {delay}); // Set the delay (to not open every link at once)
                }}
            }}

            openNextLink(); // Start opening links
        }}
    </script>
</head>
<body>
    <h1>Endorsement List</h1>
    <ul id=\"nations-to-endorse\">
        {links}
    </ul>

    <button onclick=\"openLinksWithDelay()\">Open Nation pages</button>
</body>
</html>
"""

if __name__ == "__main__":
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description="Utility to return a list of nations to endorse")
    parser.add_argument("nation", type=str, help="Your nation")
    parser.add_argument('-e','--exclude', default=[], metavar="NATION", nargs='+', help='List of excluded nation')
    parser.add_argument('-d','--delay', default=500, type=int, help='set delay for opening links in html in miliseconds (default: 500)')
    args = parser.parse_args()

    startTime = datetime.now()

    endorsable_nations = get_endorsable_nations(args.nation.lower().replace(' ', '_'),
                                                [s.lower().replace(' ', '_') for s in args.exclude])

    print("Nations you can endorse:")
    for nation in endorsable_nations:
        print(f"{nation}: {nation_to_url(nation)}")

    # Create a html page for easy page opening
    with open('to_endorse_nation.html', 'w') as file:
        urls = ''.join(f'<li><a href="{nation_to_url(nation)}">{nation}</a></li>\n' for nation in endorsable_nations)
        file.write(html_template.format(nation=args.nation, links=urls, delay=args.delay))

    print("Time taken: " + str(datetime.now() - startTime))
