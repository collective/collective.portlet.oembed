import unittest2 as unittest

from zope.component import getUtility, getMultiAdapter
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from plone.app.portlets.storage import PortletAssignmentMapping

from collective.portlet.oembed import portlet
from collective.portlet.oembed.tests.base import IntegrationTestCase


class TestPortlet(IntegrationTestCase):

    def test_portlet_type_registered(self):
        portlet_oembed = getUtility(
            IPortletType,
            name='collective.portlet.oembed.OEmbed'
        )
        self.assertEquals(portlet_oembed.addview,
                          'collective.portlet.oembed.OEmbed')

    def test_interfaces(self):
        # TODO: Pass any keyword arguments to the Assignment constructor
        portlet_oembed = portlet.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet_oembed))
        self.failUnless(IPortletDataProvider.providedBy(portlet_oembed.data))

    def test_invoke_add_view(self):
        portlet_oembed = getUtility(
            IPortletType,
            name='collective.portlet.oembed.OEmbed')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet_oembed.addview)

        # TODO: Pass a dictionary containing dummy form inputs from the add
        # form.
        # Note: if the portlet has a NullAddForm, simply call
        # addview() instead of the next line.
        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0],
                                   portlet.Assignment))

    def test_invoke_edit_view(self):
        # NOTE: This test can be removed if the portlet has no edit form
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = portlet.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, portlet.EditForm))

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn',
                             context=self.portal)

        # TODO: Pass any keyword arguments to the Assignment constructor
        assignment = portlet.Assignment()

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, portlet.Renderer))


class TestRenderer(IntegrationTestCase):

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        # TODO: Pass any default keyword arguments to the Assignment
        # constructor.
        assignment = assignment or portlet.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def test_render(self):
        # TODO: Pass any keyword arguments to the Assignment constructor.
        r = self.renderer(context=self.portal,
                          assignment=portlet.Assignment())
        r = r.__of__(self.folder)
        r.update()
        #output = r.render()
        # TODO: Test output


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
