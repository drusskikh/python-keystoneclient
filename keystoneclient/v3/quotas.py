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

    def build_user_quota_base_url(self, user_id):
        self.base_url = '/users/%s/OS-QUOTAS' % user_id

    def build_project_quota_base_url(self, project_id):
        self.base_url = '/projects/%s/OS-QUOTAS' % project_id

    def create_user_quota(self, user_id, resource_id,
               limit=None):
        self.build_user_quota_base_url(user_id)

        return super(QuotaManager, self).create(
            base_url=self.base_url,
            resource_id=resource_id,
            limit=limit)

    def list_user_quotas(self, user_id):
        self.build_user_quota_base_url(user_id)

        return super(QuotaManager, self).list(base_url=self.base_url)

    def get_user_quota(self, user_id, quota_id):
        self.build_user_quota_base_url(user_id)

        return super(QuotaManager, self).get(
            base_url=self.base_url,
            quota_id=quota_id)

    def update_user_quota(self, user_id, quota_id, limit):
        self.build_user_quota_base_url(user_id)

        return super(QuotaManager, self).update(
            base_url=self.base_url,
            quota_id=quota_id,
            limit=limit)

    def delete_user_quota(self, user_id, quota_id):
        self.build_user_quota_base_url(user_id)

        return super(QuotaManager, self).delete(
            base_url=self.base_url,
            quota_id=quota_id)

    def create_project_quota(self, project_id, resource_id,
               limit=None):
        self.build_project_quota_base_url(project_id)

        return super(QuotaManager, self).create(
            base_url=self.base_url,
            resource_id=resource_id,
            limit=limit)

    def list_project_quotas(self, project_id, **kwargs):
        import collections
        StrictedQuota = collections.namedtuple('StrictedQuota', 'name, limit, id')

        self.build_project_quota_base_url(project_id)
        quotas = super(QuotaManager, self).list(base_url=self.base_url,
                                              **kwargs)
        result_lst = []
        for quota in quotas:
            quota_dict = {'name': quota.resource['name'],
                          'limit': quota.limit,
                          'id': quota.id}
            obj = StrictedQuota(**quota_dict)
            result_lst.append(obj)

        return result_lst

    def get_project_quota(self, project_id, quota_id):
        self.build_project_quota_base_url(project_id)

        return super(QuotaManager, self).get(
            base_url=self.base_url,
            quota_id=quota_id)

    def update_project_quota(self, project_id, quota_id, limit):
        self.build_project_quota_base_url(project_id)

        return super(QuotaManager, self).update(
            base_url=self.base_url,
            quota_id=quota_id,
            limit=limit)

    def delete_project_quota(self, project_id, quota_id):
        self.build_project_quota_base_url(project_id)

        return super(QuotaManager, self).delete(
            base_url=self.base_url,
            quota_id=quota_id)
