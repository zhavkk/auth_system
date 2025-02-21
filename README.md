# auth_system_MAI_task
Задание: Авторизация.
реализовать систему авторизацию (JWT )с поддержкой авторизации через Yandex, VK. 
Организовать ролевую модель и историю заходов с помощью этой авторизации. При регистрации, необходимо отправлять письмо в телеграм чат с приветственным сообщением.
Для этого нужно написать воркер,  который слушает события из кафки / rabbit и отправляет сообщение пользователю

NOTE: Для авторизации через VK нужно дополнительно использовать ngrok
Роли : role_id = 1 - admin, role_id = 2 - user

Ниже приведены все маршруты: 
![Маршруты: ](https://github.com/user-attachments/assets/98040447-2298-459a-a663-c3a8b3ba6be2)
Их краткое описание:   
1. POST /api/v1/demo-auth/register Register User - регистрирует нового пользователя локально ( без использования VK, Yandex)
2. POST /api/v1/demo-auth/token Login For Access Token - чтобы получить JWT токен, нужно залогиниться
3. GET /api/v1/admin/users Get All Users - Админ может просматривать всех зарегистрированных пользователей
4. GET /api/v1/admin/history Get Auth History - Админ может просматривать историю заходов
5. GET /login/yandex/ Login Yandex - перенаправляем на Yandex, чтобы пользователь вошел через почту
6. GET /login/yandex/callback Yandex Callback - после того как пользователь войдет в почту Яндекса, Яндекс перенаправляет на этот эндпоинт с параметром code, По этому коду мы запросим access_token от Яндекса и узнаем данные о пользователе.
7. GET /login/vk/ Vk Login - Аналогично .5
8. GET /login/vk/callback Vk Callback - Аналогично .6






При успешной регистрации нового пользователя система генерирует событие и публикует его в специальный топик Kafka. 
Затем воркер, подписанный на этот топик, получает событие, выполняет необходимую обработку данных и отправляет уведомление в указанный Telegram-канал.
Пример работы воркера:



![Пример работы воркера: ](https://github.com/user-attachments/assets/8b7d5c3e-f318-4e79-afaf-33c28ba1378d)



# HOW TO START
Ставим .env, все необходимые переменные прописаны в .env.template

1. docker-compose up -d

2. cd app/core

3. python3 kafka_worker.py
