Клонирование репозитория и создание папки
git clone https://github.com/romazanovma/jedi.bigdata.1.git
cd jedi.bigdata.1/
mkdir mromazanov
touch mromazanov/.gitkeep
git add mromazanov/*
git commit -m 'Init commit'

Добавление Airflow
git remote add airflow https://github.com/apache/airflow.git
git merge airflow/v1-8-stable --allow-unrelated-histories
vim .gitignore
vim README.md
git commit -m 'Add airflow'

Внесение изменений в Airflow
git checkout airflow/v1-8-stable
rm TODO.md
vim UPDATING.md
vim MANIFEST.in
vim DISCLAIMER
vim README.md
vim setup.py
vim setup.cfg
vim NOTICE
vim CONTRIBUTING.md
vim CHANGELOG.txt
git commit -am 'WIP: Testing working with git'
git branch testing

Удаление коммита от 16 Июня 2017
git checkout -b fix main
git log --until='17 Jun 2017'
git revert ca97ca752bad4b793c24d574a2f434bb561e84cd

Добавление файла SOLUTION.md
touch SOLUTION.md
gedit SOLUTION.md &
git add SOLUTION.md
git checkout main	
git commit -m 'Add SOLUTION.md'

upd. Удаление коммита от 16 Июня
git chekout main^
git rebase -i 9831f41028f88299f435a03c1c66c152ae3df963
vim .gitignore
vim README.md
git add README.md .gitignore
git rebase --continue
git branch -f fix

