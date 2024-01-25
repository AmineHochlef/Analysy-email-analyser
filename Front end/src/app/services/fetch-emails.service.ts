import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Email } from '../models/email';

const apiUrl = 'http://localhost:5000/api';

@Injectable({
  providedIn: 'root'
})
export class FetchEmailsService {

  constructor(private httpClient: HttpClient) {}

  getEmails(limit= '15',senderEmail: string) : Observable<Array<Email>>{
    return this.httpClient.get<Array<Email>>(
      `${apiUrl}/emails?limit=${limit}&sender_email=${senderEmail}`
    );
  }

}
