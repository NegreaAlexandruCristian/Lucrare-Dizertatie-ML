import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class BitcoinPredictionService {

  constructor(private http: HttpClient) {
  }

  getBitcoinPrediction(): void/* Observable<any> */ {
    // TODO Call the service to predict the price
    const url = 'http://127.0.0.1:5000/predict-bitcoin-price';
    this.http.get(url).subscribe((response) => {
      console.log(response);
    });
  }
}
