from users.models import User


def create_user(message):
    is_private = True if message['user_type'] == 'private' else False
    message['private'] = is_private
    user, _ = User.objects.update_or_create(user_id=message['user_id'], defaults={'first_name': message['first_name'],
                                                                                  'last_name': message["last_name"],
                                                                                  'email': message["email"],
                                                                                  'avatar': message['avatar'],
                                                                                  'private': True if message[
                                                                                                         'user_type'] == 'private' else False,
                                                                                  'avg_rate': message['avg_rate']})
    return user
