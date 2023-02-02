import requests
import tools as t

logger = t.get_logger(__name__)

VAULT_ADDR = t.get_env('VAULT_ADDR')
KEYS_PATH = t.get_env('KEYS_PATH')
   
vault_tokens = t.read_json(KEYS_PATH)


def is_sealed() -> bool:
    """Check if vault is sealed. Returns True if sealed, False if unsealed"""
    try:
        url = f'{VAULT_ADDR}/v1/sys/health'
        r = requests.get(url)
        return r.json()['sealed']
    
    except Exception as e:
        logger.error(e)
        return True
    
    
def unseal(key: str) -> dict:
    """Unseal vault with key. Returns dict with seal status and progress"""
    try:
        logger.info(f'Unsealing vault with key: {key[:8]}...')
        url = f'{VAULT_ADDR}/v1/sys/unseal'
        headers = {'X-Vault-Token': vault_tokens['root_token']}
        r = requests.post(url, headers=headers, json={'key': key})
        return r.json()
    
    except Exception as e:
        logger.error(e)
        return False


def main():
    try:
        if not is_sealed():
            logger.info('Vault is already unsealed')
            return

        for key in vault_tokens['keys']:
            r = unseal(key)
            logger.info(r)
            
            if not is_sealed():
                logger.info('Vault is unsealed successfully')
                return
    
    except Exception as e:
        logger.error(e)
        return


if __name__ == '__main__':
    INTERVAL = int(t.get_env('INTERVAL'))
    
    logger.info('Starting autounseal script')
    logger.debug(
        f"""Vault address: {VAULT_ADDR}
        Keys path: {KEYS_PATH}
        Interval: {INTERVAL}s"""
    )
    
    main()
