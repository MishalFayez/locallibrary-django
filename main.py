import flet
from flet import Page, Text, TextField, FloatingActionButton, Column, WEB_BROWSER, app
import requests

tf = TextField(hint_text="give some text")
def main(page: Page):

    def get(e):
        r = requests.get("http://127.0.0.1:8000/api/book/").json()
        for i in range(len(r)):
            page.add(Text(r[i]['title']))

        page.update()

    def post(e):
        requests.post("http://127.0.0.1:8000/api/book/add/", data={'title':str(tf.value)})


    page.add(
        Column(controls= [
            tf,
            FloatingActionButton(text='get', on_click=get),
            FloatingActionButton(text='post', on_click=post)
        ])
    )

app(target=main, view=WEB_BROWSER)