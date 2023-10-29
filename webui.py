import json
import flask
from testdb import db
from testdb.const import *

app = flask.Flask("jlutag")


def const2zh(s: str) -> str:
    return {
        ARTWORK: '作品',
        CHARACTER: '角色',
    }.get(s, s)


def lnk(j: dict) -> str:
    return '<a_href="/uid/%s">%s</a>' % (j[UID], j[ALIAS][0])


def htm(s: str) -> str:
    return s.replace('\n', '<br>').replace(' ', '&nbsp;&nbsp;').replace(
        '<a_href="',
        '<a href="'
    )


@app.route('/')
def root():
    return 'Hello world!'


@app.route('/api/search/<s>')
def api_search(s: str) -> str:
    ans = json.dumps(
        db.s_linked(s),
        skipkeys=True,
        ensure_ascii=False,
        indent=4,
    )
    return htm(ans)


@app.route('/search/<s>')
def search(s: str) -> str:
    j = db.s_linked(s)
    ans = '您可能在找:\n'
    for i in j:
        ans += const2zh(j[i][TYPE])
        ans += ' '
        ans += lnk(j[i])
        ans += ': '
        if len(j[i][ALIAS]) > 1:
            ans += '别名 '
            ans += ', '.join(j[i][ALIAS][1:])
        else:
            ans += '无别名'
        ans += ', '
        if j[i][TYPE] == CHARACTER:
            ans += '是作品 '
            ans += ', '.join([lnk(k) for k in j[i][LINK][ARTWORK]])
            ans += ' 中的角色, '
        ans += '{描述}'
        ans += '.\n'
    return htm(ans)


@app.route('/api/uid/<s>')
def api_uid(s: str) -> str:
    ans = json.dumps(
        db.get_linked(s),
        skipkeys=True,
        ensure_ascii=False,
        indent=4,
    )
    return htm(ans)


@app.route('/uid/<s>')
def uid(s: str) -> str:
    j = db.get_linked(s)
    ans = 'uuid '
    ans += s
    ans += ':\n'
    ans += '类型: '
    ans += const2zh(j[TYPE])
    ans += '\n'
    ans += '名称(别名): '
    ans += ', '.join(j[ALIAS])
    ans += '\n'
    ans += '相关链接:\n'
    for i in j[LINK]:
        ans += ' '
        ans += const2zh(i)
        ans += ': '
        ans += ', '.join([lnk(k) for k in j[LINK][i]])
        ans += '\n'
    return htm(ans)


# flask -A webui run --debug --port 23648
