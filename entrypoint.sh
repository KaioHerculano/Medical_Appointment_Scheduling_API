echo "Aguardando o banco de dados..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Aplicando as migrações..."
poetry run python manage.py migrate

echo "Coletando arquivos estáticos..."
poetry run python manage.py collectstatic --noinput

echo "Iniciando o servidor..."
exec "$@"
