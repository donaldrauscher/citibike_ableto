About
-----
Ableto take home data challenge

Design a microservice which returns the best station when coming to or departing from the office at various times of day.

Parameters:
Flag for whether arriving or departing
Hour of day

Response:
Optimal station


Slides
-------
Final presentation slides
[Here](https://docs.google.com/presentation/d/1IhHxAeKih0Lj_leoizIes1RjUCTLcWAhmSYhgmBP31w/edit?usp=sharing)

Contact Info
-----
Nidhin Pattaniyil <npatta01@gmail.com>


API
-----
Request
```
localhost:5000/predict?hour=8&arriving=true
```

Response
```
{
    "flow": -0.0728267233241351,
    "station_name": "W 42 St & 8 Ave"
}
```


Directory
--------
notebooks: jupyter notebook used when exploring models
code: core python code for running model
data: pickle of scikit learn model
k8s:  kubernetes infrastructure file
infrastructure: sample [Terraform](https://www.terraform.io/) code




Installation
------------

## Local
```
conda env create -f environment.yml -n citibike
python app.py

```


## Docker
```
docker build . -t citibke
docker run -p 9018:9018 -t citibke
```



## Prod build

```

export PROJECT_ID=$(gcloud config get-value project -q)
export VERSION=v1.0.0
gcloud docker -- build -t us.gcr.io/${PROJECT_ID}/citibike:${VERSION} -f Dockerfile .
gcloud docker -- push us.gcr.io/${PROJECT_ID}/citibike:${VERSION}


kubectl apply -f k8s/prod/service.yaml 
kubectl apply -f k8s/prod/deployment.yaml 

```

