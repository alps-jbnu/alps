from alps.post import Post


def test_posts_are_created(fx_session, fx_posts):
    assert fx_session.query(Post).count() > 0
    hello_post = fx_session.query(Post) \
                           .filter_by(title='Hello, ALPS!') \
                           .first()
    assert hello_post == fx_posts.post_3
