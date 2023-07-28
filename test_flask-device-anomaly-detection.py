from unittest.mock import patch

from app.app import create_sequences, on_close, on_error, on_open


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
