from rest_framework import serializers,viewsets
from rest_framework.decorators import list_route

from django.shortcuts import get_object_or_404
from django.db.models import Count, Case, When, CharField
from miller.api.serializers import AuthorSerializer, LiteAuthorSerializer
from miller.api.utils import Glue
from miller.models import Author, Story

from rest_framework.response import Response


class AuthorViewSet(viewsets.ModelViewSet):
  """
  Author view set api.
  Author request can be handled in two ways: with an author ID, 
  useful for updating etc.. or with 
  the user username. In this case, since we can have multiple 
  authors identities per user, we provide aliases. Cfr api.serializers.AuthorWithAliasesSerializer

  """
  queryset = Author.objects.all()
  serializer_class = AuthorSerializer
  list_serializer_class = LiteAuthorSerializer
  # lookup_field = 'pk'
  # lookup_value_regex = '[0-9a-zA-Z\.-_]+'

  def _getAuthorizedQueryset(self, request):
    if request.user.is_staff:
      q = Author.objects.all()
    elif request.user.is_authenticated():
      q = Story.objects.filter(Q(owner=request.user) | Q(status=Story.PUBLIC) | Q(authors__user=request.user)).distinct()
    else:
      q = Author.objects.filter(status=Story.PUBLIC)
    return q


  def list(self, request):
    # authors = self.queryset.annotate(num_stories=Count(Case(
    #     When(stories__status=Story.PUBLIC, then=1),
    #     output_field=CharField(),
    # ),distinct=True))

    authors = self.queryset.distinct()

    g = Glue(request=request, queryset=authors, extra_ordering=['num_stories', 'stories__date_last_modified'])

    page    = self.paginate_queryset(g.queryset)
    #print g.queryset.query
    serializer = self.list_serializer_class(page, many=True, context={'request': request})
    return self.get_paginated_response(serializer.data)
# def list(self, request):
#     authors = self.queryset.annotate(num_stories=Count('stories', distinct=True))
#     g = Glue(request=request, queryset=authors, extra_ordering=['num_stories'])
#     page    = self.paginate_queryset(g.queryset)
#     serializer = self.list_serializer_class(page, many=True, context={'request': request})
#     return self.get_paginated_response(serializer.data)

  def retrieve(self, request, *args, **kwargs):
    if 'pk' in kwargs and not kwargs['pk'].isdigit():
      # by author.slug
      author = get_object_or_404(Author, slug=kwargs['pk'])
    else:
      # by author.pk
      author = get_object_or_404(Author, pk=kwargs['pk'])
    
    serializer = AuthorSerializer(author, context={'request': request})
    return Response(serializer.data)


  @list_route(methods=['get'])
  def hallOfFame(self, request):
    stories = Story.objects.all()
    if not request.user.is_staff:
      stories = stories.filter(status=Story.PUBLIC)

    g = Glue(queryset=stories, request=request)
    
    
    # print g.filters, g.filtersWaterfall

    ids = g.queryset.values('pk')
    
    # top n authors, per story filters.
    top_authors = Author.objects.filter(stories__pk__in=[s['pk'] for s in ids]).annotate(
      num_stories=Count('stories', distinct=True)
    ).order_by('-num_stories')
    
    page    = self.paginate_queryset(top_authors)
    serializer = LiteAuthorSerializer(page, many=True, context={'request': request})
    return self.get_paginated_response(serializer.data)


