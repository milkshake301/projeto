# Quiz de cyberbullying (Django)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations quiz
python manage.py migrate
python manage.py seed_quiz          # cria 8 perguntas (use --reset para recriar)
python manage.py createsuperuser    # opcional: editar perguntas em /admin/
python manage.py runserver
```

Abra http://127.0.0.1:8000/. O progresso fica na sessão (sem login).
Em produção: defina DJANGO_SECRET_KEY, DJANGO_DEBUG=0 e DJANGO_ALLOWED_HOSTS.
