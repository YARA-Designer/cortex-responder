# YARA Designer: TheHive/Cortex Responder

This responder sends a `thehive:case` to a listener which then creates
a YARA rule based on it.

## Setup

1. Cortex needs to have cortexutils installed at _operating system_ level:
    ```
    $ sudo pip3 install cortexutils
    ```
2. Configure `YaraDesigner.json`.
    - Notable settings:
        - url (The URL where the responder is stored (git).)
        - config
            - designer_core_endpoint
            - operations (list of dicts with TheHive operations to be applied to case after processing (e.g. set a "Sent to YARA Designer" tag)).
3. Upload contents of `responder/` to `CORTEX_RESPONDERS/YaraDesigner/` on Cortex host.
4. Restart TheHive and Cortex:
    ```
    $ sudo systemctl restart cortex thehive
    ```
5. Enable the Cortex Responder:
    1. Log into Cortex with your TheHive user.
    2. Click "Organization" in the top bar.
    3. Click the "Responders" tab.
    4. Click the "+ Enable" link at the far right on the entry "YARA Designer <some version>".
    5. Configure any options you want set and click "Save".
    6. Click "Responders" in the top bar and verify that it is listed on the Responders page.
6. 


Further documentation: https://github.com/TheHive-Project/CortexDocs/blob/master/api/how-to-create-a-responder.md