#!/usr/bin/env python3
# encoding: utf-8
import json
import requests

from cortexutils.responder import Responder

TH_DATATYPE_ALERT = "thehive:alert"
TH_DATATYPE_CASE = "thehive:case"


class YaraDesignerResponder(Responder):
    def __init__(self):
        Responder.__init__(self)

        self.operations_list = []
        self.endpoint = self.get_param(
            "config.designer_core_endpoint",
            message="Endpoint is not configured, aborting!")

        # Input will be on the form of a list of strings.
        [self.add_tag_to_artifact(tag) for tag in self.get_param("config.add_tags_to_artifact")]
        [self.add_tag_to_case(tag) for tag in self.get_param("config.add_tags_to_case")]

        # Input will be on the form of a list of stringified JSON objects.
        [self.add_operation(op) for op in self.get_param("config.add_custom_fields")]
        [self.add_operation(op) for op in self.get_param("config.custom_operations")]

    def add_operation(self, operation: str):
        """
        Add a operation (JSON) to the operations list,
        to be executed after a successful run.

        :param operation: A JSON string.
        :return:
        """
        if operation:
            print(operation)
            self.operations_list.append(json.loads(operation))
            print(self.operations_list)

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

    def run(self):
        if self.data_type != TH_DATATYPE_CASE:
            self.error("Invalid dataType: got '{data_type}', expected '{case_data_type}'!".format(
                data_type=self.data_type, case_data_type=TH_DATATYPE_CASE))

        try:
            # POST data to YARA Designer core endpoint.
            r = requests.post(self.endpoint, json=self.get_data(), headers={'Content-type': 'application/json'})

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
                "in": self._input,
                "out": json.loads(r.text)
            })
        except Exception as exc:
            self.error("An unexpected Exception occurred: {exc}".format(exc=str(exc)))

    def operations(self, raw):
        """Returns the list of operations to be executed after the job completes"""
        return self.operations_list


if __name__ == "__main__":
    YaraDesignerResponder().run()

