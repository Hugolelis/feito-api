import os

os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://feito:feito@localhost:5432/feito_test")
os.environ.setdefault("SECRET_KEY", "chave-de-teste")
