# from datetime import datetime
# from unittest import mock
#
# import freezegun
# import pandas as pd
# from azure.storage.blob import BlobServiceClient, BlobClient
#
# from src.main import prepare_data
# from src.repository.datastore import DataStore


# def test_csv_is_read_if_blob_exists():
#     test_data = {
#         "Date": [datetime(2022, 1, 1)],
#         "Price": [450.0],
#     }
#     test_csv_as_bytes = bytes(pd.DataFrame(data=test_data).to_csv(), 'utf-8')
#
#     mocked_datastore = mock.MagicMock(spec=DataStore)
#     mocked_datastore.dowload.return_value = test_csv_as_bytes
#     mocked_datastore.exists.return_value = test_csv_as_bytes
#
#     mocked_datastore.save_data.assert_called_once_with()

# @freezegun.freeze_time("2022-01-01")
# def test_price_is_added_to_dataframe():
#     test_data = {
#         "Date": [datetime(2022, 1, 1)],
#         "Price": [450.0],
#     }
#     expected = pd.DataFrame(data=test_data)
#     actual = prepare_data(450.0)
#     pd.testing.assert_frame_equal(expected, actual)
