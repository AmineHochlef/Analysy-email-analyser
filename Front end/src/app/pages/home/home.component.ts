import { ChangeDetectorRef, Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { Email } from 'src/app/models/email';
import { FetchEmailsService } from 'src/app/services/fetch-emails.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
})
export class HomeComponent implements OnInit, OnDestroy {
  loading: boolean = false; // Initialize with true to show the skeleton loader during the initial fetch
  emailNotFound = false;  
  cols = 1;
  emails!: Array<Email>;
  sort = 'Negative';
  count = '15';
  displayedCount = '15';
  senderEmail = ''; // Add property to store sender's email
  fetchedEmails: Array<Email> = [];
  emailsSubscription: Subscription | undefined;

  constructor(private fetchEmailsService: FetchEmailsService, private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.getEmails();
  }

  getEmails(): void {
    this.loading = true; // Set to true before fetching emails
    console.log('Initializing HomeComponent...');
    this.emails = [];
    this.emailNotFound = false; 
    this.emailsSubscription = this.fetchEmailsService
      .getEmails(this.count, this.senderEmail) // Pass sender's email dynamically
      .subscribe(
        (_emails) => {
          this.fetchedEmails = _emails;
          this.updateDisplayedEmails();
          console.log('Received data:', _emails);
          if (_emails.length === 0) {
            this.emailNotFound = true; // Set emailNotFound to true
          }
        },
        (error) => {
          console.error('Error fetching emails:', error);
        },
        () => {
          console.log('Subscription completed.');
          this.loading = false;
        }
      );
  }

  onEmailsCountChange(newCount: number): void {
    this.displayedCount = newCount.toString();
    this.updateDisplayedEmails();
  }

  onSortChange(newSort: string): void {
    this.sort = newSort;
    if (this.emails) {
      this.sortEmails();
    }
  }

  onEmailSubmit(): void {
    // Trigger fetching emails when the email is submitted
    this.getEmails();
  }

  private updateDisplayedEmails(): void {
    if (this.fetchedEmails && this.displayedCount) {
      this.emails = this.fetchedEmails.slice(0, +this.displayedCount);
    }
  }

  private sortEmails(): void {
    this.emails = this.emails.sort((a, b) => {
      if (this.sort === 'Negative') {
        return a.Sentiment_Label === 'Negative' ? -1 : 1;
      } else if (this.sort === 'Positive') {
        return a.Sentiment_Label === 'Positive' ? -1 : 1;
      }
      return 0;
    });
  }

  ngOnDestroy(): void {
    if (this.emailsSubscription) {
      this.emailsSubscription.unsubscribe();
    }
  }
}
