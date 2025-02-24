# Основная логика бота
import telebot
import buttons
import database


# Создаем объект бота
bot = telebot.TeleBot('TOKEN')


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if database.check_user(user_id):
        pr = database.get_pr_buttons()
        bot.send_message(user_id, 'Добро пожаловать!', reply_markup=buttons.main_menu(pr))
    else:
        bot.send_message(user_id, 'Здравствуйте! Давайте начнем регистрацию!\n'
                                  'Введите свое имя', reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)


# Этап получения имени
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text

    bot.send_message(user_id, 'Отлично! Теперь отправьте свой номер телефона!',
                     reply_markup=buttons.num_button())
    # Переход на этап получения номера
    bot.register_next_step_handler(message, get_num, user_name)


# Этап получения номера
def get_num(message, user_name):
    user_id = message.from_user.id

    # Проверка, если пользователь отправил номер по кнопке
    if message.contact:
        user_num = message.contact.phone_number
        database.register(user_id, user_name, user_num)

        bot.send_message(user_id, 'Регистрация прошла успешно!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Отправьте номер телефона по кнопке!')
        # Возврат на этап получения номера
        bot.register_next_step_handler(message, get_num, user_name)


# Админ-панель
@bot.message_handler(commands=['admin'])
def admin(message):
    if message.from_user.id == 6775701667:
        bot.send_message(message.from_user.id,
                         'Введите информацию о продукте в следующем порядке:\n\n'
                         '<b>Название, описание, количество, цена, фото</b>\n\n'
                         'Фотографию загружать на <a href="https://postimages.org/">сайте</a> '
                         'и отправлять прямую ссылку!', parse_mode='HTML')
        bot.register_next_step_handler(message, get_product)


def get_product(message):
    data = message.text.split(', ')

    if len(data) == 5:
        database.add_product(data[0].strip(), data[1].strip(),
                             data[2].strip(), data[3].strip(), data[4].strip())
        bot.send_message(message.from_user.id, 'Успешно!')
    else:
        bot.send_message(message.from_user.id, 'Ошибка в данных!')




bot.polling(non_stop=True)
