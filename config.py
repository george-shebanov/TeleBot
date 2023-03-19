with open(file='config.txt', mode='rt', encoding='utf-8') as f:
    for line in f:
        k, v = line.split()
        if k == "apikey":
            key = v
        if k == 'token':
            TOKEN = v


currencies = {"доллар": "USD", "евро": "EUR", "рубль": "RUB"}
