# WP4 Analytic: Privacy-Aware Device Fault Detection

[![Actions Status][actions badge]][actions]
[![CodeCov][codecov badge]][codecov]
[![LICENSE][license badge]][license]

<!-- Links -->
[actions]: https://github.com/sifis-home/flask-device-anomaly-detection/actions
[codecov]: https://codecov.io/gh/sifis-home/flask-device-anomaly-detection
[license]: LICENSES/MIT.txt

<!-- Badges -->
[actions badge]: https://github.com/sifis-home/flask-device-anomaly-detection/workflows/flask-device-anomaly-detection/badge.svg
[codecov badge]: https://codecov.io/gh/sifis-home/flask-device-anomaly-detection/branch/master/graph/badge.svg
[license badge]: https://img.shields.io/badge/license-MIT-blue.svg

Faulty devices can either affect the whole performance of a system by getting disconnected or by staying connected to the network while not performing as expected and sending wrong readings to intended data recipients. The aim of this analytic is to ensure network reliability, service availability, good performance, and better monitoring of connected devices for service restoring and correction action time minimization in case an anomaly has been detected. 

Device fault detection uses time series data collected from sensors such as readings of humidity, temperature, noise, vibration, and air flows. Then this analytic processes these data and flags abnormal data deviations based on a specific threshold defined after the training phase leveraging readings during normal device behaviour. The device fault detection analytic uses an unsupervised learning method since the anomaly that might occur is unknown and not expected. A type of artificial neural network trained on unlabelled dataset, namely Autoencoder, is used in this context.

The used dataset to train the model is Intel Berkeley Research Lab Sensor [(IBRL) Dataset](http://db.csail.mit.edu/labdata/labdata.html), should be exported from the previous link and saved as "data.txt" of the same directory as the code. It contains information about data collected from 54 sensors deployed in the Intel Berkeley Research lab between February 28th and April 5th, 2004. This dataset includes a log of about 2.3 million readings collected from the sensors related to temperature, humidity, voltage, and light. Only the data related to temperature and humidity are used in the performed analytics.

Autoencoders are used for anomaly detection, and they are also used for data reconstruction. Thus, real data are kept private and only the reconstructed data are shared. Moreover, differential privacy is used with autoencoders during the analysis phase to minimize data memorization by the analytics model and protect individual data instances privacy. 


## Deploying

### Privacy-Aware Device Fault Detection in a container
The DHT and the Analytics-API containers should be running before starting to build and run the image and container of the Privacy-Aware Device Fault Detection.

Privacy-Aware Device Fault Detection is intended to run in a docker container on port 9090. The Dockerfile at the root of this repo describes the container. To build and run it execute the following commands:

`docker build -t flask-device-anomaly-detection .`

`docker-compose up`

## REST API of Privacy-Aware Device Fault Detection

Description of the REST endpoint available while Privacy-Aware Device Fault Detection is running.

---

#### GET /temperature

Description: Returns the result of the temperature series normal or anomalous.

Command: 

`curl http://localhost:9090/temperature/<temps>/<requestor_id>/<requestor_type>/<request_id>`

Sample Anomalous: 

`curl http://localhost:9090/temperature/22,23,21,26,25,20,28,29,23,28,21,22,25,27,30,29,29,26,21,26,23,24,25,24,22,23,21,26,25,20,28,29,23,28,21,22,25,27,30,29,29,26,21,26,23,24,25,24/123/NSSD/123_23:07:2023`

Sample Normal: 

`curl http://localhost:9090/temperature/19.12986842,18.97528276,18.78109444,18.61134194,18.46130435,18.30064878,18.1754,18.065395,17.95954872,17.85228,17.75864211,17.62884,17.51735882,17.4929,17.46825263,17.50991875,17.88537297,19.29543684,20.3559,20.25651795,20.274,20.95731053,21.19933913,21.20485641,21.28777949,20.93873514,21.19835814,21.46036,21.21860625,21.21743529,20.80544,20.37007027,20.06127179,19.90968387,19.74453953,19.56573548,19.39732,19.26005,19.1358,19.04670909,18.971405,18.89797073,18.84261667,18.8075,18.734,18.64976667,18.56043684,18.4792123/NSSD/123_23:07:2023`

---
## License

Released under the [MIT License](LICENSE).

## Acknowledgements

This software has been developed in the scope of the H2020 project SIFIS-Home with GA n. 952652.
