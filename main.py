import requests
import json
# from pprint import pprint


def buscar_dados():
    cep = ["01133000", "01222000",
           "01226010",
           "01317001",
           "02041060",
           "02212000",
           "02212000",
           "02356010",
           "03152155",
           "03164120",
           "03254050",
           "03366010",
           "04038900",
           "04045002",
           "04049060",
           "04149100",
           "04524030",
           "04548001",
           "05009060",
           "05017020",
           "05433002",
           "05541030",
           "05616000",
           "05871330",
           "07124300",
           "07124300",
           "09130460",
           "09531150",
           "09715090"]
    for i in range(len(cep)):
        url = f"https://viacep.com.br/ws/{cep[i]}/json/"
        request = requests.get(url)

        if request.status_code == 200:
            data = json.loads(request.content)
            print(f"{i+1}º Endereço: {data['logradouro']}, {data['bairro']} - {data['localidade']} / {data['uf']}, "
                  f"CEP: {data['cep']}")
        else:
            print(f'Ocorreu o erro: {request.status_code}\nTente novamente!!\n')


if __name__ == '__main__':
    buscar_dados()
