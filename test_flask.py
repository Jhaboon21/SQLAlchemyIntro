from unittest import TestCase

from app import app
from models import db, connect_db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
#connect_db(app)
with app.app_context():
    db.drop_all()
    db.create_all()

#db.drop_all()
#db.create_all()

class UserTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """add sample User"""
        with app.app_context():
            User.query.delete()

            user = User(first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id
        
    def tearDown(self):
        """Clean up after test"""
        with app.app_context():
            db.session.rollback()

    def test_list_user(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)

    def test_show_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>John Doe</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            TEST_IMG = "https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_1280.png"
            d = {"first_name": "Jack", "last_name": "Black", "image_url": TEST_IMG}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/users/2">Jack Black</a>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            with app.app_context():
                User.query.filter_by(id=self.user_id).delete()
                #db.session.delete(user)
                db.session.commit()

                resp = client.get("/users")
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn('<ul>\n  \n</ul>', html)