## Author: Dongyou James Seo
Linkedin: https://www.linkedin.com/in/dongyou-james-seo

## Project name: urlmon
Simple python webserver which has one path **/metrics** and collect URL availability and response time(ms). \
**GET /metrics**: collect availability, UP(1) or DOWN(0), and URL response time in Prometheus format like this:
```BASH
sample_external_url__up{url="https://httpstat.us/503"} 0.0
sample_external_url__response_ms{url="https://httpstat.us/503"} 155.116
sample_external_url__up{url="https://httpstat.us/200"} 1.0
sample_external_url__response_ms{url="https://httpstat.us/200"} 93.34
```

## Prerequisites
Please prepare the below prerequisites before start.
1. python3
2. jsonnet
3. kubectl
4. pip packages
```BASH
pip install -r requirements.txt
```

## How to run unittests
It simply verifies class one by one and in case of Collector and HTTPConnector classes, set up a mock server and the test cases actually uses the classes to access the mock server and collect metrics.  
```BASH
python -m unittest discover -v
test_collectFromWrongURL (test.test_collector.TestCollector) ... 2020-10-23 19:01:03,589         [DEBUG | http_connector.py:23] > GET http://localhost:9999/404
127.0.0.1 - - [23/Oct/2020 19:01:04] "GET /404 HTTP/1.1" 404 -
ok
/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.7/lib/python3.7/unittest/suite.py:107: ResourceWarning: unclosed <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 9999)>
  for index, test in enumerate(self):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
test_collectSuccessfully (test.test_collector.TestCollector) ... 2020-10-23 19:01:04,613         [DEBUG | http_connector.py:23] > GET http://localhost:9999/200
127.0.0.1 - - [23/Oct/2020 19:01:06] "GET /200 HTTP/1.1" 200 -
2020-10-23 19:01:06,618          [DEBUG | collector.py:35] > HTTP Status (200) and elapsedTime (2003.506 ms) 
2020-10-23 19:01:06,618          [DEBUG | collector.py:49] > Collecting done
2020-10-23 19:01:06,618          [DEBUG | http_connector.py:23] > GET http://localhost:9999/503
127.0.0.1 - - [23/Oct/2020 19:01:07] "GET /503 HTTP/1.1" 503 -
2020-10-23 19:01:07,627          [DEBUG | collector.py:35] > HTTP Status (503) and elapsedTime (1007.254 ms) 
2020-10-23 19:01:07,627          [DEBUG | collector.py:49] > Collecting done
ok
/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.7/lib/python3.7/unittest/suite.py:84: ResourceWarning: unclosed <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 9999)>
  return self.run(*args, **kwds)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
test_getTargets (test.test_config.TestConfig) ... ok
testAccessToMockserver (test.test_http_connector.TestHttpConnector) ... 2020-10-23 19:01:08,135          [DEBUG | http_connector.py:23] > GET http://localhost:9999/200
127.0.0.1 - - [23/Oct/2020 19:01:09] "GET /200 HTTP/1.1" 200 -
2020-10-23 19:01:09,145          [DEBUG | http_connector.py:23] > GET http://localhost:9999/503
127.0.0.1 - - [23/Oct/2020 19:01:10] "GET /503 HTTP/1.1" 503 -
ok
test_getLogger (test.test_utils.TestUtils) ... ok
test_retouch (test.test_utils.TestUtils) ... ok

----------------------------------------------------------------------
Ran 6 tests in 7.069s

OK
```

## How to locally run urlmon for debug purpose
1. Prepare config.json
```JSON
{
	"TARGETS": [
	    "<any URL1 like https://httpstat.us/503>",
	    "<any URL2 like https://httpstat.us/200>",
        ...
    ]
}
```
2. Export CONFIG_PATH
```BASH
export CONFIG_PATH=config.json
```

3. Run main python file
```BASH
python src/url_mon.py <target port>

For example,
python src/url_mon.py 8080
2020-10-23 19:16:58,504          [INFO | url_mon.py:53] > Serving on port 8080...
``` 

## How to build docker
```BASH
docker buld -t <imageName>:<any tag> ./

For example, 
docker build -t test-image-42:vmware ./
Sending build context to Docker daemon  16.15MB
Step 1/5 : FROM python:3.7-slim
 ---> 217e85391449
Step 2/5 : WORKDIR /app
 ---> Using cache
 ---> 09c6ebf72cda
Step 3/5 : COPY src/ .
 ---> Using cache
 ---> 91dad9105ea9
Step 4/5 : COPY requirements.txt .
 ---> Using cache
 ---> 6cf40818a4e8
Step 5/5 : RUN pip install -r requirements.txt
 ---> Using cache
 ---> 65dafa3bc2c9
Successfully built 65dafa3bc2c9
Successfully tagged test-image-42:vmware
```
If you wanna push the image into docker hub and use it in non-local Kubernetes.
```
docker login
docker tag <imageName>:<any tag> <your account name>/<imageName>:<any tag>
docker push <your account name>/<imageName>:<any tag>
```

## How to generate kubernetes manifest
To generate the manifest, we need to define the below ones in Jsonnet command.
1. namespace
2. number of replicas
3. target port number
4. image built in previous section: \<imageName\>:\<any tag\>
```BASH
jsonnet urlmon.jsonnet --ext-str namespace=<namespace> --ext-str replicas=<number of replicas> --ext-str port=<target port number> --ext-str image=<the image> > <k8s manifest name>.json

For example,
jsonnet urlmon.jsonnet --ext-str namespace=url-monitoring --ext-str replicas=1 --ext-str port=8080 --ext-str image=solver1318/test-image-42:vmware > k8s.json
```

## How to deploy
```BASH
kubectl apply -f <k8s manifest JSON file path>

For example,
kubectl apply -f k8s.json
```

## Description
After **How to deploy**, you deployed total 5 K8s resources.
1. Namespace: your target namespace
2. Deployment: urlmon : urlmon backend deployment
3. Service: urlmon-service : internal load balancer and redirect traffics to urlmon pod(s) 
4. ConfigMap: urlmon-config : configuration which includes target URLs
5. CronJob: client-job : Client Cronjob which accesses to http://urlmon-service:8080/metrics every 1min and receives the metrics

```BASH
kubectl get pods -n url-monitoring
NAME                          READY   STATUS      RESTARTS   AGE
client-job-1603505940-dzn5k   0/1     Completed   0          4m37s
client-job-1603506000-zlrwk   0/1     Completed   0          3m37s
client-job-1603506060-bmpkb   0/1     Completed   0          2m37s
client-job-1603506120-db6rr   0/1     Completed   0          97s
client-job-1603506180-xlncc   0/1     Completed   0          37s
urlmon-64c99b957f-ttkl7       1/1     Running     0          29m

kubectl logs -f client-job-1603506180-xlncc -n url-monitoring
sample_external_url__up{url="https://httpstat.us/503"} 0.0
sample_external_url__response_ms{url="https://httpstat.us/503"} 282.474
sample_external_url__up{url="https://httpstat.us/200"} 1.0
sample_external_url__response_ms{url="https://httpstat.us/200"} 191.151
```
