#!/usr/bin/env python3
# encoding: utf-8
import json
import requests
import os

from cortexutils.responder import Responder

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(CURRENT_DIR, "YaraDesigner.json")

TH_DATATYPE_ALERT = "thehive:alert"
TH_DATATYPE_CASE = "thehive:case"


class YaraWhitelistRuleCreator(Responder):
    def __init__(self):
        Responder.__init__(self)

        with open(CONFIG_PATH) as f:
            self.config = json.load(f)["config"]

        self.endpoint = self.config["designer_core_endpoint"]

    def run(self):
        if self.data_type != TH_DATATYPE_CASE:
            self.error("Invalid dataType: got '{}', expected '{}'!".format(self.data_type, TH_DATATYPE_CASE))

        # POST data to YARA Designer core endpoint.
        try:
            r = requests.post(self.endpoint, json=self.get_data(), headers={'Content-type': 'application/json'})

            if r.status_code != 200:
                self.error("POST Request to {endpoint} failed with status: {code} {reason}! Data: {data}".format(
                    endpoint=self.endpoint,
                    code=r.status_code,
                    reason=r.reason,
                    data=r.text))

            js = json.loads(r.text)

            self.report(js)
        except Exception as exc:
            self.error("An unexpected Exception occurred: {exc}".format(exc=str(exc)))

    def operations(self, raw):
        retv = self.config["operations"] if "operations" in self.config else []

        return retv


if __name__ == "__main__":
    YaraWhitelistRuleCreator().run()

