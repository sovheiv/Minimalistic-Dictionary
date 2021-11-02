import requests
from flask import Blueprint, request


admin = Blueprint("admin", __name__)


@admin.route("/")
def index():
    return "main page"


@admin.route("/definitions")
def get_info():
    word = request.args.get("word")
    result = {
        "success": False,
        "error_message": "",
        "definitions": [],
    }
    error_message = initial_error_check(word)

    if error_message:
        result["error_message"] = error_message
        return result

    json_data = requests.get(
        f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    ).json()

    if (
        type(json_data) == dict
        and json_data["title"]
        and json_data["title"] == "No Definitions Found"
    ):
        result["error_message"] = "No definitions dound"
    elif type(json_data) == list and json_data[0]["meanings"][0]["definitions"]:
        definitions = [
            definition["definition"]
            for definition in json_data[0]["meanings"][0]["definitions"]
        ]
        result["success"] = True
        result["definitions"] = definitions
    else:
        result["error_message"] = "incorect data from dictionary"

    return result


def initial_error_check(word_to_chech, max_len=45):
    error_message = ""
    if not word_to_chech:
        error_message = "empty string"
    elif len(word_to_chech) > max_len:
        error_message = f"word is too long. Max {max_len} characters"
    else:
        for character in word_to_chech:
            if not character.isalpha():
                error_message = f"unsupported character: {character}"
                break

    return error_message


@admin.app_errorhandler(404)
def handle_404(error):
    print(error)
    return "<center><b><mark> Page not found </mark></b></center>"
