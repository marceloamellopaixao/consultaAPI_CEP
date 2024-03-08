import requests
import json


def buscar_dados():
    while True:
        print('\n[--------------------------- [MENU - CONSULTA DE CEP] ---------------------------]\n')
        cep = []
        try:
            contd_cep = int(input('Digite a quantidade de CEP (Somente números): '))
            print()
        except ValueError:
            print('Ocorreu um Erro, digite somente números a quantidade de CEP!!')
            print()
        else:
            while contd_cep <= 0:
                print(f'\nQuantidade de CEP {contd_cep}, inválido!! Quantia Minima de 1 CEP\n')
                contd_cep = int(input('Digite a quantidade de CEP (Somente números): '))

            while contd_cep > 100:
                print(f'\nQuantidade de CEPs {contd_cep} excessivo!! Quantia Máxima de 100 CEPs\n')
                contd_cep = int(input('Digite a quantidade de CEP (Somente números): '))

            for i in range(contd_cep):
                try:
                    numerous_cep = input('Digite o CEP (Somente números): ')
                except ValueError:
                    print('Ocorreu um Erro, digite o CEP sendo Somente Números!!')
                else:
                    while len(numerous_cep) < 7 or len(numerous_cep) > 8:
                        print('CEP inválido, exemplo (01234000)')
                        numerous_cep = input('Digite o CEP (Somente números): ')
                    cep.append(numerous_cep)

        print()
        print('[----------- Endereço(s) Consultados] -----------\n')
        for i in range(len(cep)):
            url = f"https://viacep.com.br/ws/{cep[i]}/json/"
            try:
                request = requests.get(url)
            except Exception as e:
                print(f'Ocorreu um erro: {e}')
            else:
                if request.status_code == 200:
                    try:
                        data = json.loads(request.content)
                    except Exception as e:
                        print(f'Error: {e}')
                        print()
                    else:
                        if 'erro' in data:
                            print(f'Erro!! CEP Inválido/Não Existente para CEP: {cep[i]}')

                        else:
                            print(f"{i + 1}º Endereço: {data['logradouro']}, {data['bairro']} - {data['localidade']} / "
                                  f"{data['uf']}, CEP: {data['cep']}")

                elif request.status_code != 200:
                    print(f'\nOcorreu o erro no (CEP: {cep[i]}) - Código {request.status_code} Erro!!'
                          f'\nVerifique o CEP e tente novamente!!\n')

                else:
                    print(f'Ocorreu o erro: {request.status_code}\nTente novamente!!\n')


if __name__ == '__main__':
    buscar_dados()
