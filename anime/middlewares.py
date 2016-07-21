def process_response(self, request, response, spider):
    if response.status == 403:
        return request
    else:
        return response