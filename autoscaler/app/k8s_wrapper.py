from kubernetes import client, config
from log import logger


class K8sAutoScaler:

    def __init__(self, options):
        self.options = options
        config.load_incluster_config()
        self.client = client.AppsV1Api()

    def get_deployment(self):
        label = "app={}".format(self.options['kubernetes_deployment'])

        deployments = self.client.list_namespaced_deployment(namespace=self.options['kubernetes_namespace'],
                                                             label_selector=label)
        deployment = deployments.items[0]
        return deployment

    def update_deployment(self, deployment):
        self.client.patch_namespaced_deployment(name=self.options['kubernetes_deployment'],
                                                namespace=self.options['kubernetes_namespace'],
                                                body=deployment)

    def get_current_replica_count(self):
        deployment = self.get_deployment()
        return deployment.spec.replicas

    def scale_out(self):
        deployment = self.get_deployment()
        deployment.spec.replicas += 1
        logger.info('Scaling out to {} replicas'.format(deployment.spec.replicas))
        self.update_deployment(deployment)

    def scale_in(self):
        deployment = self.get_deployment()
        if deployment.spec.replicas == 0:
            return
        deployment.spec.replicas -= 1
        logger.info('Scaling in to {} replicas'.format(deployment.spec.replicas))
        self.update_deployment(deployment)
