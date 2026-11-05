COUNTRY_ALIASES = {
    "afgahnistan": "afghanistan",
    "afganistan": "afghanistan",
    "afghnaistan": "afghanistan",
    "azerbaijcan": "azerbaijan",
    "azerbaycan": "azerbaijan",
    "beninese": "benin",
    "bostvana": "botswana",
    "bostwana": "botswana",
    "bottwana": "botswana",
    "brundi": "burundi",
    "burkine faso": "burkina faso",
    "cad": "chad",
    "cameron": "cameroon",
    "central africa": "central african republic",
    "centrla africa": "central african republic",
    "cibuti": "djibouti",
    "comoros islands": "comoros",
    "democratic kongo": "congo",
    "democratic republic of the congo": "congo",
    "djibbouti": "djibouti",
    "djbouti": "djibouti",
    "djibout": "djibouti",
    "egpyt": "egypt",
    "eritre": "eritrea",
    "equator": "equatorial guinea",
    "ethiyopia": "ethiopia",
    "etiyopia": "ethiopia",
    "etiyopya": "ethiopia",
    "fas": "morocco",
    "fildisi sahili": "cote d'ivoire",
    "fildisi sahilleri": "cote d'ivoire",
    "filistin": "palestine",
    "gabonese": "gabon",
    "gambiya": "gambia",
    "gana": "ghana",
    "gine": "guinea",
    "guines": "guinea",
    "iraaq": "iraq",
    "irak": "iraq",
    "iranian": "iran",
    "ivory": "cote d'ivoire",
    "ivory coast": "cote d'ivoire",
    "kamerun": "cameroon",
    "kazakhistan": "kazakhstan",
    "kingdom saudi arabia": "saudi arabia",
    "komor ad": "comoros",
    "kongo": "congo",
    "kuveyt": "kuwait",
    "lebonan": "lebanon",
    "liberya": "liberia",
    "mauretania": "mauritania",
    "misir": "egypt",
    "moldovia": "moldova",
    "nigerya": "nigeria",
    "nijeria": "nigeria",
    "o afrika": "central african republic",
    "orta afrika": "central african republic",
    "palestina": "palestine",
    "palastine": "palestine",
    "palesitine": "palestine",
    "paletine": "palestine",
    "republic of benin": "benin",
    "republic of botswana": "botswana",
    "republic of chad": "chad",
    "republic of guatemala": "guatemala",
    "ruanda": "rwanda",
    "rusia": "russia",
    "senegalese": "senegal",
    "somali": "somalia",
    "somalie": "somalia",
    "sierra lenone": "sierra leone",
    "sierra lone": "sierra leone",
    "sleone": "sierra leone",
    "suriye": "syria",
    "syira": "syria",
    "tanzanya": "tanzania",
    "tunusia": "tunisia",
    "turkey": "turkiye",
}


def unalias_country(s):
    if s in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[s]
    return s


def unalias_province(s):
    if s == "zmir":
        return "izmir"
    if s == "baikesir" or s == "baliesir":
        return "balikesir"
    return s


def unalias_district(s):
    if s == "ayvaci":
        return "ayvacik"
    if s == "yeni foca":
        return "yenifoca"
    return s
