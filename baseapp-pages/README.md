# BaseApp Page

Reusable app to handle pages, URL's paths and metadata. It provides useful models and GraphQL Interfaces.

## How to install:

Add dependencies to your `requirements/base.txt` file:

```
baseapp-pages
```

And run provision or manually `pip install -r requirements/base.ext`

If you want to develop, [install using this other guide](#how-to-develop).

## How to use

Add `modeltranslation` to the beginning of `INSTALLED_APPS`.

Add `baseapp_pages` to your project's `INSTALLED_APPS` and run `./manage.py migrate` as any other django model.

Expose `PagesMutations` and `PagesQuery` in your GraphQL/graphene endpoint, like:

```python
from baseapp_pages.graphql.mutations import PagesMutations
from baseapp_pages.graphql.queries import PagesQuery

class Query(graphene.ObjectType, PagesQuery):
    pass

class Mutation(graphene.ObjectType, PagesMutations):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
```

This will expose `urlPath` and `page` query.

### `urlPath` query:

Example:

```graphql
{
    urlPath(path: '/about') {
        path
        language
        target {
          metaTitle
        }
    }
}
```

## How to to customize the Page model

In some cases you may need to extend Page model, and we can do it following the next steps:

Start by creating a barebones django app:

```
mkdir my_project/pages
touch my_project/pages/__init__.py
touch my_project/pages/models.py
```

Your `models.py` will look something like this:

```python
from django.db import models
from django.utils.translation import gettext_lazy as _

from baseapp_pages.models import AbstractBasePage

class Page(AbstractBasePage):
    custom_field = models.CharField(null=True)

    class PageTypes(models.IntegerChoices):
        LIKE = 1, _("like")
        DISLIKE = -1, _("dislike")

        @property
        def description(self):
            return self.label
```

Now make your to add your new app to your `INSTALLED_APPS` and run `makemigrations` and `migrate` like any normal django app.

Now in your `settings/base.py` make sure to tell baseapp-pages what is your custom model for Page:

```python
BASEAPP_REACTIONS_REACTION_MODEL = 'pages.Page'
```

## Writing test cases in your project

There is a `AbstractPageFactory` which helps you write other factories:

```
import factory
from baseapp_pages.tests.factories import AbstractPageFactory

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "comments.Comment"


class CommentPageFactory(AbstractPageFactory):
    target = factory.SubFactory(CommentFactory)

    class Meta:
        model = "baseapp_pages.Page"
        # OR if you have a custom model, point to it:
        model = "pages.Page"
```

In the above example we have a easy way to make pages to any comment into the database for testing proporses using `CommentPageFactory`.

## How to develop

Clone the project inside your project's backend dir:

```
git clone git@github.com:silverlogic/baseapp-backend.git
```

And manually install the package:

```
pip install -e baseapp-backend/baseapp-pages
```

The `-e` flag will make it like any change you make in the cloned repo files will effect into the project.