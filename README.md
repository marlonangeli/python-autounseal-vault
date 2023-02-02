# python-autounseal-vault

> ⚠️ This is a simple Python script that unseal Vault using your API. It isn’t the safest method, please check the [documentation](https://developer.hashicorp.com/vault/tutorials/auto-unseal).

## Why use this?

Vault is an identity-based secrets and encryption management system. The sealing/unsealing method is a process to encrypt or decrypt data when the service is started or restarted, it is a security method to protect data that only those with physical access can open. Read more [here](https://developer.hashicorp.com/vault/docs/concepts/seal).

The problem in this case is the human intervention for each restart, so this simple script can check in determined interval Vault status and unseal it.

---

## Hot to use

This script is developed to use in Docker Swarm, using `docker secrets`, a better method than `environment variables` or `volumes` but it can easy change. Just remove the `secrets` block in `docker-stack.yml`, add the `volume` bind between your host and the container and add this in **autounseal** service in `docker-stack.yml`:

```docker
environment:
	KEYS_PATH: <your_keys_path>
```

After this, check your Vault host, if you use Docker you can use the `hostname` service.

---

## Environment variables

| Name | Default Value |
| --- | --- |
| **VAULT_ADDR** | http://vault:8200 |
| **KEYS_PATH** | /run/secrets/keys |
| **INTERVAL** | 60 |

---

## How to build and run

1. You can clone this repository:

```bash
git clone https://github.com/marlonangeli/python-autounseal-vault.git
cd autounseal
```

2. And build the image

```bash

docker build -t python-autounseal-vault autounseal/
```

3. Add your `keys.json` to `secrets` as `keys`

```bash
docker secret create keys ./keys.json
```

If you don’t have the keys, just comment **autounseal** service in `docker-stack.yml` and run just **vault**.

Open your browser in `http://localhost:8200`

![https://a.imagem.app/boz2IV.png](https://a.imagem.app/boz2IV.png)

Click in **Initialize** and download your keys.

Your JSON file will be like this:

```json
{
  "keys": [
    "673e516bfde61e5462266a111370619761c916d5a8fcb8408c9c63c7d7d3df4924",
    "e345923e486258d8cfa444965df77fa93a2601c5f1de1f0088bcaa057522e7f550",
    "b8391f462cce3e8bf6a19ba6d7532e2b5020ffc7aab05884f62695d5d67fab2d7b",
    "532d8c59c33168ef342fe14bc3a460031cd2b105b796dfb0276f934b8f0f841b3a",
    "45fddaacc7ab33a74dc26ff81ba62da4195eed2251300b83e115971b2b4b6c5f02"
  ],
  "keys_base64": [
    "Zz5Ra/3mHlRiJmoRE3Bhl2HJFtWo/LhAjJxjx9fT30kk",
    "40WSPkhiWNjPpESWXfd/qTomAcXx3h8AiLyqBXUi5/VQ",
    "uDkfRizOPov2oZum11MuK1Ag/8eqsFiE9iaV1dZ/qy17",
    "Uy2MWcMxaO80L+FLw6RgAxzSsQW3lt+wJ2+TS48PhBs6",
    "Rf3arMerM6dNwm/4G6YtpBle7SJRMAuD4RWXGytLbF8C"
  ],
  "root_token": "hvs.IuLmJPDEqVeKaaGDrLh9ww5I"
}
```
>💡 ******NOTE:****** If you change your keys, you need to remove your old secrets and recreate.

4. Check if Docker Swarm is enabled:

```bash
docker node ls
```

If you aren’t in Swarm Node, use

```bash
docker swarm init
```

5. And run the services

```bash
docker stack deploy -c docker-stack.yml secrets
```

Now, cross your fingers and hope it works 🙃

You can check the logs for info or errors in container.