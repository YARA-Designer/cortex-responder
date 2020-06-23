#!/usr/bin/env python3
# encoding: utf-8
import json
import requests

from cortexutils.responder import Responder

TH_DATATYPE_ALERT = "thehive:alert"
TH_DATATYPE_CASE = "thehive:case"


class YaraDesigner(Responder):
    def __init__(self):
        Responder.__init__(self)

        self.operations_list = []
        self.endpoint = self.get_param(
            "config.endpoint",
            message="Endpoint is not configured, aborting!")

        # Input will be on the form of a list of strings.
        [self.add_tag_to_artifact(tag) for tag in self.get_param("config.add_tags_to_artifact")]
        [self.add_tag_to_case(tag) for tag in self.get_param("config.add_tags_to_case")]

        # Input will be on the form of a list of stringified JSON objects.
        [self.add_operation(op) for op in self.get_param("config.custom_operations")]

        self.send_added_tags = self.get_param("config.send_added_tags", default=False)

    def add_operation(self, operation: str):
        """
        Add a operation (JSON) to the operations list,
        to be executed after a successful run.

        :param operation: A JSON string.
        :return:
        """
        if operation:
            self.operations_list.append(json.loads(operation))

    def add_tag_to_artifact(self, tag: str):
        """
        Add a tag to the artifact related to the object.

        :param tag: A tag.
        :return:
        """
        if tag:
            self.operations_list.append({"type": "AddTagToArtifact", "tag": tag})

    def add_tag_to_case(self, tag: str):
        """
        Add a tag to the case related to the object.

        :param tag:
        :return:
        """
        if tag:
            self.operations_list.append({"type": "AddTagToCase", "tag": tag})

    def get_added_tags(self) -> list:
        """Returns a list of all the custom added tags specified in config"""
        return [js["tag"] for js in self.operations_list if "tag" in js]

    def run(self):
        if self.data_type != TH_DATATYPE_CASE:
            self.error("Invalid dataType: got '{data_type}', expected '{case_data_type}'!".format(
                data_type=self.data_type, case_data_type=TH_DATATYPE_CASE))

        try:
            # Make a copy of the case data (to allow for modifications that don't persist).
            case = self.get_data()

            if self.send_added_tags is False:
                # Strip all the custom tags from the copied case's tags list.
                case["tags"] = [tag for tag in case["tags"] if tag not in self.get_added_tags()]

            # POST data to YARA Designer core endpoint.
            r = requests.post(self.endpoint, json=case, headers={'Content-type': 'application/json'})

            if r.status_code != 200:
                self.error("POST Request to {endpoint} failed with status: {code} {reason}! Data: {data}".format(
                    endpoint=self.endpoint,
                    code=r.status_code,
                    reason=r.reason,
                    data=r.text))

            self.report({
                "message": "Case successfully sent to YARA Designer.",
                "destination_endpoint": self.endpoint,
                "operations": self.operations_list,
                "send_added_tags": self.send_added_tags,
                "in": self._input,
                "out": json.loads(r.text)
            })
        except Exception as exc:
            self.error("An unexpected Exception occurred: {exc}".format(exc=str(exc)))

    def operations(self, raw):
        """Returns the list of operations to be executed after the job completes"""
        return self.operations_list


if __name__ == "__main__":
    YaraDesigner().run()

