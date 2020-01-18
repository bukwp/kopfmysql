# from dataclasses import dataclass, field
#
# from providers.crd import SecretField, SecretsMixin
# from providers.mysql.api.v1alpha1.crd_connector import SecretConnectorField
# from providers.mysql.api.v1alpha1.crd_user import SecretUserField
#
#
# @dataclass
# class CRDDatabase(SecretsMixin):
#     """
#     apiVersion: mysql.witcher.space/v1alpha1
#     kind: Database
#     metadata:
#       name: "mysql-example-user"
#       namespace: "mysql"
#     spec:
#       name: "my-database"
#       permissions: "DROP,INSERT,DELETE"
#
#       secret_user: "mysql-example-user"
#       secret_connector: "mysql-example-user"
#     """
#     name: str           # database name
#     permissions: str    # permissions for user on this database
#
#     secret_user: SecretUserField             # name of 'CRDUser' object
#     secret_connector: SecretConnectorField   # name of 'CRDConnector' object
