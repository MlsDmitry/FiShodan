# -*- coding: utf-8 -*-

#importing libraries
from sklearn.externals import joblib
from . import inputScript
from bs4 import BeautifulSoup, NavigableString
from celery import Celery
import os
import requests

NOT_TRUSTED_CA = ["Let's Encrypt Authority X3"]
#load the pickle file
classifier = joblib.load('rpadml/final_models/rf_final.pkl')

#input url
celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379")


class CTLog:
    def __init__(
        self, _id, logget_at, not_before, not_after, matching_ident, issuer_name
    ):
        self._id = _id
        self.logget_at = logget_at
        self.not_before = not_before
        self.not_after = not_after
        self.matching_ident = matching_ident
        self.issuer_name = issuer_name


@celery.task()
def verify_domain(domain):
    response = {}
    d = Domain(domain)
    checkprediction = inputScript.main(domain)
    prediction = classifier.predict(checkprediction)
    print(prediction)
    return True


class Domain:

    def __init__(self, domain):
        self.domain = domain
        self.pages = {}

    def whois(self):
        pass
        # data = query(self.domain)
        # return data

    def lookup(self):
        dns.resolver.query(self.domain)

    def extract_tld(self):
        tld = tldextract.extract(self.domain)
        return tld

    def check_certificate(self) -> bool:
        if '/' not in self.pages:
            try:
                html_text = requests.get(self.domain).text
            except Exception as e:
                print("Cannot fetch data from {url}")
                return False

        soup = BeautifulSoup(html_text, "html.parser")

        collected_logs = []
        for table in soup.find_all("table")[1]:
            if isinstance(table, NavigableString):
                continue

            for table_row in table.find_all("tr")[1:]:
                tds = [td for td in table_row.find_all("td")]
                try:
                    collected_logs.append(
                        CTLog(
                            tds[0].text,
                            tds[1].text,
                            tds[2].text,
                            tds[3].text,
                            [x for x in tds[4] if isinstance(x, NavigableString)],
                            tds[5].text,
                        )
                    )
                except Exception as e:
                    print(f"Could not retreive CT logs from {self.domain}, {e}")
                    return False

        for ca in NOT_TRUSTED_CA:
            for ctlog in collected_logs:
                if self.domain in ctlog.matching_ident:  # checking domain matching
                    if ca in ctlog.issuer_name:  # checking CA
                        return False

        if not collected_logs:
            return False

        return True

    
    
# #checking and predicting
# checkprediction = inputScript.main(url)
# prediction = classifier.predict(checkprediction)

# print(prediction)

# x = prediction.tolist()
#print(type(prediction))
