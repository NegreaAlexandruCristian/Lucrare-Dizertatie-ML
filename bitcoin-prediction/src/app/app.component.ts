import {CurrencyService} from './crypto-api/currency.service';
import {Component} from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  selectedCurrency: string = "EUR";
  title: string = "Crypto Checker";

  constructor(private currencyService: CurrencyService) {

  }

  sendCurrency(event: string) {
    console.log(event);
    this.currencyService.setCurrency(event);
  }
}
