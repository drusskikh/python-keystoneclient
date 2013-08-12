# Copyright 2010 Jacob Kaplan-Moss
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
import argparse
import getpass
from keystoneclient.v3 import client
from keystoneclient import utils

CLIENT_CLASS = client.Client

@utils.arg('--tenant-id', metavar='<tenant-id>',
           help='Tenant ID;  lists all users if not specified')
@utils.arg('--tenant_id', help=argparse.SUPPRESS)
def do_user_list(kc, args):
    """List users"""
    users = kc.users.list(project=args.tenant_id)
    utils.print_list(users, ['id', 'name', 'enabled', 'email'],
                     order_by='name')

@utils.arg('user', metavar='<user>', help='Name or ID of user to display')
def do_user_get(kc, args):
    """Display user details."""
    user = utils.find_resource(kc.users, args.user)
    utils.print_dict(user._info)

@utils.arg('--name', metavar='<user-name>', required=True,
           help='New user name (must be unique)')
@utils.arg('--tenant-id', metavar='<tenant-id>',
           help='New user default tenant')
@utils.arg('--tenant_id', help=argparse.SUPPRESS)
@utils.arg('--domain-id', metavar='<domain>',
           help='ID of domain')
@utils.arg('--domain_id', help=argparse.SUPPRESS)
@utils.arg('--pass', metavar='<pass>', dest='passwd',
           help='New user password')
@utils.arg('--email', metavar='<email>',
           help='New user email address')
@utils.arg('--enabled', metavar='<true|false>', default=True,
           help='Initial user enabled status (default true)')
def do_user_create(kc, args):
    """Create new user"""
    domain_id = args.domain_id
    if not domain_id:
        domain = utils.find_resource(kc.domains, kc.project_domain_name)
        domain_id = domain.id
    user = kc.users.create(name=args.name, password=args.passwd,
                           email=args.email,
                           project=args.tenant_id, domain=domain_id,
                           enabled=utils.string_to_bool(args.enabled))
    utils.print_dict(user._info)

@utils.arg('--name', metavar='<user-name>',
           help='Desired new user name')
@utils.arg('--email', metavar='<email>',
           help='Desired new email address')
@utils.arg('--enabled', metavar='<true|false>',
           help='Enable or disable user')
@utils.arg('user', metavar='<user>', help='Name or ID of user to update')
def do_user_update(kc, args):
    """Update user's name, email, and enabled status"""
    kwargs = {}
    if args.name:
        kwargs['name'] = args.name
    if args.email:
        kwargs['email'] = args.email
    if args.enabled:
        kwargs['enabled'] = utils.string_to_bool(args.enabled)
    if not len(kwargs):
        print "User not updated, no arguments present."
        return
    user = utils.find_resource(kc.users, args.user)
    try:
        kc.users.update(user, **kwargs)
        print 'User has been updated.'
    except Exception as e:
        print 'Unable to update user: %s' % e

@utils.arg('--pass', metavar='<password>', dest='passwd', required=True,
           help='Desired new password')
@utils.arg('user', metavar='<user>',
           help='Name or ID of user to update password')
def do_user_password_update(kc, args):
    """Update user password"""
    user = utils.find_resource(kc.users, args.user)
    kc.users.update_password(user, args.passwd)

@utils.arg('--current-password', metavar='<current-password>',
           dest='currentpasswd', required=False, help='Current password, '
           'Defaults to the password as set by --os-password or '
           'OS_PASSWORD')
@utils.arg('--new-password ', metavar='<new-password>', dest='newpasswd',
           required=False, help='Desired new password')
def do_password_update(kc, args):
    """Update own password"""
    # we are prompting for these passwords if they are not passed in
    # this gives users the option not to have their password
    # appear in bash history etc..
    currentpasswd = args.os_password
    if args.currentpasswd is not None:
        currentpasswd = args.currentpasswd
    if currentpasswd is None:
        currentpasswd = getpass.getpass('Current Password: ')
    newpasswd = args.newpasswd
    while newpasswd is None:
        passwd1 = getpass.getpass('New Password: ')
        passwd2 = getpass.getpass('Repeat New Password: ')
        if passwd1 == passwd2:
            newpasswd = passwd1
    kc.users.update_own_password(currentpasswd, newpasswd)
    if args.os_password != newpasswd:
        print "You should update the password you are using to authenticate "\
              "to match your new password"

@utils.arg('user', metavar='<user>', help='Name or ID of user to delete')
def do_user_delete(kc, args):
    """Delete user"""
    user = utils.find_resource(kc.users, args.user)
    kc.users.delete(user)

def do_tenant_list(kc, args):
    """List all tenants"""
    tenants = kc.projects.list()
    utils.print_list(tenants, ['id', 'name', 'enabled', 'description'],
                     order_by='name')

@utils.arg('tenant', metavar='<tenant>',
           help='Name or ID of tenant to display')
def do_tenant_get(kc, args):
    """Display tenant details"""
    tenant = utils.find_resource(kc.projects, args.tenant)
    utils.print_dict(tenant._info)

@utils.arg('--name', metavar='<tenant-name>', required=True,
           help='New tenant name (must be unique)')
@utils.arg('--description', metavar='<tenant-description>', default=None,
           help='Description of new tenant (default is none)')
@utils.arg('--enabled', metavar='<true|false>', default=True,
           help='Initial tenant enabled status (default true)')
@utils.arg('--domain-id', metavar='<domain>',
           help='ID of domain')
@utils.arg('--domain_id', help=argparse.SUPPRESS)
def do_tenant_create(kc, args):
    """Create new tenant"""
    domain_id = args.domain_id
    if not domain_id:
        domain = utils.find_resource(kc.domains, kc.project_domain_name)
        domain_id = domain.id
    tenant = kc.projects.create(args.name,
                                domain_id,
                                description=args.description,
                                enabled=utils.string_to_bool(args.enabled))
    utils.print_dict(tenant._info)

@utils.arg('--name', metavar='<tenant_name>',
           help='Desired new name of tenant')
@utils.arg('--description', metavar='<tenant-description>', default=None,
           help='Desired new description of tenant')
@utils.arg('--enabled', metavar='<true|false>',
           help='Enable or disable tenant')
@utils.arg('tenant', metavar='<tenant>', help='Name or ID of tenant to update')
def do_tenant_update(kc, args):
    """Update tenant name, description, enabled status"""
    tenant = utils.find_resource(kc.projects, args.tenant)
    kwargs = {}
    if args.name:
        kwargs.update({'name': args.name})
    if args.description is not None:
        kwargs.update({'description': args.description})
    if args.enabled:
        kwargs.update({'enabled': utils.string_to_bool(args.enabled)})
    if kwargs == {}:
        print "Tenant not updated, no arguments present."
        return
    tenant.update(**kwargs)

@utils.arg('tenant', metavar='<tenant>', help='Name or ID of tenant to delete')
def do_tenant_delete(kc, args):
    """Delete tenant"""
    tenant = utils.find_resource(kc.projects, args.tenant)
    kc.projects.delete(tenant)

@utils.arg('--name', metavar='<name>', required=True,
           help='Name of new service (must be unique)')
@utils.arg('--type', metavar='<type>', required=True,
           help='Service type (one of: identity, compute, network, '
                'image, or object-store)')
@utils.arg('--description', metavar='<service-description>',
           help='Description of service')
def do_service_create(kc, args):
    """Add service to Service Catalog"""
    service = kc.services.create(args.name,
                                 args.type,
                                 args.description)
    utils.print_dict(service._info)

def do_service_list(kc, args):
    """List all services in Service Catalog"""
    services = kc.services.list()
    utils.print_list(services, ['id', 'name', 'type', 'description'],
                     order_by='name')

@utils.arg('service', metavar='<service>',
           help='Name or ID of service to display')
def do_service_get(kc, args):
    """Display service from Service Catalog"""
    service = utils.find_resource(kc.services, args.service)
    utils.print_dict(service._info)

@utils.arg('service', metavar='<service>',
           help='Name or ID of service to delete')
def do_service_delete(kc, args):
    """Delete service from Service Catalog"""
    service = utils.find_resource(kc.services, args.service)
    kc.services.delete(service.id)

def do_role_list(kc, args):
    """List all roles"""
    roles = kc.roles.list()
    utils.print_list(roles, ['id', 'name'], order_by='name')

@utils.arg('role', metavar='<role>', help='Name or ID of role to display')
def do_role_get(kc, args):
    """Display role details"""
    role = utils.find_resource(kc.roles, args.role)
    utils.print_dict(role._info)

@utils.arg('--name', metavar='<role-name>', required=True,
           help='Name of new role')
def do_role_create(kc, args):
    """Create new role"""
    role = kc.roles.create(args.name)
    utils.print_dict(role._info)

@utils.arg('role', metavar='<role>', help='Name or ID of role to delete')
def do_role_delete(kc, args):
    """Delete role"""
    role = utils.find_resource(kc.roles, args.role)
    kc.roles.delete(role)

@utils.arg('--user', '--user-id', '--user_id', metavar='<user>',
           required=True, help='Name or ID of user')
@utils.arg('--role', '--role-id', '--role_id', metavar='<role>',
           required=True, help='Name or ID of role')
@utils.arg('--tenant', '--tenant-id', metavar='<tenant>',
           help='Name or ID of tenant')
@utils.arg('--tenant_id', help=argparse.SUPPRESS)
@utils.arg('--domain', '--domain-id', metavar='<domain>',
           help='Name or ID of domain')
@utils.arg('--domain_id', help=argparse.SUPPRESS)
def do_user_role_add(kc, args):
    """Add role to user"""
    user = utils.find_resource(kc.users, args.user)
    role = utils.find_resource(kc.roles, args.role)
    if args.tenant:
        tenant = utils.find_resource(kc.projects, args.tenant)
    elif args.tenant_id:
        tenant = args.tenant_id
    else:
        tenant = None
    if args.domain:
        domain = utils.find_resource(kc.domains, args.domain)
    elif args.domain_id:
        domain = args.domain_id
    else:
        domain = None
    kc.roles.grant(role, user, domain, tenant)

@utils.arg('--user', '--user-id', '--user_id', metavar='<user>',
           required=True, help='Name or ID of user')
@utils.arg('--role', '--role-id', '--role_id', metavar='<role>',
           required=True, help='Name or ID of role')
@utils.arg('--tenant', '--tenant-id', metavar='<tenant>',
           help='Name or ID of tenant')
@utils.arg('--tenant_id', help=argparse.SUPPRESS)
def do_user_role_remove(kc, args):
    """Remove role from user"""
    user = utils.find_resource(kc.users, args.user)
    role = utils.find_resource(kc.roles, args.role)
    if args.tenant:
        tenant = utils.find_resource(kc.projects, args.tenant)
    elif args.tenant_id:
        tenant = args.tenant_id
    else:
        tenant = None
    kc.roles.remove_user_role(user, role, tenant)

@utils.arg('--user', '--user-id', metavar='<user>',
           help='List roles granted to a user')
@utils.arg('--user_id', help=argparse.SUPPRESS)
@utils.arg('--tenant', '--tenant-id', metavar='<tenant>',
           help='List roles granted on a tenant')
@utils.arg('--tenant_id', help=argparse.SUPPRESS)
def do_user_role_list(kc, args):
    """List roles granted to a user"""
    if args.tenant:
        tenant_id = utils.find_resource(kc.projects, args.tenant).id
    elif args.tenant_id:
        tenant_id = args.tenant_id
    else:
        # use the authenticated tenant id as a default
        tenant_id = kc.auth_tenant_id
    if args.user:
        user_id = utils.find_resource(kc.users, args.user).id
    elif args.user_id:
        user_id = args.user_id
    else:
        # use the authenticated user id as a default
        user_id = kc.auth_user_id
    roles = kc.roles.list(user=user_id, project=tenant_id)
    # this makes the command output a bit more intuitive
    for role in roles:
        role.user_id = user_id
        role.project_id = tenant_id
    utils.print_list(roles, ['id', 'name', 'user_id', 'project_id'],
                     order_by='name')

@utils.arg('--user-id', metavar='<user-id>', help='User ID')
@utils.arg('--user_id', help=argparse.SUPPRESS)
@utils.arg('--tenant-id', metavar='<tenant-id>', help='Tenant ID')
@utils.arg('--tenant_id', help=argparse.SUPPRESS)
def do_ec2_credentials_create(kc, args):
    """Create EC2-compatible credentials for user per tenant"""
    if not args.tenant_id:
        # use the authenticated tenant id as a default
        args.tenant_id = kc.auth_tenant_id
    if not args.user_id:
        # use the authenticated user id as a default
        args.user_id = kc.auth_user_id
    credentials = kc.ec2.create(args.user_id, args.tenant_id)
    utils.print_dict(credentials._info)

@utils.arg('--user-id', metavar='<user-id>', help='User ID')
@utils.arg('--user_id', help=argparse.SUPPRESS)
@utils.arg('--access', metavar='<access-key>', required=True,
           help='Access Key')
def do_ec2_credentials_get(kc, args):
    """Display EC2-compatible credentials"""
    if not args.user_id:
        # use the authenticated user id as a default
        args.user_id = kc.auth_user_id
    cred = kc.ec2.get(args.user_id, args.access)
    if cred:
        utils.print_dict(cred._info)

@utils.arg('--user-id', metavar='<user-id>', help='User ID')
@utils.arg('--user_id', help=argparse.SUPPRESS)
def do_ec2_credentials_list(kc, args):
    """List EC2-compatible credentials for a user"""
    if not args.user_id:
        # use the authenticated user id as a default
        args.user_id = kc.auth_user_id
    credentials = kc.ec2.list(args.user_id)
    for cred in credentials:
        try:
            cred.tenant = getattr(kc.projects.get(cred.tenant_id), 'name')
        except Exception:
            # FIXME(dtroyer): Retrieving the tenant name fails for normal
            #                 users; stuff in the tenant_id instead.
            cred.tenant = cred.tenant_id
    utils.print_list(credentials, ['tenant', 'access', 'secret'])

@utils.arg('--user-id', metavar='<user-id>', help='User ID')
@utils.arg('--user_id', help=argparse.SUPPRESS)
@utils.arg('--access', metavar='<access-key>', required=True,
           help='Access Key')
def do_ec2_credentials_delete(kc, args):
    """Delete EC2-compatible credentials"""
    if not args.user_id:
        # use the authenticated user id as a default
        args.user_id = kc.auth_user_id
    try:
        kc.ec2.delete(args.user_id, args.access)
        print 'Credential has been deleted.'
    except Exception as e:
        print 'Unable to delete credential: %s' % e

@utils.arg('--service', metavar='<service-type>', default=None,
           help='Service type to return')
#@require_service_catalog
def do_catalog(kc, args):
    """List service catalog, possibly filtered by service."""
    print "not supported."

@utils.arg('--service', metavar='<service-type>', required=True,
           help='Service type to select')
@utils.arg('--endpoint-type', metavar='<endpoint-type>', default='publicURL',
           help='Endpoint type to select')
@utils.arg('--endpoint_type', default='publicURL',
           help=argparse.SUPPRESS)
@utils.arg('--attr', metavar='<service-attribute>',
           help='Service attribute to match for selection')
@utils.arg('--value', metavar='<value>',
           help='Value of attribute to match')
def do_endpoint_get(kc, args):
    """Find endpoint filtered by a specific attribute or service type"""
    print "not supported."

def do_endpoint_list(kc, args):
    """List configured service endpoints"""
    endpoints = kc.endpoints.list()
    utils.print_list(endpoints,
                     ['id', 'region', 'interface', 'url', 'service_id'])

@utils.arg('--region', metavar='<endpoint-region>',
           help='Endpoint region', default='regionOne')
@utils.arg('--service-id', '--service_id', metavar='<service-id>',
           required=True, help='ID of service associated with Endpoint')
@utils.arg('--publicurl', metavar='<public-url>',
           help='Public URL endpoint')
@utils.arg('--adminurl', metavar='<admin-url>',
           help='Admin URL endpoint')
@utils.arg('--internalurl', metavar='<internal-url>',
           help='Internal URL endpoint')
def do_endpoint_create(kc, args):
    """Create a new endpoint associated with a service"""
    endpoint = kc.endpoints.create(args.region,
                                   args.service_id,
                                   args.publicurl,
                                   args.adminurl,
                                   args.internalurl)
    utils.print_dict(endpoint._info)

@utils.arg('id', metavar='<endpoint-id>', help='ID of endpoint to delete')
def do_endpoint_delete(kc, args):
    """Delete a service endpoint"""
    try:
        kc.endpoints.delete(args.id)
        print 'Endpoint has been deleted.'
    except Exception:
        print 'Unable to delete endpoint.'

@utils.arg('--wrap', metavar='<integer>', default=0,
           help='wrap PKI tokens to a specified length, or 0 to disable')
def do_token_get(kc, args):
    """Display the current user token"""
    print kc.auth_token

@utils.arg('--name', metavar='<domain-name>',
           help='Name of the domain to be created', required=True)
@utils.arg('--description', metavar='<domain-description>',
           help='Domain description', default=None)
@utils.arg('--enabled', metavar='<true|false>',
           help='Enable or disable a domain', default=True)
def do_domain_create(kc, args):
    """Create a domain"""
    domain = kc.domains.create(name=args.name,
                               description=args.description,
                               enabled=utils.string_to_bool(args.enabled))
    utils.print_dict(domain._info)

@utils.arg('domain', metavar='<domain>', help='Name or id of domain to delete')
def do_domain_delete(kc, args):
    """Delete a domain."""
    domain = utils.find_resource(kc.domains, args.domain)
    kc.domains.delete(domain)

def do_domain_list(kc, args):
    """List domains"""
    domains = kc.domains.list()
    utils.print_list(domains, ['id', 'name', 'enabled', 'description'],
                     order_by='name')

@utils.arg('--name', metavar='<domain-name>',
           help='Value to update the domain name')
@utils.arg('--description', metavar='<domain-description>',
           help='Value to update the domain description')
@utils.arg('--enabled', metavar='<true|false>',
           help='Enable or disable a domain')
@utils.arg('domain', metavar='<domain>', help='Id of the domain to be updated')
def do_domain_update(kc, args):
    """Update a domain name, description or/and enabled status."""
    kwargs = {}
    if args.name:
        kwargs['name'] = args.name
    if args.description:
        kwargs['description'] = args.description
    if args.enabled:
        kwargs['enabled'] = utils.string_to_bool(args.enabled)
    if not len(kwargs):
        print "Domain not updated, no arguments present."
        return
    domain = utils.find_resource(kc.domains, args.domain)
    updt_domain = kc.domains.update(domain=domain, **kwargs)
    utils.print_dict(updt_domain._info)

@utils.arg('domain', metavar='<domain>', help='Name or id of domain to show')
def do_domain_get(kc, args):
    """Display a domain."""
    domain = utils.find_resource(kc.domains, args.domain)
    domain = kc.domains.get(domain)
    utils.print_dict(domain._info)

