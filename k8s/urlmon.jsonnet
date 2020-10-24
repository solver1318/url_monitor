local namespace = std.extVar('namespace');
local replicas = std.parseInt(std.extVar('replicas'));
local port = std.parseInt(std.extVar('port'));
local image = std.extVar('image');

local label = {'app': 'urlmon'};
local configName = 'urlmon-config';
local svcName = 'urlmon-service';

local ns = {
    apiVersion: 'v1',
    kind: 'Namespace',
    metadata: {
        name: namespace
    }
};

local deploy = {
    apiVersion: 'apps/v1',
    kind: 'Deployment',
    metadata: {
        name: 'urlmon',
        namespace: namespace,
        labels: {
            app: 'urlmon'
        }
    },
    spec: {
        replicas: replicas,
        selector: {
            matchLabels: label
        },
        template: {
            metadata: {
                labels: label
            },
            spec: {
                containers: [
                    {
                        command: ['python', '/app/url_mon.py', std.toString(port)],
                        env: [{'name': 'CONFIG_PATH', 'value': '/config/config.json'}],
                        image: image,
                        imagePullPolicy: 'IfNotPresent',
                        livenessProbe: {
                            failureThreshold: 5,
                            tcpSocket: {port: port},
                            initialDelaySeconds: 60,
                            periodSeconds: 10,
                            successThreshold: 1,
                            timeoutSeconds: 5
                        },
                        readinessProbe: {
                            failureThreshold: 3,
                            tcpSocket: {port: port},
                            periodSeconds: 10,
							successThreshold: 1,
							timeoutSeconds: 1
                        },
                        name: 'urlmon',
                        ports: [{
                            containerPort: port,
                            name: 'metrics',
							protocol: 'TCP'
                        }],
                        resources: {
                            limits: {
                                memory: '170Mi',
                                "ephemeral-storage": '512Mi'
                            },
                            requests: {
                                cpu: '100m',
                                memory: '70Mi',
                                "ephemeral-storage": '512Mi'
                            }
                        },
                        volumeMounts: [{
                            mountPath: '/config',
                            name: 'config-volume',
                            readOnly: true
                        }]
                }],
                restartPolicy: 'Always',
                volumes: [
                    {
                        configMap: {
                            defaultMode: 420,
                            name: configName
                        },
                        name: 'config-volume'
                    }
                ]
            }
        }
    }
};

local svc = {
    apiVersion: 'v1',
    kind: 'Service',
    metadata: {
        name: svcName,
        namespace: namespace
    },
    spec: {
        type: 'ClusterIP',
        selector: label,
        ports: [{name: "urlmon", port: port, protocol: "TCP",targetPort: port}]
    }
};

local configJson = importstr 'config.json';
local cm = {
    apiVersion: 'v1',
    kind: 'ConfigMap',
    metadata: {
        name: configName,
        namespace: namespace
    },
    data: {'config.json': configJson}
};

local clientCronJob = {
    apiVersion: 'batch/v1beta1',
    kind: 'CronJob',
    metadata: {
        name: 'client-job',
        namespace: namespace
    },
    'spec': {
        successfulJobsHistoryLimit: 5,
        failedJobsHistoryLimit: 5,
        schedule: '*/1 * * * *', # Every 1 min
        jobTemplate: {
            spec: {
                template: {
                    spec: {
                        containers: [
                            {
                                name: 'client-job',
                                image: 'curlimages/curl',
                                args: ['-s', '-XGET', 'http://' + svcName + ':' + std.toString(port) + '/metrics']
                            }
                        ],
                        restartPolicy: 'OnFailure'
                    }
                }
            }
        }
    }
};

{
	kind: 'List',
	apiVersion: 'v1',
	items: [ns, deploy, svc, cm, clientCronJob]
}