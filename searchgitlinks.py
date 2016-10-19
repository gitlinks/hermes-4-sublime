import threading
import requests
import sublime
import logging

logging.getLogger("requests").setLevel(logging.WARNING)


class GitlinksSearchApiCall(threading.Thread):
    def __init__(self, searchTerms):
        self.search = searchTerms
        threading.Thread.__init__(self)

    def run(self):
        settings = sublime.load_settings("hermes.sublime-settings")
        email = settings.get('email')
        token = settings.get('token')

        if email is None or email == "":
            sublime.message_dialog("You should set up the \"email\" field" +
                                   "in the hermes preference")
            return

        if token is None or token == "":
            sublime.message_dialog("You should set up the \"token\" field" +
                                   "in the hermes preference")
            return

        try:
            res = requests.get(
                'https://hermes-api.gitlinks.io/search?q=' + self.search,
                auth=(email, token)
            )

            if res.status_code == requests.codes.UNAUTHORIZED:
                sublime.message_dialog("Wrong email or token in your " +
                                       "preferences")

                return

            to_show = format_json_results(res.json())
            print(str(to_show))
            sublime.active_window().show_quick_panel(
                to_show,
                self.on_selected
            )

            return

        except requests.ConnectionError as e:
            err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))

        sublime.error_message(err)

    def on_selected(self, index):
        return


def format_json_results(json):
    return list(map(format_result, json))


def format_result(elem):
    if (len(elem["categories"]) == 0):
        return [elem["name"], "No categories"]
    else:
        return [elem["name"], ", ".join(elem["categories"])]
