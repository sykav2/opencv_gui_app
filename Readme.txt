1. Создать виртуальное окружение conda 
conda create -n cv_env python=3.6
conda activate cv_env
2. Установи зависимости
conda install -c conda-forge opencv numpy
3. Свяжи локальный репозиторий с удалённым
Инструкция для запуска
1. Клонирование репозитория
git clone https://github.com/sykav2/opencv_gui_app.git
cd opencv_gui_app
2. Создание виртуального окружения
conda create -n cv_env python=3.6
conda activate cv_env
3. Запуск приложения
python app.py