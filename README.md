## 개발 시작하기
*기본적으로, 패키지 관리로 APT를 사용하는 리눅스 배포판 기준으로 설명하고 있습니다.
(추후 설명 보완예정)*

###Python 3.4 이상, Git
```console
$ sudo apt-get install python3 git
```
로 쉽게 설치할 수 있습니다.

대부분의 리눅스 배포판에 파이썬이 설치되어 있지만,
파이썬 버전을 업그레이드 하고 싶다면,
[여기](https://www.python.org/downloads/)서 최신 버전의 파이썬을 다운로드 하십시오.
압축을 풀고 해당 폴더 내에서,
```console
$ ./configure
$ make
$ make test
$ sudo apt-get build-dep python3.4
$ sudo make altinstall
```
명령을 수행하면 됩니다.

###Node.js
npm을 사용하기 위해 Node.js가 필요합니다.

```console
$ curl -sL https://deb.nodesource.com/setup | sudo bash -
$ sudo apt-get install nodejs
$ sudo apt-get install build-essential
```

###Less
사용하는 테마의 CSS 파일들은 [Less](http://en.wikipedia.org/wiki/Less_%28stylesheet_language%29)로
컴파일하여 만들어졌습니다. `.less` 파일을 수정하기 위한 [도구](http://lesscss.org/)가 필요합니다.

```console
$ sudo npm install -g less
```

## 소스 코드 받기
```console
$ git clone git@github.com:alps-jbnu/alps.git
$ cd alps/
```

개발에 참여하길 원한다면, 위와 같은 방법으로 소스 코드를 받길 권장하지 않습니다.
대신 GitHub 계정을 생성한 후, [저장소](https://github.com/alps-jbnu/alps)를
포크하세요. 그리고, 자신의 저장소를 `git clone` 하길 바랍니다.

예)
```console
$ git clone git@github.com:your-github-username-here/alps.git
$ cd alps/
$ git remote add upstream 
```
이후엔 자신의 저장소(origin)에 push하고, pull request를 요청하면 됩니다.
또한, 최신 변경사항을 master 브랜치에 받아오려면, `$ git pull upstream master`를
수행하세요.

## 파이썬 가상환경 만들기
각각의 파이썬 프로젝트마다 virtualenv 또는 pyvenv를 사용하세요. 시스템 site-packages를
공유하지 않고, 프로젝트 별로 필요한 외부 패키지들을 분리할 수 있습니다.

alps-env 디렉토리에 가상환경을 처음 만들 경우,
```console
$ pyvenv alps-env
```

가상환경에 들어가려면,
```console
$ source alps-env/bin/activate
```

가상환경에서 나오려면,
```console
(alps-env) $ deactivate
```

## 필요한 외부 패키지 설치
```console
$ pip install -e .[docs,tests]
```
가상환경에서 수행하는 것을 잊지 마세요.

## pre-commit hook
커밋 전, [PEP8](https://www.python.org/dev/peps/pep-0008/) 확인을 위한 커밋 훅을 설정합니다.
PEP8에 명시된, 파이썬 코드 스타일을 따르도록 합니다.

```console
$ cp hooks/pre-commit .git/hooks/
$ pip install flake8
```

## 설정 파일 만들기
서버를 돌리려면, 설정 파일이 필요합니다. 설정 파일은 YAML 포맷으로 작성됩니다.
예제 파일로 프로젝트 내 `example.cfg.yml` 파일을 참조하세요.

## 데이터베이스 생성 및 연동하기

## 데이터베이스 마이그레이션

## 데이터베이스 마이그레이션 스크립트 작성하기

## 테마 수정하기
`alps/static/theme/Documentation`을 참조하세요.

### CSS
`.less` 파일을 수정하고 변경사항을 반영하기 위해서는 Less 전처리기를 사용해야 합니다.
Template 폴더 내에 위치하고 있다면, 다음과 같은 명령을 실행하세요.
```console
$ lessc _less/main.less > assets/css/main.css
```

## 서버 돌리기
개발 시 테스트나 디버깅 목적으로 Flask built-in 서버를 이용할 수 있습니다.
```console
$ alps runserver
```
