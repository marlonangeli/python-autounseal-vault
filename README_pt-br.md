# python-autounseal-vault

:us: [English](README.md) | :brazil: [Portuguese](README_pt-br.md)

> ⚠️ Esse é um simples script Python “deslacrar” o Vault utilizando sua API. Esse não é o método mais seguro, por favor cheque a [documentação](https://developer.hashicorp.com/vault/tutorials/auto-unseal).

## Porque usar isso?

O Vault é um sistema de gerenciamento de criptografia e segredos baseado em identidade. O método de lacre/deslacre é um processo para criptografar e descriptografar os dados quando o serviço for iniciado ou reiniciado, é um método de segurança para proteger os dados em que apenas quem possui acesso físico podem deslacrar. Leia mais [aqui](https://developer.hashicorp.com/vault/docs/concepts/seal).

O problema nesse caso é a necessidade de intervenção humana cada vez que reiniciar o serviço, sendo assim, esse script simples verifica o status do Vault em um determinado intervalo e se o mesmo estiver lacrado, então o script injeta as chaves para deslacrá-lo.

---

## Como usar

Esse script foi desenvolvido para usar com Docker Swarm, pois utiliza `docker secrets`, um método mais seguro que variáveis de ambiente ou volumes, mas que pode ser facilmente alterado. Apenas remova o bloco `secrets` no arquivo `docker-stack.yml`, adicione um volume entre o host e o container e adicione essa variável de ambiente do serviço **autounseal** em `docker-stack.yml`:

```docker
environment:
	KEYS_PATH: <your_keys_path>
```

Depois disso, verifique o endereço do Vault e altere se precisar utilizando a variável de ambiente `**VAULT_ADDR**`. Se você utiliza Docker pode usar o `hostname`do serviço.

---

## Variáveis de ambiente

| Nome | Valor padrão |
| --- | --- |
| **VAULT_ADDR** | http://vault:8200 |
| **KEYS_PATH** | /run/secrets/keys |
| **INTERVAL** | 60 |

---

## Como fazer build e executar

Você pode utilizar a imagem do [Docker Hub](https://hub.docker.com/repository/docker/marlonangeli/python-autounseal-vault/), mas caso queira alterar e utilizar localmente siga os seguintes passos:

1. Você pode clonar esse repositório

```bash
git clone https://github.com/marlonangeli/python-autounseal-vault.git
cd autounseal
```

2. E criar a imagem

```bash

docker build -t python-autounseal-vault autounseal/
```

3. Adicione seu arquivo `keys.json` usando `secrets` com o nome `keys`

```bash
docker secret create keys ./keys.json
```

Se você não tiver as chaves, comente o serviço **autounseal** e as **secrets** e rode apenas o **vault**.

Abra seu navegador em `http://localhost:8200`

![https://a.imagem.app/boz2IV.png](https://a.imagem.app/boz2IV.png)

Clique em `**Initialize`** e baixe as chaves.

Seu arquivo JSON vai se parecer com isso:

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

>💡 **NOTA:** Se você alterar suas chaves, é preciso recriar os `secrets`, utilize o script `recreate-secrets.sh` para facilitar.

4. Verifique se o Docker Swarm está habilitado:

```bash
docker node ls
```

Se você não estiver no modo Swarm, use

```bash
docker swarm init
```

5. Rode os serviços

```bash
docker stack deploy -c docker-stack.yml secrets
```

Agora, cruze os dedos e torça para funcionar 🙃

Você pode verificar os logs para informações e erros do container.