let
  inherit (builtins)
    attrNames
    listToAttrs
    concatStringsSep
    readFile
    replaceStrings
    ;
  showSettings = import <nix/generate-settings.nix>;
  showStoreDocs = import <nix/generate-store-info.nix>;

  # 简体中文翻译仓库：为侧边栏与索引中的 store 类型名称提供中文映射。
  # 未在映射表中的类型名保持英文原文（or 兜底）。
  nameMap = {
    "Dummy Store" = "虚拟 Store（Dummy）";
    "Experimental Local Overlay Store" = "实验性本地 Overlay Store";
    "Experimental SSH Store" = "实验性 SSH Store";
    "Experimental SSH Store with filesystem mounted" = "实验性 SSH Store（挂载文件系统）";
    "HTTP Binary Cache Store" = "HTTP 二进制缓存 Store";
    "Local Binary Cache Store" = "本地二进制缓存 Store";
    "Local Daemon Store" = "本地守护进程 Store";
    "Local Store" = "本地 Store";
    "S3 Binary Cache Store" = "S3 二进制缓存 Store";
  };

  showName = store: nameMap.${store.name} or store.name;
in

storeInfo:

let
  storesList = showStoreDocs {
    inherit storeInfo;
    inlineHTML = true;
  };

  index =
    let
      showEntry = store: "- [${showName store}](./${store.filename})";
    in
    concatStringsSep "\n" (map showEntry storesList);

  "index.md" = replaceStrings [ "@store-types@" ] [ index ] (
    readFile ./source/store/types/index.md.in
  );

  tableOfContents =
    let
      showEntry = store: "    - [${showName store}](store/types/${store.filename})";
    in
    concatStringsSep "\n" (map showEntry storesList) + "\n";

  "SUMMARY.md" = tableOfContents;

  storePages = listToAttrs (
    map (s: {
      name = s.filename;
      value = s.page;
    }) storesList
  );

in
storePages // { inherit "index.md" "SUMMARY.md"; }
