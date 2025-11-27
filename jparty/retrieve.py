import requests
from bs4 import BeautifulSoup
from html import unescape
import re
import json
from jparty.game import Question, Board, FinalBoard, GameData
import logging
import csv
from jparty.constants import MONIES, MED_POINTS


def list_to_game(s):
    """
    Parse standard Jeopardy format from Google Sheets.
    Template link: https://docs.google.com/spreadsheets/d/1_vBBsWn-EVc7npamLnOKHs34Mc2iAmd9hOGSzxHQX0Y/edit?usp=sharing
    """
    alpha = "BCDEFG"  # columns
    boards = []
    # gets single and double jeopardy rounds
    for n1 in [1, 14]:
        categories = s[n1 - 1][1:7]
        questions = []
        for row in range(5):
            for col, cat in enumerate(categories):
                address = alpha[col] + str(row + n1 + 1)
                index = (col, row)
                text = s[row + n1][col + 1]
                answer = s[row + n1 + 6][col + 1]
                value = int(s[row + n1][0])
                dd = address in s[n1 - 1][-1]
                questions.append(Question(index, text, answer, cat, value, dd))

        boards.append(Board(categories, questions, dj=(n1 == 14)))

    # gets final jeopardy round
    fj = s[-1]
    index = (0, 0)
    text = fj[2]
    answer = fj[3]
    category = fj[1]
    question = Question(index, text, answer, category)
    boards.append(FinalBoard(category, question))
    date = fj[5]
    comments = fj[7]
    return GameData(boards, date, comments)


def _find_section_headers(s, start_row=0):
    """
    Dynamically find section header rows by searching for keywords.

    Returns dict with section names as keys and row indices as values.
    """
    sections = {
        "questions": None,
        "answers": None,
        "rationale": None,
        "images": None,
        "difficulty": None,
        "specialty": None,
    }

    keywords = {
        "answer": "answers",
        "rationale": "rationale",
        "image": "images",
        "difficulty": "difficulty",
        "specialty": "specialty",
    }

    for row_idx in range(start_row, min(start_row + 50, len(s))):
        if row_idx >= len(s) or not s[row_idx]:
            continue
        first_cell = str(s[row_idx][0]).lower().strip()
        for keyword, section in keywords.items():
            if keyword in first_cell:
                sections[section] = row_idx
                break

    return sections


def _find_round_starts(s):
    """
    Dynamically find round start rows by looking for category headers.

    Returns list of (round_start_row, is_medical_format) tuples.
    """
    rounds = []
    is_medical_format = False

    for row_idx in range(len(s)):
        if row_idx >= len(s) or not s[row_idx]:
            continue

        # Look for rows that look like category headers (non-numeric first cell, multiple columns)
        first_cell = str(s[row_idx][0]).strip().lower()
        row_len = len([c for c in s[row_idx] if c])

        # Check for "round 1" or "round 2" markers, or rows with value labels
        if first_cell in ["", "value", "round 1", "round 2", "jeopardy", "double jeopardy"]:
            # Check if next row has point values (100, 200, etc.)
            if row_idx + 1 < len(s) and s[row_idx + 1]:
                next_first = str(s[row_idx + 1][0]).strip()
                if next_first.isdigit() and int(next_first) in [100, 200]:
                    rounds.append(row_idx + 1)

        # Also check for rationale/image headers to detect medical format
        if any(kw in first_cell for kw in ["rationale", "image", "difficulty", "specialty"]):
            is_medical_format = True

    # Default fallback: standard positions
    if not rounds:
        rounds = [1, 14]

    return rounds, is_medical_format


def list_to_medical_game(s):
    """
    Parse medical education format from Google Sheets.

    Dynamically detects section headers (ANSWERS, RATIONALE, IMAGES, etc.)
    to handle sheets with varying row spacing.

    Expected Medical Education Google Sheets format:
    Row 0: Headers - Value, Cat1, Cat2, Cat3, Cat4, Cat5, Cat6, DD
    Row 1-5: Questions with point values
    [ANSWERS] section header
    Row N-N+4: Answers
    [RATIONALE] section header (MEDICAL EXTENSION)
    Row M-M+4: Rationales
    [IMAGES] section header (MEDICAL EXTENSION)
    ...and so on

    Similar structure for Round 2, then Final Jeopardy at the end.
    """
    alpha = "BCDEFG"  # columns
    boards = []

    # Dynamically find round starts and detect format
    detected_rounds, is_medical_format = _find_round_starts(s)

    # Also check row count as fallback
    if len(s) > 40:
        is_medical_format = True

    # Use detected rounds or calculate from sheet structure
    # Round 1 at row 1, Round 2 follows after round 1's data sections
    if is_medical_format and len(detected_rounds) < 2:
        # Medical format: Round 1 data spans ~36 rows, Round 2 starts after
        round_starts = [1, 37]
    elif len(detected_rounds) >= 2:
        round_starts = detected_rounds[:2]
    else:
        round_starts = [1, 14]

    for round_idx, n1 in enumerate(round_starts):
        if n1 >= len(s):
            break

        # Find section headers for this round
        sections = _find_section_headers(s, n1 - 1)

        categories = s[n1 - 1][1:7] if len(s[n1 - 1]) >= 7 else s[n1 - 1][1:]
        questions = []

        # Calculate answer offset: either from detected section or default (+6)
        answer_offset = (sections["answers"] - n1 + 1) if sections["answers"] else 6

        for row in range(5):
            if n1 + row >= len(s):
                break

            for col, cat in enumerate(categories):
                address = alpha[col] + str(row + n1 + 1) if col < len(alpha) else ""
                index = (col, row)

                # Get question text
                q_row = s[n1 + row] if n1 + row < len(s) else []
                text = q_row[col + 1] if col + 1 < len(q_row) else ""

                # Get answer using dynamic or default offset
                a_row_idx = n1 + answer_offset + row
                a_row = s[a_row_idx] if a_row_idx < len(s) else []
                answer = a_row[col + 1] if col + 1 < len(a_row) else ""

                # Get value
                value = int(q_row[0]) if q_row and q_row[0].isdigit() else MED_POINTS[round_idx][row]

                # Check daily double
                dd_col = s[n1 - 1][-1] if len(s[n1 - 1]) > 0 else ""
                dd = address in dd_col

                # Medical education extensions (if available)
                rationale = None
                image_url = None
                difficulty = None
                specialty = None

                if is_medical_format:
                    # Rationale - use detected section or calculate offset
                    if sections["rationale"]:
                        rationale_base = sections["rationale"] + 1
                    else:
                        rationale_base = n1 + 12
                    if rationale_base + row < len(s):
                        r_row = s[rationale_base + row]
                        rationale = r_row[col + 1] if col + 1 < len(r_row) and r_row[col + 1] else None

                    # Images - use detected section or calculate offset
                    if sections["images"]:
                        image_base = sections["images"] + 1
                    else:
                        image_base = n1 + 18
                    if image_base + row < len(s):
                        i_row = s[image_base + row]
                        image_url = i_row[col + 1] if col + 1 < len(i_row) and i_row[col + 1] else None

                    # Difficulty - use detected section or calculate offset
                    if sections["difficulty"]:
                        diff_base = sections["difficulty"] + 1
                    else:
                        diff_base = n1 + 24
                    if diff_base + row < len(s):
                        d_row = s[diff_base + row]
                        difficulty = d_row[col + 1] if col + 1 < len(d_row) and d_row[col + 1] else None

                    # Specialty - use detected section or calculate offset
                    if sections["specialty"]:
                        spec_base = sections["specialty"] + 1
                    else:
                        spec_base = n1 + 30
                    if spec_base + row < len(s):
                        sp_row = s[spec_base + row]
                        specialty = sp_row[col + 1] if col + 1 < len(sp_row) and sp_row[col + 1] else None

                # Determine question type
                question_type = "standard"
                if image_url:
                    question_type = "image"
                elif len(text) > 200:  # Long questions are likely case vignettes
                    question_type = "case"

                questions.append(Question(
                    index=index,
                    text=text,
                    answer=answer,
                    category=cat,
                    value=value,
                    dd=dd,
                    image_url=image_url,
                    rationale=rationale,
                    difficulty=difficulty,
                    specialty=specialty,
                    question_type=question_type
                ))

        boards.append(Board(categories, questions, dj=(round_idx == 1)))

    # Final Jeopardy
    fj = s[-1] if len(s) > 0 else []
    if len(fj) >= 4:
        index = (0, 0)
        text = fj[2]
        answer = fj[3]
        category = fj[1]

        # Medical extensions for Final Jeopardy
        rationale = fj[4] if len(fj) > 4 else None
        image_url = fj[5] if len(fj) > 5 else None
        difficulty = fj[6] if len(fj) > 6 else None
        specialty = fj[7] if len(fj) > 7 else None

        question = Question(
            index=index,
            text=text,
            answer=answer,
            category=category,
            rationale=rationale,
            image_url=image_url,
            difficulty=difficulty,
            specialty=specialty
        )
        boards.append(FinalBoard(category, question))

    # Get metadata
    date = fj[8] if len(fj) > 8 else "Medical Education Game"
    comments = fj[9] if len(fj) > 9 else ""

    return GameData(boards, date, comments)


def detect_sheet_format(s):
    """Detect whether the sheet is standard or medical format."""
    if len(s) < 15:
        return "standard"

    # Check for medical format indicators
    # Look for "Rationale" or "Image" or "Difficulty" headers
    for row in s[:40]:
        if row and len(row) > 0:
            first_cell = str(row[0]).lower()
            if any(keyword in first_cell for keyword in ["rationale", "image", "difficulty", "specialty"]):
                return "medical"

    # Check if there are more than 30 rows (medical format is larger)
    if len(s) > 40:
        return "medical"

    return "standard"


def get_Gsheet_game(file_id, force_medical_format=False):
    """
    Get game from Google Sheets.

    Args:
        file_id: The Google Sheets file ID
        force_medical_format: If True, always use medical format parser

    Returns:
        GameData object with parsed game content
    """
    csv_url = f"https://docs.google.com/spreadsheet/ccc?key={file_id}&output=csv"
    with requests.get(csv_url, stream=True) as r:
        lines = (line.decode("utf-8") for line in r.iter_lines())
        r3 = csv.reader(lines)
        data = list(r3)

        # Detect format and use appropriate parser
        if force_medical_format or detect_sheet_format(data) == "medical":
            logging.info("Using medical education format parser")
            return list_to_medical_game(data)
        else:
            logging.info("Using standard format parser")
            return list_to_game(data)


class RetrievalException(Exception):
    pass


class IncompleteException(Exception):
    pass


def get_game(game_id):
    if len(str(game_id)) < 7:
        try:
            logging.info("trying jarchive")
            return get_jarchive_game(game_id)
        except RetrievalException as e:
            logging.error(e)
            logging.info("trying wayback")
            return get_wayback_game(game_id)
    else:
        return get_Gsheet_game(str(game_id))


def get_jarchive_game(game_id):
    return get_generic_game(
        game_id, f"http://www.j-archive.com/showgame.php?game_id={game_id}"
    )


def get_wayback_game(game_id):
    # kudos to Abhi Kumbar: https://medium.com/analytics-vidhya/the-wayback-machine-scraper-63238f6abb66
    # this query's the wayback cdx api for possible instances of the saved jarchive page with the specified game id & returns the latest one
    JArchive_url = f"j-archive.com/showgame.php?game_id={str(game_id)}"  # use the url w/o the http:// or https:// to include both in query
    url = f"http://web.archive.org/cdx/search/cdx?url={JArchive_url}&collapse=digest&limit=-2&fastLatest=true&output=json"  # for some reason, using limit=-1 does not work
    urls = requests.get(url).text
    parse_url = json.loads(urls)  # parses the JSON from urls.
    if len(parse_url) == 0:  # if no results, return None
        logging.info("no games found in wayback")
        # alternative: use fallback to get game from scraping j-archive directly
        raise RetrievalException("no games found in wayback")

    # Extracts timestamp and original columns from urls and compiles a url list.
    url_list = []
    for i in range(1, len(parse_url)):  # gets the wayback url
        orig_url = parse_url[i][2]
        tstamp = parse_url[i][1]
        waylink = tstamp + "/" + orig_url
        final_url = f"http://web.archive.org/web/{waylink}"
        url_list.append(final_url)
    latest_url = url_list[-1]
    return get_generic_game(game_id, latest_url)


def findanswer(clue):
    return re.findall(r'correct_response">(.*?)</em', unescape(str(clue)))[0]


def get_generic_game(game_id, url):
    logging.info(f"getting game {game_id} from url {url}")
    try:
        r = requests.get(url, timeout=5)
    except requests.exceptions.ConnectTimeout as e:
        logging.info(repr(type(e)))
        raise RetrievalException(repr(e))

    logging.info(f"returned status {r.status_code}")
    if r.status_code != 200:
        raise RetrievalException(f"{url} returned HTTP code {r.status_code}")

    soup = BeautifulSoup(r.text, "html.parser")
    datesearch = re.search(r"<h1>(.*?)</h1>", str(soup.select("#game_title > h1")[0]))

    if datesearch is None:
        raise RetrievalException("Cannot get game summary")

    date = datesearch.groups()[0]
    comments = soup.select("#game_comments")[0].contents
    comments = comments[0] if len(comments) > 0 else ""

    # Normal Rounds
    boards = []
    rounds = soup.find_all(class_="round")
    for i, ro in enumerate(rounds):
        categories_objs = ro.find_all(class_="category")
        categories = [c.find(class_="category_name").text for c in categories_objs]
        questions = []
        for clue in ro.find_all(class_="clue"):
            text_obj = clue.find(class_="clue_text")
            if text_obj is None:
                raise IncompleteException()

            text = text_obj.text
            index_key = text_obj["id"]
            index = (
                int(index_key[-3]) - 1,
                int(index_key[-1]) - 1,
            )  # get index from id string
            dd = clue.find(class_="clue_value_daily_double") is not None
            value = MONIES[i][index[1]]
            answer = findanswer(clue)
            questions.append(
                Question(index, text, answer, categories[index[0]], value, dd)
            )
        boards.append(Board(categories, questions, dj=(i == 1)))

    # Final Jeopardy
    final_round_obj = soup.find_all(class_="final_round")[0]
    category_obj = final_round_obj.find_all(class_="category")[0]
    category = category_obj.find(class_="category_name").text
    clue = final_round_obj.find_all(class_="clue")[0]
    text_obj = clue.find(class_="clue_text")
    if text_obj is None:
        raise IncompleteException()

    text = text_obj.text
    answer = findanswer(final_round_obj)
    question = Question((0, 0), text, answer, category)

    boards.append(FinalBoard(category, question))

    return GameData(boards, date, comments)


def get_game_sum(soup):
    date = re.search(
        r"- \w+, (.*?)$", soup.select("#game_title > h1")[0].contents[0]
    ).groups()[0]
    comments = soup.select("#game_comments")[0].contents

    return date, comments


def get_random_game():
    r = requests.get("http://j-archive.com/")
    soup = BeautifulSoup(r.text, "html.parser")

    link = soup.find_all(class_="splash_clue_footer")[1].find("a")["href"]
    return int(link[21:])
