from django.shortcuts import render

def index(request):
    # Здесь ты будешь получать данные из своей модели
    # Например: 
    # info = HackerSpaceInfo.objects.first()
    # context = {
    #     'address': info.address,
    #     'residents_count': info.residents_count,
    #     ...
    # }
    
    # Пока используем заглушки для демонстрации
    context = {
        'address': 'г. Алматы, ул. Байзакова, 280, Smart Point',
        'residents_count': 42,
        'news_list': [
            {
                'title': 'Открытие сезона мастер-классов',
                'date': '24.11.2025',
                'desc': 'Запускаем серию воркшопов по Arduino и IoT для начинающих.'
            },
            {
                'title': 'Новое оборудование: HackRF One',
                'date': '20.11.2025',
                'desc': 'В нашем арсенале пополнение. Теперь доступен SDR трансивер для экспериментов.'
            },
            {
                'title': 'Хакатон: CyberSecurity 2025',
                'date': '15.11.2025',
                'desc': 'Приглашаем всех желающих принять участие в ночном кодинге.'
            }
        ],
        'hardware_list': [
            'Arduino Uno R3/Mini/Nano',
            'Raspberry Pi 2/3/Zero',
            'Orange Pi Prime/R1/2G-IOT/Zero H2+',
            'HackRF One',
            'Motorola Calypso',
            'RTL-SDR R820T2 RTL2832U',
            'ACS ACR122u NFC',
            'Proxmark3 Easy',
            'Wi-Fi & Bluetooth Dongles',
            'Many More+'
        ]
    }
    return render(request, 'index.html', context)