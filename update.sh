curl localhost:5000/stopServer
cd /flask-playground/
git config --global --add safe.directory /flask-playground
sudo git pull
source venv/bin/activate
export AWS_DEFAULT_REGION=eu-central-1
flask run --debug --host=0.0.0.0 --port=5000
