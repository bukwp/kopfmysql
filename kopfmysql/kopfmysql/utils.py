from base64 import b64decode, b64encode
import kubernetes


def value_for_secret(value):
    return b64encode(value.encode('utf-8'))

def value_from_secret(secret, key):
    return b64decode(secret.data[key]).decode('utf-8')

def get_secret(name, namespace):
    return kubernetes.client.CoreV1Api().read_namespaced_secret(
        name=name,
        namespace=namespace,
    )
