import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        response = event['Records'][0]['cf']['response']
        headers = response.get('headers', {})

        logger.info("Intercepted CloudFront viewer response successfully.")

        headers['x-frame-options'] = [{
            'key': 'X-Frame-Options', 
            'value': 'DENY'
        }]

        headers['x-xss-protection'] = [{
            'key': 'X-XSS-Protection', 
            'value': '1; mode=block'
        }]

        headers['x-content-type-options'] = [{
            'key': 'X-Content-Type-Options', 
            'value': 'nosniff'
        }]

        headers['strict-transport-security'] = [{
            'key': 'Strict-Transport-Security', 
            'value': 'max-age=63072000; includeSubDomains; preload'
        }]

        response['headers'] = headers
        return response

    except Exception as e:
        logger.error(f"Error processing security headers: {str(e)}")
        return response