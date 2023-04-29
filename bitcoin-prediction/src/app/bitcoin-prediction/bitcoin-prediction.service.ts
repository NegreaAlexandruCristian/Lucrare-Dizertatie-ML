import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {catchError} from 'rxjs/operators';
import {Observable, throwError} from "rxjs";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class BitcoinPredictionService {

  constructor(private http: HttpClient) {
  }

  getBitcoinPrediction(bitcoinPrice: number): Observable<any> {
    // TODO exception handling here
    const url = environment.FLUSK_SERVER + '/predict-bitcoin-price';
    const body = {bitcoinPrice: bitcoinPrice};
    return this.http.post(url, body).pipe(
      catchError((error: HttpErrorResponse) => {
        console.error('An error occurred:', error);
        return throwError((): string => 'Something went wrong');
      })
    );
  }
}
