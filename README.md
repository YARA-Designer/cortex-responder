# YARA Designer: TheHive/Cortex Responder

This responder sends a `thehive:case` to a listener which then creates
a YARA rule based on it.

## Setup

1. Cortex needs to have cortexutils installed at _operating system_ level:
    ```
    $ sudo pip3 install cortexutils
    ```
2. Upload contents of `responder/` to `CORTEX_RESPONDERS/YaraDesigner/` on Cortex host.
3. Restart TheHive and Cortex:
    ```
    $ sudo systemctl restart cortex thehive
    ```
4. Enable the Cortex Responder:
    1. Log into Cortex with your TheHive user.
    2. Click "Organization" in the top bar.
    3. Click the "Responders" tab.
    4. Click the "+ Enable" link at the far right on the entry "YARA Designer <some version>".
    5. Configure options and click "Save".
    6. Click "Responders" in the top bar and verify that it is listed on the Responders page. 

Tip: Responder script runtime stdout/stdin can be found in `/var/log/cortex/application.log`, should you need to diagnose any problems.

Further documentation: https://github.com/TheHive-Project/CortexDocs/blob/master/api/how-to-create-a-responder.md