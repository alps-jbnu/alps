from alps.post import Board, Post


def test_posts_are_created(fx_session, fx_posts):
    assert fx_session.query(Post).count() > 0
    hello_post = fx_session.query(Post) \
                           .filter_by(title='Hello, ALPS!') \
                           .first()
    assert hello_post == fx_posts.post_3


def test_boards_are_created(fx_session, fx_boards):
    assert fx_session.query(Board).count() > 0
    member_board = fx_session.query(Board) \
                             .filter_by(name='member') \
                             .first()
    assert member_board == fx_boards.board_2
