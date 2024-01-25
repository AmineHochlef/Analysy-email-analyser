import { Component, EventEmitter, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-emails-header',
  templateUrl: './emails-header.component.html',
})
export class EmailsHeaderComponent implements OnInit {
  @Output() emailsCountChange = new EventEmitter<number>();
  @Output() sortChange = new EventEmitter<string>();
  sort = 'Negative';
  emails_show_count = 15;

  constructor() {}

  ngOnInit(): void {}

  onSortUpdated(newSort: string): void {
    this.sort = newSort;
    this.sortChange.emit(newSort);
  }

  onCountUpdated(count: number): void {
    this.emails_show_count = count;
    this.emailsCountChange.emit(count);
  }
}
