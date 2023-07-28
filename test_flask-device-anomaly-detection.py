# from unittest.mock import MagicMock, patch
# import pytest

# import datetime
# import hashlib
# import platform

# # from app.app import temperature
# import app.app as app

# @pytest.fixture
# def mock_predict_instance():
#     with patch("catch_topic.predict_instance") as mock_predict_instance:
#         yield mock_predict_instance


# @pytest.fixture
# def mock_kernel_classification():
#     with patch(
#         "catch_topic.kernel_classification.receive_data"
#     ) as mock_kernel_classification:
#         yield mock_kernel_classification


# def test_temperature():
#     temps = "22,23,21,26,25,20,28,29,23,28,21,22,25,27,30,29,29,26,21,26,23,24,25,24,22,23,21,26,25,20,28,29,23,28,21,22,25,27,30,29,29,26,21,26,23,24,25,24"
#     requestor_id = "Device123"
#     requestor_type = "NSSD"
#     request_id = "Device123_22/05/2023"

#     analyzer_id = platform.node()

#     # Get current date and time
#     now = datetime.datetime.now()

#     # Generate a random hash using SHA-256 algorithm
#     hash_object = hashlib.sha256()
#     hash_object.update(bytes(str(now), "utf-8"))
#     hash_value = hash_object.hexdigest()

#     # Concatenate the time and the hash
#     analysis_id = str(analyzer_id) + str(now) + hash_value

#     ws_req_final = {
#         "RequestPostTopicUUID": {
#             "topic_name": "SIFIS:Privacy_Aware_Device_Anomaly_Detection_Results",
#             "topic_uuid": "Device_Anomaly_Detection_Results",
#             "value": {
#                 "description": "Device Anomaly Detection Results",
#                 "requestor_id": "Device123",
#                 "requestor_type": "NSSD",
#                 "request_id": "Device123_22/05/2023",
#                 "analyzer_id": str(analyzer_id),
#                 "analysis_id": str(analysis_id),
#                 "connected": True,
#                 "anomaly": "True",
#             },
#         }
#     }

#     response = app.app.temperature(
#         temps, requestor_id, requestor_type, request_id
#     )
#     assert response == ws_req_final



import pytest
from app.app import create_sequences,on_error,on_close,on_open,temperature
from unittest.mock import MagicMock, patch
import json
import datetime
from app import app

def test_create_sequences():
    values = [1, 2, 3, 4, 5]
    time_steps = 3
    result = create_sequences(values, time_steps)
    expected_result = [
        [1, 2, 3],
        [2, 3, 4],
        [3, 4, 5],
    ]
    assert result.tolist() == expected_result

def test_on_error():
    error = "WebSocket error occurred"

    with patch("builtins.print") as mock_print:
        on_error(None, error)

    mock_print.assert_called_once_with(error)

def test_on_close():
    close_status_code = 1000
    close_msg = "Connection closed"

    with patch("builtins.print") as mock_print:
        on_close(None, close_status_code, close_msg)

    mock_print.assert_called_once_with("### Connection closed ###")

def test_on_open():
    with patch("builtins.print") as mock_print:
        on_open(None)

    mock_print.assert_called_once_with("### Connection established ###")


# def test_temperature():
#     temps = "22,23,21,26,25,20,28,29,23,28,21,22,25,27,30,29,29,26,21,26,23,24,25,24,22,23,21,26,25,20,28,29,23,28,21,22,25,27,30,29,29,26,21,26,23,24,25,24"
#     requestor_id = "123"
#     requestor_type = "TypeA"
#     request_id = "456"

#     # Mock platform.node() function to return a fixed value
#     with patch("platform.node", return_value="mocked_analyzer_id"):
#         # Mock datetime.datetime.now() to return a fixed value
#         with patch("datetime.datetime") as mock_datetime:
#             mock_datetime.now.return_value = datetime.datetime(2023, 7, 28, 12, 34, 56)

#             # Mock hashlib.sha256() to return a fixed hash value
#             with patch("hashlib.sha256") as mock_sha256:
#                 mock_sha256_instance = mock_sha256.return_value
#                 mock_sha256_instance.hexdigest.return_value = "mocked_hash_value"

#                 # Mock the websocket.WebSocketApp class
#                 with patch("websocket.WebSocketApp") as mock_ws:
#                     # Mock the send method of the WebSocketApp object
#                     mock_ws_instance = mock_ws.return_value
#                     mock_ws_instance.send = MagicMock()

#                     response = app.app.test_client().get(f'/temperature/{temps}/{requestor_id}/{requestor_type}/{request_id}')

#     # Assertions
#     expected_analysis_id = "mocked_analyzer_id2023-07-28 12:34:56mocked_hash_value"
#     assert response.status_code == 200
#     data = response.get_json()
#     assert data['RequestPostTopicUUID']['value']['connected'] is True

#     # Check if the WebSocketApp constructor was called with the expected arguments
#     mock_ws.assert_called_once_with(
#         "ws://localhost:3000/ws",
#         on_open=ANY,
#         on_error=ANY,
#         on_close=ANY,
#     )

#     # Check if the WebSocketApp send method was called with the expected payload
#     mock_ws_instance.send.assert_called_once()
#     args, kwargs = mock_ws_instance.send.call_args
#     ws_req_final = json.loads(args[0])
#     assert ws_req_final['RequestPostTopicUUID']['value']['analyzer_id'] == "mocked_analyzer_id"
#     assert ws_req_final['RequestPostTopicUUID']['value']['analysis_id'] == expected_analysis_id
#     assert ws_req_final['RequestPostTopicUUID']['value']['connected'] is True
#     assert ws_req_final['RequestPostTopicUUID']['value']['anomaly'] == "False"