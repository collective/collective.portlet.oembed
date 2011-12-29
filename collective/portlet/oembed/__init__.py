# See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)


from zope.i18nmessageid import MessageFactory
messageFactory = MessageFactory('collective.portlet.oembed')
ploneMessageFactory = MessageFactory('plone')

from Products.CMFCore.permissions import setDefaultRoles
setDefaultRoles('collective.portlet.embed: Add oembed portlet',
                ('Manager', 'Site Administrator', 'Owner',))
