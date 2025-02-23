# Детектор автомобилей

## Общее описание

Выполнение тестового задания компании "Комплексные системы"

Приложение представляет собой веб сервис на FastAPI, содержащий html-форму для загрузки изображений и демонстрации результатов детекции автомобилей на них.

Приложение работает в Docker контейнере

Модель для обнаружения объектов реализована через дообучение модели YOLO.

Устройство работы модели, IP и порт приложения FastAPI и Docker контейнера задаются через переменные окружения ```APP_DEVICE```, ```APP_IP```, ```APP_PORT```, ```DOCKER_IP``` и ```DOCKER_PORT``` соответсвенно. Изначально переменные заданы в файле ```.env```

## Запуск

Чтобы построить контейнер и запустить приложение необходимо выполнить команду ```make up```

После построения и запуска конетейнера приложение будет запущено и доступно. По указанному адерсу можно будет видеть форму для загрузки изображений

## Использование

Нажмите кнопку "Обзор", выберите любое количество изображений форматов ".jpg" или ".png" и нажмите кнопку "Найти автомобили". Приложение выведет на тойже странице изображения с ограничивающими прямоугольниками и строки с их координатами в формате xyxy.

## Обучение

Обучение проводилось в среде Google Collab. Блокнот ```train_cars.ipynb``` представлен в репозитории.

## Точность

### Валидация

После обучении была построена PR кривая и расчитана метрика mAP50-95, составившая 0.705 на валидационной выборке.

<img src="./images/PR_curve_val.png" width="300" height="300" alt='PR-curve-val'>

### Тест

После обучении была построена PR кривая и расчитана метрика mAP50-95, составившая 0.725 на тетовой выборке.

<img src="./images/PR_curve_test.png" width="300" height="300" alt='PR-curve-test'>

### Предобученная модель

Для сравнения была проведена валидация предобученной модели на валижационной выборке. Была построена PR кривая и расчитана метрика mAP50-95, составившая 0.32.

<img src="./images/PR_curve_pretrain.png" width="300" height="300" alt='PR-curve-pretrain'>

Как видно, дообучение модели на предоставленной выборке ощутимо улучшило предсказания, увеличив более чем в два раза метрику mAP50-90. Это связанно в том числе с тем, что предобученная модель имеет больше классов предсказания и некоторые автомобили машина принимала за грузовики.

### Пример работы

Пример детекции изображений на валидационной выборке в сравнении с разметкой.

 <div class="row">
  <div class="column">
    <img src="./images/val_batch0_labels.jpg" alt="label" width="300" height="300">
  </div>
  <div class="column">
    <img src="./images/val_batch0_pred.jpg" alt="pred" width="300" height="300">
  </div>
 </div>

 ### Рекомендации по повышению точности

 В первую очередь надо сказать, что дообучение модели проводилось на 600 изображениях и только порядка 30% содержали объекты (соотношение сохранено из всей выборки). С одной стороны, это обучает модель на более менее реальной картине, когда большая часть приходящих кадров не будет содержать объектов. Но с другой стороны непосредственно объектов модель видит не много, так что можно было бы увеличить датасет либо самым прямым путем (сделать фотографии "в поле"), либо косвенным (создание искусственных фотографий - набор из открытых источников или увеличение количества объектов на изображениях путем копирования с других изображений, более простые аугументации). Второй вариант менее затратен и позволит проверить, будет ли увеличение датасета сказываться на точности.

 Во-вторых, дообучение проходило с дефолтными параметрами, так что можно пройтись по сетке lr, оптимизаторов, это требует времени и ресурсов, т.к. проесс обучения сверточной нейросети - времязатратный. Можно добавить dropuot для регуляризации весов. 

 В-третьих, можно было бы изменить архитектуру сети. Это на мой взгляд спорный метод, т.к. исходная архитектура YOLO создана професионалами и проверена на множестве случаев. Экспериментировать с архитектурой можно, но необходимо глубокое понимание и опыт.

 Так же можно не только частично менять архитектуру, но и воспользоваться вообще другой или даже другим методом работы сети. Например попробовать модели семейства Faster-RCNN.