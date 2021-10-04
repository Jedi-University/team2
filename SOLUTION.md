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
git checkout airflow/v1-8-stable
git rebase -i 6fa52cf3109b2c1a9598c3ddd029503380b1a8b9
git merge 857cab47525d6b4daa1210eef123fbbca17c3e21 --allow-unrelated-histories
vim .gitignore
vim README.md 
git add README.md .gitignore 
git commit
git branch -f fix
git push -f origin fix

