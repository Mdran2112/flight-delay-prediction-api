# Flight delay prediction REST API
This is a REST API, built with Python and FastAPI, that can be used to serve a scikit-learn binary model classifier for 
predicting if a flight will be delayed or not. Some examples of binary classifier pipelines can be trained and prepared for deployment 
using the Jupyter notebook located in the `notebook/` folder. A preprocessed dataset was included (features.csv), so it can be used to replicate 
the training pipeline and testing metrics.
The API has three endpoints: 

#### POST  /prediction-server/predictions
Make predictions for a batch of observationd, using a binary classifier previously loaded (see next endpoint). 
Requires a json body with this schema:
```
{
  "flights": [
    {
      "flight_id": <integer>,
      "OPERA": <string>,
      "TIPOVUELO": <string>,
      "MES": <integer>
    },
    ...
  ]
```

`OPERA`, `TIPOVUELO` and `MES` are categorical variables needed by the model pipeline (see the training workflow in the jupyter notebook.)

#### PUT   /prediction-server/model/{model-name}
It is used to load/change the classification model package and configure the prediction pipeline according to the model configuration file (see Model package). 

#### GET   /prediction-server/model
Returns information about the model currently loaded on the server.


## Model package

A model package represents a group of several files, consumed by the prediction service for classification. 
A "model package" consists in:
* <model_name>.pkl file (saved model pipeline)
* json configuration file (<model_name>_metadata.json)

Those files have to be located inside a folder named as the model itself. For example:
```
my_model/
        |__my_model.pkl
        |__ my_model_metadata.json
```
 Note that the json config filename needs the suffix ```_metadata```.
 The folder ```my_model/``` will be inside the docker ```models``` volume (see docker-compose.yml).

## Prediction Service

The Prediction Service uses the model json configuration file in order to configure how the model output processing will be. 
With that information, it creates a prediction pipeline and delivers a response with the results.

Including the following object in the json file:

```
"post_proc": {
    "type": "threshold",
    "params": {
        "th": <threshold-value>
    }
}
```        

... will tell to the prediction workflow that it has to change the threshold in order to consider that an observation will belong
to the "positive" class if its prediction score (probability) is above that threshold (by default the threshold is 0.5 in binary classifiers).

Otherwise, we can avoid postprocessing by defining `"type": "default"` and `"params": {}`.

## Build & deploy

This repository has a Dockerfile for building a docker image. By executing ```docker_build.sh```, a docker image will be created.
The deploy can be made by using the ```docker-compose.yml``` file. The ```X_API_KEY``` environment variable is for authentication when using the API.
For sending requests, include the header `"X-API-KEY": <X_API_KEY>`.
The model packages (folders with models and json configs) have to be inside the ```models/``` volume.

## Swagger 
The API has its own Swagger portal. It can be used also as a client for sending requests to the API. 
The URL is `http://<host>:5050/docs`

## Tag creation 
The repository has a github workflow for tag creation when merging to master.
When you make a PR to master, include one of the following flags in the commit message string.

* MAJOR CHANGE: `#major`
* MINOR CHANGE: `#minor`
* PATCH: `#patch `
* NONE: `#none`

For example if initial version is v0.0.0, commit message 
`ADD - certain feature #minor` will lead to `v0.1.0`. 
Then, if I make another PR to master with commit `FIX - bug in certain feature #patch`
will lead to `v0.1.1`

The workflow will build the new tag and publish it in the repository.
