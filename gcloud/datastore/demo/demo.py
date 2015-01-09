# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Welcome to the gCloud Datastore Demo! (hit enter)
# We're going to walk through some of the basics...
# Don't worry though. You don't need to do anything, just keep hitting enter...

# Let's start by importing the demo module and initializing our connection.
from gcloud.datastore import demo
demo.initialize()

# Let's import the package containing our helper classes:
from gcloud import datastore

# Let's create a new entity of type "Thing" and name it 'Toy':
key = datastore.Key('Thing')
toy = datastore.Entity(key)
toy.update({'name': 'Toy'})

# Now let's save it to our datastore:
toy.save()

# If we look it up by its key, we should find it...
print(datastore.get([toy.key]))

# And we should be able to delete it...
toy.key.delete()

# Since we deleted it, if we do another lookup it shouldn't be there again:
print(datastore.get([toy.key]))

# Now let's try a more advanced query.
# First, let's create some entities.
SAMPLE_DATA = [
    (1234, 'Computer', 10),
    (2345, 'Computer', 8),
    (3456, 'Laptop', 10),
    (4567, 'Printer', 11),
    (5678, 'Printer', 12),
    (6789, 'Computer', 13)]
samples = []
for id, name, age in SAMPLE_DATA:
    key = datastore.Key('Thing', id)
    samples.append(key)
    entity = datastore.Entity(key)
    entity['name'] = name
    entity['age'] = age
    entity.save()
# We'll start by look at all Thing entities:
query = datastore.Query(kind='Thing')

# Let's look at the first two.
print(list(query.fetch(limit=2)))

# Now let's check for Thing entities named 'Computer'
query.add_filter('name', '=', 'Computer')
print(list(query.fetch()))

# If you want to filter by multiple attributes,
# you can call .add_filter multiple times on the query.
query.add_filter('age', '=', 10)
print(list(query.fetch()))

# Now delete them.
print([key.delete() for key in samples])

# You can also work inside a transaction.
# (Check the official docs for explanations of what's happening here.)
with datastore.Transaction():
    print('Creating and saving an entity...')
    key = datastore.Key('Thing', 'foo')
    thing = datastore.Entity(key)
    thing['age'] = 10
    thing.save()

    print('Creating and saving another entity...')
    key2 = datastore.Key('Thing', 'bar')
    thing2 = datastore.Entity(key2)
    thing2['age'] = 15
    thing2.save()

    print('Committing the transaction...')

# Now that the transaction is commited, let's delete the entities.
print(key.delete(), key2.delete())

# To rollback a transaction, just call .rollback()
with datastore.Transaction() as t:
    key = datastore.Key('Thing', 'another')
    thing = datastore.Entity(key)
    thing.save()
    t.rollback()

# Let's check if the entity was actually created:
created = datastore.get([key])
print('yes' if created else 'no')

# Remember, a key won't be complete until the transaction is commited.
# That is, while inside the transaction block, thing.key will be incomplete.
with datastore.Transaction():
    key = datastore.Key('Thing')  # partial
    thing = datastore.Entity(key)
    thing.save()
    print(thing.key)  # This will still be partial

print(thing.key)  # This will be complete

# Now let's delete the entity.
thing.key.delete()
