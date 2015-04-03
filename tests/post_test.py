from flask import url_for

from alps.post import Board, Post


def test_posts_are_created(fx_session, fx_posts):
    assert fx_session.query(Post).count() > 0
    hello_post = fx_session.query(Post) \
                           .filter_by(title='이 곳은 임원게시판입니다.') \
                           .first()
    assert hello_post == fx_posts.executive_post_1


def test_boards_are_created(fx_session, fx_boards):
    assert fx_session.query(Board).count() > 0
    member_board = fx_session.query(Board) \
                             .filter_by(name='member') \
                             .first()
    assert member_board == fx_boards.member_board


def test_board_has_posts(fx_session, fx_boards, fx_posts):
    free_posts = fx_session.query(Post) \
                           .filter_by(board=fx_boards.free_board) \
                           .all()
    assert len(free_posts) == 2


def test_board_permission(fx_session, fx_request_context, fx_users,
                          fx_boards, fx_flask_client):
    # user_2로 로그인한다. (권한: 회원)
    username = 'hihi'
    password = 'hellohello'
    fx_flask_client.post(url_for('login'),
                         data=dict(username=username,
                                   password=password),
                         follow_redirects=True)

    # 자유게시판에 글쓰기한다.
    response = fx_flask_client.get(
        url_for('write_post', board_name=fx_boards.free_board.name)
    ).data.decode(encoding='utf-8')
    assert '404' not in response

    # 회원게시판에 글쓰기한다.
    response = fx_flask_client.get(
        url_for('write_post', board_name=fx_boards.member_board.name)
    ).data.decode(encoding='utf-8')
    assert '404' not in response

    # 임원게시판에 글쓰기한다.
    response = fx_flask_client.get(
        url_for('write_post', board_name=fx_boards.executive_board.name)
    ).data.decode(encoding='utf-8')
    assert '404' in response
