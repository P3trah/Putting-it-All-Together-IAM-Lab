from app import db
from app.models import User, Recipe

def seed():
    # Create users
    user1 = User(username='user1', password='password1', image_url='https://example.com/image1.jpg', bio='User 1 bio')
    user2 = User(username='user2', password='password2', image_url='https://example.com/image2.jpg', bio='User 2 bio')

    # Create recipes
    recipe1 = Recipe(title='Recipe 1', instructions='Instructions for recipe 1', minutes_to_complete=30, user=user1)
    recipe2 = Recipe(title='Recipe 2', instructions='Instructions for recipe 2', minutes_to_complete=45, user=user2)

    # Add to session and commit
    db.session.add_all([user1, user2, recipe1, recipe2])
    db.session.commit()

if __name__ == '__main__':
    seed()
