> [!Important]
>
> - For SSL and HTTPS to work, change SSL context from None to Context and allow self-signed certificates (will show up as unsafe)
>

[![Python Version](https://img.shields.io/badge/python-3.12.2-blue.svg?style=flat-square)](https://www.python.org/downloads/release/python-3122/)
# study-plus
**CONTACT FOR ENQUIRIES: roman.lacbungan@education.nsw.gov.au**

## Overview ##
To track/remind labelled tasks through a tree structure, improves student wellbeing. An easily accessible app with visual reminders and streaks which motivate users and promote high productivity.

## Main features ##
- Strict Content Security Policy
  - No inline `<script></script>`.
  - Restricted `<iframe>` loading
  - CORS JS blocked
- Automatic account deletion after 6+ months
- Enforces an 8 character minimum password with letters and numbers
- User data can be downloaded and deleted through settings
- Passwords are hashed with randomised cryptography
- Secure session handling with Flask
- Strict input sanitization and validation
- App logging and alerts for suspicious activities
- SSL and HTTPS support (allow self-signed certificates)
- Dark Mode support
- Configurable navbar
- Progression chart
- View public profiles

## Installation
1. Clone repository
<pre>git clone https://github.com/TempeHS/2025SE-Roman.L-StudyPlus</pre>

2. Check directory
<pre>cd 2025SE-Roman.L-StudyPlus2025</pre>
   
3. Gather dependencies
<pre>pip install -r requirements.txt</pre>

4. Deploy live server (port: 5000)
<pre>python main.py</pre>

Once deployed, the app can be accessed on either:
- http://localhost:5000
- http://127.0.0.1:5000

## Previous sprints

### [sprint-0.0.1](https://github.com/TempeHS/2025SE-Roman.L-StudyPlus/tree/sprint-0.0.1): June, 2025 - Roman Lacbungan

After my client's feedback through Google Forms and emails, I added a node network to better visualise tasks. Additionally, I added a stat chart, a profile page, and properly abstracted my 'main.py' file. Overall, the primary components are working, however I still need to implement better security (2FA) and other features. I disabled my CSP however I still need it for later and my dark mode is not reliable. This particular sprint was quite long, thus future sprints will be minimised.

### [sprint-0.0.2](https://github.com/TempeHS/2025SE-Roman.L-StudyPlus/tree/sprint-0.0.1): June, 2025 - Roman Lacbungan

### [sprint-0.0.3](https://github.com/TempeHS/2025SE-Roman.L-StudyPlus/tree/sprint-0.0.1): June, 2025 - Roman Lacbungan

## Screenshots
### Dashboard

## Acknowledgments

Inspiration, code snippets, etc.

* https://github.com/TempeHS/2025SE-Roman.L-HSCTask1
* https://github.com/TempeHS/Secure_Flask_PWA_Template