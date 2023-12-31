﻿# FastAPI online shop

**Backend for an online store.** It was made to learn the basics of the backend developing.
Implemented custom authentication, database migrations and unit tests for each endpoint

## Installation 
To install and set up the project, follow these steps:

1. Make sure that python is installed on your computer

2. Clone the repository:
```bash
git clone https://github.com/Amir23714/fastapi_online_shop.git
```

3. Navigate to the project directory:
```bash
cd fastapi_online_shop
```

4. Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```
5. Create .env file with all neccessary variables.

### Alembic configuration
6. Initialize alembic migrations

```bash
alembic init migrations
```

7. In file alembic.ini update value of variable **sqlalchemy.url** to your url to database
8. In file migrations/env.py update row **target_metadata = None** with:
```bash
from models.models import Base
target_metadata = Base.metadata
```

9. Run
```bash
alembic revision --autogenerate
alembic upgrade head
```

10. Configure root directory

### Windows
```bash
set PYTHONPATH=.
```

### Linux
```bash
export PYTHONPATH=.
```

11. Start the server using the following command:
```bash
uvicorn main:app --reload      
```

