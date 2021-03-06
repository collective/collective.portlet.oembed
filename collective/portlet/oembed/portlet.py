from zope import component
from zope import schema
from zope import interface
from zope.formlib import form

from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.portlets.interfaces import IPortletDataProvider

from plone.app.portlets.portlets import base
from plone.portlet.static import static

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.oembed import messageFactory as _
from collective.portlet.oembed import ploneMessageFactory as _p
from plone.registry.interfaces import IRegistry


class IOEmbedPortlet(IPortletDataProvider):
    """A portlet which renders external content using oembed service"""

    header = schema.TextLine(
        title=_p(u"Portlet header"),
        description=_p(u"Title of the rendered portlet"),
        required=True)

    remote_url = schema.URI(
        title=_(u"Remote URL"),
        description=_(u"The external content you want to display using "
                      u"oembed"),
        required=True)

    maxwidth = schema.Int(
        title=_(u"Maximum width"),
        description=_(u"The width will be added to the oembed request"),
        required=False)

    maxheight = schema.Int(
        title=_(u"Maximum height"),
        description=_(u"The height will be added to the oembed request"),
        required=False)

    responsive = schema.Bool(
        title=_(u"Responsive"),
        description=_(u"If the response is an iframe the code will be updated \
        to become responsive. In some case this can broke the returned code.\
        In that case you can unactivate it by uncheck this option."),
        default=True)

    omit_border = schema.Bool(
        title=_(u"Omit portlet border"),
        description=_(u"Tick this box if you want to render the text above "
                      "without the standard header, border or footer."),
        required=True,
        default=False)

    footer = schema.TextLine(
        title=_(u"Portlet footer"),
        description=_(u"Text to be shown in the footer"),
        required=False)

    more_url = schema.ASCIILine(
        title=_(u"Details link"),
        description=_(u"If given, the header and footer "
                      "will link to this URL."),
        required=False)


class Assignment(base.Assignment):
    interface.implements(IOEmbedPortlet)

    header = _(u"title_portlet", default=u"OEmbed portlet")

    remote_url = ""
    maxwidth = None
    maxheight = None
    responsive = True
    omit_border = False
    footer = u""
    more_url = ''

    def __init__(self, header=u"", remote_url=None, maxwidth=None,
                 maxheight=None, omit_border=False, footer=u"",
                 more_url='', responsive=True):
        self.header = header
        self.omit_border = omit_border
        self.footer = footer
        self.more_url = more_url
        self.maxheight = maxheight
        self.maxwidth = maxwidth
        self.responsive = responsive
        self.remote_url = remote_url

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class Renderer(static.Renderer):
    """Portlet renderer.
    """

    render = ViewPageTemplateFile('portlet.pt')
    jsoembedall = ViewPageTemplateFile('jsoembedall.pt')
    jsoembed = ViewPageTemplateFile('jsoembed.pt')

    def get_rendering(self):
        registry = component.getUtility(IRegistry)
        if 'collective.portlet.oembed.rendering' in registry:
            return registry['collective.portlet.oembed.rendering']
        return 'collective.oembed'

    def embed(self):
        if self.get_rendering() == "collective.js.oembedall":
            return self.jsoembedall()
        if self.get_rendering() == "collective.oembed.jquery":
            return self.jsoembed()
        #rendering should be "collective.oembed"
        return self.embed_collective_oembed()

    def embed_collective_oembed(self):
        consumer_view = component.queryMultiAdapter(
            (self.context, self.request),
            name=u'collective.oembed.superconsumer'
        )
        if consumer_view is None:
            return u""
        consumer_view._url = self.data.remote_url
        if self.data.maxwidth is not None:
            consumer_view._maxwidth = self.data.maxwidth
        if self.data.maxheight is not None:
            consumer_view._maxheight = self.data.maxheight
        return consumer_view.get_embed_auto()

    def css_class(self):
        """Generate a CSS class from the portlet header
        """
        header = self.data.header
        normalizer = component.getUtility(IIDNormalizer)
        return "portlet-oembed-%s" % normalizer.normalize(header)

    def has_link(self):
        return bool(self.data.more_url)

    def has_footer(self):
        return bool(self.data.footer)

    def is_responsive(self):
        return self.data.responsive


class AddForm(base.AddForm):
    """add form"""
    form_fields = form.Fields(IOEmbedPortlet)
    label = _(u"title_add_portlet", default=u"Add oembed portlet")
    description = _(u"description_portlet",
                    default=u"A portlet which renders external content using "
                    u"oembed service")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.
    """
    form_fields = form.Fields(IOEmbedPortlet)
    label = _(u"title_edit_portlet",
              default=u"Edit oembed portlet")
    description = _(u"description_portlet",
                    default=u"A portlet which renders external content using "
                    u"oembed service")
