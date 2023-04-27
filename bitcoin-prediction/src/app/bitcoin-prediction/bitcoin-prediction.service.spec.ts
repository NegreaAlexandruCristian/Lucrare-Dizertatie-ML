import { TestBed } from '@angular/core/testing';

import { BitcoinPredictionService } from './bitcoin-prediction.service';

describe('BitcoinPredictionService', () => {
  let service: BitcoinPredictionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BitcoinPredictionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
