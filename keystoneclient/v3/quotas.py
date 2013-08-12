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


class Quota(base.Resource):
    """Represents an Identity quota.

    Attributes:
        * id: a uuid that identifies the quota

    """
    pass


class QuotaManager(base.CrudManager):
    """Manager class for manipulating Identity quotas."""
    resource_class = Quota
    collection_key = 'quotas'
    key = 'quota'

    def _require_user_xor_project(self, user_id, project_id):
        if (user_id and project_id) or (not user_id and not project_id):
            msg = 'Specify either a user_id or project_id, not both'
            raise exceptions.ValidationError(msg)

    def build_base_url(self, user_id=None, project_id=None):
        self._require_user_xor_project(user_id, project_id)

        if user_id is not None:
            base_url = '/users/%d/OS-QUOTAS' % user_id
        else:
            base_url = '/projects/%d/OS-QUOTAS' % project_id


    def create(self, resource_id, user_id=None, project_id=None,
               limit=None):
        self.build_base_url(user_id, project_id)

        return super(QuotaManager, self).create(
            resource_id=resource_id,
            limit=limit)

    def list(self, user_id=None, project_id=None, **kwargs):
        self.build_base_url(user_id, project_id)

        return super(QuotaManager, self).list(**kwargs)

    def get(self, quota_id, user_id=None, project_id=None):
        self.build_base_url(user_id, project_id)

        return super(QuotaManager, self).get(
            quota_id=quota_id)

    def update(self, quota_id, limit, user_id=None, project_id=None):
        self.build_base_url(user_id, project_id)

        return super(QuotaManager, self).update(
            quota_id=quota_id,
            limit=limit)

    def delete(self, quota_id, user_id=None, project_id=None):
        self.build_base_url(user_id, project_id)

        return super(QuotaManager, self).delete(
            quota_id=quota_id)
