import re
import socket
import ssl
from urllib.parse import urlparse
import tldextract

def extract_features(url):
    features = {}
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        parsed_url = urlparse(url)
        ext = tldextract.extract(url)
        domain = parsed_url.netloc
    except Exception:
        return None

    features['url_length'] = len(url)
    features['domain_length'] = len(domain)
    features['qty_dots'] = url.count('.')
    features['qty_hyphen'] = url.count('-')
    features['qty_at'] = url.count('@')
    features['qty_question'] = url.count('?')
    features['qty_equal'] = url.count('=')
    
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    features['is_ip'] = 1 if ip_pattern.match(domain) else 0
    features['has_subdomain'] = 1 if ext.subdomain else 0
    
    features['has_valid_ssl'] = 0
    if url.startswith('https://'):
        hostname = domain.split(':')[0]
        context = ssl.create_default_context()
        try:
            with socket.create_connection((hostname, 443), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    features['has_valid_ssl'] = 1
        except Exception:
            features['has_valid_ssl'] = 0

    return features