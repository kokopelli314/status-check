# status-check

Check the HTTP status of a page and send a notification if it's down. Used as a simple health check and notification when a site is down.

If a URL is expected to return a 200 status, this script will send you an email alert if the site instead returns a 500, for example.

## Config

Clone this repo and create a module `src/private_sites.py`. For each site you want to check, implement a subclass of the `Site` class. For instance:

```python
from Site import Site
from typing import List

class Homepage(Site):                          
        def __init__(self):
                self.url = 'https://nathanclonts.com'
                self.expectedStatus = 200
                self.name = 'Homepage'

exports: List[Site] = [
        Homepage(),
]
```

Create a `.env` file giving the SMTP credentials with which to send emails when you get a bad status.

Then trigger the `main.py` script with a cron job. For example:

```bash
# Check system statuses every 5 minutes & send warning emails if needed
*/5 * * * *  ( sleep 30 ; /home/{my-user}/.virtualenvs/status-check/bin/python ~/status-check/src/main.py > ~/cron-test-status-check.log 2>&1 )
```

Alerts will then fire when any of your pages don't respond with the expected statuses.
