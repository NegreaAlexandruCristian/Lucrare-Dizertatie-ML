import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable, of} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class BitcoinPredictionService {

  constructor(private http: HttpClient) {
  }

  getBitcoinPrediction(): Observable<any> {
    // TODO exception handling here
    const url = 'http://127.0.0.1:5000/predict-bitcoin-price';
    this.http.get(url).subscribe((response) => {
      return response;
    });
    return of(0)
  }
}
