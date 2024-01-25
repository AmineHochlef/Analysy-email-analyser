# Analysy

Simple email analyser app.
## Why Analysy ?

The idea of this project is to make email checking efficient and easier. So the main point is analysing emails using different NLP techniques so you don't have to read the email in it's entirety, this project presents some NLP features such as :

- Large text summarization this is used to summarize the body of the email
- Sentimental analysis this is used to prioritize emails as Negative or Positive sentimentally
- Topic and keywords extraction this is useful to search for emails with certain keywords :)

This project was done during an Internship.

- [How_does_it_work](#How_does_it_work)
- [Technologies](#Technologies)
- [Development_server](#Development server)
- [Contribute](#Contribute)
- [Author](#Author)

## How does it work 

1. Make sure you enable IMAP in your gmail settings
(Log on to your Gmail account and go to Settings, See All Settings, and select
 Forwarding and POP/IMAP tab. In the "IMAP access" section, select Enable IMAP.)

2. If you have 2-factor authentication, gmail requires you to create an application
specific password that you need to use. 
Go to your Google account settings and click on 'Security'.
Scroll down to App Passwords under 2 step verification.
Select Mail under Select App. and Other under Select Device. (Give a name, e.g., python)
The system gives you a password that you need to use to authenticate from python.

### ⚠️ This is the password you are going to use to log into your gmail account  from python in `credentials.yml`⚠️

## Technologies

#### This project was generated with these technologies :

### Front end :
`Angular 14`, `Angular Material` & `tailwindcss` for extra styling.
### Back end : 
`Flask` using `Python 3`

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

Run `python app.py` in the back end folder for the flask server to run.

## Contribute

For any type of contribution, please follow the instructions in [CONTRIBUTING.md](https://github.com/AmineHochlef/Analysy-email-analyser/blob/master/CONTRIBUTING.md).

## Author

**Amine Hochlef (Hochlef)**

- <https://twitter.com/AmineHochlef22>
- <https://github.com/AmineHochlef>