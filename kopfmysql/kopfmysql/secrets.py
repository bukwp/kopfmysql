from dataclasses import dataclass

from kubernetes.client import V1Secret

from .utils import value_from_secret, get_secret


@dataclass
class Secret:
    """
    CRD field that can initalize from `V1Secret`.
    """
    @classmethod
    def from_secret(cls, secret: V1Secret):
        return cls(
            **{
                # TODO validation
                k: value_from_secret(secret, k)
                for k in cls.__dataclass_fields__.keys()
                if all((
                    cls.__dataclass_fields__[k].init is True,
                    secret.data.get(k, None) is not None,
                ))
            }
        )


class SecretResourceMetaClass(type):

    def __init__(cls, name, bases, clsdict):
        """
        A basic check for each secret type.
        """
        # TODO validate on dataclass?
        for field, field_type in clsdict.get("__annotations__", {}).items():
            if field.startswith('secret'):
                if not issubclass(field_type, Secret):
                    raise TypeError(
                        f"{field_type} is not a sublass of {Secret} "
                        f"field: {field} class: {name}"
                    )
        super().__init__(name, bases, clsdict)


@dataclass
class SecretsMixin(metaclass=SecretResourceMetaClass):
    """
    Custom Resource Definition
    where each field starting with 'secret'
    will be loaded from a secret named with this field value.
    """

    @classmethod
    def get_secret(cls, name, namespace) -> V1Secret:
        # TODO validation; returning exception if secret not found.
        return get_secret(
            name=name,
            namespace=namespace,
        )

    @classmethod
    def field_from_secret(cls, field, secret: V1Secret):
        return cls.__dataclass_fields__[field].type.from_secret(secret)

    @classmethod
    def from_resource(cls, spec: dict, namespace: str):
        init_kwargs = {}

        for field, value in spec.copy().items():
            if field.startswith('secret'):
                v1secret = cls.get_secret(name=field, namespace=namespace)
                init_kwargs[field] = cls.field_from_secret(field=field, secret=v1secret)
                spec.pop(field)

        init_kwargs.update(spec)
        return cls(**init_kwargs)

