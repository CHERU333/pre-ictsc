## 問題を解くための演習環境構築
Dev Container（とVSCode）とContainer Lab（とDocker Desktop）を扱う

参考：

[GitHub](https://github.com/srl-labs/containerlab/pkgs/container/containerlab%2Fdevcontainer-dood-slim)

1. VSCodeからDevContainerをインストール（ver.0.427.0）
2. image versionの最新化のために、以下のコマンドを実行

```jsx
docker pull [ghcr.io/srl-labs/containerlab/devcontainer-dood-slim:sha-7ef796f](http://ghcr.io/srl-labs/containerlab/devcontainer-dood-slim:sha-7ef796f~)
```

参考：

[GitHub](https://github.com/srl-labs/containerlab/pkgs/container/containerlab%2Fdevcontainer-dood-slim)

1. 自分の作業したいディレクトリのルートに、`.devcontainer` ディレクトリを作成
2. そのディレクトリの中に`devcontainer.json` を作成し、下記の内容を記載する

```
{
    "image": "ghcr.io/srl-labs/containerlab/devcontainer-dood-slim",
    "runArgs": [
        "--network=host",
        "--pid=host",
        "--privileged"
    ],
    "mounts": [
        "type=bind,src=/var/lib/docker,dst=/var/lib/docker",
        "type=bind,src=/lib/modules,dst=/lib/modules"
    ],
    "workspaceFolder": "${localWorkspaceFolder}",
    "workspaceMount": "source=${localWorkspaceFolder},target=${localWorkspaceFolder},type=bind,consistency=cached"
}
```

1. VSCode左下の青いアイコン(Open a Remote Window)を押して、「Reopen in Container」を選択すると裏でDockerが起動する。
2. 起動したら`containerlab version` を実行すると

```jsx
❯ containerlab version
  ____ ___  _   _ _____  _    ___ _   _ _____ ____  _       _     
 / ___/ _ \| \ | |_   _|/ \  |_ _| \ | | ____|  _ \| | __ _| |__  
| |  | | | |  \| | | | / _ \  | ||  \| |  _| | |_) | |/ _` | '_ \ 
| |__| |_| | |\  | | |/ ___ \ | || |\  | |___|  _ <| | (_| | |_) |
 \____\___/|_| \_| |_/_/   \_\___|_| \_|_____|_| \_\_|\__,_|_.__/ 

    version: 0.71.0
     commit: 7ef796f07
       date: 2025-10-10T17:36:13Z
     source: https://github.com/srl-labs/containerlab
 rel. notes: https://containerlab.dev/rn/0.71/
```

---

使い方の理解・試してみる

1. トポロジーファイルのDL

```jsx
❯ mkdir quick-start
❯ cd quick-start 
❯ curl -LO \
https://raw.githubusercontent.com/srl-labs/containerlab/main/lab-examples/srlceos01/srlceos01.clab.yml
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   306  100   306    0     0   1303      0 --:--:-- --:--:-- --:--:--  1307

/Users/ri/ictsc/pre-ictsc/quick-start                                          
❯ docker images | grep ceos
何も出ない
```

このラボでは、Nokia SR LinuxイメージとArista cEOSイメージが含まれている。

Nokia SR Linuxは一般公開されているイメージで誰でも取得できるが、Arista cEOSイメージはパブリックレジストリでは入手できない。よって、イメージのDLのために以下の手順を踏む。

1. Aristaに会員登録しよう(arista.com)、メールアドレスを有効化しないといけないので注意
2. `cEOS64-lab-4.32.0F.tar.xz` をDLして、そのファイルがあるフォルダに移動し、以下のコマンドをうつ

```jsx
# コンテナ・イメージをインポートし、ceos:4.32.0Fという名前で保存する
docker import cEOS64-lab-4.32.0F.tar.xz ceos:4.32.0F
```

この後、docker imagesしたらこうなるはず

```jsx
docker images | grep ceos
ceos                                                   4.32.0F       716a06da483f   2 minutes ago   3.35GB
```

1. Docker Desktop の Rosetta エミュを有効化

Docker Desktop → Settings → General（または Features in development）で“Use Rosetta for x86/amd64 emulation on Apple Silicon”をONにして、再起動

Use Rosetta for x86_64/amd64 emulation on Apple Silicon

Turns on Rosetta to accelerate x86_64/amd64 binary emulation on Apple Silicon.Note: You must have Apple Virtualization framework enabled.

1. デプロイをしてみよう

クリーンアップしてデプロイする。

```jsx
❯ sudo containerlab destroy -t srlceos01.clab.yml -c
sudo containerlab deploy  -t srlceos01.clab.yml
06:43:46 INFO Parsing & checking topology file=srlceos01.clab.yml
06:43:46 INFO Parsing & checking topology file=srlceos01.clab.yml
06:43:46 INFO Destroying lab name=srlceos01
06:43:46 INFO Removed container name=clab-srlceos01-ceos
06:43:46 INFO Removed container name=clab-srlceos01-srl
06:43:46 INFO Removing host entries path=/etc/hosts
06:43:46 INFO Removing SSH config path=/etc/ssh/ssh_config.d/clab-srlceos01.conf
06:43:46 INFO Containerlab started version=0.71.0
06:43:46 INFO Parsing & checking topology file=srlceos01.clab.yml
06:43:46 INFO Creating docker network name=clab IPv4 subnet=172.20.20.0/24 IPv6 subnet=3fff:172:20:20::/64 MTU=0
06:43:46 INFO Creating lab directory path=/Users/ri/ictsc/pre-ictsc/quick-start/clab-srlceos01
06:43:46 INFO unable to adjust Labdir file ACLs: operation not supported
06:43:46 INFO Creating container name=srl
06:43:46 INFO Creating container name=ceos
06:43:47 INFO Running postdeploy actions for Arista cEOS 'ceos' node
06:43:47 INFO Created link: srl:e1-1 (ethernet-1/1) ▪┄┄▪ ceos:eth1
06:43:47 INFO Running postdeploy actions kind=nokia_srlinux node=srl
06:44:17 INFO Adding host entries path=/etc/hosts
06:44:17 INFO Adding SSH config for nodes path=/etc/ssh/ssh_config.d/clab-srlceos01.conf
You are on the latest version (0.71.0)
╭─────────────────────┬─────────────────────────────┬─────────┬───────────────────╮
│         Name        │          Kind/Image         │  State  │   IPv4/6 Address  │
├─────────────────────┼─────────────────────────────┼─────────┼───────────────────┤
│ clab-srlceos01-ceos │ arista_ceos                 │ running │ 172.20.20.2       │
│                     │ ceos:4.32.0F                │         │ 3fff:172:20:20::2 │
├─────────────────────┼─────────────────────────────┼─────────┼───────────────────┤
│ clab-srlceos01-srl  │ nokia_srlinux               │ running │ 172.20.20.3       │
│                     │ ghcr.io/nokia/srlinux:24.10 │         │ 3fff:172:20:20::3 │
╰─────────────────────┴─────────────────────────────┴─────────┴───────────────────╯
```

1. 入れるかを確認

SR Linux

```jsx
❯ docker exec -it clab-srlceos01-srl sr_cli
Using configuration file(s): []
Welcome to the srlinux CLI.
Type 'help' (and press <ENTER>) if you need any help using this.
--{ running }--[  ]--
A:srl#
```

cEOS

```jsx
❯ docker exec -it clab-srlceos01-ceos FastCli -p 15 -c 'show version'
Arista cEOSLab
Hardware version: 
Serial number: 
Hardware MAC address: 001c.73cb.7cc6
System MAC address: 001c.73cb.7cc6

Software image version: 4.32.0F-36401836.4320F (engineering build)
Architecture: x86_64
Internal build version: 4.32.0F-36401836.4320F
Internal build ID: e97bbe15-478c-45d1-84fa-332db23aef84
Image format version: 1.0
Image optimization: None

cEOS tools version: (unknown)
Kernel version: 6.10.14-linuxkit

Uptime: 0 minutes
Total memory: 8025424 kB
Free memory: 1892876 kB

❯ docker exec -it clab-srlceos01-ceos Cli
ce
```

お片付け

```jsx
❯ sudo containerlab destroy -t srlceos01.clab.yml -c
06:59:57 INFO Parsing & checking topology file=srlceos01.clab.yml
06:59:57 INFO Parsing & checking topology file=srlceos01.clab.yml
06:59:57 INFO Destroying lab name=srlceos01
06:59:57 INFO Removed container name=clab-srlceos01-srl
06:59:57 INFO Removed container name=clab-srlceos01-ceos
06:59:57 INFO Removing host entries path=/etc/hosts
06:59:57 INFO Removing SSH config path=/etc/ssh/ssh_config.d/clab-srlceos01.conf

```
