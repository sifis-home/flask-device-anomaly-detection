from unittest.mock import MagicMock, patch

import pytest

import app.app
import platform
import datetime
import hashlib


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

def test_temperature():
    tems = "22,23,21,26,25,20,28,29,23,28,21,22,25,27,30,29,29,26,21,26,23,24,25,24,22,23,21,26,25,20,28,29,23,28,21,22,25,27,30,29,29,26,21,26,23,24,25,24"
    requestor_id = "Device123"
    requestor_type = "NSSD"
    request_id = "Device123_22/05/2023"

    analyzer_id = platform.node()

    # Get current date and time
    now = datetime.datetime.now()

    # Generate a random hash using SHA-256 algorithm
    hash_object = hashlib.sha256()
    hash_object.update(bytes(str(now), 'utf-8'))
    hash_value = hash_object.hexdigest()

    # Concatenate the time and the hash
    analysis_id = str(analyzer_id) + str(now) + hash_value

    ws_req_final = {
                    "RequestPostTopicUUID": {
                    "topic_name": "SIFIS:Privacy_Aware_Device_Anomaly_Detection_Results",
                    "topic_uuid": "Device_Anomaly_Detection_Results",
                    "value": {
                        "description": "Device Anomaly Detection Results",
                        "requestor_id": "Device123",
                        "requestor_type": "NSSD",
                        "request_id": "Device123_22/05/2023",
                        "analyzer_id": str(analyzer_id),
                        "analysis_id": str(analysis_id),
                        "connected": True,
                        "anomaly": "True"
                    }
                }
            }

    response = app.app.temperature(temps,requestor_id,requestor_type,request_id)

# def test_transform_json_to_instance():
#     # Dato un dato JSON con solo alcuni attributi validi
#     json_data = '{"brk": 1, "openat": 2, "read": 3}'
#     expected_instance = [
#         1,
#         0,
#         0,
#         0,
#         2,
#         0,
#         0,
#         3,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#         0,
#     ]

#     # Chiama la funzione transform_json_to_instance con il dato JSON
#     instance = kernel_classification.transform_json_to_instance(json_data)
#     print("expected instance: " + str(expected_instance))
#     print("instance: " + str(instance))

#     # Verifica che l'istanza restituita sia uguale a quella attesa
#     assert instance == expected_instance


# def test_on_message(mock_kernel_classification):
#     ws = MagicMock()
#     message = '{"Persistent": {"topic_name": "SIFIS:Privacy_Aware_Device_KERNEL_monitor", "value": {"Dictionary": {"key": "value"}}}}'

#     # Call the on_message function with the mock WebSocket and message
#     catch_topic.on_message(ws, message)

#     # Assert that kernel_classification.receive_data() is called with the correct dictionary
#     mock_kernel_classification.assert_called_once_with({"key": "value"})


# def test_on_error():
#     error = "WebSocket error occurred"

#     with patch("builtins.print") as mock_print:
#         catch_topic.on_error(None, error)

#     mock_print.assert_called_once_with(error)


# def test_on_close():
#     close_status_code = 1000
#     close_msg = "Connection closed"

#     with patch("builtins.print") as mock_print:
#         catch_topic.on_close(None, close_status_code, close_msg)

#     mock_print.assert_called_once_with("### Connection closed ###")


# def test_on_open():
#     with patch("builtins.print") as mock_print:
#         catch_topic.on_open(None)

#     mock_print.assert_called_once_with("### Connection established ###")