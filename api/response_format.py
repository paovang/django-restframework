class ResponseFormat:
    def to_format(self, data):
        return {
            'id': data['id'],
            'username': data['username'],
            'email': data['email'],
            'created_at': data['created_at'],
            'updated_at': data['updated_at']
        }