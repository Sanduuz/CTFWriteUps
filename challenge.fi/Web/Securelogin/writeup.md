## GenerationZ Challenge (challenge.fi) | Web | Securelogin
##### Author: Sanduuz | Date: 19.05.2021
---
### Challenge details:
* Points: 299
* Solves: 16
* Difficulty: Hard (?)
* Description:

> The development team has made a proof of concept of the new Securelogin site. Somebody managed to put it to the public internet, but dev team is so confident that they don't think it matters so they left it open!
>
> Can you prove them wrong?! Are you the one who fetches the flag from /etc/flag.txt - file?
>
> You can find the challenge from: http://securelogin.challenge.fi:8880/

> Note: This challenge is based on a real world example of a finding from a bug bounty target. Pretty much 1=1, but some clues maybe around what to do...

---

### Writeup:

**TL;DR**\
**Out-of-band XML External Entity (OOB-XXE) attack to read contents of /etc/flag.txt on server.**

---

### Reconnaissance

The challenge starts with a website that looks like this:

<img src="https://github.com/Sanduuz/CTFWriteUps/blob/master/challenge.fi/Web/Securelogin/attachments/website_frontpage.png" width="428" height="281" />

First we should take a look at the source code of the website in order to see what it might be hiding. This can be achieved by clicking the right mouse button and choosing `View page source` or simply with the keyboard shortcut <kbd>CTRL</kbd>+<kbd>U</kbd>.

The source code of the frontpage:

<img src="https://github.com/Sanduuz/CTFWriteUps/blob/master/challenge.fi/Web/Securelogin/attachments/website_sourcecode.png" width="1440" height="320" />

As we can see, the source code of the wegpage is hiding a comment left behind by the developer. The comment starts with `Debug info, remember to remove before moving to prod:`

We can clearly see that this comment was not removed before moving to production. The debug information now gives us attackers some extra information about the service that we can leverage.

The debug information seems to be a HTTP POST request to `xml.php` residing on the server itself. Some data is sent with the request in a field labeled `xml`. The data seems to be url encoded base64 data.

Decoding this data sent in the debug request results in some XML data.
<img src="https://github.com/Sanduuz/CTFWriteUps/blob/master/challenge.fi/Web/Securelogin/attachments/xml_data.png" />

The XML data sent with the request starts with a XML declaration that is used to specify metadata for the parser. This metadata includes xml version and character encoding to be used by the parser.

After the XML declaration there is the root element `<creds>` (Elements are sometimes also referred as tags). This root tag has 2 child-tags: `<user>` and `<pass>`.

So it seems that the `xml.php` file is used for some kind of XML-based authentication system running on the server.

Time to dig deeper and start experimenting by ourselves.

<br />

### Experimentation

Let us traverse to the path `/xml.php` on the server to see whether the file still exists after moving to production.
<img src="https://github.com/Sanduuz/CTFWriteUps/blob/master/challenge.fi/Web/Securelogin/attachments/xml.php.png" />

We did not get a 404-error, which means that the file still exists. The response returns an error message stating that username or password was not found. This is because instead of sending a HTTP POST request with the XML data, a HTTP GET request was sent to the server.

Let us send a simple HTTP POST request containing the XML data with username and password "admin" to the server for test purposes. We can easily achieve this with the help of Python3.

```python
import requests                   # Import requests module for making HTTP requests
import base64                     # Import base64 for encoding our data
from urllib.parse import quote    # Import quote from urllib.parse for urlencoding

# Specify Content-Type header to correspond the servers expectations.
headers = {
  "Content-Type":"application/x-www-form-urlencoded"
}

# Our XML data to be sent with the request
xml_data = b"""<?xml version="1.0" encoding="ISO-8859-1"?>
<creds>
	<user>admin</user>
	<pass>admin</pass>
</creds>"""

# Encode data and set data to be sent with the "xml" field
encoded_data = quote(base64.b64encode(xml_data))
post_data = u"xml="+encoded_data

# Send request to the webpage with set headers and data
request = requests.post("http://securelogin.challenge.fi:8880/xml.php", headers=headers, data=post_data)

# Print server response
print(request.text)
```

Running the script `python3 send_request.py` lets us see the server response when trying to authenticate with `admin:admin` credentials.
<img src="https://github.com/Sanduuz/CTFWriteUps/blob/master/challenge.fi/Web/Securelogin/attachments/creds_not_found.png">

Yet again the same error as previously. No more new information it seems.

- There must be a XML parser to make any sense of sent data -> XXE
