from shutil import rmtree

import pytest
from tortoise import Tortoise
from app.models import Company, VATSClient


@pytest.fixture(autouse=True)
async def db(tmp_path):
    dsn = f'sqlite://{tmp_path}/db.sqlite'
    await Tortoise.init(db_url=dsn, modules={'models': ['app.models']})
    await Tortoise.generate_schemas()

    company = await Company.create(name='test company')
    await VATSClient.create(
        company=company,
        client_id='1',
        client_sign='1',
        admin_domain='vats1.fs.loc',
    )

    try:
        yield
    finally:
        await Tortoise.close_connections()
        rmtree(tmp_path, True)
