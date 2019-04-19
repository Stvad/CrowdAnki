# CrowdAnki
[![Build Status](https://travis-ci.org/Stvad/CrowdAnki.svg?branch=master)](https://travis-ci.org/Stvad/CrowdAnki)

**CrowdAnki** 是 http://ankisrs.net/ 的一个插件，该插件使用户能以 JSON 格式导入导出牌组/笔记等所有相关信息。其主要目的是使众包(多人协作)制作 Anki 牌组和笔记更加简单。

从 0.6 版本开始，该插件还与 Git 集成，为用户提供自动保存牌组编辑历史记录的功能。 
详情请见 [以下][#快照]. 

AnkiWeb 上此插件的链接： https://ankiweb.net/shared/info/1788670778

---
**Please consider supporting the plugin development by becoming a Patron - this helps me to dedicate more time and love to the project**

[![Become a Patron!](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/bePatron?u=13102903)

---
## 如何通过 GitHub 进行协作
本节说明使用 GitHub 的协作工作流程。

假设你有一个名为牌组X的牌组，并且你想与其它人协作改进它。为了实现这一目标，你需要：

1. 导出牌组X。你可以在 Anki 上：文件>导出>导出格式：CrowdAnki JSON Representation (*directory)、包含：牌组X
2. 为你自己创建一个 GitHub 账号，并请你的协作者们也这么做 (参见：https://github.com/join)。
3. 根据这个[指南](https://guides.github.com/activities/hello-world/#repository)为你的牌组创建仓库。仓库的名称必须与牌组导出时创建的目录的名称相对应。在本案例下，仓库应该被命名为牌组X。(译者注：其实没必要两者名称相同，况且中文无法作为仓库名)
4. 为这个仓库添加协作者：https://help.github.com/articles/inviting-collaborators-to-a-personal-repository/。

### 图形界面工作流程
**前言**：

我的目标是提供一个便于用户理解的协作工作流程描述。为了做到这一点，我试了很多图形界面的 Git 客户端。为了我们的目的，我认为 **GitHub Desktop** 是最好的选择(作为对用户最为友好的客户端)。但是 GitHub Desktop 存在一个问题—— 它没有 Linux 版本。这令我特别难过，因为我主要使用 Linux 作为我的操作系统。我曾考虑过在本教程中使用 GitKraken ，但是它存在一些问题而不符合我们的目的。(但如果你是 Linux 用户或者由于某种原因你不喜欢 GitHub Desktop  —— 你仍可以考虑使用它)

#### 协作准备
1. 在电脑上安装 [GitHub Desktop](https://desktop.github.com/) 。
2. 登录之前你创建的 GitHub 账号。
3. 创建一个新仓库：File>Create a new repository. "Local path" 应该指向你导出牌组的地方，"repository name"应该与导出的文件夹名称相同。(译者注：考虑到中文不能作为仓库名，大家可以参考我的项目：[L-M-Sherlock/Ankigaokao-ScienceComprehensive-Biology-MoleculesAndCells](https://github.com/L-M-Sherlock/Ankigaokao-ScienceComprehensive-Biology-MoleculesAndCells)，先用 GitHub Desktop 在任意文件夹创建一个仓库，仓库名为英文，然后把导出的文件夹中的 media 文件夹和牌组X.json 文件移至该仓库，即与 .git 文件夹和 .gitattributes 文件同目录。)
  ![Image](misc/image/2.png?raw=true)
4. 将你的目录下的内容添加至仓库，通过选中所有文件，添加一些评论在评论区并点击 "Commit to **master**" 。
  ![Image](misc/image/4.png?raw=true)
5. 点击 "Publish repository" 将你刚才做的更改上传到 GitHub 。在本案例，你不需要提前在 GitHub 上创建仓库，GitHub Desktop 将帮你自动完成。(译者注： GitHub Desktop 更新后默认将仓库设为私有，需要在 Publish repository 界面将 Keep this code private 这个勾选去掉)
  ![Image](misc/image/6.png?raw=true)

#### 为了开始在此牌组工作，你的协作者需要：
1. 在他们的电脑安装 [GitHub Desktop](https://desktop.github.com/) 。
2. 克隆你已经创建的仓库。他们可以通过在 GitHub 仓库页面点击 "Clone or download -> Open in Desktop" 做到这一点。
	![Image](misc/image/7.png?raw=true)
3. [导入牌组](#导入).

如果有些人**只是想使用**你在 GitHub 上上传的**牌组**，他们可以[直接从仓库导入牌组]()。

#### 如何上传更改

当你或你的一个协作者想将你们做出的更改上传到 GitHub 时，你们需要：

1. 通过点击 "Fetch Origin" 从 GitHub 获取其他人的提交历史，如果有新的更改，则可以点击 "Pull Origin" 获取最新的更改。
  ![Image](misc/image/8.png?raw=true)
2. 为了合并你和其他人做出的更改，请[导入牌组](#导入)。
3. 导出牌组到你仓库的本地目录，然后导出将覆盖 media 文件夹和 json 文件。(替代选项是，你可以将牌组导出到其他地方，然后将 media 文件夹和 json 文件复制到仓库目录下，然后选择合并同名文件夹，替换已存在的文件。)
4. 在评论区添加 comment ，点击 "Commit to master" 上传你做出的更改。
  ![Image](misc/image/4.png?raw=true)
5. 点击 "Push Origin" 上传你做出的更改到 GitHub 。

如果你只想**获取别人做出的最新更改**，你只需要执行第一步和第二步。

### 命令行工作流程
#### 协作准备
4. 在你的电脑上安装 git 。
5. 到导出的目录。
6. 用下面的命令初始化仓库：
   
    ```
    git init
    git remote add origin git@github.com:<username>/<repository>.git
    ```

    <username> 是你的 GitHub 用户名 (我的是 Stvad) ， <repository> 是仓库的名字 (DeckX)。 所以本案例中的命令应该是：

    ```
    git remote add origin git@github.com:Stvad/DeckX.git
    ```
7. 添加目录下的所有内容到仓库：

    ```
    git add *
    git commit -m "initial export"
    ```
8. 上传你做出的更改到 GitHub：

    ```
    git push origin master
    ```

#### 为了开始在此牌组工作，你的协作者需要：

1. 在他们的电脑室安装 git
2. 克隆你创建好的仓库：

    ```
    git clone https://github.com/Stvad/DeckX.git
    ```

3. [导入牌组](#导入).

如果有些人**只是想使用**你在 GitHub 上上传的**牌组**，他们可以[直接从仓库导入牌组]()。

#### 如何上传更改

当你或你的一个协作者想将你们做出的更改上传到 GitHub 时，你们需要：

1. 从 GitHub 获取最新的更改：
   
    ```
    git pull
    ```
2. 为了合并你和其他人做出的更改，请[导入牌组](#导入)。
3. 导出牌组到你仓库的本地目录，然后导出将覆盖 media 文件夹和 json 文件。(替代选项是，你可以将牌组导出到其他地方，然后将 media 文件夹和 json 文件复制到仓库目录下，然后选择合并同名文件夹，替换已存在的文件。)
4. 将更改添加到仓库：

    ```
    git add *
    git commit -m "new updates"
    ```
5. 上传你做出的更改到 GitHub ：

    ```
    git push origin master
    ```

如果你只想**获取别人做出的最新更改**，你只需要执行第一步和第二步。


## 通用协作工作流程
目前的工作流程可以表述为：
* 用户创建或者导入一个 Anki 牌组。
* 用户做了一些更改(比如笔记内容、牌组设置、牌组结构或笔记模板)。
* 然后用户以 JSON 格式导出牌组(附带媒体文件夹和该牌组中引用的媒体文件)并分享给其他用户。例如通过为此创建 GitHub 仓库。
* 其他人可以直接修改 JSON 文件，也可以导入牌组到他们自己的 Anki 中并做一些修改。
* 然后这些人做出的更改就会更新最初的 JSON 文件(必要时将几个更改合并在一起)。
* 之后，最初的用户（和其他人）可以导入更新的牌组，将这些新的更改整合到他们的集合中。

## 导出
导出请到菜单：文件>导出

选择牌组(**注**：不支持导出所有的牌组，你需要选择一个特定的牌组)并将导出格式改为 "CrowdAnki JSON representation (*directory )" 。
点击导出之后，选择一个保存导出的目录。

## 导入
导入请到菜单：文件>"CrowdAnki: Import from disk" 并选择牌组储存的目录。 

## 从 GitHub 导入
从 GitHub 导入牌组请到菜单：文件>"CrowdAnki: Import from GitHub" 并以建议的格式输入 GitHub 用户名和仓库名。

以我的仓库为例，为了获取我的[Ankigaokao-理科-理综-生物-分子与细胞](https://github.com/L-M-Sherlock/Ankigaokao-ScienceComprehensive-Biology-MoleculesAndCells)，你需要输入

L-M-Sherlock/Ankigaokao-ScienceComprehensive-Biology-MoleculesAndCells

### 导入时需要注意：
* 自动备份将在导入前触发；
* 如果卡片的笔记模板改变，或者笔记模板本身以难以自动更新的方式改变：系统会弹出一个窗口，要求你解决新旧模板的冲突；
* 如果笔记被移动到另一个 JSON 文件中的牌组，则在导入时，该笔记的所有卡片（筛选牌组中的卡片除外）将被移动到指定的卡片组。

## 快照

**CrowdAnki** 能帮助你保存 **你牌组的编辑历史**。
该插件将牌组导出到一个特定位置并在每一次你创建快照时创建一个 git commit 。

你可以在菜单手动创建快照：文件>CrowdAnki: Snapshot 。
或者你可以在插件配置页开启自动快照，详情请见[这里](crowd_anki/config.md) 。

其他你可以[配置](crowd_anki/config.md)的参数是快照的储存地址和快照包括的牌组。