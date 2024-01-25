import { Component, Input, OnInit } from '@angular/core';
import { Email } from 'src/app/models/email';

@Component({
  selector: 'app-email-box',
  templateUrl : './email-box.component.html'
})
export class EmailBoxComponent implements OnInit {
  @Input() fullWidthMode = true;
  @Input() email !: Email ;
  
  constructor() { }

  ngOnInit(): void {
  }

}
