import re
from datetime import timedelta
from urllib.parse import parse_qs, urlparse

import archieml
from allauth.socialaccount.models import SocialToken
from bleach.sanitizer import Cleaner
from django.conf import settings
from django.utils import timezone
from html5lib.filters.base import Filter
from requests_oauthlib import OAuth2Session

from .constants import *


def add_to_repo_folder(session, package):
    payload = {
        "id": settings.REPOSITORY_FOLDER_ID
    }
    res = session.post(GOOGLE_API_PREFIX + "/v2/files/" + package.drive_folder_id + "/parents", json=payload)
    return res.json()

def get_file(session, file_id, download=False):
    res = session.get(GOOGLE_API_PREFIX + "/v2/files/" + file_id + ("?alt=media" if download else ""), stream=download)
    res.raise_for_status()
    if download:
        # Returns the requests object
        return res
    else:
        return res.json()

def list_folder(session, package):
    text = "### No article document was found in this package!\n"
    images = []

    payload = {
        "q": "'%s' in parents" % package.drive_folder_id,
        "maxResults": 1000
    }
    # we assume there's always less than 100 files in a package. change this if assumption untrue

    def img_check(item: dict):
        valid_extensions = [".jpeg", ".png", ".jpg", ".gif", ".webp"]
        for ext in valid_extensions:
            if ext in item["title"].lower():
                return True
        return False

    res = session.get(GOOGLE_API_PREFIX + "/v2/files", params=payload)
    items = res.json()['items']
    article = list(filter(lambda f: "article" in f['title'], items))
    data_files = list(filter(lambda f: ".aml" in f['title'], items))
    images = list(filter(img_check, items))
    folders = list(filter(lambda f: f["mimeType"] == "application/vnd.google-apps.folder", items))
    #print("RES:")
    #print(article)
    #print(images)

    aml_data = {}

    # adds title of article as key, and parsed data as value. Saves info to aml_data

    for aml in data_files:
        if aml['mimeType'] != "application/vnd.google-apps.document":
            # if the mimetype is not a google docs file, we can only treat it as plaintext
            req = get_file(session, aml['id'], download=True)
            aml_text = req.content.decode('utf-8')
        else:
            if package.content_type == HTML:

                def check_span(tag, name, value):
                    print(tag, name, value)

                data = session.get(GOOGLE_API_PREFIX + "/v2/files/" + aml['id'] + "/export", params={"mimeType":"text/html"})
                #aml_content = data.content.decode('utf-8')
                aml_content = data.text
                aml_text = googleDocHTMLCleaner.clean(aml_content)
            else:
                data = session.get(GOOGLE_API_PREFIX + "/v2/files/" + aml['id'] + "/export", params={"mimeType": "text/plain"})
                aml_text = data.content.decode('utf-8')
        #print("IN ARCHIEML ")
        aml_content = archieml.loads(aml_text)
        
        # HACK: Fixes a bad bug in the archieml parser
        for key, value in aml_content.items():
            if isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, dict):
                        if item.get("type") is None and item.get("value") and isinstance(value[index-1], dict) and value[index-1].get("type"):
                            aml_content[key][index-1]["value"] = item["value"]
                            aml_content[key][index] = None
                aml_content[key] = [ i for i in aml_content[key] if i is not None ]

        aml_data[aml['title']] = aml_content

    # only taking the first one - assuming there's only one article file

    if len(article) >= 1:
        if article[0]['mimeType'] != "application/vnd.google-apps.document":
            req = get_file(session, article[0]['id'], download=True)
            text = req.content.decode('utf-8')
        else:
            data = session.get(GOOGLE_API_PREFIX + "/v2/files/" + article[0]['id'] + "/export", params={"mimeType": "text/plain"})
            text = data.content.decode('utf-8')
        # fix indentation for yaml
        text = text.replace("\t", "  ")
    # this will take REALLY long.

    # return everything
    return text, images, folders, aml_data

def create_package(session, package, existing=False):
    payload = {
        'parents': [{'id': settings.REPOSITORY_FOLDER_ID}],
        'title': package.slug,
        'description': package.description,
        'mimeType': "application/vnd.google-apps.folder"
    }

    res = session.post(GOOGLE_API_PREFIX + "/v2/files", json=payload)
    folder_resource = res.json()

    file_payload = {
        'parents': [{'id': folder_resource['id']}],
        'title': "article.md",
        'description': "Article data",
        'mimeType': "application/vnd.google-apps.document"
    }
    session.post(GOOGLE_API_PREFIX + "/v2/files", json=file_payload)

    return (folder_resource['alternateLink'], folder_resource['id'])


# https://github.com/pennersr/django-allauth/issues/420
def get_oauth2_session(user) -> OAuth2Session:
    """ Create OAuth2 session which autoupdates the access token if it has expired """

    refresh_token_url = "https://accounts.google.com/o/oauth2/token"

    social_token = SocialToken.objects.get(account__user=user, account__provider='google')

    def token_updater(token):
        social_token.token = token['access_token']
        social_token.token_secret = token['refresh_token']
        social_token.expires_at = timezone.now() + timedelta(seconds=int(token['expires_in']))
        social_token.save()

    client_id = social_token.app.client_id
    client_secret = social_token.app.secret

    extra = {
        'client_id': client_id,
        'client_secret': client_secret
    }

    expires_in = (social_token.expires_at - timezone.now()).total_seconds()
    token = {
        'access_token': social_token.token,
        'refresh_token': social_token.token_secret,
        'token_type': 'Bearer',
        'expires_in': expires_in  # Important otherwise the token update doesn't get triggered.
    }

    return OAuth2Session(client_id, token=token, auto_refresh_kwargs=extra,
                         auto_refresh_url=refresh_token_url, token_updater=token_updater)

### Additional Modifiers for Cleaning HTML

TAGS = ['a', 'p', 'span', 'em', 'strong']
ATTRS = {
    'span': ['style'],
    'a': ['href']
}
STYLES = ['font-weight', 'font-style', 'text-decoration']

class KeepOnlyInterestingSpans(Filter):
    drop_next_close = False
    
    def _style_is_boring(self, prop, value):
        boring_styles = {
            'font-weight': ['400', 'normal'],
            'text-decoration': ['none'],
            'font-style': ['normal']
        }
        
        return value in boring_styles.get(prop, [])
    
    def _reduce_to_interesting_styles(self, token):
        styles = token['data'].get((None,'style'))
        if styles is not None:
            final_styles = ''
            for prop, value in re.findall(r"([-\w]+)\s*:\s*([^:;]*)", styles):
                if not self._style_is_boring(prop, value):
                    final_styles += '%s:%s;' % (prop, value)
            token['data'][(None, 'style')] = final_styles
            return final_styles
        return ''
    
    def __iter__(self):
        for token in Filter.__iter__(self):
            if token['type'] == 'StartTag' and token['name'] == 'span':
                if not token['data']:
                    drop_next_close = True
                    continue

                reduced_styles = self._reduce_to_interesting_styles(token)
                #print("final:", token)
                if reduced_styles == '':
                    drop_next_close = True
                    continue
            elif token['type'] == 'EndTag' and token['name'] == 'span' and drop_next_close:
                drop_next_close = False
                continue
            yield(token)
            
            
class ConvertPTagsToNewlines(Filter):
    
    NEWLINE_TOKEN = {
        'type': "Characters" ,
        'data': "\n"
    }
    
    def __iter__(self):
        for token in Filter.__iter__(self):
            if token['type'] == 'StartTag' and token['name'] == 'p':
                continue
            elif token['type'] == 'EndTag' and token['name'] == 'p':
                yield(self.NEWLINE_TOKEN)
                continue
            yield(token)

            
class RemoveGoogleTrackingFromHrefs(Filter):
    
    def __iter__(self):
        for token in Filter.__iter__(self):
            if token['type'] == 'StartTag' and token['name'] == 'a' and token['data']:
                url = token['data'].get((None, 'href'))
                if url is not None:
                    actual_url = parse_qs(urlparse(url).query).get('q')
                    if actual_url is not None and len(actual_url) > 0:
                        token['data'][(None, 'href')] = actual_url[0]
            yield(token)

googleDocHTMLCleaner = Cleaner(tags=TAGS,
                  attributes=ATTRS,
                  styles=STYLES,
                  strip=True,
                  filters=[KeepOnlyInterestingSpans, ConvertPTagsToNewlines, RemoveGoogleTrackingFromHrefs])
