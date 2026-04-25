def fetch_rates(http_client):
    return http_client.get('/rates')
