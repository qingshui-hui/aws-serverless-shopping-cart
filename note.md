#
[repo](https://github.com/aws-samples/aws-serverless-shopping-cart)

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
