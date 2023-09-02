

def proxy_reformer(str_proxy: str):
    proxy_list = str_proxy.split(':')
    if len(proxy_list) == 3:
        proxy = {
            'proxy_type': proxy_list[0],  # (mandatory) protocol to use (see above)
            'addr': proxy_list[1],  # (mandatory) proxy IP address
            'port': int(proxy_list[2]),  # (mandatory) proxy port number
            'rdns': True  # (optional) whether to use remote or local resolve, default remote
        }
        return proxy
    elif proxy_list[0] == 'MTP':
        if proxy_list[3] == '0':
            proxy = (proxy_list[1], proxy_list[2], '00000000000000000000000000000000')
            return proxy
        else:
            if len(proxy_list[3]) == 32:
                proxy = (proxy_list[1], int(proxy_list[2]), proxy_list[3])
                return proxy
            elif proxy_list[3].startswith('ee'):
                proxy = (proxy_list[1], int(proxy_list[2]), proxy_list[3].lstrip('ee'))
                return proxy
            elif proxy_list[3].startswith('7'):
                proxy = (proxy_list[1], int(proxy_list[2]), proxy_list[3].lstrip('7'))
                return proxy
    elif len(proxy_list) == 5:
        if proxy_list[0].lower() == 'https':
            proxy = {
                'proxy_type': 'http',
                'addr': proxy_list[1],
                'port': int (proxy_list[2]),
                'username': proxy_list[3],
                'password': proxy_list[4],
                'rdns': True}
        else:
            proxy = {
                'proxy_type': proxy_list[0],
                'addr': proxy_list[1],
                'port': int (proxy_list[2]),
                'username': proxy_list[3],
                'password': proxy_list[4],
                'rdns': True}
        return proxy
    else:
        print('Unsupported proxy format')

