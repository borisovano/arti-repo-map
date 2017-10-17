# arti-repo-map
Python tool that recursively scan Artifactory repo and print sub-folders info and size. Usefull in analyzing space usage issues.

The tool parses nested json obtained from Artifactory api, uri: artifactory/api/storage/libs-snapshot-local?list&deep=1&listFolders=1&mdTimestamps=1


Usage:
Either run and point to remote artifactory repo (see examples section) or choose local json datasource(previously downloaded via artifactory api)


 - Local data json can be obtained via curl or wget to: www.artifactory.mycompany.com/artifactory/api/storage/libs-snapshot-local?list&deep=1&listFolders=1&mdTimestamps=1
 - Tested with python3.6.2
 - Command line options: python ./arti_parse.py --help


Examples:

1. Remote artifactory
python ./arti_parse.py -r www.artifactory.mycompany.com/artifactory/api/storage/libs-snapshot-local?list&deep=1&listFolders=1&mdTimestamps=1 -u myuser -p mypass

-- Some output omitted --
com/mycompany/tools/platform                         - 64.8GiB         (Total: 420.9GiB)
com/mycompany/tools/ba                               - 71.2GiB         (Total: 492.1GiB)
com/mycompany/common/server                          - 115.4GiB        (Total: 607.5GiB)
com/mycompany/common/client                          - 169.7GiB        (Total: 777.2GiB)
com/mycompany/common/AutomationTest                  - 295.4GiB        (Total: 1.0TiB)


2. Local json (already downloaded)
python ./arti_parse.py -r /home/user/my_artifactory_data.json

-- Some output omitted --
com/mycompany/tools/platform                         - 64.8GiB         (Total: 420.9GiB)
com/mycompany/tools/ba                               - 71.2GiB         (Total: 492.1GiB)
com/mycompany/common/server                          - 115.4GiB        (Total: 607.5GiB)
com/mycompany/common/client                          - 169.7GiB        (Total: 777.2GiB)
com/mycompany/common/AutomationTest                  - 295.4GiB        (Total: 1.0TiB)

