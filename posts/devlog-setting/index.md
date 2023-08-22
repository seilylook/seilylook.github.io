# Hugo 개발 블로그 개설


`Hogo`: The worlds's fastest framework for building static website.

# Hugo

> https://gohugo.io/

## hugo 설치

```shell
# Install brew
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# download hugo
brew install hugo

```

## 프로젝트 생성

```shell
# 프로젝트 생성 디렉터리 접근
cd development

hugo new site <원하는 파일 이름>

# 나의 경우
hugo new site devlog
```

{{<admonition note 주의>}}
hugo version upgrade인지 대부분의 사이트에서 말하는 것과 다르게 사이트를 hugo new site를 통해 프로젝트를 생성하면 config.toml이 생성되는 것이 아니라 hugo.toml이 생성된다. 두개 다 같으니 걱정할 필요 없다.
{{</admonition>}}

## Repository 생성

두개의 repo를 생성해야 한다.

1. hugo 사용해 블로그 안의 내용과 소스 코드를 저장하기 위한 repo
2. gibhub page를 사용해 호스팅 해줄 repo

## 테마 적용

```shell
# 생성한 프로젝트로 이동
cd devlog

# 원하는 테마 적용
git submodule add <SOME THEME>

git submodule add https://github.com/dillonzq/LoveIt themes/loveit

```

### submodule 로 가져온 theme의 config.toml을 참고해서 hugo.toml을 수정

{{<admonition note hugo.toml 수정>}}

```
baseURL = "https://seilylook.github.io/"
defaultContentLanguage = "en"
# Change the default theme to be use when building the site with Hugo
theme = "LoveIt"

# website title
title = "Devlog"
# whether to use robots.txt
enableRobotsTXT = true
# whether to use git commit log
enableGitInfo = true
# whether to use emoji code
enableEmoji = true
canonifyURLs = false

# language code ["en", "zh-CN", "fr", "pl", ...]
languageCode = "en"
# language name ["English", "简体中文", "Français", "Polski", ...]
languageName = "English"

# Author config
[author]
  name = "seilylook"
  email = "seilylook@naver.com"
  link = "https://github.com/seilylook"

[params]
  # site default theme ["auto", "light", "dark"]
  defaultTheme = "light"
  # public git repo url only then enableGitInfo is true
  gitRepo = "https://github.com/seilylook"
  # which hash function used for SRI, when empty, no SRI is used
  # ["sha256", "sha384", "sha512", "md5"]
  fingerprint = ""
  # date format
  dateFormat = "2006-01-02"
  # website title for Open Graph and Twitter Cards
  title = "My cool site"
  # website description for RSS, SEO, Open Graph and Twitter Cards
  description = "This is my cool site"
  # website images for Open Graph and Twitter Cards
  images = ["/images/profile.png"]

  # Header config
  [params.header]
    # desktop header mode ["fixed", "normal", "auto"]
    desktopMode = "auto"
    # mobile header mode ["fixed", "normal", "auto"]
    mobileMode = "auto"
    # Header title config
    [params.header.title]
      # URL of the LOGO
      # LOGO 的 URL
      logo = ""
      name = "<span style='color: #FF0000;'>Devlog</span>"
      # you can add extra information before the name (HTML format is supported), such as icons
      pre = ""
      # you can add extra information after the name (HTML format is supported), such as icons
      post = ""
      # whether to use typeit animation for title name
      typeit = true

  # Footer config
  # 页面底部信息配置
  [params.footer]
    enable = true
    # Custom content (HTML format is supported)
    custom = ""
    # whether to show Hugo and theme info
    hugo = true
    # whether to show copyright info
    copyright = true
    # whether to show the author
    author = true
    # site creation time
    since = 2022
    # ICP info only in China (HTML format is supported)
    icp = ""
    # license info (HTML format is supported)
    license= ""

  # Section (all posts) page config
  # Section (所有文章) 页面配置
  [params.section]
    # special amount of posts in each section page
    paginate = 100
    # date format (month and day)
    # 日期格式 (月和日)
    dateFormat = "01-02"
    # amount of RSS pages
    # RSS 文章数目
    rss = 10

  # List (category or tag) page config
  # List (目录或标签) 页面配置
  [params.list]
    # special amount of posts in each list page
    # list 页面每页显示文章数量
    paginate = 20
    # date format (month and day)
    # 日期格式 (月和日)
    dateFormat = "01-02"
    # amount of RSS pages
    # RSS 文章数目
    rss = 10

  # App icon config
  # 应用图标配置
  [params.app]
    # optional site title override for the app when added to an iOS home screen or Android launcher
    title = "seilylook"
    # whether to omit favicon resource links
    noFavicon = false
    # modern SVG favicon to use in place of older style .png and .ico files
    svgFavicon = "/favicon/favicon.ico"
    # Android browser theme color
    themeColor = "#ffffff"
    # Safari mask icon color
    # Safari 图标颜色
    iconColor = "#5bbad5"
    # Windows v8-11 tile color
    # Windows v8-11 磁贴颜色
    tileColor = "#da532c"

  # Search config
  # 搜索配置
  [params.search]
    enable = false
    # type of search engine ["lunr", "algolia"]
    # 搜索引擎的类型 ["lunr", "algolia"]
    type = "lunr"
    # max index length of the chunked content
    # 文章内容最长索引长度
    contentLength = 4000
    # placeholder of the search bar
    # 搜索框的占位提示语
    placeholder = ""
    # max number of results length
    # 最大结果数目
    maxResultLength = 10
    # snippet length of the result
    # 结果内容片段长度
    snippetLength = 30
    # HTML tag name of the highlight part in results
    # 搜索结果中高亮部分的 HTML 标签
    highlightTag = "em"
    # whether to use the absolute URL based on the baseURL in search index
    # 是否在搜索索引中使用基于 baseURL 的绝对路径
    absoluteURL = false
    [params.search.algolia]
      index = ""
      appID = ""
      searchKey = ""

  # Home page config
  # 主页信息设置
  [params.home]
    # amount of RSS pages
    rss = 10
    # Home page profile
    # 主页个人信息
    [params.home.profile]
      enable = true
      # Gravatar Email for preferred avatar in home page
      gravatarEmail = ""
      # URL of avatar shown in home page
      avatarURL = "/images/profile.png"
      # title shown in home page (HTML format is supported)
      title = "Se Hyeon Kim"
      # subtitle shown in home page (HTML format is supported)
      subtitle = "seilylook's Devlog"
      # whether to use typeit animation for subtitle
      typeit = true
      # whether to show social links
      social = true
      # disclaimer (HTML format is supported)
      disclaimer = ""
    # Home page posts
    [params.home.posts]
      enable = true
      # special amount of posts in each home posts page
      paginate = 6
  # Social config in home page
  # 主页的社交信息设置
  [params.social]
    GitHub = "seilylook"
    Linkedin = ""
    Twitter = ""
    Instagram = "seilylook"
    Facebook = ""
    Telegram = ""
    Medium = ""
    Gitlab = ""
    Youtubelegacy = ""
    Youtubecustom = ""
    Youtubechannel = ""
    Tumblr = ""
    Quora = ""
    Keybase = ""
    Pinterest = ""
    Reddit = ""
    Codepen = ""
    FreeCodeCamp = ""
    Bitbucket = ""
    Stackoverflow = ""
    Weibo = ""
    Odnoklassniki = ""
    VK = ""
    Flickr = ""
    Xing = ""
    Snapchat = ""
    Soundcloud = ""
    Spotify = ""
    Bandcamp = ""
    Paypal = ""
    Fivehundredpx = ""
    Mix = ""
    Goodreads = ""
    Lastfm = ""
    Foursquare = ""
    Hackernews = ""
    Kickstarter = ""
    Patreon = ""
    Steam = ""
    Twitch = ""
    Strava = ""
    Skype = ""
    Whatsapp = ""
    Zhihu = ""
    Douban = ""
    Angellist = ""
    Slidershare = ""
    Jsfiddle = ""
    Deviantart = ""
    Behance = ""
    Dribbble = ""
    Wordpress = ""
    Vine = ""
    Googlescholar = ""
    Researchgate = ""
    Mastodon = ""
    Thingiverse = ""
    Devto = ""
    Gitea = ""
    XMPP = ""
    Matrix = ""
    Bilibili = ""
    Discord = ""
    DiscordInvite = ""
    Lichess = ""
    ORCID = ""
    Pleroma = ""
    Kaggle = ""
    MediaWiki= ""
    Plume = ""
    HackTheBox = ""
    RootMe= ""
    Email = "seilylook@naver.com"
    Phone = ""
    RSS = "true"

  # Page global config
  # 文章页面全局配置
  [params.page]
    # whether to hide a page from home page
    hiddenFromHomePage = false
    # whether to hide a page from search results
    hiddenFromSearch = false
    # whether to enable twemoji
    twemoji = false
    # whether to enable lightgallery
    lightgallery = true
    # whether to enable the ruby extended syntax
    # 是否使用 ruby 扩展语法
    ruby = true
    # whether to enable the fraction extended syntax
    fraction = true
    # whether to enable the fontawesome extended syntax
    fontawesome = true
    # whether to show link to Raw Markdown content of the content
    linkToMarkdown = true
    # whether to show the full text content in RSS
    rssFullText = false
    # Table of the contents config
    [params.page.toc]
      # whether to enable the table of the contents
      # 是否使用目录
      enable = true
      # whether to keep the static table of the contents in front of the post
      # 是否保持使用文章前面的静态目录
      keepStatic = false
      # whether to make the table of the contents in the sidebar automatically collapsed
      # 是否使侧边目录自动折叠展开
      auto = true
    # Code config
    # 代码配置
    [params.page.code]
      # whether to show the copy button of the code block
      # 是否显示代码块的复制按钮
      copy = true
      # the maximum number of lines of displayed code by default
      # 默认展开显示的代码行数
      maxShownLines = 50
    # KaTeX mathematical formulas config (KaTeX https://katex.org/)
    # KaTeX 数学公式配置 (KaTeX https://katex.org/)
    [params.page.math]
      enable = false
      # default inline delimiter is $ ... $ and \( ... \)
      # 默认行内定界符是 $ ... $ 和 \( ... \)
      inlineLeftDelimiter = ""
      inlineRightDelimiter = ""
      # default block delimiter is $$ ... $$, \[ ... \], \begin{equation} ... \end{equation} and some other functions
      # 默认块定界符是 $$ ... $$, \[ ... \],  \begin{equation} ... \end{equation} 和一些其它的函数
      blockLeftDelimiter = ""
      blockRightDelimiter = ""
      # KaTeX extension copy_tex
      # KaTeX 插件 copy_tex
      copyTex = true
      # KaTeX extension mhchem
      # KaTeX 插件 mhchem
      mhchem = true
    # Mapbox GL JS config (Mapbox GL JS https://docs.mapbox.com/mapbox-gl-js)
    # Mapbox GL JS 配置 (Mapbox GL JS https://docs.mapbox.com/mapbox-gl-js)
    [params.page.mapbox]
      # access token of Mapbox GL JS
      # Mapbox GL JS 的 access token
      accessToken = ""
      # style for the light theme
      # 浅色主题的地图样式
      lightStyle = "mapbox://styles/mapbox/light-v10?optimize=true"
      # style for the dark theme
      # 深色主题的地图样式
      darkStyle = "mapbox://styles/mapbox/dark-v10?optimize=true"
      # whether to add NavigationControl (https://docs.mapbox.com/mapbox-gl-js/api/#navigationcontrol)
      # 是否添加 NavigationControl (https://docs.mapbox.com/mapbox-gl-js/api/#navigationcontrol)
      navigation = true
      # whether to add GeolocateControl (https://docs.mapbox.com/mapbox-gl-js/api/#geolocatecontrol)
      # 是否添加 GeolocateControl (https://docs.mapbox.com/mapbox-gl-js/api/#geolocatecontrol)
      geolocate = true
      # whether to add ScaleControl (https://docs.mapbox.com/mapbox-gl-js/api/#scalecontrol)
      # 是否添加 ScaleControl (https://docs.mapbox.com/mapbox-gl-js/api/#scalecontrol)
      scale = true
      # whether to add FullscreenControl (https://docs.mapbox.com/mapbox-gl-js/api/#fullscreencontrol)
      # 是否添加 FullscreenControl (https://docs.mapbox.com/mapbox-gl-js/api/#fullscreencontrol)
      fullscreen = true
    # Social share links in post page
    [params.page.share]
      enable = true
      Twitter = true
      Facebook = true
      Linkedin = false
      Whatsapp = false
      Pinterest = false
      Tumblr = false
      HackerNews = true
      Reddit = false
      VK = false
      Buffer = false
      Xing = false
      Line = true
      Instapaper = false
      Pocket = false
      Flipboard = false
      Weibo = true
      Blogger = false
      Baidu = false
      Odnoklassniki = false
      Evernote = false
      Skype = false
      Trello = false
      Mix = false
    # Comment config
    [params.page.comment]
      enable = true
      [params.page.comment.disqus]
        enable = true
        # Disqus shortname to use Disqus in posts
        # Disqus 的 shortname，用来在文章中启用 Disqus 评论系统
        shortname = ""
      # Gitalk comment config (https://github.com/gitalk/gitalk)
      # Gitalk 评论系统设置 (https://github.com/gitalk/gitalk)
      [params.page.comment.gitalk]
        enable = false
        owner = ""
        repo = ""
        clientId = ""
        clientSecret = ""
      # Valine comment config (https://github.com/xCss/Valine)
      # Valine 评论系统设置 (https://github.com/xCss/Valine)
      [params.page.comment.valine]
        enable = false
        appId = ""
        appKey = ""
        placeholder = ""
        avatar = "mp"
        meta= ""
        pageSize = 10
        # automatically adapt the current theme i18n configuration when empty
        # 为空时自动适配当前主题 i18n 配置
        lang = ""
        visitor = true
        recordIP = true
        highlight = true
        enableQQ = false
        serverURLs = ""
        # emoji data file name, default is "google.yml"
        # ["apple.yml", "google.yml", "facebook.yml", "twitter.yml"]
        # located in "themes/LoveIt/assets/lib/valine/emoji/" directory
        # you can store your own data files in the same path under your project:
        # "assets/lib/valine/emoji/"
        # emoji 数据文件名称, 默认是 "google.yml"
        # ["apple.yml", "google.yml", "facebook.yml", "twitter.yml"]
        # 位于 "themes/LoveIt/assets/lib/valine/emoji/" 目录
        # 可以在你的项目下相同路径存放你自己的数据文件:
        # "assets/lib/valine/emoji/"
        emoji = ""
      # Facebook comment config (https://developers.facebook.com/docs/plugins/comments)
      # Facebook 评论系统设置 (https://developers.facebook.com/docs/plugins/comments)
      [params.page.comment.facebook]
        enable = false
        width = "100%"
        numPosts = 10
        appId = ""
        # automatically adapt the current theme i18n configuration when empty
        # 为空时自动适配当前主题 i18n 配置
        languageCode = ""
      # Telegram comments config (https://comments.app/)
      # Telegram comments 评论系统设置 (https://comments.app/)
      [params.page.comment.telegram]
        enable = false
        siteID = ""
        limit = 5
        height = ""
        color = ""
        colorful = true
        dislikes = false
        outlined = false
      # Commento comment config (https://commento.io/)
      # Commento comment 评论系统设置 (https://commento.io/)
      [params.page.comment.commento]
        enable = false
      # utterances comment config (https://utteranc.es/)
      # utterances comment 评论系统设置 (https://utteranc.es/)
      [params.page.comment.utterances]
        enable = true
        # owner/repo
        repo = "seilylook/seilylook.github.io"
        issueTerm = "pathname"
        label = "💡"
        lightTheme = "github-light"
        darkTheme = "github-dark"
      # giscus comment config (https://giscus.app/)
      # giscus comment 评论系统设置 (https://giscus.app/zh-CN)
      [params.page.comment.giscus]
        # You can refer to the official documentation of giscus to use the following configuration.
        # 你可以参考官方文档来使用下列配置
        enable = false
        repo = ""
        repoId = ""
        category = "Announcements"
        categoryId = ""
        # automatically adapt the current theme i18n configuration when empty
        # 为空时自动适配当前主题 i18n 配置
        lang = ""
        mapping = "pathname"
        reactionsEnabled = "1"
        emitMetadata = "0"
        inputPosition = "bottom"
        lazyLoading = false
        lightTheme = "light"
        darkTheme = "dark"
    # Third-party library config
    [params.page.library]
      [params.page.library.css]
        # someCSS = "some.css"
        # located in "assets/" 位于 "assets/"
        # Or 或者
        # someCSS = "https://cdn.example.com/some.css"
      [params.page.library.js]
        # someJavascript = "some.js"
        # located in "assets/" 位于 "assets/"
        # Or 或者
        # someJavascript = "https://cdn.example.com/some.js"
    # Page SEO config
    # 页面 SEO 配置
    [params.page.seo]
      # image URL
      images = ["/images/profile.png"]
      # Publisher info
      [params.page.seo.publisher]
        name = "seilylook"
        logoUrl = "/images/profile.png"

  # TypeIt config
  # TypeIt 配置
  [params.typeit]
    # typing speed between each step (measured in milliseconds)
    # 每一步的打字速度 (单位是毫秒)
    speed = 100
    # blinking speed of the cursor (measured in milliseconds)
    # 光标的闪烁速度 (单位是毫秒)
    cursorSpeed = 1000
    # character used for the cursor (HTML format is supported)
    # 光标的字符 (支持 HTML 格式)
    cursorChar = "|"
    # cursor duration after typing finishing (measured in milliseconds, "-1" means unlimited)
    # 打字结束之后光标的持续时间 (单位是毫秒, "-1" 代表无限大)
    duration = -1

  # Site verification code for Google/Bing/Yandex/Pinterest/Baidu
  # 网站验证代码，用于 Google/Bing/Yandex/Pinterest/Baidu
  [params.verification]
    google = ""
    bing = ""
    yandex = ""
    pinterest = ""
    baidu = ""

  # Site SEO config
  [params.seo]
    # image URL
    # 图片 URL
    image = "/images/profile.png"
    # thumbnail URL
    # 缩略图 URL
    thumbnailUrl = "/images/profile.png"

  # Analytics config
  [params.analytics]
    enable = true
    # Google Analytics
    [params.analytics.google]
      id = ""
      # whether to anonymize IP
      # 是否匿名化用户 IP
      anonymizeIP = true
    # Fathom Analytics
    [params.analytics.fathom]
      id = ""
      # server url for your tracker if you're self hosting
      # 自行托管追踪器时的主机路径
      server = ""
    # Plausible Analytics
    [params.analytics.plausible]
      dataDomain = ""
    # Yandex Metrica
    [params.analytics.yandexMetrica]
      id = ""

  # Cookie consent config
  # Cookie 许可配置
  [params.cookieconsent]
    enable = false
    # text strings used for Cookie consent banner
    # 用于 Cookie 许可横幅的文本字符串
    [params.cookieconsent.content]
      message = ""
      dismiss = ""
      link = ""

  # CDN config for third-party library files
  # 第三方库文件的 CDN 设置
  [params.cdn]
    # CDN data file name, disabled by default
    # ["jsdelivr.yml"]
    # located in "themes/LoveIt/assets/data/cdn/" directory
    # you can store your own data files in the same path under your project:
    # "assets/data/cdn/"
    # CDN 数据文件名称, 默认不启用
    # ["jsdelivr.yml"]
    # 位于 "themes/LoveIt/assets/data/cdn/" 目录
    # 可以在你的项目下相同路径存放你自己的数据文件:
    # "assets/data/cdn/"
    data = "jsdelivr.yml"

  # Compatibility config
  [params.compatibility]
    # whether to use Polyfill.io to be compatible with older browsers
    # 是否使用 Polyfill.io 来兼容旧式浏览器
    polyfill = false
    # whether to use object-fit-images to be compatible with older browsers
    # 是否使用 object-fit-images 来兼容旧式浏览器
    objectFit = false


# Menu config
[menu]
  [[menu.main]]
    weight = 1
    identifier = "posts"
    # you can add extra information before the name (HTML format is supported), such as icons
    pre = ""
    # you can add extra information after the name (HTML format is supported), such as icons
    post = ""
    name = "Posts"
    url = "/posts/"
    # title will be shown when you hover on this menu link
    title = ""
  [[menu.main]]
    weight = 2
    identifier = "tags"
    pre = ""
    post = ""
    name = "Tags"
    url = "/tags/"
    title = ""
  [[menu.main]]
    weight = 3
    identifier = "categories"
    pre = ""
    post = ""
    name = "Categories"
    url = "/categories/"
    title = ""

[markup]
  # Syntax Highlighting (https://gohugo.io/content-management/syntax-highlighting)
  [markup.highlight]
    codeFences = true
    guessSyntax = true
    lineNos = true
    lineNumbersInTable = true
    # false is a necessary configuration (https://github.com/dillonzq/LoveIt/issues/158)
    noClasses = false
  # Goldmark is from Hugo 0.60 the default library used for Markdown
  [markup.goldmark]
    [markup.goldmark.extensions]
      definitionList = true
      footnote = true
      linkify = true
      strikethrough = true
      table = true
      taskList = true
      typographer = true
    [markup.goldmark.renderer]
      # whether to use HTML tags directly in the document
      unsafe = true
  # Table Of Contents settings
  [markup.tableOfContents]
    startLevel = 2
    endLevel = 6

# Options to make output .md files
[mediaTypes]
  [mediaTypes."text/plain"]
    suffixes = ["md"]

# Options to make output .md files
[outputFormats.MarkDown]
  mediaType = "text/plain"
  isPlainText = true
  isHTML = false

# Options to make hugo output files
[outputs]
  home = ["HTML", "RSS", "JSON"]
  page = ["HTML", "MarkDown"]
  section = ["HTML", "RSS"]
  taxonomy = ["HTML", "RSS"]
  taxonomyTerm = ["HTML"]

[languages]
  [languages.en]
    languageName = "English"
    weight = 1
    languageCode = "en"
  [languages.ko]
    languageName = "Korean"
    weight = 2
    languageCode = "ko"

```

{{</admonition>}}

## 게시물 작성

```shell
hugo new posts/first-post/index.en.md

```

자동으로 이런 frontmatter가 생성된다.

```
---
title: "Hugo 개발 블로그 개설"
date: 2023-08-22T17:04:46+09:00
---
```

## git push

1. hugo 소스 코드 올리기

```shell
git init
git add .
git commit -m "init commit"
git branch -M main
git remote add origin <본인이 만든 repo 주소>

# 나의 경우
git remote add origin https://github.com/seilylook/devlog.git

```

2. github.io에 올리기

```shell
git submodule add <git 아이디.github.io 주소>

# 나의 경우
git submodule add https://github.com/seilylook/seilylook.github.io.git public
```

## 테스트 해보기

```shell
hugo server -D
```

내가 적용한 테마와 포스트를 확인할 수 있다.

### public에 데이터 올리기

```shell
hugo -t <테마이름>

# 나의 경우
hugo -t LogeIt
```

## 결과물 업로드

- [x] username.github.io에 업로드

```shell
cd public
git add .
git commit -m "init commit"
git push -u origin main
```

- [x] 프로젝트에 업로드

```shell
cd ..
git add .
git commit -m "init commit"
git push -u origin main
```

## shell script를 사용해 자동 업로드

프로젝트 루트 디렉터리에 .sh 파일을 생성한다.

나의 경우 deploy.sh

```shell
#!/bin/sh

# If a command fails then the deploy stops
set -e
printf "\033[0;32m I Love seilylook \033[0m\n"
printf "\033[0;32mDeploying updates to GitHub...\033[0m\n"

printf "\033[0;32mBuild the project.\033[0m\n"
hugo -D
# hugo -t timeline # if using a theme, replace with `hugo -t <YOURTHEME>`


printf "\033[0;32m  Go To Public folder \033[0m\n"
cd public


printf "\033[0;32m  Setting for submodule commit \033[0m\n"
git config --local user.name "seilylook"
git config --local user.email "seilylook@naver.com"
git submodule update --init --recursive


printf "\033[0;32m  Add changes to git. \033[0m\n"
git add .

printf "\033[0;32m  Commit changes.. \033[0m\n"
msg="rebuilding site $(date)"
if [ -n "$*" ]; then
	msg="$*"
fi
git commit -m "$msg"

printf "\033[0;32m  Push blog(presentation) source and build repos. \033[0m\n"
git push origin main


printf "\033[0;32m  Come Back up to the Project Root \033[0m\n"
cd ..
echo $pwd

printf "\033[0;32m  root repository Commit & Push. \033[0m\n"
git add .

msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi

git commit -m "$msg"

git push origin main

```

다음부터는 명령어를 통해 배포할 수 있다.

```shell
$ sh git-push.sh <COMMIT_MSG>

```

