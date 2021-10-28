import requests
from flask import Blueprint


admin = Blueprint("admin", __name__)


@admin.route("/")
def index():
    return "main page"


@admin.route("/definitions/<word>")
def get_info(word):

    error_check_result = initial_error_check(word)
    result = {
        "success": False,
        "error_message": "",
        "definitions": [],
    }
    if error_check_result[0]:

        json_data = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        ).json()

        if (
            type(json_data) == dict
            and json_data["title"]
            and json_data["title"] == "No Definitions Found"
        ):
            result["error_message"] = "No definitions dound"
        else:
            if type(json_data) == list and json_data[0]["meanings"][0]["definitions"]:
                definitions = [
                    definition["definition"]
                    for definition in json_data[0]["meanings"][0]["definitions"]
                ]
                result["success"] = True
                result["definitions"] = definitions
            else:
                result["error_message"] = "incorect data from dictionary"
    else:
        result["error_message"] = error_check_result[1]

    return frontend_crutch(result)


def initial_error_check(word_to_chech, max_len=45):
    success = True
    error_message = ""
    if not word_to_chech:
        success = False
        error_message = "empty string"
    elif len(word_to_chech) > max_len:
        success = False
        error_message = f"word is too long. Max {max_len} characters"
    else:
        for character in word_to_chech:
            if not character.isalpha():
                success = False
                error_message = f"unsupported character: {character}"
                break

    return (success, error_message)


def frontend_crutch(backend_result):
    html_result = "success: " + str(backend_result["success"]) + "<br>"
    html_result += "error_message: " + backend_result["error_message"] + "<br>"
    html_result += "definitions:<br>&emsp;" + "<br>&emsp;".join(backend_result["definitions"])

    return html_result


@admin.app_errorhandler(404)
def handle_404(error):
    print(error)
    return "<center><b><mark> Page not found </mark></b></center>"
