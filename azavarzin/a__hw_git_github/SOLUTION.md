* Создаем форк и клонируем свой репозиторий

```bash
git clone git@github.com:AlexeyZavarzin/jedi.bigdata.1.git
cd jedi.bigdata.1
```

* Создаем папку по шаблону и делаем `Initial commit`

```bash
mkdir azavarzin
cd azavarzin
touch .gitkeep
git add -A
git commit -m "Initial commit"
```

* Подключаемся к удаленному репозиторию `apache airflow` и забираем ветку `v1-8-stable` и сливаем ее с основной

```bash
git remote add airflow git@github.com:apache/airflow.git
git fetch airflow v1-8-stable
git merge v1-8-stable --allow-unrelated-histories
```

* Решаем конфликты (через `vim`) и делаем коммит

```bash
git add -A
git commit -m "Add airflow"
```

* Вносим в ветку `v1-8-stable` изменения и делаем коммит (Upd.)

```bash
git checkout v1-8-stable
vim ... # вносим изменения в файлы
git add -A
git commit -m "WIP: Testing working with git"
```

> переносим коммит `"WIP: Testing working with git"` на ветку `main`
```bash
git checkout main
git cherry-pick v1-8-stable
```

* Создаем еще одну ветку и удаляем из нее коммиты (Upd.)

```bash
git checkout -b fix
git log
git rebase -i 9831f410~
vim ... # решаем конфликты
git add -A
git rebase --continue
git merge be5e4362 # мержимся к Initial commit 
vim ... # снова решаем конфликты
git add -A
git commit -m "Merge fix to Initial commit"
git push origin fix
```

* Создаем файл со списком команд и коммитим его в `main`

```bash
git checkout main
touch SOLUTION.md
git add -A
git commit -m "Adding a solution (SOLUTION.md)"
```

* Пушим локальные ветки на удаленный репозиторий

```bash
git push origin --all
```
