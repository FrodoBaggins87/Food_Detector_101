name: Deploy to Heroku

on:
  push:
    branches:
      - main  # Change to your default branch if different

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Heroku Container Registry
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
        run: |
          echo "$HEROKU_API_KEY" | docker login --username=_ --password-stdin registry.heroku.com

      - name: Build, push and release Docker container
        env:
          HEROKU_APP_NAME: ${{ secrets.HEROKU_APP_NAME }}
        run: |
          docker build -t registry.heroku.com/${{ secrets.HEROKU_APP_NAME }}/web .
          docker push registry.heroku.com/${{ secrets.HEROKU_APP_NAME }}/web
          heroku container:release web --app ${{ secrets.HEROKU_APP_NAME }}

      - name: Deploy application
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
          HEROKU_APP_NAME: ${{ secrets.HEROKU_APP_NAME }}
        run: heroku ps:scale web=1 --app ${{ secrets.HEROKU_APP_NAME }}
