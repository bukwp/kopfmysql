# kopfmysql
[![Docker Repository on Quay](https://quay.io/repository/bukowwp/kopfmysql/status "Docker Repository on Quay")](https://quay.io/repository/bukowwp/kopfmysql)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: "mysql-credentials"
  namespace: "wordpress"
stringData:
  user: "testaccount"
  password: "testpassword"
  database: "testdatabase"
---
apiVersion: bukwp.kopfmysql/v1alpha1
kind: Account
metadata:
  name: "mysql-account"
  namespace: "wordpress"
spec:
  service: "mysql"
  secret: "mysql-credentials"
---
```
