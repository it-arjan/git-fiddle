import requests
import sys
import json
import inspect
import simple_log

API_BASE_URL = 'http://localhost:6600/api/prices'


class JsonSerializable(object):

    def serialize(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.serialize()

    @staticmethod
    def dumper(obj):
        if "serialize" in dir(obj):
            return obj.serialize()

        return obj.__dict__


class Orderline(JsonSerializable):
    def __init__(self, EanArticle, UnitPrice):
        self.EanArticle = EanArticle
        self.UnitPrice = UnitPrice

    def default(self, o):
        return o.__dict__


def current_function_name():
    return sys._getframe(1).f_code.co_name


def ttest_refprice_get():
    logger = simple_log.get_log()
    resp = requests.get(f"{API_BASE_URL}/some_fake_ean/23")
    assert resp.status_code == 200 or resp.status_code == 404, 'HTTP response should return OK or notfount'
    # print("api result: {}"  form  at(resp.status_code))
    logger.info(
        f"{current_function_name()}: result code={resp.status_code}.")

    if (resp.status_code == 200):
        assert resp.content != None, "response should have content"
        try:
            obj = json.loads(resp.content)
        except json.decoder.JSONDecodeError:  # this does not prevent pytest from throwing an error
            assert False, 'response is not json'
        except:
            assert False, 'error converting json response, but not JSONDecodeError'
        else:
            assert 'ean_article' in obj and 'adjusted_price' in obj, "get should return object containing ean_article and adjusted_price"
            assert obj['ean_article'] == 'some_fake_ean', 'ean_article not correct'
            assert obj['adjusted_price'] == 22 or obj['adjusted_price'] == 24, 'unexpected adjusted_price'


def ttest_refprice_post_without_content():
    data = None
    logger = simple_log.get_log()
    resp = requests.post(f'{API_BASE_URL}', data=data)

    assert resp.status_code == 400, 'post without content should return badrequest'
    assert resp.content != None, "response should have content"

    obj = json.loads(resp.content)

    assert 'Message' in obj, "post without content should return obj containing Message"
    assert obj['Message'] == 'Please provide a list of orderlines.', 'wrong message'

    logger.info(f"{current_function_name()} result code:{resp.status_code}.")


def test_refprice_post_with_content():
    data = []
    # TODO check python object json serialization internals
    #data.append(Orderline('one', 11))
    #data.append(Orderline('two', 22))

    data.append({'EanArticle': 'two', 'UnitPrice': 22})
    data.append({'EanArticle': 'one', 'UnitPrice': 11})

    jsonstr = json.dumps(data)
    logger = simple_log.get_log()
    headers = {'content-type': 'application/json'}
    resp = requests.post(f'{API_BASE_URL}', data=jsonstr, headers=headers)
    assert resp.status_code == 200, 'HTTP response should return 200 OK'
    logger.info(f"{current_function_name()} result code:{resp.status_code}.")
    assert resp.content != None, "response should have content"
    obj = json.loads(resp.content)
    # logger.info(obj)

    assert obj == [] or obj == [{'ean_article': 'one', 'adjusted_price': 10.0}] or obj == [
        {'ean_article': 'one', 'adjusted_price': 12.0}] or obj == [{'ean_article': 'two', 'adjusted_price': 23.0}] or obj == [
        {'ean_article': 'two', 'adjusted_price': 21.0}]
