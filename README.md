# Application documentation

## What the app does
App is a simple FastAPI application that returns JSON responses from the below endpoints.

Following endpoints available:
* `lab/health` - Returns `{"time": <CURRENT DATE/TIME IN ISO8601 FORMAT>}`
* `lab/hello?name=<USER NAME>` - Name is a required parameter. Returns `{"message": "Hello <USER NAME>"}`
* `lab/predict` - Following parameters are required: MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude; Returns prediction for house value
* `lab/bulk-predict` - Requires a list of inputs comprising the following parameters: MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude; Returns a list of predictions for house values
* `lab/docs` - Returns Lab subapp documentation
* `lab/openapi.json` - Returns a JSON object that meets the OpenAPI specification version 3+ for subapp
* `/docs` - Returns main app documentation
* `/openapi.json` - Returns a JSON object that meets the OpenAPI specification version 3+ for main app


## How to deploy application to Azure Kubernetes Service (AKS)
Note: Please ensure you have [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) and [Azure Kubelogin](https://azure.github.io/kubelogin/install.html) installed on your machine.

### Push image to ACR and update tag in kustomization.yaml
Note: As a prerequisite, the kubernetes namespace and image prefix must be updated to your specific namespace (i.e., a namespace that is accessible to you) in the Kubernetes overlay configuration files and the bash script.
1. Authenticate to Azure 
2. In a terminal, navigate to app folder and enter the following: `bash ./build-push.sh`

### Deploy application
1. Authenticate to Azure

2. Authenticate to the AKS cluster: `az aks get-credentials --name <NAME> --resource-group <RESOURCE GROUP> --overwrite-existing`  
 Note: If you need to change your kubernetes context between the AKS cluster and minikube, use the following commands:
    * Minikube: `kubectl config use-context minikube`
    * AKS: `kubectl config use-context <NAME>`

3. Deploy resources.

    * Development - To deploy application to minikube using Kustomize: In a terminal, navigate to app folder, set context to minikube, and enter the following: `kubectl apply -k .k8s/overlays/dev`
    * Production - To deploy application to AKS using Kustomize: In a terminal, navigate to app folder, set context to AKS cluster, and enter the following: `kubectl apply -k .k8s/overlays/prod`

4. Once the application is deployed to the AKS cluster, verify if you can get a prediction from the API. See "Return a prediction" below.


## Return a prediction
### Single prediction
Once application is running, enter the following in a terminal:  
`NAMESPACE=<NAMESPACE>
curl -X 'POST' "https://${NAMESPACE}.<ACR_NAME>.com/lab/predict" -L -H 'Content-Type: application/json' -d '{"MedInc": <FLOAT>, "HouseAge":  <FLOAT>, "AveRooms": <FLOAT>, "AveBedrms": <FLOAT>, "Population": <FLOAT>, "AveOccup": <FLOAT>, "Latitude": <FLOAT>, "Longitude": <FLOAT>}'`
  
Values must be numerals and/or able to be parsed to type float if not entered as a float (i.e., no letters should be entered as values). Values for Latitude must be between -90 and 90, and values for Longitude must be between -180 and 180.
 
Output is returned as a single number of type float. 

#### EXAMPLE
`NAMESPACE=<NAMESPACE>
curl -X 'POST' "https://${NAMESPACE}.<ACR_NAME>.com/lab/predict" -L -H 'Content-Type: application/json' -d '{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.984127, "AveBedrms": 1.023810, "Population": 322.0, "AveOccup": 2.555556, "Latitude": 37.88, "Longitude": -122.23}'`

### Multiple predictions
Once application is running, enter the following in a terminal:  
`NAMESPACE=<NAMESPACE>
curl -X 'POST' "https://${NAMESPACE}.<ACR_NAME>.com/lab/bulk-predict" -L -H 'Content-Type: application/json' -d '{houses: [{"MedInc": <FLOAT>, "HouseAge":  <FLOAT>, "AveRooms": <FLOAT>, "AveBedrms": <FLOAT>, "Population": <FLOAT>, "AveOccup": <FLOAT>, "Latitude": <FLOAT>, "Longitude": <FLOAT>}]}'`
  
Values must be numerals and/or able to be parsed to type float if not entered as a float (i.e., no letters should be entered as values). Values for Latitude must be between -90 and 90, and values for Longitude must be between -180 and 180.
 
Output is returned as a list of numbers of type float. 

#### EXAMPLE
`NAMESPACE=<NAMESPACE>
curl -X 'POST' "https://${NAMESPACE}.<ACR_NAME>.com/lab/bulk-predict" -L -H 'Content-Type: application/json' -d '{"houses": [{"MedInc": 7.3252, "HouseAge": 32.0, "AveRooms": 6.984127, "AveBedrms": 2.023810, "Population": 392.0, "AveOccup": 2.755556, "Latitude": 37.78, "Longitude": -122.23}, {"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.984127, "AveBedrms": 1.023810, "Population": 322.0, "AveOccup": 2.555556, "Latitude": 37.88, "Longitude": -122.23}, {"MedInc": 5.3252, "HouseAge": 80.0, "AveRooms": 6.984127, "AveBedrms": 1.023810, "Population": 352.0, "AveOccup": 2.555556, "Latitude": 37.98, "Longitude": -122.23}]}'`
	
