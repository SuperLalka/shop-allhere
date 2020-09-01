from django import forms


class ApplicationForOrderingForm(forms.Form):
    the_contact_person = forms.CharField(label="Контактное лицо", max_length=100)
    tin_of_the_organization = forms.CharField(label="ИНН Организации")
    email = forms.EmailField(label="E-mail", max_length=40)
    contact_phone_number = forms.CharField(label="Номер телефона для связи", initial="+7")
    order_list = forms.CharField(label="Состав заказа (список и количество позиций)", max_length=1000,
                                 help_text="Сумма заказа должна быть от 50 000 рублей",
                                 widget=forms.Textarea(attrs={'rows': 4}))


TYPE_SENTENCE = (
    ('rr', 'Аренда помещения'),
    ('sr', 'Продажа помещения'),
    ('sl', 'Продажа земельного участка'),
    ('ot', 'Иное'),
)


class ForLandlordsForm(forms.Form):
    type_sentence = forms.ChoiceField(label="Тип предложения", choices=TYPE_SENTENCE)
    region = forms.CharField(label="Регион", max_length=60)
    town = forms.CharField(label="Город", max_length=20)
    street_house = forms.CharField(label="Улица, дом", max_length=30)
    map_link = forms.CharField(label="Ссылка на карту или файл с указанием месторасположения участка или объекта:",
                               help_text="необязательное для заполнения поле", required=False)
    land_area = forms.CharField(label="Предлагаемая площадь помещения/земельного участка:", max_length=20)
    land_cadastral_number = forms.CharField(label="Кадастровый номер земельного участка",
                                            help_text="необязательное для заполнения поле", required=False)
    contact_person = forms.CharField(label="Ф.И.О. контактного лица", max_length=50)
    contact_telephone = forms.CharField(label="Телефонный номер контактного лица", max_length=15)
    contact_email = forms.EmailField(label="E-mail контактного лица", max_length=30)
    additional_information = forms.CharField(
        label="Дополнительная информация", max_length=600,
        help_text="Текст не более 600 символов, для больших обьёмов текста воспользуйтесь функцией загрузки файла ниже",
        required=False, widget=forms.Textarea(attrs={'rows': 4}))
    file = forms.FileField(label="Вложение", required=False)


class ForLeaseHoldersForm(forms.Form):
    contact_person = forms.CharField(label="Ф.И.О. контактного лица", max_length=50)
    contact_telephone = forms.CharField(label="Телефонный номер контактного лица", max_length=15)
    contact_fax = forms.CharField(
        label="Факс контактного лица", max_length=15, help_text="необязательное для заполнения поле", required=False)
    contact_email = forms.EmailField(label="E-mail контактного лица", max_length=30)
    contact_website = forms.CharField(
        label="Сайт контактного лица", max_length=25, help_text="необязательное для заполнения поле", required=False)
    company_name = forms.CharField(label="Название компании", max_length=50)
    brand = forms.CharField(label="Торговая марка/Название магазина", max_length=50)
    description_company = forms.CharField(
        label="Краткое описание деятельности компании", max_length=500,
        help_text="Текст не более 500 символов",
        widget=forms.Textarea(attrs={'rows': 3}))
    presented_tm = forms.CharField(
        label="Представленные торговые марки", max_length=300,
        help_text="Текст не более 300 символов", widget=forms.Textarea(attrs={'rows': 3}))
    current_stores = forms.CharField(
        label="Информация о действующих магазинах сети с указанием адреса", max_length=300,
        help_text="Текст не более 300 символов", widget=forms.Textarea(attrs={'rows': 3}))
    network_develops = forms.CharField(
        label="Если сеть развивает разные форматы, пожалуйста, укажите их",
        max_length=300, help_text="Текст не более 300 символов",
        widget=forms.Textarea(attrs={'rows': 3}))
    development_plans = forms.CharField(
        label="Планы развития сети", max_length=300,
        help_text="Текст не более 300 символов",
        widget=forms.Textarea(attrs={'rows': 3}))
    interested_region = forms.CharField(
        label="Какой город/регион Вас интересует?", max_length=100,
        help_text="Текст не более 100 символов",
        widget=forms.Textarea(attrs={'rows': 1}))
    competitor_store = forms.CharField(
        label="Кого вы считаете прямым конкурентом магазина, сети?", max_length=100,
        help_text="Текст не более 100 символов",
        widget=forms.Textarea(attrs={'rows': 1}))
    favorable_neighborhood = forms.CharField(
        label="Соседство с каким профилем, магазином какого вида деятельности для вас наиболее благоприятно?",
        max_length=100,
        help_text="Текст не более 100 символов",
        widget=forms.Textarea(attrs={'rows': 1}))
    price_range = forms.CharField(
        label="Укажите ценовой диапазон товаров, представленных в магазинах сети",
        max_length=100,
        help_text="Текст не более 100 символов",
        widget=forms.Textarea(attrs={'rows': 1}))
    kind_of_consumer = forms.CharField(
        label="На какого потребителя рассчитан магазин, сеть?",
        max_length=100,
        help_text="Текст не более 100 символов",
        widget=forms.Textarea(attrs={'rows': 1}))
    required_footage = forms.CharField(
        label="Необходимый метраж помещения (минимальный, максимальный, оптимальный)", max_length=50)
    technical_requirements = forms.CharField(
        label="Уточните технические требования (по электроэнергии, воде, др.)",
        max_length=300,
        help_text="Текст не более 300 символов",
        widget=forms.Textarea(attrs={'rows': 3}))


SELECT_REGION = (
    ('ekt', 'Екатеринбург'),
    ('knd', 'Краснодар'),
    ('mos', 'Москва'),
    ('nng', 'Нижний Новгород'),
    ('sam', 'Самара'),
    ('spb', 'Санкт-Петербург')
)


class CardApplicationForm(forms.Form):
    region = forms.ChoiceField(label="Регион", choices=SELECT_REGION, initial="mos")
    user_name = forms.CharField(label="Ф.И.О", max_length=60)
    user_phone = forms.CharField(label="Номер телефона", max_length=20)
