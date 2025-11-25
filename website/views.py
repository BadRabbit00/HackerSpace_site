from django.shortcuts import render

def index(request):
    # Данные об адресе и количестве резидентов теперь берутся из context_processors.py
    
    # Пока используем заглушки для новостей и оборудования
    context = {
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
    return render(request, 'website/index.html', context)