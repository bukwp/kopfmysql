from dataclasses import dataclass, field
from unittest import TestCase, mock

from kubernetes.client.models import V1Secret

from .secrets import SecretsMixin, Secret
from .utils import value_for_secret


@dataclass
class SecretTestClass(Secret):
    v1: str
    v2: str
    v3: str = field(init=False)

@dataclass
class SecretTestClass2(Secret):
    v1: str
    v2: str
    v3: str = field(init=False)

@dataclass
class SecretMixinTestClass(SecretsMixin):
    some_value: str
    bad_value: str = field(init=False)
    secret: SecretTestClass
    secret_user: SecretTestClass2
    secret_account: SecretTestClass2


class SecretFieldTestCase(TestCase):

    def test_from_secret(self):
        secret = V1Secret(data=dict(
            v1=value_for_secret("test1"),
            v2=value_for_secret("test2"),
            v3=value_for_secret("test3"),
            v4=value_for_secret("test4"),
        ))
        res = SecretTestClass.from_secret(secret)

        self.assertEqual("test1", res.v1)
        self.assertEqual("test2", res.v2)
        self.assertEqual(2, len(res.__dict__))


class SecretMixinTestCase(TestCase):

    @mock.patch('kopfmysql.secrets.get_secret', side_effect=lambda **k: V1Secret(data=dict(
        v1=value_for_secret("test1"),
        v2=value_for_secret("test2"),
        v3=value_for_secret("test3"),
        v4=value_for_secret("test4"),
    )))
    def test_from_resource(self, get_secret):
        obj = SecretTestClass(v1="test1", v2="test2")

        resource = SecretMixinTestClass.from_resource(
            spec=dict(
                secret="test",
                secret_user="user",
                secret_account="account",
                some_value="test",
            ),
            namespace="namespace"
        )
        self.assertEqual(obj.__dict__, resource.secret.__dict__)
        self.assertEqual(resource.some_value, 'test')
        self.assertIsInstance(resource.secret, SecretTestClass)
        self.assertIsInstance(resource.secret_user, SecretTestClass2)
        self.assertIsInstance(resource.secret_account, SecretTestClass2)
        self.assertEqual(4, len(resource.__dict__.keys()))

    def test_metaclass_validation(self):

        @dataclass
        class BadClass1(SecretsMixin):
            secret: Secret

        with self.assertRaises(TypeError) as exc:
            @dataclass
            class BadClass1(SecretsMixin):
                secret: str
