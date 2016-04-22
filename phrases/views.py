from django.shortcuts import render

# Create your views here.

from rest_framework import routers, serializers, viewsets
from rest_framework.authentication import BasicAuthentication
# api views

from rest_framework.authentication import SessionAuthentication
import models
import datetime

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

# Serializers define the API representation.
class PhraseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Phrase
        fields = ('id', 'phrase', 'translated', 'comment', 'created_at', 'updated_at')

# ViewSets define the view behavior.
class PhraseViewSet(viewsets.ModelViewSet):
    authentication_classes=(CsrfExemptSessionAuthentication,BasicAuthentication)
    tc = datetime.datetime.now()+datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=13, weeks=0)
    queryset = models.Phrase.objects.filter(updated_at__isnull=False, updated_at__month = tc.month, updated_at__day = tc.day).order_by('updated_at')
    serializer_class = PhraseSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'phrases', PhraseViewSet)
