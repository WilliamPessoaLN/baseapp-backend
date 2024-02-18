from graphene_django.filter import DjangoFilterConnectionField

from .object_types import FileNode


class FilesQueries:  
    my_files = DjangoFilterConnectionField(FileNode)
