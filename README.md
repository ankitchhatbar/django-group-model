# Django Custom Group Model

## Overview

Django Custom Group Model is a package that allows you to replace the default Django Group model with a custom one with full compatibility with the Django permissions framework.

Here are some reasons why you may want to use this package:

- Add more fields to the Django Group model

- Override existing Django Group model fields

- Rename the Group model to something else

- When starting a project, setting a custom Group model will allow you to customize it in the future when the need arises.

## Requirements

- Python: 3.6+

- Django: 3.0+

## Installation

Install using pip:

```bash
pip install django-group-model
```

Add `'django_group_model'`  to your `INSTALLED_APPS`. Make sure to place it before any apps that define the `Group` or `User` models.

```python
INSTALLED_APPS = [
    ...
    'django_group_model',
]
```

## Usage

### Overriding the default Group model

`django-group-model` allows overriding the `Group` model by setting the `AUTH_GROUP_MODEL` setting to a value that references a custom model.

```python
AUTH_GROUP_MODEL = 'myapp.Group'
```

The below model is identical to the default `Group` model from `django.contrib.auth.models`, but allows customizing in the future.

```python
from django_group_model.models import AbstractGroup


class Group(AbstractGroup):
    # You can add custom fields here
    pass
```

Here, the name of the class being `Group` is important. See below on how to customize the name of the model. In order to use this, set the `AUTH_GROUP_MODEL` setting in your `settings.py` to point to your custom `Group` model.

In your custom `User` model (see [Customizing authentication in Django](https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#substituting-a-custom-user-model)), set a field to point to your custom `Group` model

```python
...

class User(AbstractUser, ...):
    ...
    groups = models.ManyToManyField(
        'myapp.Group',
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",

    )
    ...
```

Once again, the name of the field is important. See below on how to customize the name of the model. Also take note of the `related_name` and `related_query_name`. Most of the time, the pattern shown above should work. For a deeper understanding see [Django docs here](https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.ForeignKey.related_name).

### Customizing the name of the Group model

Overriding the default `Group` model with a custom name involves 2 steps:

1. Create a model class that extends `AbstractGroup` with any name that you like.

2. Override `verbose_name` and `verbose_name_plural` attributes of the `Meta` class. 

Let's go through this with an example. We'll override the default `Group` model with a model called `Role` in this example. But you could call it whatever you like.

First we will create a `Role` model that extends `AbstractUser`

```python
from django_group_model.models import AbstractGroup


class Role(AbstractGroup):
    # You can add custom fields here

    class Meta:
        verbose_name = "role"
        verbose_name_plual = "roles"
```

Next, we'll use it in our user class.

```python
...

class User(AbstractUser, ...):
    ...
    roles = models.ManyToManyField(
        'myapp.Role',
        blank=True,
        related_name="user_set",
        related_query_name="user",
    )
    groups = None
    ...
```

**IMPORTANT: The name of the field must be the name of your <nobr>custom model in lowercase + 's'.</nobr>** So, the `Role` model becomes `roles`. This is a limitation at this point. Feel free to open an issue and a pull request with ideas to resolve this (see the contributing section below).

**Note:** Here we are setting the `groups` to `None` which is important to remove the default linking to the default group model in order to avoid conflicts.

Also, take note of the `related_name` and `related_query_name`. Most of the time, the pattern shown above should work. For a deeper understanding see [Django docs here](https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.ForeignKey.related_name).

Don't forget to set this model as the `AUTH_GROUP_MODEL` in `settings.py`.

## AbstractGroup

The `AbstractGroup` class implements the same attributes as Django's default `Group` model.

- **name**
  A unique `CharField` with a `max_length` of 150.
  If you would like to override this field, and **you want to call it something else**, you must also override the `__str__` and `natural_key` methods to return the new field.
  
  **Example:**
  
  ```python
  class Role(AbstractGroup):
      name = None
      new_name = models.CharField(max_length=150, unique=True)
      # Your other fields
  
      def __str__(self):
          return self.new_name
  
      def natural_key(self):
          return (self.new_name,)
  
      class Meta:
          verbose_name = "role"
          verbose_name_plual = "roles"
  ```

- **permissions**
  A `ManyToManyField` to Django's `Permission` model.
  You don't want to override this unless you have a very good reason.

## Contributing and Issue Tracking

We welcome contributions and feedback! If you encounter any issues with the package or have suggestions for improvement, please don't hesitate to open an issue on [GitHub](https://github.com/ankitchhatbar/django-group-model).

When opening an issue, please provide as much detail as possible, including steps to reproduce the problem, your environment (Python version, Django version, etc.), and any relevant error messages.

If you'd like to contribute code to this project, you can do so by creating a pull request. We appreciate all contributions, whether it's fixing a bug, implementing a new feature, writing tests, or improving the documentation.

To create a pull request:

1. Fork the repository and create a new branch for your changes.

2. Make your changes, following the project's coding style and conventions.

3. Write tests to cover your changes, if applicable.

4. Ensure that all existing tests pass by running the test suite.

5. Submit a pull request, explaining the changes you've made and why they're valuable.

Thank you for using this package and your interest in contributing to this project! Your contributions help make it better for everyone.
