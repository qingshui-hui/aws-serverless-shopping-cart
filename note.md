#
[repo](https://github.com/aws-samples/aws-serverless-shopping-cart)

https://code.visualstudio.com/docs/python/debugging
特にDebugging specific app typesが参考になる。

mock
https://adamj.eu/tech/2020/10/13/how-to-mock-environment-variables-with-pythons-unittest/

[aws-lambda-powertools](https://awslabs.github.io/aws-lambda-powertools-python/latest/)
[pytest import](https://stackoverflow.com/questions/25827160/importing-correctly-with-pytest)

## 環境構築
windows
https://github.com/coreybutler/nvm-windows
https://qiita.com/kota344/items/c47ed4d0deb4dc446f35

nvm useがエラーになり、管理者権限で実行すると治る場合があるようだったが、nodejsのインストール先に直接パスを通した。
C:\Users\upl-member\scoop\persist\nvm\nodejs\v16.14.0

- nvm (1.1.9)
- node 16.14.0, npm 8.5.3
- yarn 1.22.17
- Make for Windows
  - 依存するdllファイルもダウンロードし、パスを通すことに注意する。
  - in desktop
- sam-cli 1.40.1
  - scoop install aws-sam-cli msiファイルをローカルユーザ権限で実行してくれる。
- aws 2.4.23
  - via scoop
  - https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-configure-quickstart.html

C:\Users\upl-member\AppData\Local\Amazon\AWSSAMCLI\

https://classic.yarnpkg.com/en/docs/selective-version-resolutions

**awsへの接続確認**

windows

```:cmd
aws configure --profile saiki
aws configure list
aws dynamodb list-tables --profile saiki

type %USERPROFILE%\.aws\config
set AWS_PROFILE=saiki
setx AWS_PROFILE saiki
aws dynamodb list-tables

set AWS_DEFAULT_PROFILE=saiki
setx AWS_DEFAULT_PROFILE saiki
```

## 記録
Windows fatal exception: access violation
https://github.com/pytest-dev/pytest/issues/7634#issuecomment-672863350
pytestの代わりにpython -m pytestで実行するとそのエラーが表示されなくなる。
オプションで -p no:faulthandlerを設定する方法もある。

Metricsを使用している場合は次の2つの環境変数をセットする。
set POWERTOOLS_SERVICE_NAME="Example"
set POWERTOOLS_METRICS_NAMESPACE="Application"
https://awslabs.github.io/aws-lambda-powertools-python/latest/core/metrics/#testing-your-code
すると、validation errorは起こらなくなるが、UserWarningは起こることがあるため、無視するリストに加えてもよい。

coverage
pytest --cov=shopping-cart-service

### Cognito
API Gateway layerでログインのチェックを行うと、event["requestContext"]["authorizer"]["claims"]["sub"]に値が含まれる。
backend\shopping-cart-service\checkout_cart.pyを参照する。

> Because this method is authorized at API gateway layer, we don't need to validate the JWT claims here

ログイン済みか自分でチェックするにはHeaderのAuthorizationの値をcognitojwt.decodeで問い合わせる。

### Lambda Powertools Python
CloudWatchで確認できるログやトレースなどを補助するツール
Tracer  -> CloudWatch X-Rayのトレース
Logger  -> CloudWatch ログ
Metrics -> CloudWatch メトリクス
