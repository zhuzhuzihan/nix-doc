# 在 Docker 中使用 Nix

要用 Docker 运行最新的稳定版 Nix，请运行以下命令：

```console
$ docker run -ti docker.io/nixos/nix
Unable to find image 'docker.io/nixos/nix:latest' locally
latest: Pulling from docker.io/nixos/nix
5843afab3874: Pull complete
b52bf13f109c: Pull complete
1e2415612aa3: Pull complete
Digest: sha256:27f6e7f60227e959ee7ece361f75d4844a40e1cc6878b6868fe30140420031ff
Status: Downloaded newer image for docker.io/nixos/nix:latest
35ca4ada6e96:/# nix --version
nix (Nix) 2.3.12
35ca4ada6e96:/# exit
```

> 如果你想要最新的预发布版本，可以使用 ghcr.io/nixos/nix，并可在 https://github.com/nixos/nix/pkgs/container/nix 查看它们

# Nix 的 Docker 镜像包含什么？

官方 Docker 镜像是使用 `pkgs.dockerTools.buildLayeredImage` 创建的（而不是像通常的 Docker 镜像那样使用 `Dockerfile`）。你仍然可以像基于其他任何 Docker 镜像那样，把自定义的 Docker 镜像构建在它之上。

该 Docker 镜像不基于任何其他镜像，并且只包含使用 Nix 所需的最小运行时依赖集。


# 包含最新开发版 Nix 的 Docker 镜像

要获取由 [Hydra](https://hydra.nixos.org) 构建的最新镜像，请运行以下命令：

```console
$ curl -L https://hydra.nixos.org/job/nix/master/dockerImage.x86_64-linux/latest/download/1 | docker load
$ docker run -ti nix:2.5pre20211105
```

你也可以自己从源码构建 Docker 镜像：

```console
$ nix build ./\#hydraJobs.dockerImage.x86_64-linux
$ docker load -i ./result/image.tar.gz
$ docker run -ti nix:2.5pre20211105
```

# 以非 root 用户运行 Nix 的 Docker 镜像

如果你想在容器中以 `root` 以外的用户运行 Nix，可以通过向 `docker.nix` 指定 `uid`、`gid`、`uname` 和 `gname` 参数，构建一个采用非 root 单用户安装的 Nix 镜像：

```console
$ nix build --file docker.nix \
    --arg uid 1000 \
    --arg gid 1000 \
    --argstr uname user \
    --argstr gname user \
    --argstr name nix-user \
    --out-link nix-user.tar.gz
$ docker load -i nix-user.tar.gz
$ docker run -ti nix-user
```
