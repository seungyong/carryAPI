def response_data(data):
    if len(data) > 0:
        res = {
            'results': data,
            'statusCode': 200
        }
    elif len(data) == 0:
        res = {
            'statusCode': 404
        }
    else:
        res = {
            'statusCode': 500
        }

    return res
