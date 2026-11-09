# 机密信息（Secrets）

store 对系统上的所有用户可读。因此，通常不建议让机密信息进入 store。

即使在单用户系统上，各系统用户之间也会相互隔离服务；而让所有本地用户都能读取的机密信息会削弱这种隔离。在使用外部 store 缓存时，机密信息可能最终会进入其中；而在多用户系统上，机密信息将对所有这些用户可用。

应当这样组织你的 derivation：在运行时从文件系统（配合适当的访问控制）读取机密信息。可以手动将机密信息放置在文件系统上，也可以采用这样一种方案：以加密形式将机密信息纳入 store，并在系统激活时对其进行解密并附加相应的访问控制。
NixOS 上有多种此类方案，参见 wiki 上的[机密管理方案对比]。

[comparison of secret managing schemes]: https://wiki.nixos.org/wiki/Comparison_of_secret_managing_schemes
