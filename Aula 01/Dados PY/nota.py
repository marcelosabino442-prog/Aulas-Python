nota = float(input("digite sua nota: "))
frequencia = int(input("digite sua frequencia: "))

if nota >= 5 and frequencia >= 75:
    situacao = "aprovado"
elif nota >= 5 or frequencia >= 75:
    situacao = "recuperação"
else:
    situacao = "reprovado"

print(f"voce esta na {situacao}")
    