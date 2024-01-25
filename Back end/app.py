# Import necessary Libraries
import datetime
import imaplib
import email
import yaml
from email.header import decode_header
from textblob import TextBlob
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from summarizer import summarize
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
import hashlib
from flask_cors import CORS
from nltk.corpus import stopwords
from flask import Flask, jsonify, request


app = Flask(__name__)
# useful for rest api requests
CORS(app)

# Function to extract a summary from text
def extract_summary(text):
    try:
        summary = summarize('greeting', text)
        return summary
    except Exception as e:
        print(f"Error while summarizing: {e}")
        return None

# Function to extract keywords from text
def extract_keywords(text):
    # Load a spaCy language model (you can choose a different model based on your requirements)
    nlp = spacy.load('en_core_web_sm')

    # Tokenize the text using NLTK
    tokens = word_tokenize(text)

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]

    # Use spaCy for part-of-speech tagging and noun extraction
    doc = nlp(' '.join(tokens))
    unique_nouns = set()
    for token in doc:
        if token.pos_ == 'NOUN':
            unique_nouns.add(token.text)

    return list(unique_nouns)

# Main function
def fetch_emails(sender_email="example@email.com", limit=15):

    # Read credentials from the YAML file
    with open("credentials.yml") as f:
        content = f.read()

    my_credentials = yaml.load(content, Loader=yaml.FullLoader)
    user, password = my_credentials["user"], my_credentials["password"]

    imap_url = 'imap.gmail.com'
    my_mail = imaplib.IMAP4_SSL(imap_url)
    my_mail.login(user, password)
    my_mail.select('Inbox')

    # This is a default sender email you don't have to do that 
    sender_email = sender_email or "example@email.com"

    if sender_email:
        search_criterion = f'FROM "{sender_email}"'
        search_command = f'FROM "{sender_email}"'
    elif limit :
        search_criterion = 'ALL'
        search_command = f'Last {limit} emails'
    else :
        search_criterion = 'ALL'
        search_command = 'Last 15 emails by default'

    # Debug print to see the constructed IMAP SEARCH command
    print(f'Search Command: {search_command}')

    _, data = my_mail.search(None, 'ALL', search_criterion)

    mail_id_list = data[0].split()

    # Fetch only the specified number of emails if limit is provided
    if int(limit) > 0:
        mail_id_list = mail_id_list[-int(limit):]

    emails = []

    for num in reversed(mail_id_list):
        # Use the FETCH command to retrieve the entire message
        typ, message_data = my_mail.fetch(num, '(RFC822)')

        for response_part in message_data:

            if isinstance(response_part, tuple):
                my_msg = email.message_from_bytes(response_part[1])

                # Use parseaddr to extract the email address from the "from" field

                sender_name, sender_email = email.utils.parseaddr(my_msg['from'])
                
                # The dictionnary that we are sending to the front end 
                email_data = {
                    "subject": my_msg['subject'],
                    "from": sender_email,
                    "sender": sender_name,
                    "body": None,
                    "gravatar_url": None,
                    "date": None
                }
                email_data["sender"] = sender_name

                date_tuple = email.utils.parsedate_tz(my_msg['Date'])
                if date_tuple:
                    local_date = datetime.datetime.fromtimestamp(
                        email.utils.mktime_tz(date_tuple)
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    email_data["date"] = local_date

                # Compute the MD5 hash of the lowercase email address
                md5_email = hashlib.md5(sender_email.lower().encode('utf-8')).hexdigest()

                # Construct the Gravatar URL
                gravatar_url = f'https://www.gravatar.com/avatar/{md5_email}?s=100&d=identicon&r=PG'
                email_data["gravatar_url"] = gravatar_url

                for part in my_msg.walk():
                    if part.get_content_type() == 'text/plain':
                        # printable encoding
                        message_body = part.get_payload(decode=True).decode()
                        email_data["body"] = str(message_body).replace("\r\n"," ")
                        
                        # Perform sentiment analysis
                        sentiment_analysis = TextBlob(message_body)
                        sentiment_score = sentiment_analysis.sentiment.polarity  # Range: -1 (negative) to 1 (positive)

                        # Extract a summary from the email content
                        email_content = str(message_body).replace("\r\n"," ")  # Use the email content you've extracted
                        email_summary = extract_summary(email_content)

                        # Adding summarization results to email_data
                        if email_summary:
                            
                            email_data["Extracted_Summary"] = email_summary
                        else:
                            print("Unable to generate a summary.")

                        # Classify the sentiment
                        if sentiment_score > 0.2:
                            sentiment_label = 'Positive'
                        elif sentiment_score < 0.2:
                            sentiment_label = 'Negative'
                        else:
                            sentiment_label = 'Neutral'
                        
                        # Adding sentiment results to email_data
                        email_data["Sentiment_Label"] = sentiment_label
                        email_data["Sentiment_Score"] = sentiment_score

                        # Topic extraction
                        topic_keywords = extract_keywords(message_body)
                        email_data["Extracted_Topics_Keywords"] = ', '.join(topic_keywords)
 
        emails.append(email_data)

    my_mail.close()
    my_mail.logout()

    return emails

@app.route('/api/emails')
def get_emails():
    # Use the provided sender_email and limit parameters
    sender_email = request.args.get('sender_email')
    limit = request.args.get('limit')
    limit = int(limit) if limit is not None else 15
    emails = fetch_emails(sender_email, limit)
    return jsonify(emails)

if __name__ == '__main__':
    app.run(debug=True)
