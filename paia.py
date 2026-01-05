from requests import get, post
from requests_oauthlib import OAuth1
from time import sleep
from schedule import every, run_pending
from logging import basicConfig, info
from configparser import ConfigParser
from argparse import ArgumentParser
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live


class Retweeter:
    def __init__(self, query, lang):
        self.full_query = f"{query} lang:{lang}" if lang else query

        config = ConfigParser(interpolation=None)
        config.read("auth.conf")

        self.consumer_key = config["twitter"]["consumer_key"]
        self.consumer_secret = config["twitter"]["consumer_secret"]
        self.access_token = config["twitter"]["access_token"]
        self.access_secret = config["twitter"]["access_secret"]
        self.bearer = config["twitter"]["bearer_token"]
        self.user_id = config["twitter"]["userid"]

        self.auth = OAuth1(
            self.consumer_key,
            self.consumer_secret,
            self.access_token,
            self.access_secret
        )

        self.console = Console()
        self.tweets_pendentes = []

    def buscar(self):
        url = (
            "https://api.x.com/2/tweets/search/recent"
            f"?query={self.full_query}"
            "&tweet.fields=id,author_id,text,lang,created_at"
            "&max_results=10"
        )

        headers = {"Authorization": f"Bearer {self.bearer}"}
        r = get(url, headers=headers)

        if r.status_code != 200:
            self.console.print(f"[red]erro busca: {r.status_code} {r.text}")
            return

        tweets = r.json().get("data", [])
        if not tweets:
            self.console.print(f"[yellow]nenhum tweet encontrado para: {self.full_query}")
            return

        self.tweets_pendentes = tweets

    def retweetar(self):
        if not self.tweets_pendentes:
            self.buscar()
            if not self.tweets_pendentes:
                return

        tweet = self.tweets_pendentes.pop(0)
        tweet_id = tweet["id"]
        autor = tweet["author_id"]
        texto = tweet["text"]

        try:
            rt_url = f"https://api.x.com/2/users/{self.user_id}/retweets"
            resp = post(rt_url, auth=self.auth, json={"tweet_id": tweet_id})

            self.console.print(f"[cyan]retweet resp: {resp.status_code} {resp.text}")

            if resp.status_code in [200, 201]:
                info(f"@{autor} tweet: '{texto}' retweetado")
                self.console.print(f"[green]@{autor} retweetado")

        except Exception:
            sleep(60)

basicConfig(filename='paia.log', level=10, format='%(asctime)s %(message)s')

parser = ArgumentParser()
parser.add_argument("--query", required=True)
parser.add_argument("--lang")
args = parser.parse_args()

bot = Retweeter(args.query, args.lang)

every(9).hours.do(bot.retweetar)

if __name__ == "__main__":
    bot.retweetar()

    spinner = Spinner("dots")
    with Live(spinner, refresh_per_second=12):
        while True:
            spinner.text = f"aguardando agendamento... query: {bot.full_query}"
            run_pending()
            sleep(30)