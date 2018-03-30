########################################################################
# LDAP Authentication
########################################################################
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType
#AUTH_LDAP_START_TLS = True
AUTH_LDAP_GLOBAL_OPTIONS = {
 ldap.OPT_X_TLS_REQUIRE_CERT: False,
 ldap.OPT_REFERRALS: False,
}
# Baseline configuration.
AUTH_LDAP_SERVER_URI = "ldap://my.ldap.domain"
AUTH_LDAP_BIND_DN = "cn=admin,dc=my,dc=ldap,dc=domain"
AUTH_LDAP_BIND_PASSWORD = "myP@ssw0rd"
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=Users,dc=my,dc=ldap,dc=domain", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
# or perhaps:
# AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=users,dc=example,dc=com"
AUTH_LDAP_ALWAYS_UPDATE_USER = True
# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=Groups,dc=parent,dc=ssischool,dc=org",
 ldap.SCOPE_SUBTREE, "(objectClass=posixGroup)"
)
# set group type
AUTH_LDAP_GROUP_TYPE = PosixGroupType()
# Simple group restrictions
#~ AUTH_LDAP_REQUIRE_GROUP = "cn=enabled,ou=django,ou=groups,dc=example,dc=com"
#~ AUTH_LDAP_DENY_GROUP = "cn=disabled,ou=django,ou=groups,dc=example,dc=com"
# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
 "first_name": "givenName",
 "last_name": "sn",
 "email": "mail"
}
#~ AUTH_LDAP_PROFILE_ATTR_MAP = {
 #~ "employee_number": "employeeNumber"
#~ }
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
 "is_active": "cn=active,ou=Groups,dc=parent,dc=ssischool,dc=org",
 "is_staff": "cn=staff,ou=Groups,dc=parent,dc=ssischool,dc=org",
 "is_superuser": "cn=superuser,ou=Groups,dc=parent,dc=ssischool,dc=org"
}
#~ AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = {
 #~ "is_awesome": "cn=awesome,ou=django,ou=groups,dc=example,dc=com",
#~ }
# important! to use the group's permission
AUTH_LDAP_MIRROR_GROUPS = True
# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True
# Cache group memberships for an hour to minimize LDAP traffic
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 2

# !important# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = ( 'django_auth_ldap.backend.LDAPBackend', 'django.contrib.auth.backends.ModelBackend',)
# End LDAP Authentication Settings
