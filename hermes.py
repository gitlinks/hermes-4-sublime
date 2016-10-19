import sublime
import sublime_plugin
import requests
from .searchgitlinks import GitlinksSearchApiCall


class GitlinksSearchCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel(
            "Search on Gitlinks",
            "",
            self.on_done,
            self.on_change,
            self.on_cancel
        )

    def on_done(self, string):
        thread = GitlinksSearchApiCall(string)
        thread.start()
        return

    def on_change(self, input):
        return

    def on_cancel(self, index):
        return
