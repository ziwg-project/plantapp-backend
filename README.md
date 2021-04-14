# plantapp-backend

## Getting started
### Local development
1. Clone repository `git clone https://github.com/ziwg-project/plantapp-backend.git`
2. Change working directory `cd plantapp-backend`
3. Create virtual environment `python3 -m venv venv`
4. Activate virtual environment `source venv/bin/activate`
5. Install dependencies `pip install -r requirements.txt`
6. Start application `python manage.py runserver`

### Running inside docker containers
#### Prerequisites
* docker
* docker-compose
#### Instructions
1. Clone repository `git clone https://github.com/ziwg-project/plantapp-backend.git`
2. Change working directory `cd plantapp-backend`
3. Build and start docker containers `docker-compose up -d`
