import pandas as pd
import pytest
import os
from well_data_filter import filter_and_calculate_percentiles_by_date

def test_grouped_percentiles():
    # Create test data with multiple dates
    test_data = pd.DataFrame({
        'date': ['2024-01-01', '2024-01-01', '2024-01-01', '2024-02-01', '2024-02-01'],
        'status': ['prod', 'prod', 'not work', 'inj', 'prod'],
        'well': ['14312', '14314', '14312', '14316', '14312'],
        'QOIL': [16.27, 1.34, 12.49, 2.05, 3.69],
        'QWAT': [248.21, 33.23, 244.02, 0.52, 62.43]
    })
    
    result = filter_and_calculate_percentiles_by_date(test_data, save_to_csv=False)
    
    # Should have separate results for each date
    assert len(result) == 2  # Two dates
    assert '2024-01-01' in result
    assert '2024-02-01' in result
    
    # Check that percentiles are calculated correctly for each date group
    assert 'QOIL' in result['2024-01-01']
    assert 'P10' in result['2024-01-01']['QOIL']
    
    print("Test passed - grouped percentiles work correctly")