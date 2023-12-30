class ResponseFormatComPanyUser:
    def to_format(self, data):
        return {
            'id': data['id'],
            'profile': data['profile'],
            'user': data['user'],
            'company': data['company'],
        }