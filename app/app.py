import datetime
import hashlib
import json
import platform
import re

import numpy as np
import rel
import tensorflow as tf
import websocket
from flask import Flask, json
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow_privacy.privacy.optimizers.dp_optimizer_keras import (
    DPKerasAdamOptimizer,
)

app = Flask(__name__)

training_mean = np.float64(21.92122783091833)
training_std = np.float64(2.4978318311474985)
threshold = np.float64(0.8328843699944564)

TIME_STEPS = 48


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")


def on_open(ws):
    print("### Connection established ###")


def create_sequences(values, time_steps=TIME_STEPS):
    output = []
    for i in range(len(values) - time_steps + 1):
        output.append(values[i : (i + time_steps)])
    return np.stack(output)


model = keras.Sequential(
    [
        layers.Input(shape=(48, 1)),
        layers.Conv1D(
            filters=32,
            kernel_size=7,
            padding="same",
            strides=2,
            activation="relu",
        ),
        layers.Dropout(rate=0.2),
        layers.Conv1D(
            filters=16,
            kernel_size=7,
            padding="same",
            strides=2,
            activation="relu",
        ),
        layers.Conv1DTranspose(
            filters=16,
            kernel_size=7,
            padding="same",
            strides=2,
            activation="relu",
        ),
        layers.Dropout(rate=0.2),
        layers.Conv1DTranspose(
            filters=32,
            kernel_size=7,
            padding="same",
            strides=2,
            activation="relu",
        ),
        layers.Conv1DTranspose(filters=1, kernel_size=7, padding="same"),
    ]
)

optimizer = DPKerasAdamOptimizer(
    l2_norm_clip=1.0,
    noise_multiplier=0.1,
    num_microbatches=1,
    learning_rate=0.001,
)
mse = tf.keras.losses.MeanSquaredError(
    reduction="auto", name="mean_squared_error"
)
model.compile(optimizer=optimizer, loss=mse, metrics=["accuracy"])
model.load_weights("dp_temp_anomaly_model.h5")

@app.route("/temperature/<temps>/<requestor_id>/<requestor_type>/<request_id>")
def temperature(temps, requestor_id, requestor_type, request_id):
    request_id = (
        re.sub("[^a-zA-Z0-9\n\.]", "", request_id)
        .replace("\n", "")
        .replace(" ", "")
    )
    analyzer_id = platform.node()

    # Get current date and time
    now = datetime.datetime.now()

    # Generate a random hash using SHA-256 algorithm
    hash_object = hashlib.sha256()
    hash_object.update(bytes(str(now), "utf-8"))
    hash_value = hash_object.hexdigest()

    # Concatenate the time and the hash
    analysis_id = str(analyzer_id) + str(now) + hash_value

    temps = list(temps.split(","))
    temp = [float(i) for i in temps]
    sum(temp) / len(temp)

    g = (temp - training_mean) / training_std
    w = create_sequences(g)
    w = np.reshape(w, (len(w), 48, 1))
    model.predict(w)
    mae_loss = np.mean(np.abs(model.predict(w) - w), axis=1)
    mae_loss = mae_loss.reshape((-1))

    anomaly = mae_loss > threshold

    ws_req_final = {
        "RequestPostTopicUUID": {
            "topic_name": "SIFIS:Privacy_Aware_Device_Anomaly_Detection_Results",
            "topic_uuid": "Device_Anomaly_Detection_Results",
            "value": {
                "description": "Device Anomaly Detection Results",
                "requestor_id": str(requestor_id),
                "requestor_type": str(requestor_type),
                "request_id": str(request_id),
                "analyzer_id": str(analyzer_id),
                "analysis_id": str(analysis_id),
                "connected": True,
                "anomaly": str(anomaly[0]),
            },
        }
    }

    ws.send(json.dumps(ws_req_final))
    return ws_req_final


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "ws://localhost:3000/ws",
        on_open=on_open,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt

    app.run(host="0.0.0.0", port=9090)
