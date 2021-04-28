import re
import os
import os.path as path

SPECIAL_CHARACTER_REGEX = r"[`'.]"
NON_WORD_REGEX = r"[\W]"
BEGINNING_THE =r"^the\s"

class MediaInformation:

    def __init__(self, imdb_id, original_name, name, year):
        self.imdb_id = imdb_id
        self.original_name = original_name
        self.name = name
        self.year = year

    def __repr__(self) -> str:
        return str(self.__dict__)

def clean_movie_title(title) -> str:
    if title is None:
        return None
    clean_title = re.sub(BEGINNING_THE, '', title, flags=re.IGNORECASE)
    clean_title = clean_title.replace('&', 'and')
    clean_title = re.sub(SPECIAL_CHARACTER_REGEX, '+', clean_title)
    clean_title = re.sub(NON_WORD_REGEX, '+', clean_title)
    clean_title = re.sub(r"\+{2,}", '+', clean_title)
    return clean_title.replace('+', ' ')

# Regexes from https://github.com/Radarr/Radarr/blob/627ab64fd023269c8bedece61e529329600a3419/src/NzbDrone.Core/Parser/Parser.cs
EDITION_REGEX = r"\(?\b(?P<edition>(((Recut.|Extended.|Ultimate.)?(Director.?s|Collector.?s|Theatrical|Ultimate|Extended|Despecialized|(Special|Rouge|Final|Assembly)(?=(.(Cut|Edition|Version)))|\d{2,3}(th)?.Anniversary)(.(Cut|Edition|Version))?(.(Extended|Uncensored|Remastered|Unrated|Uncut|IMAX|Fan.?Edit))?|((Uncensored|Remastered|Unrated|Uncut|IMAX|Fan.?Edit|Edition|Restored|((2|3|4)in1))))))\b\)?"
TITLE_REGEXES = [
    r"^(?P<title>(?![(\[]).+?)((\W|_))(" + EDITION_REGEX + r".{1,3})?(?:(?<!(19|20)\d{2}.)(German|French|TrueFrench))(.+?)(?=((19|20)\d{2}|$))(?P<year>(19|20)\d{2}(?!p|i|\d+|\]|\W\d+))?(\W+|_|$)(?!\\)",
    r"^(?P<title>(?![(\[]).+?)?(?:(?:[-_\W](?<![)\[!]))*" + EDITION_REGEX + r".{1,3}(?P<year>(1(8|9)|20)\d{2}(?!p|i|\d+|\]|\W\d+)))+(\W+|_|$)(?!\\)",
    r"^(?P<title>(?![(\[]).+?)?(?:(?:[-_\W](?<![)\[!]))*(?P<year>(1(8|9)|20)\d{2}(?!p|i|(1(8|9)|20)\d{2}|\]|\W(1(8|9)|20)\d{2})))+(\W+|_|$)(?!\\)",
    r"^(?P<title>.+?)?(?:(?:[-_\W](?<![()\[!]))*(?P<year>(\[\w *\])))+(\W+|_|$)(?!\\)",
    r"^(?P<title>(?![(\[]).+?)?(?:(?:[-_\W](?<![)!]))*(?P<year>(1(8|9)|20)\d{2}(?!p|i|\d+|\W\d+)))+(\W+|_|$)(?!\\)",
    r"^(?P<title>.+?)?(?:(?:[-_\W](?<![)\[!]))*(?P<year>(1(8|9)|20)\d{2}(?!p|i|\d+|\]|\W\d+)))+(\W+|_|$)(?!\\)"
]
REVERSE_TITLE_REGEX = r"(?:^|[-._ ])(p027|p0801)[-._ ]"
FILE_EXTENSION_REGEX = r"\.[a-z0-9]{2,4}$"
IMDB_REGEX = r"(?P<imdbid>tt\d{7,8})"
SIMPLE_TITLE_REGEX = r"\s*(?:480[ip]|576[ip]|720[ip]|1080[ip]|2160[ip]|[xh][\W_]?26[45]|DD\W?5\W1|[<>?*:|]|848x480|1280x720|1920x1080|(8|10)b(it)?)"
WEBSITE_PREFIX_REGEX = r"^\[\s*[-a-z]+(\.[a-z]+)+\s*\][- ]*|^www\.[a-z]+\.(?:com|net|org)[ -]*"
WEBSITE_POSTFIX_REGEX = r"\[\s*[-a-z]+(\.[a-z0-9]+)+\s*\]$"
CLEAN_QUALITY_BRACKETS_REGEX = r"\[[a-z0-9 ._-]+\]$"

def _parse_movie_title(title: str) -> MediaInformation:
    original_title = title
    print(f"Parsing string '{title}'")

    if re.match(REVERSE_TITLE_REGEX, title, re.IGNORECASE):
        print(f"Reversed title found")
        title_without_ex = remove_file_extension(title)
        title_without_ex = title_without_ex[::-1]
        title = title_without_ex + title[len(title_without_ex):]
    release_title = remove_file_extension(title)
    release_title = release_title.rstrip('-').rstrip('_')
    # Fix some weird brackets
    release_title = release_title.replace('【', '[').replace('】', ']')
    simple_title = re.sub(SIMPLE_TITLE_REGEX, '', release_title, flags=re.IGNORECASE)
    simple_title = re.sub(WEBSITE_PREFIX_REGEX, '', simple_title, flags=re.IGNORECASE)
    simple_title = re.sub(WEBSITE_POSTFIX_REGEX, '', simple_title, flags=re.IGNORECASE)

    simple_title = re.sub(CLEAN_QUALITY_BRACKETS_REGEX, '', simple_title)
    # Actually do the title parsing
    for regex in TITLE_REGEXES:
        match = re.match(regex, simple_title, re.IGNORECASE)
        if match is not None:
            groups = match.groupdict()
            title = clean_movie_title(groups.get('title', None))
            year = groups.get('year', None)
            print(f"title={title}, year={year}")
            imdb_match = re.findall(IMDB_REGEX, simple_title)
            return MediaInformation(imdb_match[0] if len(imdb_match) > 0 else None, original_title, title, year)
    # if we get this far, we didn't get a match
    return None

def remove_file_extension(title: str) -> str:
    return re.sub(FILE_EXTENSION_REGEX, '', title, flags=re.IGNORECASE)


def parse_file(file: str) -> MediaInformation:
    basename = os.path.splitext(os.path.basename(file))[0]
    return _parse_movie_title(basename)

if __name__ == "__main__":
    print(parse_file(
        "~/Desktop/Batman.The.Dark.Knight.2008.1080p.BluRay.x264.YIFY.mp4"))
