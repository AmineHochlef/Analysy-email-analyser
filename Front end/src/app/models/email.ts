export interface Email {
    subject: string;
    from: string;
    body: string;
    sender : string;
    date : string;
    gravatar_url: string;
    Sentiment_Label: string;
    Sentiment_Score: number;
    Extracted_Summary: string[];
    Extracted_Topics_Keywords: string;
  }