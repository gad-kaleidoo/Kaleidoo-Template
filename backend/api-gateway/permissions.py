import manager

class Permission:
    def __init__(self, token):
        self.user_data = self.verify_token(token)

    def verify_token(self, token):
        return manager.decode_jwt(token)  # Hypothetical function

    def check_permission(self, action):
        return action in self.user_data['permissions']
