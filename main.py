import requests
import json


def buscar_dados():
    while True:
        cep = []
        numerous_cep = ''
        try:
            contd_cep = int(input('Digite a quantidade de CEP (Somente números): '))
            for i in range(contd_cep):
                numerous_cep = str(input('Digite o CEP (Somente números): '))
                cep.append(numerous_cep)
        except ValueError:
            print('Ocorreu um Erro, digite somente números no CEP!!')

        else:
            print()
            for i in range(len(cep)):
                url = f"https://viacep.com.br/ws/{cep[i]}/json/"
                request = requests.get(url)

                if request.status_code == 200:
                    data = json.loads(request.content)
                    print(f"{i+1}º Endereço: {data['logradouro']}, {data['bairro']} - {data['localidade']} / {data['uf']}, "
                          f"CEP: {data['cep']}")
                elif request.status_code != 200:
                    print(f'\nOcorreu o erro no (CEP: {cep[i]}) - Código {request.status_code} Erro!!'
                          f'\nVerifique o CEP e tente novamente!!\n')

                else:
                    print(f'Ocorreu o erro: {request.status_code}\nTente novamente!!\n')
            print()


if __name__ == '__main__':
    buscar_dados()
