# Copyright 2011 OpenStack LLC.
# Copyright 2011 Nebula, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from keystoneclient import base


class Resource(base.Resource):
    """Represents an Identity resource.

    Attributes:
        * id: a uuid that identifies the resource

    """
    pass


class ResourceManager(base.CrudManager):
    """Manager class for manipulating Identity resources."""
    resource_class = Resource
    collection_key = 'resources'
    key = 'resource'
    base_url='/OS-QUOTAS'

    def create(self, name, description, default_limit):
        return super(ResourceManager, self).create(
            name=name,
            description=description,
            default_limit=default_limit)

    def list(self):
        return super(ResourceManager, self).list()

    def get(self, resource_id):
        return super(ResourceManager, self).get(
            resource_id=resource_id
            )

    def update(self, resource_id, name=None, description=None,
              default_limit=None):
        return super(ResourceManager, self).update(
            resource_id=resource_id,
            name=name,
            description=description,
            default_limit=default_limit)

    def delete(self, resource_id):
        return super(ResourceManager, self).delete(
            resource_id=resource_id)
