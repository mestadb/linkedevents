# -*- coding: utf-8 -*-

# django
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.reverse import reverse


# 3rd party
import pytest
from rest_framework.test import APIClient

# events 
from events.models import (
    DataSource, Organization, Place, Language, Keyword, KeywordLabel
)
from events.api import (
    KeywordSerializer, PlaceSerializer, SYSTEM_DATA_SOURCE_ID
)


TEXT = 'testing'
URL = "http://localhost"
DATETIME = timezone.now().isoformat()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
@pytest.fixture
def data_source():
    return DataSource.objects.create(id=SYSTEM_DATA_SOURCE_ID)


@pytest.mark.django_db
@pytest.fixture
def user():
    return get_user_model().objects.create(
        username='test_user',
        first_name='Cem',
        last_name='Kaner',
        email='cem@kaner.com'
    )


@pytest.mark.django_db
@pytest.fixture
def organization(data_source, user):
    org = Organization.objects.create(
        id='test_organization',
        data_source=data_source
    )
    org.admin_users.add(user)
    org.save()
    return org


@pytest.mark.django_db
@pytest.fixture
def minimal_event_dict(data_source, organization):
    return {
        'publisher': organization.id,
        'name': {'fi': 'minimal_event'},
        'event_status': 'EventScheduled',
        'external_links': [],
        'offers': [],
    }


@pytest.mark.django_db
@pytest.fixture
def place(data_source, organization):
    return Place.objects.create(
        id='test location',
         data_source=data_source,
         publisher=organization
    )


@pytest.mark.django_db
@pytest.fixture
def location_id(place):
    obj_id = reverse(PlaceSerializer().view_name, kwargs={'pk': place.id})
    return 'http://testserver%s' % obj_id


@pytest.mark.django_db
@pytest.fixture
def keyword(data_source, kw_name):
    lang_objs = [
        Language.objects.get_or_create(id=lang)[0]
        for lang in ['fi', 'sv', 'en']
    ]

    labels = [
        KeywordLabel.objects.create(
            name='%s%s' % (kw_name, lang.id),
            language=lang
        )
        for lang in lang_objs
    ]

    obj = Keyword.objects.create(
        id=kw_name,
        name=kw_name,
        data_source=data_source
    )
    for label in labels:
        obj.alt_labels.add(label)
    obj.save()

    return obj



@pytest.mark.django_db
@pytest.fixture
def keyword_id(data_source, kw_name):
    obj = keyword(data_source, kw_name)
    obj_id = reverse(KeywordSerializer().view_name, kwargs={'pk': obj.id})
    return 'http://testserver%s' % obj_id


@pytest.mark.django_db
@pytest.fixture
def complex_event_dict(data_source, organization, location_id):
    return {
        'publisher': organization.id,
        'name': {'fi': 'complex_event'},
        'name': {'en': TEXT, 'sv': TEXT, 'fi': TEXT},
        'event_status': 'EventScheduled',
        'location': {'@id': location_id},
        'keywords': [
            {'@id': keyword_id(data_source, 'simple')},
            {'@id': keyword_id(data_source, 'test')},
            {'@id': keyword_id(data_source, 'keyword')},
        ],
        'external_links': [
            {'name': TEXT, 'link': URL, 'language': 'fi'},
            {'name': TEXT, 'link': URL, 'language': 'sv'},
            {'name': TEXT, 'link': URL, 'language': 'en'},
        ],
        'offers': [
            {
                'is_free': False,
                'price': {'en': TEXT, 'sv': TEXT, 'fi': TEXT},
                'description': {'en': TEXT, 'sv': TEXT, 'fi': TEXT},
                'info_url': {'en': URL, 'sv': URL, 'fi': URL}
            }
        ],
        'custom_data': {'my': 'data', 'your': 'data'},
        'image': URL,
        'origin_id': TEXT,
        'date_published': DATETIME,
        'start_time': DATETIME,
        'end_time': DATETIME,
        'audience': TEXT,
        'location_extra_info': {'fi': TEXT},
        'info_url': {'en': URL, 'sv': URL, 'fi': URL},
        'secondary_headline': {'en': TEXT, 'sv': TEXT, 'fi': TEXT},
        'description': {'en': TEXT, 'sv': TEXT, 'fi': TEXT},
        'headline': {'en': TEXT, 'sv': TEXT, 'fi': TEXT},
        'short_description': {'en': TEXT, 'sv': TEXT, 'fi': TEXT},
        'provider': {'en': TEXT, 'sv': TEXT, 'fi': TEXT},
    }
    return {
    }
