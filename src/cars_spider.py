from bs4 import BeautifulSoup
import requests
import json
import re


def get_content_by_class(content, class_text):
    """
    Some car pages may have empty values.
    :param content: content (Element)
    :param class_text: class attribute for searching
    :return: None or Element
    """
    try:
        return content.find_all(class_=class_text)[0]
    except IndexError:
        return None


def get_info_from_list(args):
    """
    Get one car information
    :param args: args for multiprocessing
                batch_index: the car_id of the batch. This is used for file name
                index_list:
    :return:
    """

    # TODO(tuosun): use more user agent.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/'
                      '605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    }

    batch_index, car_id_list = args
    print(batch_index, 'start')

    # all of the following three dictionaries will be saved into json files.
    outputs = dict()
    key_vin = dict()
    key_position = dict()

    for i, car_id in enumerate(car_id_list):
        if i % 10 == 0:
            print(batch_index, ':', i)
        url = 'https://www.cars.com/vehicledetail/detail/{car_id}/overview/'.format(car_id=car_id)
        response = requests.get(url, timeout=30, headers=headers).content
        soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')
        content = soup.html

        # title miles price
        title = get_content_by_class(content, 'cui-heading-2--secondary vehicle-info__title')
        if title:
            title = title.text
        odometer = get_content_by_class(content, 'vdp-cap-price__mileage--mobile vehicle-info__mileage mileage_margin')
        if odometer:
            odometer = odometer.text
        price = get_content_by_class(content, 'vehicle-info__price-display vehicle-info__price-display--dealer cui-heading-2')
        if price:
            price = price.text
        vehicle_head_info_json = {
            'title': title,
            'odometer': odometer,
            'price': price
        }

        # sell name rating review position
        seller_name = get_content_by_class(content, 'page-section__title page-section__title--dealer-name cui-heading-6')
        if seller_name:
            seller_name = seller_name.text
        seller_rateing = get_content_by_class(content, 'rating__link rating__link--has-reviews')
        if seller_rateing:
            seller_rateing=seller_rateing.contents[0][1:4]

        seller_reviews_count = get_content_by_class(content, 'rating__link--has-reviews-count')
        if seller_reviews_count:
            seller_reviews_count = seller_reviews_count.text

        seller_position = get_content_by_class(content, 'get-directions-link seller-details-location__text')
        if seller_position:
            seller_position = seller_position.a.text.replace(' ', '').replace('\n', '').replace('\xa0', '')

        seller_notes = get_content_by_class(content, 'seller-notes')
        if seller_notes:
            seller_notes = seller_notes.get('srcdoc')
        if seller_notes:
            seller_notes = re.search(r"(?is)(?<=</body>).*(?=</div>)", seller_notes).group(0)
        seller_info_json = {
            'seller_name': seller_name,
            'seller_rateing': seller_rateing,
            'seller_reviews_count': seller_reviews_count,
            'seller_position': seller_position,
            'seller_notes': seller_notes,
        }

        # car basic info
        basics_json = dict()
        basics = content.find_all(class_='vdp-details-basics__list')[0]
        for i in range(1, len(basics), 2):
            li = basics.contents[i]
            basics_json[li.strong.text[:-1]] = li.span.text

        # features string list
        all_features_list = list()
        all_features = get_content_by_class(content, 'vdp-details-basics__features-list')
        if all_features:
            for i in range(1, len(all_features), 2):
                all_features_list.append(all_features.contents[i].text)

        # extract key from car.com url
        # two possible id formats are found.
        try:
            key_value = re.search(r".*detail/(\d{9})", url).group(1)
        except AttributeError:
            key_value = re.search(r".*detail/(\d{8})", url).group(1)

        outputs[key_value] = {
            'vehicle_head_info': vehicle_head_info_json,
            'seller_info': seller_info_json,
            'basics': basics_json,
            'all_features': all_features_list,
        }

        key_vin[key_value] = basics_json.get("VIN")
        key_position[key_value] = seller_position

    # TODO(tuosun): replace saving directory.
    with open('car_data/cars_{batch_index}.json'.format(batch_index=batch_index), 'w') as f:
        f.write(json.dumps(outputs, indent=1))
    with open('car_data/key_vin_{batch_index}.json'.format(batch_index=batch_index), 'w') as f:
        f.write(json.dumps(key_vin, indent=1))
    with open('car_data/key_position_{batch_index}.json'.format(batch_index=batch_index), 'w') as f:
        f.write(json.dumps(key_position, indent=1))


# TODO(tuosun): there must be some api to achieve this function
def split_list(one_list, batch_size):
    """
    TODO(tuosun): try a iteration or a generator to replace it
    Separate car id lists into batches, which are designed for assigning tasks to concurrent crawlers
    :param one_list: a list of numbers
    :param batch_size: the size of the batches
    :return: a list of lists of separated one_list. Each elements is one task for one process.
    """
    batches = list()
    for i in range(0, len(one_list), batch_size):
        batches.append(tuple([i, one_list[i:i + batch_size]]))
    return batches
