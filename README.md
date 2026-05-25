# website monitor
Monitor the status of a single website or a list of websites from the terminal
---

**Website monitor** is a Python script that can continuously monitor a single website or a list of websites and return information whether the website(s) is/are up or down. It performs regular checks at given interval and relies on HTTP response codes.

```
$ python3 wsmon.py --help
usage: wsmon [-h] [-u URL] [-f URLS_FILE] [-t TIMER] [--version]

website monitor

options:
  -h, --help            show this help message and exit
  -u, --url URL         specify URL address to monitor
  -f, --urls-file URLS_FILE
                        specify a file with URLs to monitor
  -t, --timer TIMER     specify interval for checking (seconds)
  --version             show program version and exit

(c)Ivaylo Vasilev
```

The option `-f, --urls-file` accept a text file with a list of URLs. Each line ***must*** start with **http** or **https** respectively for the sript to treat it as a **valid URL**. Lines with ***#*** will be ignored as well as URLs that do not follow the proper schema.

**Example list of URLs:**

```
# URLs list
https://ivaylo-vasilev.github.io
http://www.example.com
```
