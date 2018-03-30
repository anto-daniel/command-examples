import ldap

AUTH_LDAP_SERVER_URI = "ldap://example.test.com"

AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0
}
