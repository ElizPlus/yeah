from flask import Blueprint, render_template, request, session, redirect

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def lab():
    if request.method == 'POST':
        # Обработка сброса данных
        if 'reset' in request.form:
            session.clear()  # Очищаем сессию
            return redirect('/lab9/')  # Перенаправляем на начальную страницу
        
        # Обработка начала опроса
        session['name'] = request.form.get('name')
        return redirect('/lab9/age')
    
    # Проверка наличия данных о поздравлении в сессии
    if 'message' in session and 'image' in session:
        return render_template('/lab9/congratulations.html', message=session['message'], image=session['image'])
    
    return render_template('/lab9/index.html')


@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    if request.method == 'POST':
        session['age'] = request.form.get('age')
        return redirect('/lab9/gender')
    return render_template('/lab9/age.html')


@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    if request.method == 'POST':
        session['gender'] = request.form.get('gender')
        return redirect('/lab9/preference')
    return render_template('/lab9/gender.html')


@lab9.route('/lab9/preference', methods=['GET', 'POST'])
def preference():
    if request.method == 'POST':
        session['preference'] = request.form.get('preference')
        return redirect('/lab9/taste')
    return render_template('/lab9/preference.html')


@lab9.route('/lab9/taste', methods=['GET', 'POST'])
def taste():
    if request.method == 'POST':
        session['taste'] = request.form.get('taste')
        return redirect('/lab9/congratulations')
    
    preference = session.get('preference')
    if preference == 'вкусное':
        options = [('сладкое', 'Сладкое'), ('сытное', 'Сытное')]
    else:
        options = [('поставь в дом', 'Поставь в дом'), ('сделай сам', 'Сделай сам')]
    
    return render_template('/lab9/taste.html', options=options)


@lab9.route('/lab9/congratulations')
def congratulations():
    name = session.get('name')
    age = session.get('age')
    gender = session.get('gender')
    preference = session.get('preference')
    taste = session.get('taste')

    if preference == 'вкусное':
        if taste == 'сладкое':
            message = f"Поздравляю тебя, {name}! Желаю, чтобы ты легко {'сдал экзамен' if gender == 'мужчина' else 'сдала экзамен'}, был{'а' if gender == 'женщина' else ''} дальновидн{'ым' if gender == 'мужчина' else 'ой'} и счастлив{'ым' if gender == 'мужчина' else 'ой'}. Вот тебе подарок — самая вкусная конфета!"
            image = 'candy.jpg'
        else:
            message = f"Поздравляю тебя, {name}! Желаю, чтобы ты легко {'сдал экзамен' if gender == 'мужчина' else 'сдала экзамен'}, был{'а' if gender == 'женщина' else ''} сильн{'ым' if gender == 'мужчина' else 'ой'} и счастлив{'ым' if gender == 'мужчина' else 'ой'}. Вот тебе подарок — пиццы!"
            image = 'pizza.jpg'
    else:
        if taste == 'поставь в дом':
            message = f"Поздравляю тебя, {name}! Желаю, чтобы ты легко {'сдал экзамен' if gender == 'мужчина' else 'сдала экзамен'}, был{'а' if gender == 'женщина' else ''} талантлив{'ым' if gender == 'мужчина' else 'ой'} и счастлив{'ым' if gender == 'мужчина' else 'ой'}. Вот тебе подарок — красивая ваза!"
            image = 'vase.jpg'
        else:
            message = f"Поздравляю тебя, {name}! Желаю, чтобы ты легко {'сдал экзамен' if gender == 'мужчина' else 'сдала экзамен'}, был{'а' if gender == 'женщина' else ''} креативн{'ым' if gender == 'мужчина' else 'ой'} и счастлив{'ым' if gender == 'мужчина' else 'ой'}. Вот тебе подарок — красивый рисунок!"
            image = 'drawing.jpg'

    # Сохраняем поздравление в сессии
    session['message'] = message
    session['image'] = image

    return render_template('/lab9/congratulations.html', message=message, image=image)