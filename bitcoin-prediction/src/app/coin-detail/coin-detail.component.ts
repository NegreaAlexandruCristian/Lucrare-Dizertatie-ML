import {CurrencyService} from '../crypto-api/currency.service';
import {ApiService} from '../crypto-api/api.service';
import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {ChartConfiguration, ChartType} from 'chart.js';
import {BaseChartDirective} from 'ng2-charts'
import {BitcoinPredictionService} from "../bitcoin-prediction/bitcoin-prediction.service";

@Component({
  selector: 'app-coin-detail',
  templateUrl: './coin-detail.component.html',
  styleUrls: ['./coin-detail.component.scss']
})
export class CoinDetailComponent implements OnInit {

  coinData: any;
  coinId !: string;
  days: number = 30;
  currency: string = "EUR";
  predictedPrice: number = 0;
  public lineChartData: ChartConfiguration['data'] = {
    datasets: [
      {
        data: [],
        label: `Price Trends`,
        backgroundColor: 'rgba(148,159,177,0.2)',
        borderColor: '#009688',
        pointBackgroundColor: '#009688',
        pointBorderColor: '#009688',
        pointHoverBackgroundColor: '#009688',
        pointHoverBorderColor: '#009688',

      }
    ],
    labels: []
  };
  public lineChartOptions: ChartConfiguration['options'] = {
    elements: {
      point: {
        radius: 1
      }
    },

    plugins: {
      legend: {display: true},
    }
  };
  public lineChartType: ChartType = 'line';
  @ViewChild(BaseChartDirective) myLineChart !: BaseChartDirective;


  constructor(
    private api: ApiService,
    private bitcoinApi: BitcoinPredictionService,
    private activatedRoute: ActivatedRoute,
    private currencyService: CurrencyService
  ) {
  }

  ngOnInit(): void {
    this.activatedRoute.params.subscribe(val => {
      this.coinId = val['id'];
    });
    this.getCoinData();
    this.getGraphData(this.days);
    this.currencyService.getCurrency()
      .subscribe(val => {
        this.currency = val;
        this.getGraphData(this.days);
        this.getCoinData();
      })
  }

  predictBitcoinPrice(bitcoinPrice: number): void {
    try {
      this.bitcoinApi.getBitcoinPrediction(bitcoinPrice).subscribe(
        (response): void => {
          console.log(response);
          this.predictedPrice = response.bitcoinPrice;
          console.log(this.predictedPrice);
        },
        (error): void => {
          console.log(`Error: ${error}`);
        }
      );
    } catch (error) {
      console.log(`Error: ${error}`);
    }
  }

  getCoinData(): void {
    this.api.getCurrencyById(this.coinId)
      .subscribe(res => {
        if (this.currency === "USD") {
          res.market_data.current_price.eur = res.market_data.current_price.usd;
          res.market_data.market_cap.eur = res.market_data.market_cap.usd;
        }
        res.market_data.current_price.eur = res.market_data.current_price.eur;
        res.market_data.market_cap.eur = res.market_data.market_cap.eur;
        this.coinData = res;
      })
  }

  getGraphData(days: number) {
    this.days = days
    this.api.getGraphicalCurrencyData(this.coinId, this.currency, this.days)
      .subscribe(res => {
        setTimeout(() => {
          this.myLineChart.chart?.update();
        }, 200);
        this.lineChartData.datasets[0].data = res.prices.map((a: any) => {
          return a[1];
        });
        this.lineChartData.labels = res.prices.map((a: any) => {
          let date: Date = new Date(a[0]);
          let time: String = date.getHours() > 12 ?
            `${date.getHours() - 12}: ${date.getMinutes()} PM` :
            `${date.getHours()}: ${date.getMinutes()} AM`
          return this.days === 1 ? time : date.toLocaleDateString();
        })
      })
  }

}
