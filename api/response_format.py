class ResponseFormat:
    def to_format(self, data):
        return {
            'id': data['id'],
            'name': data['name'],
            'surname': data['surname'],
            'email': data['email'],
            'password': data['password'],
            'created_at': data['created_at'],
            'updated_at': data['updated_at']
        }