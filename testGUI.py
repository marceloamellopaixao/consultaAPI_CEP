import requests
from tkinter import Tk, Label, Entry, Button, Toplevel, scrolledtext, filedialog
from tkinter import simpledialog, messagebox
import pandas as pd


class ConsultaCEPApp:
    def __init__(self, master):
        self.master = master
        master.title("Consulta de CEP")

        self.label = Label(master, text="Digite a quantidade de CEP (Somente números):")
        self.label.pack()

        self.entry = Entry(master)
        self.entry.pack()

        self.button = Button(master, text="Consultar", command=self.buscar_dados)
        self.button.pack()

    def buscar_dados(self):
        contd_cep = self.entry.get()
        cep = []

        try:
            contd_cep = int(contd_cep)
        except ValueError:
            messagebox.showerror("Erro", "Digite somente números para a quantidade de CEP.")
            return

        if contd_cep <= 0:
            messagebox.showerror("Erro", "Quantidade de CEP inválida. Quantidade mínima é 1.")
            return
        elif contd_cep > 100:
            messagebox.showerror("Erro", "Quantidade de CEPs excessiva. Quantidade máxima é 100.")
            return

        for i in range(contd_cep):
            numerous_cep = simpledialog.askstring("CEP", f"Digite o CEP {i + 1} (Somente números):")
            try:
                numerous_cep = str(numerous_cep)
            except ValueError:
                messagebox.showerror("Erro", "Digite o CEP sendo Somente Números.")
                return

            while len(numerous_cep) < 7 or len(numerous_cep) > 8:
                messagebox.showerror("Erro", "CEP inválido. Exemplo: 01234000")
                numerous_cep = simpledialog.askstring("CEP", f"Digite o CEP {i + 1} (Somente números):")

            cep.append(numerous_cep)

        self.display_result(cep)

    def display_result(self, cep):
        result_window = Toplevel(self.master)
        result_window.title("Resultados")

        result_text = scrolledtext.ScrolledText(result_window, wrap='word', width=40, height=10)
        result_text.pack(expand=True, fill='both')

        for i in range(len(cep)):
            url = f"https://viacep.com.br/ws/{cep[i]}/json/"
            try:
                request = requests.get(url)
                request.raise_for_status()
                data = request.json()
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"Erro na consulta do CEP {cep[i]}: {e}")
                continue

            if 'erro' in data:
                messagebox.showinfo("Resultado", f"Erro!! CEP Inválido/Não Existente para CEP: {cep[i]}")
            else:
                result_text.insert('end',
                                   f"{i + 1}º Endereço: {data['logradouro']}, {data['bairro']} - "
                                   f"{data['localidade']} / "
                                   f"{data['uf']}, CEP: {data['cep']}\n")

        export_button = Button(result_window, text="Exportar para Excel", command=lambda: self.export_to_excel(cep))
        export_button.pack()

    def export_to_excel(self, cep):
        df = pd.DataFrame(columns=['ID', 'Endereço Completo'])

        for i in range(len(cep)):
            url = f"https://viacep.com.br/ws/{cep[i]}/json/"
            try:
                request = requests.get(url)
                request.raise_for_status()
                data = request.json()
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"Erro na consulta do CEP {cep[i]}: {e}")
                continue

            if 'erro' in data:
                continue
            else:
                endereco_completo = f"{data['logradouro']}, {data['bairro']} - {data['localidade']} / {data['uf']}"
                cep_tabela = data['cep']
                df = pd.concat([df, pd.DataFrame({'Ordem': [i + 1],
                                                  'Endereço': [endereco_completo],
                                                  'CEP': [cep_tabela]}
                                                 )
                                ])

        export_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                        filetypes=[("Excel files", "*.xlsx")])

        if export_file_path:
            df = df.sort_values(by='ID')  # Ordenando pelo ID
            df.to_excel(export_file_path, index=False)
            messagebox.showinfo("Exportado", "Dados exportados para Excel com sucesso!")


if __name__ == "__main__":
    root = Tk()
    app = ConsultaCEPApp(root)
    root.mainloop()
