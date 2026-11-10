R"(

**Store URL 格式**: `s3://`*bucket-name*

此 Store 允许读取和写入存储在 AWS S3（或 S3 兼容服务）存储桶中的[二进制缓存](@docroot@/protocols/binary-cache/index.md)。
此 Store 与 [HTTP 二进制缓存 Store](@docroot@/store/types/http-binary-cache-store.md) 共享许多惯用法。

对于 AWS S3，名为 `example-nix-cache` 的存储桶对应的二进制缓存 URL 就是 <s3://example-nix-cache>。
对于 S3 兼容的二进制缓存，请查阅该缓存的文档。

### 对 S3 兼容二进制缓存的匿名读取

> 如果你的二进制缓存是公开可访问的且不需要身份验证，最简单的做法是使用 [HTTP 二进制缓存 Store] 而不是 S3 二进制缓存 Store，
> 即使用 <https://example-nix-cache.s3.amazonaws.com> 而不是 <s3://example-nix-cache>。

要让存储桶可被访问，它需要类似下面这样的
[存储桶策略](https://docs.aws.amazon.com/AmazonS3/v1/userguide/bucket-policies.html)：

```json
{
    "Id": "DirectReads",
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowDirectReads",
            "Action": [
                "s3:GetObject",
                "s3:GetBucketLocation",
                "s3:ListBucket"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::example-nix-cache",
                "arn:aws:s3:::example-nix-cache/*"
            ],
            "Principal": "*"
        }
    ]
}
```

### 身份验证

Nix 将使用
[默认凭据提供程序链](https://docs.aws.amazon.com/sdk-for-cpp/v1/developer-guide/credentials.html)
对发往 Amazon S3 的请求进行身份验证。

请注意，这意味着 Nix 在读取环境变量和文件时采用的方式与 Nix 自身的设置不同，这些惯用法由 AWS SDK 实现。
更多细节请查阅上面链接的文档。

### 对 S3 二进制缓存的经身份验证读取

存储桶需要一条允许目标用户对存储桶中所有对象执行 `s3:GetObject`、`s3:GetBucketLocation` 和 `s3:ListBucket` 操作的存储桶策略。
可以将[上面给出的匿名策略](#anonymous-reads-to-your-s3-compatible-binary-cache)修改为受限的 `Principal` 来实现这一点。

### 对 S3 兼容二进制缓存的经身份验证写入

你的账户需要一条 IAM 策略以支持向存储桶上传：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "UploadToCache",
      "Effect": "Allow",
      "Action": [
        "s3:AbortMultipartUpload",
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads",
        "s3:ListMultipartUploadParts",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::example-nix-cache",
        "arn:aws:s3:::example-nix-cache/*"
      ]
    }
  ]
}
```

### 示例

按照上文所述配置好存储桶策略和身份验证后，即可通过 [`nix copy`](@docroot@/command-ref/new-cli/nix3-copy.md)（实验性）进行上传。

- 使用特定的 Amazon S3 凭据配置上传：

  ```console
  $ nix copy nixpkgs.hello \
    --to 's3://example-nix-cache?profile=cache-upload&region=eu-west-2'
  ```

- 上传到 S3 兼容的二进制缓存：

  ```console
  $ nix copy nixpkgs.hello --to \
    's3://example-nix-cache?profile=cache-upload&endpoint=https://minio.example.com'
  ```

)"
